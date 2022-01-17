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
    default="TRACE",
    type=click.Choice(
        ["NOTSET", "TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    envvar="BOBCAT_LOG_LEVEL",
    show_envvar=True,
    help="The log level.",
)
def cli(ctx, ip_address, dry_run, discord_webhook_url, log_file, log_level):
    """Bobcat miner command line tools"""
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
            f"Failed to connect to the Bobcat ({ctx.obj['IP_ADDRESS']})"
        )


@cli.command()
@click.pass_context
def autopilot(ctx):
    """Automatically diagnose and repair the Bobcat"""
    try:
        ctx.obj["AUTOPILOT"].run()
    except Exception as err:
        autopilot.logger.exception("The Autopilot failed")


@cli.command()
@click.pass_context
@click.option(
    "--pprint/--no-pprint",
    " /-P",
    default=True,
    help="Pretty print the Bobcat endpoint JSON data.",
)
def status(ctx, pprint):
    """Print the bobcat miner status data"""
    try:
        autopilot = ctx.obj["AUTOPILOT"]
        bobcat = ctx.obj["BOBCAT"]
        bobcat.refresh_status()
        data = json.dumps(bobcat.status_data, indent=4) if pprint else bobcat.status_data
        autopilot.logger.debug(data)
    except Exception as err:
        autopilot.logger.exception("Failed to get the Bobcat status data")


@cli.command()
@click.pass_context
@click.option(
    "--pprint/--no-pprint",
    " /-P",
    default=True,
    help="Pretty print the Bobcat endpoint JSON data.",
)
def miner(ctx, pprint):
    """Print the bobcat miner data"""
    try:
        autopilot = ctx.obj["AUTOPILOT"]
        bobcat = ctx.obj["BOBCAT"]
        bobcat.refresh_miner()
        data = json.dumps(bobcat.miner_data, indent=4) if pprint else bobcat.miner_data
        autopilot.logger.debug(data)
    except Exception as err:
        autopilot.logger.exception("Failed to get the Bobcat miner data")


@cli.command()
@click.pass_context
@click.option(
    "--pprint/--no-pprint",
    " /-P",
    default=True,
    help="Pretty print the Bobcat endpoint JSON data.",
)
def speed(ctx, pprint):
    """Print the bobcat miner network speed"""
    try:
        autopilot = ctx.obj["AUTOPILOT"]
        bobcat = ctx.obj["BOBCAT"]
        bobcat.refresh_speed()
        data = json.dumps(bobcat.speed_data, indent=4) if pprint else bobcat.speed_data
        autopilot.logger.debug(data)
    except Exception as err:
        autopilot.logger.exception("Failed to get the Bobcat speed data")


@cli.command()
@click.pass_context
@click.option(
    "--pprint/--no-pprint",
    " /-P",
    default=True,
    help="Pretty print the Bobcat endpoint JSON data.",
)
def temp(ctx, pprint):
    """Print the bobcat miner temp"""
    try:
        autopilot = ctx.obj["AUTOPILOT"]
        bobcat = ctx.obj["BOBCAT"]
        bobcat.refresh_temp()
        data = json.dumps(bobcat.temp_data, indent=4) if pprint else bobcat.temp_data
        autopilot.logger.debug(data)
    except Exception as err:
        autopilot.logger.exception("Failed to get the Bobcat tempurature data")


@cli.command()
@click.pass_context
@click.option(
    "--pprint/--no-pprint",
    " /-P",
    default=True,
    help="Pretty print the Bobcat endpoint JSON data.",
)
def dig(ctx, pprint):
    """Print the bobcat miner DNS data"""
    try:
        autopilot = ctx.obj["AUTOPILOT"]
        bobcat = ctx.obj["BOBCAT"]
        bobcat.refresh_dig()
        data = json.dumps(bobcat.dig_data, indent=4) if pprint else bobcat.dig_data
        autopilot.logger.debug(data)
    except Exception as err:
        autopilot.logger.exception("Failed to get the Bobcat dig data")


@cli.command()
@click.pass_context
def reboot(ctx):
    """Reboot the Bobcat and wait for connection"""
    try:
        ctx.obj["AUTOPILOT"].reboot()
    except Exception as err:
        ctx.obj["AUTOPILOT"].logger.exception("Failed to reboot the Bobcat")


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
        ctx.obj["AUTOPILOT"].logger.exception("Failed to reset the Bobcat")


@cli.command()
@click.pass_context
def resync(ctx):
    """Resync the Bobcat and wait for connection"""
    try:
        ctx.obj["AUTOPILOT"].resync()
    except Exception as err:
        ctx.obj["AUTOPILOT"].logger.exception("Failed to resync the Bobcat")


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
        ctx.obj["AUTOPILOT"].logger.exception("Failed to fastsync the Bobcat")


# TODO autosync
# @cli.command()
# @click.pass_context
# def autosync(ctx):
#     """Automatically sync the Bobcat by monitoring the gap during the proscribed reboot -> fastsync - > reset -> fastsync"""
#     try:
#         ctx.obj['AUTOPILOT'].autosync()
#     except Exception as err:
#        ctx.obj["AUTOPILOT"].logger.exception("Failed to autosync the Bobcat")


if __name__ == "__main__":
    cli(obj={})
