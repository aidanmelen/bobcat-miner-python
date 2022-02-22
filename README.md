[![PyPI](https://img.shields.io/pypi/v/bobcat_miner.svg)](https://pypi.org/project/bobcat-miner/)
[![Dockerhub](https://img.shields.io/docker/v/aidanmelen/bobcat?color=blue&label=docker%20build)](https://hub.docker.com/r/aidanmelen/bobcat)
[![Release](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/release.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/release.yaml)
[![Tests](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/tests.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/tests.yaml)
[![Lint](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/lint.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/lint.yaml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# bobcat miner python

Automate the Bobcat miner from the command line.

## Install

### Pipx

```bash
pipx install bobcat-miner
```

ℹ️ Please see this [guide](https://packaging.python.org/en/latest/guides/installing-stand-alone-command-line-tools/) for more information about installing stand alone command line tools with [pipx](https://pypa.github.io/pipx/).

### Docker

```bash
docker pull aidanmelen/bobcat
```

## Usage

Automatically *find*, *diagnose*, and *repair* the Bobcat miner!

**Offline**
```bash
bobcat autopilot
❌ Online Status: Offline
❌ Bobcat Status: Down
⚠️ Rebooting Bobcat
✅ Reconnected to the Bobcat (fancy-awesome-bobcat)
⚠️ Resetting Bobcat
✅ Reconnected to the Bobcat (fancy-awesome-bobcat)
⚠️ Fastsyncing Bobcat
✅ Reconnected to the Bobcat (fancy-awesome-bobcat)
✅ Repair Status: Complete
✅ Relay Status: Not Relayed ✨
✅ Network Status: Good 📶
✅ Temperature Status: Good (38°C) ☀️
```

**Online**
```bash
bobcat autopilot
✅ Online Status: Online ⭐
✅ Sync Status: Synced (gap:-1) 💫
✅ Relay Status: Not Relayed ✨
✅ Network Status: Good 📶
✅ Temperature Status: Good (38°C) ☀️
```

or run with the official Docker image

```bash
docker run --rm -it aidanmelen/bobcat autopilot
```

Run `bobcat --help` to learn about the available sub-commands and options.

## Finding your Bobcat

Searching for your bobcat may be slow. This step can be skipped by using the `--ip-address` option

```bash
bobcat --ip-address 192.168.0.10 -C DEBUG autopilot
🐛 Connected to Bobcat: 192.168.0.10
🐛 The Bobcat Autopilot is starting 🚀 🚀 🚀
...
```

ℹ️ Please see the offical [bobcat instructions](https://bobcatminer.zendesk.com/hc/en-us/articles/4412905935131-How-to-Access-the-Diagnoser) to manually find the IP address.

## Monitoring with Discord

Monitor your Bobcat remotely by sending events to a Discord channel. No need for VPN or SSH agent setup!

```bash
bobcat --discord-webhook-url https://discord.com/api/webhooks/xxx autopilot
✅ Online Status: Online ⭐
✅ Sync Status: Synced (gap:0) 💫
⚠️ Relay Status: Relayed
✅ Network Status: Good 📶
❌ Temperature Status: Hot (78°C) 🌋
```

and check the Discord channel

<!-- <img src="https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/assets/bobcat-autopilot-discord-app.png" alt="drawing" style="width:500px;"/> -->
<img src="https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/assets/bobcat-autopilot-discord-app.png" alt="drawing" width="300"/>

ℹ️ Please see Discord's [Intro to Webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) document for more information.

## Dry Run

Use the `--dry-run` option to see what repair steps the `bobcat autopilot` would normally run

```bash
bobcat --dry-run autopilot
❌ Online Status: Offline
❌ Bobcat Status: Down
⚠️ Dry run: Reboot Skipped
⚠️ Dry run: Reset Skipped
⚠️ Dry run: Fastsync Skipped
✅ Network Status: Good 📶
✅ Temperature Status: Good (38°C) ☀️
```

## Bobcat SDK

Please see the [Bobcat SDK Docs](https://github.com/aidanmelen/bobcat-miner-python/blob/main/docs/bobcat_sdk.md) for more information.


## Contributions

Please see the [Contributions Docs](https://github.com/aidanmelen/bobcat-miner-python/blob/main/docs/contributions.md) for more information. This document includes sections for Development, Test, and Release.

## DIY Troubleshooting

Please see [No Witness's Troubleshooting Guide](https://www.nowitness.org/troubleshooting/) for more information.

## Donations

Donations are welcome and appreciated! :gift:

[![HNT: 14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/assets/wallet.jpg)](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)

HNT: [14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)
