
import abc
from math import fabs
import pathlib
from shelve import Shelf
from shlex import shlex
import sys
from typing import Dict
from typing import Optional, Sequence

from installer.vm_providers import errors


class Provider(abc.ABC):
    def __init__(
        self,
        *,
        echoer,
        is_ephemeral: bool = False,
        build_provider_flags: Dict[str, str] = None,
    ) -> None:
        self.echoer = echoer
        self._is_ephemeral = is_ephemeral

        self.instance_name = "microk8s-vm"

        if build_provider_flags is None:
            build_provider_flags = dict()
        self.build_provider_flags = build_provider_flags.copy()

        self._cached_home_directory: Optional[pathlib.Path] = None

    @classmethod
    def ensure_provider(cls) -> None:
        """Necessary steps to ensure the provider is correctly setup."""

    @classmethod
    def setup_provider(cls, *, echoer) -> None:
        """Necessary steps to install the provider on the host."""

    @classmethod
    def _get_provider_name(cls) -> str:
        """Return the provider name."""

    @abc.abstractmethod
    def _launch(self, specs: Dict):
        """Launch the instance."""

    @abc.abstractmethod
    def _start(self):
        """Start an existing the instance."""

    def launch_instance(self, specs: Dict) -> None:
        try:
            # An ProviderStartError exception here means we need to create.
            self._start()
        except errors.ProviderInstanceNotFoundError:
            self._launch(specs)
            self._check_connectivity()
            # We need to setup MicroK8s and scan for cli commands.
            self._setup_microk8s(specs)
            self._copy_kubeconfig_to_kubectl(specs)

    def _check_connectivity(self) -> None:
        """Check that the VM can access the internet."""
        try:
            self.run("ping -c 1 snapcraft.io".split(), hide_output=True)
        except errors.ProviderLaunchError:
            self.destroy()
            raise

    def _get_home_directory(self) -> pathlib.Path:
        """Get user's home directory path."""
        if self._cached_home_directory is not None:
            return self._cached_home_directory

        command = ["printenv", "HOME"]
        run_output = self.run(command=command, hide_output=True)

        # Shouldn't happen, but due to _run()'s return type as being Optional,
        # we need to check for it anyways for mypy.
        if not run_output:
            provider_name = self._get_provider_name()
            raise errors.ProviderExecError(
                provider_name=provider_name, command=command, exit_code=2
            )

        cached_home_directory = pathlib.Path(run_output.decode().strip())

        self._cached_home_directory = cached_home_directory
        return cached_home_directory

    def _base_has_changed(self, base: str, provider_base: str) -> bool:
        # Make it backwards compatible with instances without project info
        if base == "core18" and provider_base is None:
            return False
        elif base != provider_base:
            return True

        return False

    def _log_run(self, command: Sequence[str]) -> None:
        cmd_string = " ".join([shlex.quote(c) for c in command])
        logger.debug(f"Running: {cmd_string}")

    @abc.abstractmethod
    def stop(self) -> None:
        pass