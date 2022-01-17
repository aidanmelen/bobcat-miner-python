[![PyPI](https://img.shields.io/pypi/v/bobcat_miner.svg)](https://pypi.org/project/bobcat-miner/)
[![Dockerhub](https://img.shields.io/docker/v/aidanmelen/bobcat?color=blue&label=docker%20build)](https://hub.docker.com/r/aidanmelen/bobcat)
[![Release](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/release.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/release.yaml)
[![Tests](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/tests.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/tests.yaml)
[![Lint](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/lint.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/lint.yaml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/release.yaml)


# bobcat miner python

A command line tool used to automate the Bobcat miner. This project also offers a robust python SDK's for interacting with the Bobcat miner.

## Install

```bash
# install command line tools
$ pipx install bobcat-miner

# install SDK
$ pip3 install bobcat-miner
```

Please see this [guide](https://packaging.python.org/en/latest/guides/installing-stand-alone-command-line-tools/) for more information about installing stand alone command line tools with [pipx](https://pypa.github.io/pipx/).

## Bobcat Autopilot Usage

The `bobcat autopilot` command will automatically diagnose and repair the Bobcat!

Follow these [instructions](https://bobcatminer.zendesk.com/hc/en-us/articles/4412905935131-How-to-Access-the-Diagnoser) to find you Bobcats's ip address.

![Bobcat Autopilot Term](https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/images/bobcat-autopilot-term.png)

The `bobcat` command line tool accepts both command line options and environment variables. Please see the `bobcat --help` for more information.

### Bobcat Dry Run

Diagnostics checks will run and all actions will be skipped during a Bobcat dry run.

```bash
$ bobcat -i 192.168.0.10 --dry-run autopilot
🚧 Bobcat Autopilot Dry Run Enabled. Actions such as reboot, reset, resync, and fastsync will be skipped. Wait times will only last 1 second.
🚀 The Bobcat Autopilot is starting
```

### Discord Monitoring

The `bobcat` command line tool supports sending logs to a Discord channel using a [webhook url](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).

```bash
$ export BOBCAT_IP_ADDRESS=192.168.0.10
$ export BOBCAT_DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx/xxx
$ bobcat autopilot
🚀 The Bobcat Autopilot is starting
```

and check Discord

![Bobcat Autopilot Discord](https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/images/bobcat-autopilot-discord.png)

### File Log

Send logs to a file with

```bash
$ bobcat --ip-address 192.168.0.10 --log-file bobcat-autopilot.log autopilot
🚀 The Bobcat Autopilot is starting
```

### Bobcat Docker Container

Run the `bobcat` command line tool as a docker container.

```bash
$ docker run --rm -it aidanmelen/bobcat -i 192.168.0.10 status
{
    "status": "Synced",
    "gap": "-2",
    "miner_height": "1185959",
    "blockchain_height": "1185957",
    "epoch": "31260"
}
```

## Bobcat Autopilot SDK Usage

```python
import bobcat_miner

bobcat = bobcat_miner.Bobcat("192.168.1.10")
autopilot = bobcat_miner.Autopilot(bobcat)

# Automatically diagnose and repair the Bobcat
autopilot.run()

# diagnostics
autopilot.is_relayed()
autopilot.is_temp_dangerous()
autopilot.is_network_speed_slow()
autopilot.is_syncing()
autopilot.has_errors()

# actions
autopilot.ping()        # Ping the Bobcat until it connects or attempts are maxed out
autopilot.reboot()      # Reboot the Bobcat and wait for connection
autopilot.reset()       # Reset the Bobcat and wait for connection or exceeds max attempts
autopilot.resync()      # Fastsync the Bobcat and wait for connection
autopilot.fastsync()    # Fastsync the Bobcat until the gap is less than 400 or exceeds max attempts
autopilot.is_syncing()  # Poll the Bobcat's gap to see if it is syncing over time
```

## Bobcat SDK Usage

```python
import bobcat_miner

bobcat = bobcat_miner.Bobcat("192.168.1.10")

# refresh
bobcat.refresh_status()
bobcat.refresh_miner()
bobcat.refresh_speed()
bobcat.refresh_temp()
bobcat.refresh_dig()
bobcat.refresh()

# properties
bobcat.status
bobcat.gap
bobcat.miner_height
bobcat.blockchain_height
bobcat.epoch
bobcat.tip
bobcat.ota_version
bobcat.region
bobcat.frequency_plan
bobcat.animal
bobcat.name
bobcat.pubkey
bobcat.state
bobcat.miner_status
bobcat.names
bobcat.image
bobcat.created
bobcat.p2p_status
bobcat.ports_desc
bobcat.ports
bobcat.private_ip
bobcat.public_ip
bobcat.peerbook
bobcat.peerbook_miner
bobcat.peerbook_listen_address
bobcat.peerbook_peers
bobcat.timestamp
bobcat.error
bobcat.temp0
bobcat.temp1
bobcat.temp0_c
bobcat.temp1_c
bobcat.temp0_f
bobcat.temp1_f
bobcat.download_speed
bobcat.upload_speed
bobcat.latency
bobcat.dig_name
bobcat.dig_message
bobcat.dig_dns
bobcat.dig_records

# actions
bobcat.ping()
bobcat.reboot()
bobcat.reset()
bobcat.resync()
bobcat.fastsync()

# diagnostics
bobcat.is_bobcat()
```

## Troubleshooting

Please see [No Witness's Troubleshooting Guide](https://www.nowitness.org/troubleshooting/) for more information.

## Donations

Donations are welcome and appreciated! :gift:

[![HNT: 14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/images/wallet.jpg)](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)

HNT: [14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)
