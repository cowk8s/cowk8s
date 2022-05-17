
import logging
import shutil
import subprocess

from time import sleep
from typing import Dict, Optional, Sequence  # noqa: F401

logger = logging.getLogger(__name__)

def _run(command: Sequence[str], stdin=subprocess.DEVNULL) -> None:
    logger.debug("Running {}".format(" ".join(command)))
    subprocess.check_call(command, stdin=stdin)

def _run_output(command: Sequence[str], **kwargs) -> bytes:
    logger.debug("Running {}".format(" ".join(command)))
    return subprocess.check_output(command, **kwargs)

class MultipassCommand:
    """An object representation of common multipass cli commands."""

    provider_name = "multipass"
    provider_cmd = "multipass"


    def ensure_multipass(cls, platform: str) -> None:
        raise errors

    def mount(
        self,
        *,
        source: str,
        target: str,
        uid_map: Dict[str, str] = None,
        gid_map: Dict[str, str] = None
    ) -> None:
        """Passthrough for running multipass mount.

        :param str source: path to the local directory to mount.
        :param str target: mountpoint inside the instance in the form of
                           <instance-name>:path.
        :param dict uid_map: A mapping of user IDs for use in the mount of the form
                             <host-id> -> <instance-id>.
                             File and folder ownership will be mapped from
                             <host> to <instance-name> inside the instance.
        :param dict gid_map: A mapping of group IDs for use in the mount of the form
                             <host-id> -> <instance-id>.
                             File and folder ownership will be mapped from
                             <host> to <instance-name> inside the instance.
        :raises errors.ProviderMountError: when the mount operation fails.
        """
        cmd = [self.provider_cmd, "mount", source, target]
        if uid_map is None:
            uid_map = dict()
        for host_map, instance_map in uid_map.items():
            cmd.extend(["--uid-map", "{}:{}".format(host_map, instance_map)])
        if gid_map is None:
            gid_map = dict()
        for host_name, instance_map in gid_map.items():
            cmd.extend(["--gid-map", "{}:{}".format(host_map, instance_map)])
        try:
            _run(cmd)
        except subprocess.CalledProcessError as process_error:
            raise errors.ProviderMountError(
                
            )

    def info(self, *, instance_name: str, output_format: str = None) -> bytes:
        """Passthrough for running multipass info."""
        cmd = [self.provider_cmd, "info", instance_name]
        if output_format is not None:
            cmd.extend(["--format", output_format])
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, strerr = process.communicate()
        if process.returncode != 0:
            raise errors.Pro