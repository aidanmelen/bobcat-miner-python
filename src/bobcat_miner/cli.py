import click
import logging
import os
import json
import time

try:
    from .bobcat import Bobcat
except:
    from bobcat import Bobcat

try:
    from .autopilot import Autopilot, BobcatConnectionError
except:
    from autopilot import Autopilot, BobcatConnectionError


@click.group(name="bobcat")
@click.version_option()
@click.pass_context
@click.option(
    "--ip-address",
    "-i",
    required=True,
    envvar="BOBCAT_IP_ADDRESS",
    show_envvar=True,
    help="The Bobcat IP address.",
)
@click.option(
    "--dry-run",
    "-D",
    is_flag=True,
    envvar="BOBCAT_DRY_RUN",
    show_envvar=True,
    help="Dry run where actions are skipped and wait times are 1 second long.",
)
@click.option(
    "--discord-webhook-url",
    "-d",
    required=False,
    type=str,
    envvar="BOBCAT_DISCORD_WEBHOOK_URL",
    show_envvar=True,
    help="The Discord webhook url where log events will be sent.",
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
    "--log-level",
    "-l",
    default="DEBUG",
    type=click.Choice(
        ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    envvar="BOBCAT_LOG_LEVEL",
    show_envvar=True,
    help="The log level.",
)
def cli(ctx, ip_address, dry_run, discord_webhook_url, log_file, log_level):
    """Bobcat command line tools"""
    bobcat = Bobcat(ip_address)
    autopilot = Autopilot(
        bobcat,
        dry_run=dry_run,
        discord_webhook_url=discord_webhook_url,
        log_file=log_file,
        log_level=log_level,
    )
    ctx.ensure_object(dict)
    ctx.obj["BOBCAT"] = bobcat
    ctx.obj["AUTOPILOT"] = autopilot


@cli.command()
@click.pass_context
def ping(ctx):
    """Verify Bobcat network connectively"""
    try:
        ctx.obj["AUTOPILOT"].ping()
    except BobcatConnectionError:
        ctx.obj["AUTOPILOT"].logger.error(
            f"The Autopilot was unable to connect to the Bobcat ({ctx.obj['IP_ADDRESS']})"
        )


@cli.command()
@click.pass_context
def autopilot(ctx):
    """Automatically diagnose and repair the Bobcat"""
    try:
        ctx.obj["AUTOPILOT"].run()
    except Exception as err:
        click.echo(click.style(err, fg="red"))


@cli.command()
@click.pass_context
def status(ctx):
    """Print the bobcat miner status data"""
    try:
        bobcat = ctx.obj["BOBCAT"]
        bobcat.refresh_status()
        click.echo(json.dumps(bobcat.status_data, indent=4))
    except Exception as err:
        click.echo(click.style(err, fg="red"))


@cli.command()
@click.pass_context
def miner(ctx):
    """Print the bobcat miner data"""
    try:
        bobcat = ctx.obj["BOBCAT"]
        bobcat.refresh_miner()
        click.echo(json.dumps(bobcat.miner_data, indent=4))
    except Exception as err:
        click.echo(click.style(err, fg="red"))


@cli.command()
@click.pass_context
def speed(ctx):
    """Print the bobcat miner network speed"""
    try:
        bobcat = ctx.obj["BOBCAT"]
        bobcat.refresh_speed()
        click.echo(json.dumps(bobcat.speed_data, indent=4))
    except Exception as err:
        click.echo(click.style(err, fg="red"))


@cli.command()
@click.pass_context
def temp(ctx):
    """Print the bobcat miner temp"""
    try:
        bobcat = ctx.obj["BOBCAT"]
        bobcat.refresh_temp()
        click.echo(json.dumps(bobcat.temp_data, indent=4))
    except Exception as err:
        click.echo(click.style(err, fg="red"))


@cli.command()
@click.pass_context
def dig(ctx):
    """Print the bobcat miner DNS data"""
    try:
        bobcat = ctx.obj["BOBCAT"]
        bobcat.refresh_dig()
        click.echo(json.dumps(bobcat.dig_data, indent=4))
    except Exception as err:
        click.echo(click.style(err, fg="red"))


@cli.command()
@click.pass_context
def reboot(ctx):
    """Reboot the Bobcat and wait for connection"""
    try:
        ctx.obj["AUTOPILOT"].reboot()
    except Exception as err:
        click.echo(click.style(err, fg="red"))


@cli.command()
@click.pass_context
@click.option(
    "--max-attempts",
    "-m",
    default=3,
    type=int,
    help="The maximun number of attempts before giving up.",
)
def reset(ctx, max_attempts):
    """Reset the Bobcat and wait for connection or exceeds max attempts"""
    try:
        ctx.obj["AUTOPILOT"].reset(max_attempts)
    except Exception as err:
        click.echo(click.style(err, fg="red"))


@cli.command()
@click.pass_context
def resync(ctx):
    """Resync the Bobcat and wait for connection"""
    try:
        ctx.obj["AUTOPILOT"].resync()
    except Exception as err:
        click.echo(click.style(err, fg="red"))


@cli.command()
@click.pass_context
@click.option(
    "--max-attempts",
    "-m",
    default=3,
    type=int,
    help="The maximun number of attempts before giving up.",
)
def fastsync(ctx, max_attempts):
    """Fastsync the Bobcat until the gap is less than 400 or exceeds max attempts"""
    try:
        ctx.obj["AUTOPILOT"].fastsync(max_attempts)
    except Exception as err:
        click.echo(click.style(err, fg="red"))


# TODO autosync
# @cli.command()
# @click.pass_context
# def autosync(ctx):
#     """Automatically sync the Bobcat by monitoring the gap during the proscribed reboot -> fastsync - > reset -> fastsync"""
#     try:
#         ctx.obj['AUTOPILOT'].autosync()
#     except Exception as err:
#         click.echo(click.style(err, fg='red'))


if __name__ == "__main__":
    cli(obj={})
