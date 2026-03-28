import glob
import os
import subprocess
import time
import threading


class Camera():

    # defaults
    TOP = 0
    BOTTOM = 1
    QQVGA = 0    # 160x120
    QVGA = 1     # 320x240
    VGA = 2      # 640x480
    K4VGA = 3    # 1280x960
    RGB = 11
    YUV422 = 9

    def __init__(self, nao, photo_dir='/photos', video_dir='/video'):
        self.nao = nao
        self.log = nao.log
        self.photo_dir = photo_dir
        self.video_dir = video_dir

        self.nao.env.add_proxy("ALVideoDevice")
        self.video = self.nao.env.proxies["ALVideoDevice"]

        try:
            self.nao.env.add_proxy("ALFaceTracker")
            self.face_tracker = self.nao.env.proxies["ALFaceTracker"]
        except Exception as e:
            self.log('camera: ALFaceTracker not available: {}'.format(e))
            self.face_tracker = None

        # defaults
        self.camera_index = self.TOP
        self.resolution = self.QVGA
        self.color_space = self.RGB
        self.fps = 10

        # face tracking state
        self._face_tracking = False

        # video recording state
        self._recording = False
        self._record_thread = None

    # settings
    def set_camera(self, camera_index):
        self.camera_index = camera_index
        return self

    def set_resolution(self, resolution):
        self.resolution = resolution
        return self

    def set_color_space(self, color_space):
        self.color_space = color_space
        return self

    def set_fps(self, fps):
        self.fps = fps
        return self

    def top(self):
        self.camera_index = self.TOP
        return self

    def bottom(self):
        self.camera_index = self.BOTTOM
        return self

    # cleanup
    def clear_photos(self):
        files = glob.glob('{}/*'.format(self.photo_dir))
        for f in files:
            os.remove(f)
        self.log('camera.clear_photos: removed {} files'.format(len(files)))
        return self

    def clear_video(self):
        files = glob.glob('{}/*'.format(self.video_dir))
        for f in files:
            os.remove(f)
        self.log('camera.clear_video: removed {} files'.format(len(files)))
        return self

    # photo capture
    def photo(self, filename='photo', camera_index=None, resolution=None, color_space=None):
        cam = camera_index if camera_index is not None else self.camera_index
        res = resolution if resolution is not None else self.resolution
        cs = color_space if color_space is not None else self.color_space

        sub = self.video.subscribeCamera('fluentnao_photo', cam, res, cs, self.fps)
        try:
            img = self.video.getImageRemote(sub)
        finally:
            self.video.unsubscribe(sub)

        if not img:
            self.log('camera.photo: failed to capture')
            return None

        width = img[0]
        height = img[1]
        data = img[6]

        path = '{}/{}.ppm'.format(self.photo_dir, filename)
        header = 'P6\n{} {}\n255\n'.format(width, height)
        with open(path, 'wb') as f:
            f.write(header)
            f.write(bytearray(data))

        self.log('camera.photo: saved {}x{} to {}'.format(width, height, path))
        return path

    # video capture (burst of frames saved as PPMs)
    def start_recording(self, name='video', camera_index=None, resolution=None, color_space=None, fps=None):
        if self._recording:
            self.log('camera.start_recording: already recording')
            return self

        cam = camera_index if camera_index is not None else self.camera_index
        res = resolution if resolution is not None else self.resolution
        cs = color_space if color_space is not None else self.color_space
        capture_fps = fps if fps is not None else self.fps

        self._recording = True
        self._record_name = name
        self._record_fps = capture_fps
        self._record_thread = threading.Thread(
            target=self._record_loop,
            args=(name, cam, res, cs, capture_fps)
        )
        self._record_thread.daemon = True
        self._record_thread.start()
        self.log('camera.start_recording: started')
        return self

    def stop_recording(self):
        if not self._recording:
            self.log('camera.stop_recording: not recording')
            return self
        self._recording = False
        if self._record_thread:
            self._record_thread.join(timeout=5)
            self._record_thread = None
        self.log('camera.stop_recording: stopped')
        return self

    def to_video(self, name=None, fps=None, output_dir=None):
        vid_name = name or self._record_name or 'video'
        vid_fps = fps or self._record_fps or 10
        out_dir = output_dir or self.video_dir

        pattern = '{}/{}_%05d.ppm'.format(self.video_dir, vid_name)
        output = '{}/{}.mp4'.format(out_dir, vid_name)

        cmd = 'avconv -y -r {} -i {} -c:v libx264 -pix_fmt yuv420p {}'.format(
            vid_fps, pattern, output)
        result = subprocess.call(cmd, shell=True)

        # always clean up PPM frames
        frames = glob.glob('{}/{}_*.ppm'.format(self.video_dir, vid_name))
        for f in frames:
            os.remove(f)

        if result == 0:
            self.log('camera.to_video: created {} from {} frames'.format(output, len(frames)))
            return output
        else:
            self.log('camera.to_video: avconv failed (rc={})'.format(result))
            return None

    def _record_loop(self, name, cam, res, cs, capture_fps):
        interval = 1.0 / capture_fps
        sub = self.video.subscribeCamera('fluentnao_video', cam, res, cs, capture_fps)
        frame_num = 0
        start_time = time.time()
        try:
            while self._recording:
                img = self.video.getImageRemote(sub)
                if img:
                    width = img[0]
                    height = img[1]
                    data = img[6]
                    path = '{}/{}_{:05d}.ppm'.format(self.video_dir, name, frame_num)
                    header = 'P6\n{} {}\n255\n'.format(width, height)
                    with open(path, 'wb') as f:
                        f.write(header)
                        f.write(bytearray(data))
                    frame_num += 1
                time.sleep(interval)
        finally:
            elapsed = time.time() - start_time
            self._actual_fps = frame_num / elapsed if elapsed > 0 else capture_fps
            self.video.unsubscribe(sub)
            self.log('camera.record: {} frames in {:.1f}s = {:.1f} fps'.format(
                frame_num, elapsed, self._actual_fps))

    # face tracking
    def track_face(self):
        if not self.face_tracker:
            self.log('camera.track_face: not available')
            return self
        self.nao.env.motion.setStiffnesses("Head", 1.0)
        self.face_tracker.setWholeBodyOn(False)
        self.face_tracker.startTracker()
        self._face_tracking = True
        self.log('camera.track_face: started')
        return self

    def track_face_whole_body(self):
        if not self.face_tracker:
            self.log('camera.track_face_whole_body: not available')
            return self
        self.nao.env.motion.setStiffnesses("Head", 1.0)
        self.nao.env.motion.setStiffnesses("Body", 1.0)
        self.face_tracker.setWholeBodyOn(True)
        self.face_tracker.startTracker()
        self._face_tracking = True
        self.log('camera.track_face_whole_body: started')
        return self

    def stop_tracking(self):
        if not self.face_tracker:
            return self
        self.face_tracker.stopTracker()
        self.nao.env.motion.setStiffnesses("Head", 0)
        self._face_tracking = False
        self.log('camera.stop_tracking: stopped')
        return self

    def is_tracking(self):
        return self._face_tracking

    def face_position(self):
        if not self.face_tracker:
            return None
        return self.face_tracker.getPosition()
