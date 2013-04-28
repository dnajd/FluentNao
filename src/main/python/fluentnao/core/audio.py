from joints import Joints

class Audio():

    # init method
    def __init__(self, nao):

        # jobs for threading
        self.nao = nao
        self.joints = nao.joints
        self.chains = nao.chains
        self.log = nao.log

    def play(self, url, volume=1, pan=0):
        self.nao.env.audioPlayer.post.playWebStream(url, volume, pan)
        return self;

    def stop_all(self):
        self.nao.env.audioPlayer.stopAll()
        return self;

    def set_master_volume(self, volume=1):
        self.nao.env.audioPlayer.setMasterVolume(volume)
        return self;