"""Fake bobcat server."""

from flask import Flask
from flask_basicauth import BasicAuth
from flask import jsonify

import subprocess
import os

import data

app = Flask(__name__)

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["BASIC_AUTH_USERNAME"] = "bobcat"
app.config["BASIC_AUTH_PASSWORD"] = "miner"

basic_auth = BasicAuth(app)


def __set_bobcat_status(status="Synced"):
    if os.path.exists("state.txt"):
        with open("state.txt", "w+") as f:
            return f.write(status)
    else:
        with open("state.txt", "w+") as f:
            return f.write(status)


def __get_bobcat_status():
    if not os.path.exists("state.txt"):
        __set_bobcat_status()
    
    with open("state.txt") as f:
        return f.read()


@app.route("/")
def dashboard():
    return data.dashboard[__get_bobcat_status()]


@app.route("/status.json")
def status():
    
    return jsonify(data.status[__get_bobcat_status()])


@app.route("/miner.json")
def miner():
    return jsonify(data.miner[__get_bobcat_status()])


@app.route("/speed.json")
def speed():
    return jsonify(data.speed)


@app.route("/temp.json")
def temp():
    return jsonify(data.temp)


@app.route("/dig.json")
def dig():
    return jsonify(data.dig)


@app.route("/admin/reboot", methods=["POST"])
@basic_auth.required
def reboot():
    subprocess.run(["/bin/bash", "/app/reboot.sh"])
    return "Rebooting hotspot"


@app.route("/admin/reset", methods=["POST"])
@basic_auth.required
def reset():
    __set_bobcat_status(status="Syncing")
    subprocess.run(["/bin/bash", "/app/reset.sh"])
    return "1: Your miner is going to rest<br>3: Housekeeper was sent home<br>3: Docker is going to be stopped<br>4: Boom! Old blockchain data gone<br>5: Boom! miner gone<br>6: Housekeeper is back, but everything is gone<br>7: Rebuilding everything<br>8: Cleaning up<br>Bam! Miner successfully restarted, but it may take 30 minutes to load files from internet. Please be patient. 2022-01-20 17:39:06 +0000 UTC<br>"


@app.route("/admin/resync", methods=["POST"])
@basic_auth.required
def resync():
    __set_bobcat_status(status="Syncing")
    subprocess.run(["/bin/bash", "/app/resync.sh"])
    return "1: Your miner is going to rest<br>2: Docker is going to be stopped<br>3: Boom! Old blockchain data gone<br>4: Bam! Rebuilding miner data<br>Miner successfully restarted, but it may take 30 minutes to load files from internet, please be patient. 2022-01-20 18:12:28 +0000 UTC<br>"


@app.route("/admin/fastsync", methods=["POST"])
@basic_auth.required
def fastsync():
    __set_bobcat_status(status="Synced")
    subprocess.run(["/bin/bash", "/app/fastsync.sh"])
    return "Syncing your miner, please leave your power on."


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"message": "Internal Server Error"})


@app.route("/set/down", methods=["POST"])
def set_down():
    global bobcat_status
    __set_bobcat_status(status="Down")
    return "Set Status: Down\n"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(debug=False, host="0.0.0.0", port=port)
