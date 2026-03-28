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
