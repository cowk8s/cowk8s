import shlex
from typing import Any, Dict, Optional
from typing import Sequence  # noqa: F401

from common.errors import BaseError

class ConnectivityError(BaseError):
    pass

class ProviderBaseError(BaseError):
    pass

class ProviderNotSupportedError(ProviderBaseError):

    fmt = (
        "The {provider!r} provider is not supported, please choose a "
        "different one and try again."
    )

    def __init__(self, provider: str) -> None:
        super().__init__(provider=provider)

class ProviderNotFound(ProviderBaseError):

    fmt = "You need {provider!r} set up to build snaps: {error_message}."

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

class ProviderBadDataError(ProviderBaseError):

    fmt = (
        "The data returned by {provider_name!r} was not expected "
        "or in the wrong format: {data!r}."
    )

    def __init__(self, *, provider_name: str, data: str) -> None:
        super().__init__(provider_name=provider_name, data=data)

class ProviderMultipassDownloadFailed(ProviderBaseError):
    fmt = (
        "Failed to download Multipass: {message!r}\n"
        "Please install manually. You can find the latest release at:\n"
        "https://multipass.run"
    )

    def __init__(self, message):
        super().__init__(message=message)

class ProviderMultipassInstallationFailed(ProviderBaseError):
    fmt = (
        "Failed to install Multipass: {message!r}\n"
        "Please install manually. You can find the latest release at:\n"
        "https://multipass.run"
    )

    def __init__(self, message):
        super().__init__(message=message)