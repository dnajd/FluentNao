import BaseHTTPServer
import json
import os
import sys
import threading
import time
import traceback

from fluentnao.core.ssh import ssh, scp_to_nao

AUDIO_DIR = '/data/audio'
NAO_AUDIO_DIR = '/home/nao/audio_playback'


def _log(msg):
    if os.environ.get('FLUENTNAO_LOG'):
        sys.stderr.write('{} {}\n'.format(time.strftime('%H:%M:%S'), msg))


# event queue for long polling
_event_queue = []
_event_lock = threading.Lock()
_event_condition = threading.Condition(_event_lock)


def _push_event(event_name, value):
    with _event_condition:
        _event_queue.append({
            'event': event_name,
            'value': str(value),
            'timestamp': time.time()
        })
        _event_condition.notify_all()


def _push_to_nao(local_path, remote_path):
    ssh('mkdir -p {}'.format(NAO_AUDIO_DIR))
    return scp_to_nao(local_path, remote_path)

def _remove_from_nao(remote_path):
    ssh('rm -f {}'.format(remote_path))

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
            t0 = time.time()
            preview = script[:80].replace('\n', ' ')
            _log('[exec] >> {}'.format(preview))
            try:
                result = eval(script, {"nao": nao})
                _log('[exec] << ok ({:.3f}s)'.format(time.time() - t0))
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True, "result": str(result)}))
            except SyntaxError:
                try:
                    ns = {"nao": nao}
                    exec(script, ns)
                    _log('[exec] << ok ({:.3f}s)'.format(time.time() - t0))
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    if "result" in ns and ns["result"] is not None:
                        self.wfile.write(json.dumps({"ok": True, "result": str(ns["result"])}))
                    else:
                        self.wfile.write(json.dumps({"ok": True}))
                except Exception as e:
                    _log('[exec] << ERROR ({:.3f}s) {}'.format(time.time() - t0, e))
                    traceback.print_exc(file=sys.stderr)
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"ok": False, "error": str(e)}))
            except Exception as e:
                _log('[exec] << ERROR ({:.3f}s) {}'.format(time.time() - t0, e))
                traceback.print_exc(file=sys.stderr)
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

            # play on NAO, always clean up
            try:
                nao.env.audioPlayer.playFile(remote_path)
            finally:
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
        filename = os.path.basename(self.path.replace('/audio/play/', ''))
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

            try:
                nao.env.audioPlayer.playFile(remote_path)
            finally:
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

    def _handle_events(self):
        """Long poll endpoint. Blocks until events arrive or timeout."""
        # parse timeout from query string (default 30s)
        timeout = 30
        if '?' in self.path:
            for param in self.path.split('?')[1].split('&'):
                if param.startswith('timeout='):
                    try:
                        timeout = int(param.split('=')[1])
                    except ValueError:
                        pass

        with _event_condition:
            # if events already queued, return immediately
            if not _event_queue:
                _event_condition.wait(timeout)

            # grab and clear the queue
            events = list(_event_queue)
            del _event_queue[:]

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True, "events": events}))

    def do_GET(self):
        if self.path == '/events' or self.path.startswith('/events?'):
            self._handle_events()
        elif self.path == '/audio':
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
        import sys
        if os.environ.get('FLUENTNAO_LOG'):
            sys.stderr.write("%s - - [%s] %s\n" %
                             (self.client_address[0],
                              self.log_date_time_string(),
                              format % args))

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
