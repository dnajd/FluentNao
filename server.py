import BaseHTTPServer
import json
import os
import subprocess
import threading

AUDIO_DIR = '/audio'
NAO_AUDIO_DIR = '/home/nao/audio_playback'
NAO_USER = 'nao'
SSH_OPTS = '-F /dev/null -i /root/.ssh/id_nao -o StrictHostKeyChecking=no -o BatchMode=yes'

def _nao_ip():
    return os.environ.get('NAO_IP', '192.168.68.96')

_CLEAN_ENV = 'LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu'

def _ssh(cmd):
    ip = _nao_ip()
    return subprocess.call(
        '{} ssh {} {}@{} {}'.format(_CLEAN_ENV, SSH_OPTS, NAO_USER, ip, cmd),
        shell=True)

def _push_to_nao(local_path, remote_path):
    ip = _nao_ip()
    _ssh('mkdir -p {}'.format(NAO_AUDIO_DIR))
    return subprocess.call(
        '{} scp {} {} {}@{}:{}'.format(_CLEAN_ENV, SSH_OPTS, local_path, NAO_USER, ip, remote_path),
        shell=True)

def _remove_from_nao(remote_path):
    _ssh('rm -f {}'.format(remote_path))

class NaoHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    nao_ref = None

    def do_POST(self):
        if self.path == '/reload':
            self._handle_reload()
        elif self.path == '/audio':
            self._handle_audio()
        elif self.path.startswith('/audio/play/'):
            self._handle_audio_play()
        elif self.path == '/exec':
            length = int(self.headers.getheader('content-length', 0))
            body = self.rfile.read(length)
            script = body.strip()
            nao = self.nao_ref
            try:
                result = eval(script, {"nao": nao})
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True, "result": str(result)}))
            except SyntaxError:
                try:
                    ns = {"nao": nao}
                    exec(script, ns)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    if "result" in ns and ns["result"] is not None:
                        self.wfile.write(json.dumps({"ok": True, "result": str(ns["result"])}))
                    else:
                        self.wfile.write(json.dumps({"ok": True}))
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"ok": False, "error": str(e)}))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": str(e)}))
        else:
            self.send_response(404)
            self.end_headers()

    def _handle_reload(self):
        nao = self.nao_ref
        try:
            import fluentnao.nao as nao_module
            reload(nao_module)
            nao.__class__ = nao_module.Nao
            nao.hot_reload()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "result": "reloaded"}))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": str(e)}))

    def _handle_audio(self):
        length = int(self.headers.getheader('content-length', 0))
        content_type = self.headers.getheader('content-type', '')

        # multipart file upload: curl -F "file=@sound.wav" localhost:5050/audio
        # or raw body with filename header: curl -X POST -H "X-Filename: sound.wav" --data-binary @sound.wav localhost:5050/audio
        filename = self.headers.getheader('x-filename', None)

        if not filename:
            # try to extract from content-disposition or use default
            filename = 'playback.wav'

        nao = self.nao_ref

        try:
            data = self.rfile.read(length)

            # save to /audio volume
            local_path = '{}/{}'.format(AUDIO_DIR, filename)
            with open(local_path, 'wb') as f:
                f.write(data)

            # push to NAO
            remote_path = '{}/{}'.format(NAO_AUDIO_DIR, filename)
            result = _push_to_nao(local_path, remote_path)

            if result != 0:
                raise Exception('failed to push audio to NAO')

            # play on NAO
            nao.env.audioPlayer.playFile(remote_path)

            # clean up from NAO after playback
            _remove_from_nao(remote_path)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "file": local_path}))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": str(e)}))

    def _handle_audio_play(self):
        filename = self.path.replace('/audio/play/', '')
        nao = self.nao_ref

        try:
            local_path = '{}/{}'.format(AUDIO_DIR, filename)
            if not os.path.exists(local_path):
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": "file not found: {}".format(filename)}))
                return

            remote_path = '{}/{}'.format(NAO_AUDIO_DIR, filename)
            result = _push_to_nao(local_path, remote_path)
            if result != 0:
                raise Exception('failed to push audio to NAO')

            nao.env.audioPlayer.playFile(remote_path)
            _remove_from_nao(remote_path)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "played": filename}))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": str(e)}))

    def do_GET(self):
        if self.path == '/audio':
            try:
                files = [f for f in os.listdir(AUDIO_DIR) if not f.startswith('.')]
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True, "files": sorted(files)}))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": str(e)}))
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ready"}))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

def start(nao, port=5050, block=False):
    NaoHandler.nao_ref = nao
    httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', port), NaoHandler)
    print("FluentNao server listening on port %d" % port)
    if block:
        httpd.serve_forever()
    else:
        thread = threading.Thread(target=httpd.serve_forever)
        thread.daemon = True
        thread.start()
