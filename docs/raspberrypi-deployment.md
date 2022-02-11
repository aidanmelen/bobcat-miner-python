
# Raspberry Pi Deployment

Deploy the Bobcat Autopilot to a Raspberry Pi for unattended automation and monitoring!

## Assumptions

- Operating System: Raspbian GNU/Linux 11 (bullseye).
- The Raspberry PI is on the same network as the Bobcat.
- You want to run `bobcat autopilot` as a Docker container.
- You want to schedule `bobcat autopilot` to run 4 times a day.
- You want remotely monitor the Bobcat Autopilot with Discord.

## Setup

Install the Docker Community Edition.

```bash
sudo apt install -y docker-ce
```

Pull and tag the `bobcat` image

```
sudo docker pull aidanmelen/bobcat
```

Create a file called `/home/pi/bobcat.env` with your configuration information. For Example:

```bash
BOBCAT_HOSTNAME=192.168.0.10
BOBCAT_ANIMAL='Fancy Awesome Bobcat'
BOBCAT_LOCK_FILE=/etc/bobcat/autopilot.lock
BOBCAT_LOG_STATE=/etc/bobcat/autopilot.json
BOBCAT_LOG_FILE=/var/log/bobcat/autopilot.log
BOBCAT_DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx
BOBCAT_LOG_LEVEL_FILE=DEBUG
BOBCAT_LOG_LEVEL_CONSOLE=DEBUG
BOBCAT_LOG_LEVEL_DISCORD=WARNING
BOBCAT_TRACE=TRUE
```

ℹ️ Run `sudo docker run aidanmelen/bobcat --help` for more information about the environment variables.

Next we will verify the configuration file with a dry run

```bash
$ sudo docker run \
-v /etc/bobcat:/etc/bobcat \
-v /var/log/bobcat:/var/log/bobcat \
--env-file /home/pi/bobcat.env \
--env BOBCAT_DRY_RUN=TRUE \
aidanmelen/bobcat autopilot
```

Finally schedule Bobcat Autopilot with Cron

```bash
# write out current crontab to a file
crontab -l > mycron 2>/dev/null

# append the bobcat autopilot command to the crontab
# AKA 4 times a day: at minute 0 past hour 0, 6, 12, and 18.
echo "0 0,6,12,18 * * * sudo docker run \
-v /etc/bobcat:/etc/bobcat \
-v /var/log/bobcat:/var/log/bobcat \
--env-file /home/pi/bobcat.env \
aidanmelen/bobcat autopilot &> /dev/null" >> mycron

# install new cron file
crontab mycron

# clean up
rm mycron
```

Now the Bobcat Autopilot will run 4 times a day and will send logs events to Discord for remote monitoring ✨ 🍰 ✨
