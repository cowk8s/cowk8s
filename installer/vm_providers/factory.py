from typing import TYPE_CHECKING

from . import errors

if TYPE_CHECKING:
    from typing import Type

def get_provider_for(provider_name: str) -> "Type[Provider]":
    """Returns a Type that can build with provider_name"""
    if provider_name == "multipass":
        return Multipass
    else:
        raise errors.ProviderNotSupportedError(provider=provider_name)