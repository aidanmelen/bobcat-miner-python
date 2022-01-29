
# Raspberry Pi Deployment

Deploy the Bobcat Autopilot to a Raspberry Pi for unattended automation and monitoring!

## Assumptions

- Operating System: Raspbian GNU/Linux 11 (bullseye).
- The Raspberry PI is on the same network as the Bobcat.
- You want to remotely monitor the Bobcat Autopilot with Discord.

## Setup

Install the bobcat command line tool with Pipx.

```bash
# install pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# install the bobcat cli with pipx
python3 -m pipx install bobcat-miner

# create a new folder for bobcat autopilot log files
sudo mkdir /var/log/bobcat
sudo chown pi:adm /var/log/bobcat
sudo chmod 0777 /var/log/bobcat

# create a new folder for the bobcat autopilot lock file
sudo mkdir /etc/bobcat
sudo chown pi:adm /etc/bobcat
sudo chmod 0777 /etc/bobcat
```

<!-- docker run --rm -it \
-v /etc/bobcat:/etc/bobcat \
-v /var/log/bobcat:/var/log/bobcat \
--env-file /home/pi/.bobcat-profile \
aidanmelen/bobcat autopilot -->


Then create a file called `/home/pi/.bobcat-profile` with the following environment variables.

```bash
export BOBCAT_HOSTNAME=192.168.0.10
export BOBCAT_ANIMAL='Fancy Awesome Bobcat'
export BOBCAT_DRY_RUN=TRUE
export BOBCAT_LOCK_FILE=/etc/bobcat/autopilot.lock
export BOBCAT_LOG_FILE=/var/log/bobcat/autopilot.log
export BOBCAT_DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx
export BOBCAT_LOG_LEVEL_CONSOLE=DEBUG
export BOBCAT_LOG_LEVEL_FILE=INFO
export BOBCAT_LOG_LEVEL_DISCORD=WARNING
```

Please run `bobcat --help` for more information about the environment variables.

Finally schedule Bobcat Autopilot with Cron

```bash
# write out current crontab to a file
crontab -l > mycron 2>/dev/null

# append the bobcat autopilot command to the crontab
echo "0 * * * * . /home/pi/.bobcat-profile; /home/pi/.local/bin/bobcat autopilot &> /dev/null" >> mycron

# install new cron file
crontab mycron

# clean up
rm mycron
```

Now the Bobcat Autopilot will run on the first minute of every hour and will send logs events to Discord for remote monitoring. ✨ 🍰 ✨