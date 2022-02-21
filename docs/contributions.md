# Contributions

## Development

### Setup

The containerized development environment can be spun up with `docker compose`.

```bash
docker compose up --detach
[+] Running 3/3
 ⠿ Network bobcat-miner-python_default  Created
 ⠿ Container bobcat-miner-python-dev    Started
 ⠿ Container fancy-awesome-bobcat       Started 
```

### Usage

Get a shell in the `bobcat-miner-python-dev` container.

```
docker-compose exec bobcat-miner-python-dev poetry run /bin/bash
root@bobcat-miner-python-dev:/app# bobcat --help
Usage: bobcat [OPTIONS] COMMAND [ARGS]...

  Bobcat miner command line tools.

...
```

This dev container is networked with a fake bobcat service called `fancy-awesome-bobcat`.

```
root@bobcat-miner-python-dev:/app# bobcat autopilot
🐛 Connected to Bobcat: fancy-awesome-bobcat
🐛 Refresh: Miner Data
🐛 Verified Bobcat Animal: fancy-awesome-bobcat
🐛 The Bobcat Autopilot is starting 🚀 🚀 🚀
🐛 Lock Acquired: /etc/bobcat/autopilot.lock
🐛 Refresh: Status Data
⚠️ Online Status: Bobcat is healthy. Helium API needs time to update.
🐛 Checking: Down or Error Status
🐛 Checking: Height API Error Status
🐛 Checking: Unknown Error Status
🐛 Checking: Sync Status
✅ Sync Status: Synced (gap:0) 💫
🐛 Checking: Relay Status
✅ Relay Status: Not Relayed ✨
🐛 Checking: Network Status
🐛 Refresh: Network Speed Data
✅ Network Status: Good 📶
🐛 Checking: Temperature Status
🐛 Refresh: Temperature Data
✅ Temperature Status: Good (38°C) ☀️
🐛 Checking: OTA Version Change
🐛 Lock Released: /etc/bobcat/autopilot.lock
🐛 The Bobcat Autopilot is finished ✨ 🍰 ✨
```

`fancy-awesome-bobcat` has a special test endpoint for simulating a `Down` state

```bash
root@bobcat-miner-python-dev:/app# curl -X post fancy-awesome-bobcat/set/down
Set Status: Down
```

The bobcat is now in a `Down` state

```bash
root@bobcat-miner-python-dev:/app# bobcat -C INFO status
{'blockchain_height': '1234527', 'epoch': 'Error:', 'gap': '-', 'miner_height': 'command', 'status': 'Down'}
```

Now we can simulate a `bobcat autopilot` repair run

```
root@bobcat-miner-python-dev:/app# bobcat -C INFO autopilot
❌ Online Status: Offline
❌ Bobcat Status: Down
⚠️ Rebooting Bobcat
⚠️ The Bobcat (fancy-awesome-bobcat) is unreachable
⚠️ The Bobcat (fancy-awesome-bobcat) is unreachable
⚠️ The Bobcat (fancy-awesome-bobcat) is unreachable
⚠️ The Bobcat (fancy-awesome-bobcat) is unreachable
⚠️ The Bobcat (fancy-awesome-bobcat) is unreachable
✅ Reconnected to the Bobcat (fancy-awesome-bobcat)
⚠️ Resetting Bobcat
⚠️ The Bobcat (fancy-awesome-bobcat) is unreachable
⚠️ The Bobcat (fancy-awesome-bobcat) is unreachable
⚠️ The Bobcat (fancy-awesome-bobcat) is unreachable
⚠️ The Bobcat (fancy-awesome-bobcat) is unreachable
⚠️ The Bobcat (fancy-awesome-bobcat) is unreachable
✅ Reconnected to the Bobcat (fancy-awesome-bobcat)
⚠️ Fastsyncing Bobcat
✅ Reconnected to the Bobcat (fancy-awesome-bobcat)
✅ Repair Status: Complete
✅ Relay Status: Not Relayed ✨
✅ Network Status: Good 📶
✅ Temperature Status: Good (38°C) ☀️
```

### Teardown

```
Run the following to tear down the development environment

```bash
docker compose down
[+] Running 3/2
 ⠿ Container bobcat-miner-python-dev
 ⠿ Container fancy-awesome-bobcat
 ⠿ Network bobcat-miner-python_default  Removed 
```

Please see the [docker-compose.yml](https://github.com/aidanmelen/bobcat-miner-python/blob/main/docker-compose.yml) for more information.

## Test

Run unittests

```bash
docker build . -t bobcat-miner-python-test --target test
docker run --rm -it -v $(pwd):/app bobcat-miner-python-test
```

and run the linter

```bash
docker run --rm --volume $(pwd):/src --workdir /src pyfound/black:latest_release black --line-length 100 .
```

## Release

Read the version from `poetry`, tag, and push.

```bash
# ensure we are tagging the main branch
git checkout main
git pull

# tag with version from the pyproject.toml and push to remote
git tag $(poetry version -s)
git push --tags
```

This will trigger the [Release Github Action](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/release.yaml).