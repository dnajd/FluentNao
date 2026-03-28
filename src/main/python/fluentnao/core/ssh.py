"""
Shared SSH utility for file transfer between a Docker container and the NAO robot.

Python 2.7 compatible. Provides module-level functions (not a class).

Authentication uses key-based SSH with /root/.ssh/id_nao (PEM format), which is
mounted into the Docker container from the host. StrictHostKeyChecking is disabled
and BatchMode is enabled to avoid interactive prompts.

LD_LIBRARY_PATH is explicitly overridden to /usr/lib/x86_64-linux-gnu before
each subprocess call. This prevents pynaoqi's bundled libcrypto from conflicting
with the system SSH/SCP binaries.

The NAO's IP address is read from the NAO_IP environment variable, defaulting
to 192.168.68.96.

Functions
---------
  - nao_ip()
      Returns the NAO IP address from NAO_IP env var (default '192.168.68.96').

  - ssh(cmd)
      Runs a command on the NAO over SSH. Returns subprocess exit code.
      Example: ssh('cat /etc/naoqi/autoload.ini')

  - scp_to_nao(local_path, remote_path)
      Copies a local file to the NAO robot. Returns subprocess exit code.
      Example: scp_to_nao('/tmp/sound.wav', '/home/nao/sound.wav')

  - scp_from_nao(remote_path, local_path)
      Copies a file from the NAO robot to the local filesystem. Returns subprocess exit code.
      Example: scp_from_nao('/home/nao/recording.wav', '/tmp/recording.wav')

Used By
-------
  - audio.py: pulls recordings from NAO, pushes playback files to NAO
  - vision.py: object learning file transfer
  - server.py: audio endpoints for the HTTP bridge
"""
import os
import subprocess

NAO_USER = 'nao'
SSH_OPTS = '-F /dev/null -i /root/.ssh/id_nao -o StrictHostKeyChecking=no -o BatchMode=yes'
_CLEAN_ENV = 'LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu'


def nao_ip():
    return os.environ.get('NAO_IP', '192.168.68.96')


def ssh(cmd):
    return subprocess.call(
        '{} ssh {} {}@{} {}'.format(_CLEAN_ENV, SSH_OPTS, NAO_USER, nao_ip(), cmd),
        shell=True)


def scp_to_nao(local_path, remote_path):
    return subprocess.call(
        '{} scp {} {} {}@{}:{}'.format(_CLEAN_ENV, SSH_OPTS, local_path, NAO_USER, nao_ip(), remote_path),
        shell=True)


def scp_from_nao(remote_path, local_path):
    return subprocess.call(
        '{} scp {} {}@{}:{} {}'.format(_CLEAN_ENV, SSH_OPTS, NAO_USER, nao_ip(), remote_path, local_path),
        shell=True)
