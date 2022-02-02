[![PyPI](https://img.shields.io/pypi/v/bobcat_miner.svg)](https://pypi.org/project/bobcat-miner/)
[![Dockerhub](https://img.shields.io/docker/v/aidanmelen/bobcat?color=blue&label=docker%20build)](https://hub.docker.com/r/aidanmelen/bobcat)
[![Release](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/release.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/release.yaml)
[![Tests](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/tests.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/tests.yaml)
[![Lint](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/lint.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/lint.yaml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# bobcat miner python

A command line tool used to automate the Bobcat miner. This project also offers a robust python SDK's for interacting with the Bobcat miner.

## Install

```bash
$ pipx install bobcat-miner
```

Please see this [guide](https://packaging.python.org/en/latest/guides/installing-stand-alone-command-line-tools/) for more information about installing stand alone command line tools with [pipx](https://pypa.github.io/pipx/).

## Quick Start

The `bobcat autopilot` command will automatically diagnose and repair the Bobcat miner!

```bash
$ bobcat autopilot
✅ Sync Status: Synced (gap:-1) ✨
✅ Relay Status: Not Relayed ✨
✅ Network Status: Good 📶
✅ Temperature Status: Good (38°C) ☀️
```

or run with the offical Docker image

```bash
$ docker run --rm -it aidanmelen/bobcat autopilot
```

Run `bobcat --help` to learn about the available commands and options.

## Finding your Bobcat

By default, the Bobcat Autopilot will search the common `192.168.0.0/24` and `10.0.0.0/24` local networks to find the Bobcat miner.

### Find Bobcat by Animal Name

This will connect to the Bobcat on your network that matches the animal name.

```bash
$ bobcat --animal "Fancy Awesome Bobcat" -C DEBUG autopilot
🐛 Connected to Bobcat: 192.168.0.10
🐛 Refresh: Miner Data
🐛 Verified Bobcat Animal: fancy-awesome-bobcat
🐛 The Bobcat Autopilot is starting 🚀 🚀 🚀
```

### Specify the Hostname / IP Address

Otherwise, you can follow these [instructions](https://bobcatminer.zendesk.com/hc/en-us/articles/4412905935131-How-to-Access-the-Diagnoser) to find your Bobcats's ip address and specify it with:

```bash
$ bobcat --hostname 192.168.0.10 -C DEBUG autopilot
🐛 Connected to Bobcat: 192.168.0.10
🐛 The Bobcat Autopilot is starting 🚀 🚀 🚀
```

## Monitoring with Discord

Monitor your Bobcat remotely by sending events to a Discord channel by specifying a [webhook URL](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks). No need for VPN or SSH agent setup!

```bash
$ bobcat --discord-webhook-url https://discord.com/api/webhooks/xxx autopilot
✅ Sync Status: Synced (gap:0) ✨
⚠️ Relay Status: Relayed
✅ Network Status: Good 📶
❌ Temperature Status: Hot (78°C) 🌋
```

By default, all events `WARNING` or higher (i.e. `ERROR` and `CRITICAL`) will be sent to the Discord channel. This can be configured to include `DEBUG` and `INFO` events as well.

<!-- <img src="https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/assets/bobcat-autopilot-discord-app.png" alt="drawing" style="width:500px;"/> -->
<img src="https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/assets/bobcat-autopilot-discord-app.png" alt="drawing" width="300"/>

### Dry Run

This example is admittedly contrived, but it demonstrates how the `--dry-run` option can be used show what actions would normally be performed against the bobcat without actually running them.

```bash
$ bobcat --dry-run reboot
Do you want to reboot the Bobcat? [y/N]: y
⚠️ Dry run is enabled: Reboot Skipped
```

## Bobcat SDK

Please see [docs/bobcat_sdk.md](https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/docs/bobcat_sdk.md) for more information.


## Contributions

Please see [docs/contributions.md](https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/docs/contributions.md) for more information.

## Troubleshooting

Please see [No Witness's Troubleshooting Guide](https://www.nowitness.org/troubleshooting/) for more information.

## Donations

Donations are welcome and appreciated! :gift:

[![HNT: 14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/assets/wallet.jpg)](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)

HNT: [14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)
