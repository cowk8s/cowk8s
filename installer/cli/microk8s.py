import argparse
import logging
import click

from common import definitions
from vm_providers.factory import get_provider_for
from vm_providers.errors import ProviderNotFound, ProviderInstanceNotFoundError

logger = logging.getLogger(__name__)

@click.command(
    name="microk8s",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ),
)
@click.option("-h", "--help", is_flag=True)
@click.pass_context
def cli(ctx, help):
    try:
        if help and len(ctx.args) == 0:
            show_help()
            exit(0)
    except Exception as e:
        exit(254)

def show_help():
    msg = """Usage: microk8s [OPTIONS] COMMAND [ARGS]..."""

def install(args) -> None:
    parser = argparse.ArgumentParser("microk8s install")
    parser.add_argument("--cpu", default=definitions.DEFAULT_CORES, type=int)
    parser.add_argument("--mem", default=definitions.DEFAULT_MEMORY, type=int)
    parser.add_argument("--disk", default=definitions.DEFAULT_DISK, type=int)
    parser.add_argument("--channel", default=definitions.DEFAULT_CHANNEL, type=str)
    parser.add_argument(
        "-y", "--assume-yes", action="store_true", default=definitions.DEFAULT_ASSUME
    )
    args = parser.parse_args(args)

    vm_provider_name: str = "multipass"
    vm_provider_class = get_provider_for(vm_provider_name)
    try:
        vm_provider_class.ensure_provider()
    except ProviderNotFound as provider_error:
        if provider_error.prompt_installable:
        

    instance = vm_provider_class(echoer=echo)
    spec = vars(args)
    spec.update({"kubeconfig": get_kubeconfig_path()})
    instance.launch_instance(spec)
    echo.info("MicroK8s is up and running. See the available commands with `microk8s --help`.")

def start() -> None:
    