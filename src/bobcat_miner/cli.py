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


LOG_LEVELS_CHOICES = ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


@click.group(name="bobcat")
@click.version_option()
@click.pass_context
@click.option(
    "hostname",
    "--hostname",
    "-h",
    "--ip-address",
    "-ip",
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
    default=[
        "192.168.0.0/24",
        "10.0.0.0/24",
        "172.16.0.0/24",
        "192.168.0.1/16",
        "10.0.0.1/16",
        "172.16.0.1/16",
    ],
    metavar="CIDR",
    envvar="BOBCAT_NETWORKS",
    show_envvar=True,
    help="The networks used to search for a Bobcat.",
)
@click.option(
    "--dry-run",
    "-dr",
    is_flag=True,
    envvar="BOBCAT_DRY_RUN",
    show_envvar=True,
    help="Dry run where actions are skipped",
)
@click.option(
    "--no-wait",
    "-nw",
    is_flag=True,
    envvar="BOBCAT_NO_WAIT",
    show_envvar=True,
    help="Dry run where actions are skipped",
)
@click.option(
    "--trace",
    "-t",
    is_flag=True,
    envvar="BOBCAT_TRACE",
    show_envvar=True,
    help="Trace logging when Bobcat endpoint data is refreshed.",
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
    type=click.Choice(LOG_LEVELS_CHOICES, case_sensitive=False),
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
    type=click.Choice(LOG_LEVELS_CHOICES, case_sensitive=False),
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
    type=click.Choice(LOG_LEVELS_CHOICES, case_sensitive=False),
    metavar="LEVEL",
    envvar="BOBCAT_LOG_LEVEL_DISCORD",
    show_envvar=True,
    help="The log level for the discord channel log handler.",
)
def cli(*args, **kwargs) -> None:
    """Bobcat miner command line tools."""
    ctx = args[0]
    ctx.ensure_object(dict)

    # Hardcode the bobcat logger log level to DEBUG to ensure no logs are filtered before they reach the log handlers
    # The CLI users should instead adjust the handler's log level e.g. --log-level-console, --log-level-file, and --log-level-discord
    kwargs["log_level"] = "DEBUG"

    # create bobcat instance
    ctx.obj["BOBCAT"] = Bobcat(**kwargs)


@cli.command()
@click.pass_context
@click.option(
    "--lock-file",
    "-l",
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
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    envvar="BOBCAT_VERBOSE",
    show_envvar=True,
    help="Verbose diagnostic debug logging.",
)
def autopilot(*args, **kwargs) -> None:
    """Automatically diagnose and repair the Bobcat miner."""
    ctx = args[0]

    bobcat = ctx.obj["BOBCAT"]
    lock_file = kwargs["lock_file"]
    state_file = kwargs["state_file"]
    verbose = kwargs["verbose"]
    BobcatAutopilot(bobcat, lock_file, state_file, verbose).run()


@cli.command()
@click.pass_context
def find(ctx) -> None:
    """Search local network and find the Bobcat miner."""
    click.echo(ctx.obj["BOBCAT"]._hostname)


@cli.command()
@click.pass_context
def status(ctx) -> None:
    """Print Bobcat status data."""
    click.echo(ctx.obj["BOBCAT"].refresh_status()._status_data)


@cli.command()
@click.pass_context
def miner(ctx) -> None:
    """Print Bobcat miner data."""

    # miner data is initialized in the BobcatConnection constructor during bobcat verification
    if miner_data := ctx.obj["BOBCAT"]._miner_data:
        click.echo(miner_data)
    else:
        click.echo(ctx.obj["BOBCAT"].refresh_miner()._miner_data)


@cli.command()
@click.pass_context
def speed(ctx) -> None:
    """Print Bobcat network speed data."""

    click.echo(ctx.obj["BOBCAT"].refresh_speed()._speed_data)


@cli.command()
@click.pass_context
def temp(ctx) -> None:
    """Print Bobcat CPU temperature data."""

    click.echo(ctx.obj["BOBCAT"].refresh_temp()._temp_data)


@cli.command()
@click.pass_context
def dig(ctx) -> None:
    """Print Bobcat DNS data."""
    click.echo(ctx.obj["BOBCAT"].refresh_dig()._dig_data)


@cli.command()
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    help="Automatically say yes to confirmation prompt.",
)
@click.pass_context
def reboot(ctx, yes) -> None:
    """Reboot the Bobcat."""
    if yes:
        click.echo(ctx.obj["BOBCAT"].reboot())

    elif click.confirm("Are you sure you want to restart your hotspot?"):
        click.echo(ctx.obj["BOBCAT"].reboot())


@cli.command()
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    help="Automatically say yes to confirmation prompt.",
)
@click.pass_context
def reset(ctx, yes) -> None:
    """Reset the Bobcat."""
    click.echo(
        "This action will delete all the Helium software and blockchain data and let your miner start resyncing from 0. If your hotspot out of sync, please use Resync/Fastsync. Make sure you don't lose power or internet connectivity during the reset."
    )
    if yes:
        click.echo(ctx.obj["BOBCAT"].reset())

    elif click.confirm("Are you sure you want to reset it now?"):
        click.echo(ctx.obj["BOBCAT"].reset())


@cli.command()
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    help="Automatically say yes to confirmation prompt.",
)
@click.pass_context
def resync(ctx, yes) -> None:
    """Resync the Bobcat."""
    click.echo(
        "This action will delete all blockchain data and let your miner start resyncing from 0. Make sure you don't lose power or internet connectivity during the resync."
    )
    if yes:
        click.echo(ctx.obj["BOBCAT"].resync())

    elif click.confirm("Are you sure you want to resync it now?"):
        click.echo(ctx.obj["BOBCAT"].resync())


@cli.command()
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    help="Automatically say yes to confirmation prompt.",
)
@click.pass_context
def fastsync(ctx, yes) -> None:
    """Fastsync the Bobcat."""
    click.echo(
        'Use Fast Sync only if you just used "Resync" / "Reset" (after 30 minutes) and the LED has turned green, if the miner had recently been fully synced but out of sync again for a long time, you need to play some catch-up now.'
    )
    if yes:
        click.echo(ctx.obj["BOBCAT"].fastsync())

    elif click.confirm("Are you sure you want to fastsync it now?"):
        click.echo(ctx.obj["BOBCAT"].fastsync())


if __name__ == "__main__":
    cli(obj={})
