
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

Then schedule Bobcat Autopilot with Cron

```bash
# write out current crontab
crontab -l > mycron 2>/dev/null

# echo new cron into cron file
BOBCAT_HOSTNAME=192.168.0.10
BOBCAT_DRY_RUN=TRUE
BOBCAT_LOG_LEVEL=TRACE
BOBCAT_LOG_FILE=/var/log/bobcat/autopilot.log
BOBCAT_LOCK_FILE=/etc/bobcat/autopilot.lock
BOBCAT_DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx/xxx
BOBCAT_CMD=$(which bobcat)
BOBCAT_OPTIONS="-i $BOBCAT_HOSTNAME \
--log-level $BOBCAT_LOG_LEVEL \
--log-file $BOBCAT_LOG_FILE \
--lock-file $BOBCAT_LOCK_FILE \
--discord-webhook-url $BOBCAT_DISCORD_WEBHOOK_URL"
BOBCAT_AUTOPILOT="$BOBCAT_CMD $BOBCAT_OPTIONS autopilot"
CRON_SCHEDULE="0 * * * *" # once every hour

echo "$CRON_SCHEDULE $BOBCAT_AUTOPILOT &> /dev/null" >> mycron

# install new cron file
crontab mycron

# clean up
rm mycron
```

Now the Bobcat Autopilot will run on the first minute of every hour and will send logs events to Discord for remote monitoring. ✨ 🌟 ✨