"""SSH and SCP utilities for file transfer with the NAO robot.

Python 2.7 compatible. Provides module-level functions (not a class).
"""
import os
import subprocess

NAO_USER = 'nao'
SSH_OPTS = '-F /dev/null -i /root/.ssh/id_nao -o StrictHostKeyChecking=no -o BatchMode=yes'
_CLEAN_ENV = 'LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu'


def nao_ip():
    """Return the NAO IP from NAO_IP env var, defaulting to 192.168.68.96."""
    return os.environ.get('NAO_IP', '192.168.68.96')


def ssh(cmd):
    """Run a command on the NAO over SSH.

    Args:
        cmd: Shell command string to execute on the robot.

    Returns:
        Subprocess exit code (int).
    """
    return subprocess.call(
        '{} ssh {} {}@{} {}'.format(_CLEAN_ENV, SSH_OPTS, NAO_USER, nao_ip(), cmd),
        shell=True)


def scp_to_nao(local_path, remote_path):
    """Copy a local file to the NAO robot via SCP.

    Returns:
        Subprocess exit code (int).
    """
    return subprocess.call(
        '{} scp {} {} {}@{}:{}'.format(_CLEAN_ENV, SSH_OPTS, local_path, NAO_USER, nao_ip(), remote_path),
        shell=True)


def scp_from_nao(remote_path, local_path):
    """Copy a file from the NAO robot to the local filesystem via SCP.

    Returns:
        Subprocess exit code (int).
    """
    return subprocess.call(
        '{} scp {} {}@{}:{} {}'.format(_CLEAN_ENV, SSH_OPTS, NAO_USER, nao_ip(), remote_path, local_path),
        shell=True)
