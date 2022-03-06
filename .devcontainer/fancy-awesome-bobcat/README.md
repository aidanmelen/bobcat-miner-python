# fake-bobcat-miner

A fake Bobcat miner server.

# Endpoints

## GET

- `http://localhost:5000/status.json`
- `http://localhost:5000/miner.json`
- `http://localhost:5000/speed.json`
- `http://localhost:5000/temp.json`
- `http://localhost:5000/dig.json`

## POST

- `http://localhost:5000/admin/reboot`
- `http://localhost:5000/admin/reset`
- `http://localhost:5000/admin/resync`
- `http://localhost:5000/admin/fastsync`


# Example

```bash
# build
$ docker build . -t fake-bobcat-miner

# run
$ docker run --rm -d -p 80:80 fake-bobcat-miner

# interact
$ curl http://localhost/status.json
{"status": "Synced", "gap": "0", "miner_height": "1148539", "blockchain_height": "1148539", "epoch": "30157"}

$ curl -X POST -H "Authorization: Basic Ym9iY2F0Om1pbmVy" http://localhost/admin/reboot
Rebooting hotspot
```