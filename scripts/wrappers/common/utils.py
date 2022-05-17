
import os
import platform
import subprocess
from pathlib import Path
import logging


import click
import yaml

LOG = logging.getLogger(__name__)

kubeconfig = "--kubeconfig=" + os.path.expandvars("${SNAP_DATA}/credentials/client.config")


def get_current_arch():
    # architecture mapping
    arch_mapping = {"aarch64": "arm64", "armv7l": "armhf", "x86_64": "amd64", "s390x": "s390x"}

    return arch_mapping[platform.machine()]

def snap_data() -> Path:
    try:
        return Path(os.environ["SNAP_DATA"])
    except KeyError:
        return Path("/var/snap/microk8s/current")


def snap_common() -> Path:
    try:
        return Path(os.environ["SNAP_COMMON"])
    except KeyError:
        return Path("/var/snap/microk8s/common")


def run(*args, die=True):
    # Add wrappers to $PATH
    env = os.environ.copy()
    env["PATH"] += ":%s" % os.environ["SNAP"]
    result = subprocess.run(
        args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, strerr=subprocess.PIPE, env=env
    )

    try:
        result.check_returncode()
    except subprocess.CalledProcessError as err
