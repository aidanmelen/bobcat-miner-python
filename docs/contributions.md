# Contributions

## Development

The containerized development environment can be spun up with `docker compose`.

```bash
$ docker compose up --detach
[+] Running 3/3
 ⠿ Network bobcat-miner-python_default  Created
 ⠿ Container bobcat-miner-python-dev    Started
 ⠿ Container fancy-awesome-bobcat       Started 
```

Then get a shell in the `bobcat-miner-python-dev` container.

```
$ docker-compose exec bobcat-miner-python-dev poetry run /bin/bash
root@bobcat-miner-python-dev:/app# bobcat --help
Usage: bobcat [OPTIONS] COMMAND [ARGS]...

  Bobcat miner command line tools.

...
```

This dev container is networked with a fake bobcat service with the hostname: `fancy-awesome-bobcat`.

**Note:** The default environment variable configuration is set in the docker-compose.yml file and can be overridden with command line option.

```
$ docker-compose exec bobcat-miner-python-dev poetry run bobcat autopilot
🐛 Connected to Bobcat: fancy-awesome-bobcat
🐛 Refresh: Miner Data
🐛 Verified Bobcat Animal: fancy-awesome-bobcat
🐛 The Bobcat Autopilot is starting 🚀 🚀 🚀
🐛 Lock Acquired: /etc/bobcat/autopilot.lock
🐛 Checking: Relay Status
✅ Relay Status: Not Relayed ✨
🐛 Checking: Sync Status
🐛 Refresh: Status Data
✅ Sync Status: Synced (gap:0) ✨
🐛 Checking: Network Status
🐛 Refresh: Network Speed Data
✅ Network Status: Good 📶
🐛 Checking: Temperature Status
🐛 Refresh: Temperature Data
✅ Temperature Status: Good (38°C) ☀️
🐛 Checking: OTA Version Change
🐛 Checking: Down or Error Status
🐛 Checking: Height API Error Status
🐛 Lock Released: /etc/bobcat/autopilot.lock
🐛 The Bobcat Autopilot is finished ✨ 🍰 ✨
```

and bring the development environment down.

```bash
docker compose down
[+] Running 3/2
 ⠿ Container bobcat-miner-python-dev
 ⠿ Container fancy-awesome-bobcat
 ⠿ Network bobcat-miner-python_default  Removed 
```

Please see the [docker-compose.yml](https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/docker-compose.yml) for more information.

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
$ git checkout main
$ git pull

$ git tag $(poetry version -s)
$ git push --tags
```

This will trigger the [Release Github Action](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/release.yaml).