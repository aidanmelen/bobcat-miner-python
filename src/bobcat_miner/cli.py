import click
import logging
import os
import json
import time
import requests

try:
    from .bobcat import Bobcat
except:
    from bobcat import Bobcat

try:
    from .autopilot import BobcatAutopilot
except:
    from autopilot import BobcatAutopilot


@click.group(name="bobcat")
@click.version_option()
@click.pass_context
@click.option(
    "--hostname",
    "-h",
    required=False,
    metavar="NAME",
    envvar="BOBCAT_HOSTNAME",
    show_envvar=True,
    help="The Bobcat hostname.",
)
@click.option(
    "--animal",
    "-a",
    required=False,
    metavar="NAME",
    envvar="BOBCAT_ANIMAL",
    show_envvar=True,
    help="The Bobcat animal name to search for e.g. Fancy Awesome Bobcat.",
)
@click.option(
    "networks",
    "--network",
    "-n",
    required=False,
    multiple=True,
    default=["192.168.0.0/24", "10.0.0.0/24"],
    metavar="CIDR",
    envvar="BOBCAT_NETWORKS",
    show_envvar=True,
    help="The networks used to search for a Bobcat.",
)
@click.option(
    "--dry-run",
    "-d",
    is_flag=True,
    envvar="BOBCAT_DRY_RUN",
    show_envvar=True,
    help="Dry run where actions are skipped and wait times are 1 second long.",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    envvar="BOBCAT_VERBOSE",
    show_envvar=True,
    help="Verbosely log Bobcat Checks.",
)
@click.option(
    "--trace",
    "-t",
    is_flag=True,
    envvar="BOBCAT_TRACE",
    show_envvar=True,
    help="Trace and log Bobcat endpoint data when it is refreshed.",
)
@click.option(
    "--log-file",
    "-f",
    required=False,
    type=click.Path(writable=True),
    envvar="BOBCAT_LOG_FILE",
    show_envvar=True,
    help="The log file path.",
)
@click.option(
    "--discord-webhook-url",
    "-w",
    required=False,
    type=str,
    metavar="URL",
    envvar="BOBCAT_DISCORD_WEBHOOK_URL",
    show_envvar=True,
    help="The Discord webhook url where log events will be sent.",
)
@click.option(
    "--log-level-console",
    "-C",
    default="INFO",
    show_default=True,
    type=click.Choice(
        ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    metavar="LEVEL",
    envvar="BOBCAT_LOG_LEVEL_CONSOLE",
    show_envvar=True,
    help="The log level for the console log handler.",
)
@click.option(
    "--log-level-file",
    "-F",
    default="DEBUG",
    show_default=True,
    type=click.Choice(
        ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    metavar="LEVEL",
    envvar="BOBCAT_LOG_LEVEL_FILE",
    show_envvar=True,
    help="The log level for the file log handler.",
)
@click.option(
    "--log-level-discord",
    "-D",
    default="WARNING",
    show_default=True,
    type=click.Choice(
        ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    metavar="LEVEL",
    envvar="BOBCAT_LOG_LEVEL_DISCORD",
    show_envvar=True,
    help="The log level for the discord channel log handler.",
)
@click.option(
    "--lock-file",
    "-L",
    required=False,
    default=".bobcat.lock",
    show_default=True,
    type=click.Path(writable=True),
    envvar="BOBCAT_LOCK_FILE",
    show_envvar=True,
    help="The lock file path.",
)
@click.option(
    "--state-file",
    "-s",
    required=False,
    default=".bobcat.json",
    show_default=True,
    type=click.Path(writable=True),
    envvar="BOBCAT_STATE_FILE",
    show_envvar=True,
    help="The state file path.",
)
def cli(*args, **kwargs) -> None:
    """Bobcat miner command line tools."""
    ctx = args[0]
    ctx.ensure_object(dict)

    # Hardcode the bobcat logger log level to DEBUG to ensure no logs are filtered before they reach the log handlers
    # The CLI users should instead adjust the handler's log level e.g. --log-level-console, --log-level-file, and --log-level-discord
    kwargs["log_level"] = "DEBUG"

    ctx.obj["AUTOPILOT"] = BobcatAutopilot(**kwargs)


@cli.command()
@click.pass_context
def autopilot(ctx) -> None:
    """Automatically diagnose and repair the Bobcat miner."""
    try:
        ctx.obj["AUTOPILOT"].run()
    except Exception as err:
        raise click.ClickException(f"An unexpected error has occurred: {str(err)}")


@cli.command()
@click.pass_context
def find(ctx) -> None:
    """Search local network and find the Bobcat miner."""
    try:
        autopilot = ctx.obj["AUTOPILOT"]
        autopilot.find()
        click.echo(f"Found Bobcat: {autopilot._hostname}")
    except Exception as err:
        raise click.ClickException(f"An unexpected error has occurred: {str(err)}")


@cli.command()
@click.pass_context
def status(ctx) -> None:
    """Print Bobcat status data."""
    try:
        click.echo(ctx.obj["AUTOPILOT"].refresh_status()._status_data)
    except Exception as err:
        raise click.ClickException(f"An unexpected error has occurred: {str(err)}")


@cli.command()
@click.pass_context
def miner(ctx) -> None:
    """Print Bobcat miner data."""
    try:
        # miner_data is initialized in the BobcatConnection constructor during bobcat verification
        if miner_data := ctx.obj["AUTOPILOT"]._miner_data:
            click.echo(miner_data)
        else:
            click.echo(ctx.obj["AUTOPILOT"].refresh_miner()._miner_data)
    except Exception as err:
        raise click.ClickException(f"An unexpected error has occurred: {str(err)}")


@cli.command()
@click.pass_context
def speed(ctx) -> None:
    """Print Bobcat network speed data."""
    try:
        click.echo(ctx.obj["AUTOPILOT"].refresh_speed()._speed_data)
    except Exception as err:
        raise click.ClickException(f"An unexpected error has occurred: {str(err)}")


@cli.command()
@click.pass_context
def temp(ctx) -> None:
    """Print Bobcat CPU tempurature data."""
    try:
        click.echo(ctx.obj["AUTOPILOT"].refresh_temp()._temp_data)
    except Exception as err:
        raise click.ClickException(f"An unexpected error has occurred: {str(err)}")


@cli.command()
@click.pass_context
def dig(ctx) -> None:
    """Print Bobcat DNS data."""
    try:
        click.echo(ctx.obj["AUTOPILOT"].refresh_dig()._dig_data)
    except Exception as err:
        raise click.ClickException(f"An unexpected error has occurred: {str(err)}")


@cli.command()
@click.pass_context
def reboot(ctx) -> None:
    """Reboot the Bobcat."""
    try:
        if click.confirm("Do you want to reboot the Bobcat?"):
            click.echo(ctx.obj["AUTOPILOT"].managed_reboot())
    except Exception as err:
        raise click.ClickException(f"An unexpected error has occurred: {str(err)}")


@cli.command()
@click.pass_context
def reset(ctx) -> None:
    """Reset the Bobcat."""
    try:
        if click.confirm("Do you want to reset the Bobcat?"):
            click.echo(ctx.obj["AUTOPILOT"].managed_reset())
    except Exception as err:
        raise click.ClickException(f"An unexpected error has occurred: {str(err)}")


@cli.command()
@click.pass_context
def resync(ctx) -> None:
    """Resync the Bobcat."""
    try:
        if click.confirm("Do you want to resync the Bobcat?"):
            click.echo(ctx.obj["AUTOPILOT"].managed_resync())
    except Exception as err:
        raise click.ClickException(f"An unexpected error has occurred: {str(err)}")


@cli.command()
@click.pass_context
def fastsync(ctx) -> None:
    """Fastsync the Bobcat."""
    try:
        if click.confirm("Do you want to fastsync the Bobcat?"):
            click.echo(ctx.obj["AUTOPILOT"].managed_fastsync())
    except Exception as err:
        raise click.ClickException(f"An unexpected error has occurred: {str(err)}")


if __name__ == "__main__":
    cli(obj={})
