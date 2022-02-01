# Internet Outage

## Action

Unplug the ethernet.

## Result

### Python

<details>
  <summary>Click to expand!</summary>

```python
import backoff
import json
import requests
import time

@backoff.on_exception(
    backoff.expo,
    (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
    max_time=300,
)
def get(url):
    return requests.get(url)

def poll():
    while True:
        print("Polling status.json")
        print(json.dumps(get("http://x.x.x.x/status.json").json(), indent=4))
        time.sleep(5)
        
        print("Polling miner.json")
        print(json.dumps(get("http://x.x.x.x/miner.json").json(), indent=4))
        time.sleep(5)

poll()
```

</details><p></p>

### State Changes