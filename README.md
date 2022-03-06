[![PyPI](https://img.shields.io/pypi/v/bobcat_miner.svg)](https://pypi.org/project/bobcat-miner/)
[![Dockerhub](https://img.shields.io/docker/v/aidanmelen/bobcat?color=blue&label=docker%20build)](https://hub.docker.com/r/aidanmelen/bobcat)
[![Release](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/release.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/release.yaml)
[![Tests](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/tests.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/tests.yaml)
[![Lint](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/lint.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/lint.yaml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# bobcat miner python

Automatically *find*, *diagnose*, and *repair* the Bobcat miner!

**Online**
```console
$ bobcat autopilot
✅ Online Status: Online ⭐
✅ Sync Status: Synced (gap:-1) 💫
✅ Relay Status: Not Relayed ✨
✅ Network Status: Good 📶
✅ Temperature Status: Good (38°C) ☀️
```

**Offline**
```console
$ bobcat autopilot
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

or run with the official Docker image

```
docker run --rm -it aidanmelen/bobcat autopilot
```

ℹ️ Run `bobcat --help` to learn about the available sub-commands and options.

## Install

### Pipx

```
pipx install bobcat-miner
```

ℹ️ Please see this [guide](https://packaging.python.org/en/latest/guides/installing-stand-alone-command-line-tools/) for more information about installing stand alone command line tools with [pipx](https://pypa.github.io/pipx/).

### Docker

```
docker pull aidanmelen/bobcat
```

## Finding your Bobcat

Autopilot will automatically search and find your Bobcat. Setting the log-level to `DEBUG` will show more information about the search process.

```console
$ bobcat -C DEBUG autopilot
🐛 Searching for a bobcat in these networks: 192.168.0.0/24, 10.0.0.0/24, 172.16.0.0/24, 192.168.0.1/16, 10.0.0.1/16, 172.16.0.1/16
🐛 Searching network: 192.168.0.0/24
🐛 Connected to Bobcat: 192.168.0.10
🐛 Found Bobcat: 192.168.0.10
🐛 The Bobcat Autopilot is starting 🚀 🚀 🚀
...
```

The search may take awhile depending on your Bobcat's IP address. However; this step can be skipped by specifying either the `--ip-address` or `--hostname` options.

```console
$ bobcat --ip-address 192.168.0.10 -C DEBUG autopilot
🐛 Connected to Bobcat: 192.168.0.10
🐛 The Bobcat Autopilot is starting 🚀 🚀 🚀
...
```

ℹ️ Please see the offical [bobcat instructions](https://bobcatminer.zendesk.com/hc/en-us/articles/4412905935131-How-to-Access-the-Diagnoser) to manually find the IP address.

## Dry Run

Use the `--dry-run` option to see what repair steps the `bobcat autopilot` would normally run

```console
$ bobcat --dry-run autopilot
❌ Online Status: Offline
❌ Bobcat Status: Down
⚠️ Dry Run: Reboot Skipped
⚠️ Dry Run: Reset Skipped
⚠️ Dry Run: Fastsync Skipped
✅ Network Status: Good 📶
✅ Temperature Status: Good (38°C) ☀️
```

## Verbose

Use the `--verbose` option to see detailed diagnostics

```console
$ bobcat autopilot --verbose
...
❌ Bobcat Status: Down
**Points to:** Miner's Docker Container

**Why does this happen?** 
This can happen if your miner's Docker crashes. Sometimes losing power or internet connection during an OTA can cause a miner's Docker to crash. This can typically be fixed with a reboot or a reset, followed by a fast sync if your gap is >400. Fast Sync is recommended if your gap is >400 and your miner has been fully synced before.

**What You Can Try:** 
1. First Try Reboot
2. Try Reset
3. Then Fastsync
4. Make Sure Your Miner is Connected to the Internet. What color is your miner's LED?

**What to provide customer support if unable to resolve:**
1. If Possible, Screenshots of Your Diagnoser.
2. Indicate Miner's LED Color
3. Open Port 22, if Unable to Access the Diagnoser
4. Provide Miner's IP Address
5. Confirm Port 22 is Open (Include a Screenshot of this Page)

**Troublesooting Guides:**
- https://bobcatminer.zendesk.com/hc/en-us/articles/4413666097051-Status-Down-4413666097051-Status-Down-
...
```


## Monitoring with Discord

Monitor your Bobcat remotely by sending events to a Discord channel. No need for VPN or SSH agent setup!

```console
$ bobcat --discord-webhook-url https://discord.com/api/webhooks/xxx autopilot
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
