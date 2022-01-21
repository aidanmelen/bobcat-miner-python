from bobcat_api import BobcatAPI


class Bobcat(BobcatAPI):
    pass


if __name__ == "__main__":
    b = Bobcat(log_level="DEBUG")

    b.validate_ip_address("192.168.0.1")
    b.validate_ip_address("x.x.x.x")

    b.connect("192.168.0.1", port=80)
    b.connect("192.168.0.1")  # 44154

    b.validate_bobcat("192.168.0.8")
    b.validate_bobcat("192.168.0.1")

    b.discover_bobcat_ip_address()

    print(b.get("http://192.168.0.1").ok)
    print(b.get("http://192.168.0.8").ok)
    print(b.get("http://192.168.0.8/status.json").json())
