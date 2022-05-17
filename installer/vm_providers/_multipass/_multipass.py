
from .._base_provider import Provider

class Multipass(Provider):
    """A multipass provider for MicroK8s to execute its lifecycle."""

    def ensure_provider(cls):
        
