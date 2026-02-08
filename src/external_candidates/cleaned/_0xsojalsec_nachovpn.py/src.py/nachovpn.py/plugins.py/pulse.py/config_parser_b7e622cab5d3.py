# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-NachoVPN\src\nachovpn\plugins\pulse\config_parser.py
#!/usr/bin/env python3
import sys

ENC_AES_128_CBC = 2
ENC_AES_256_CBC = 5

HMAC_MD5 = 1
HMAC_SHA1 = 2
HMAC_SHA256 = 3

# Example packet:
#
# 00000000  00 00 0a 4c 00 00 00 01 00 00 01 60 00 00 01 fb   |...L.......`....|
# 00000010  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   |................|
# 00000020  2e 20 f0 00 00 00 00 00 00 00 01 50 2e 00 00 0d   |. .........P....|
# 00000030  03 00 00 00 40 25 00 01 01 2c 00 00 0d 03 00 00   |....@%...,......|
# 00000040  00 40 26 00 01 01 2e 00 00 18 00 00 00 01 07 00   |.@&.............|
# 00000050  00 10 00 00 ff ff 00 00 00 00 ff ff ff ff 00 00   |................|
# 00000060  00 00 01 02 03 00 00 00 40 00 00 01 00 40 01 00   |........@....@..|
# 00000070  01 00 40 1f 00 01 00 40 20 00 01 00 40 21 00 01   |..@....@ ...@!..|
# 00000080  00 40 05 00 04 00 00 05 78 00 03 00 04 01 01 01   |.@......x.......|
# 00000090  01 40 06 00 0d 6e 61 63 68 6f 76 70 6e 2e 6c 6f   |.@...nachovpn.lo|
# 000000a0  6c 00 40 07 00 04 00 00 00 01 00 04 00 04 01 01   |l.@.............|
# 000000b0  01 01 40 19 00 01 01 40 1a 00 01 00 40 24 00 01   |..@....@....@$..|
# 000000c0  01 40 0f 00 02 00 00 40 10 00 02 00 05 40 11 00   |.@.....@.....@..|
# 000000d0  02 00 03 40 12 00 04 00 00 04 b0 40 13 00 04 00   |...@.......@....|
# 000000e0  00 00 00 40 14 00 04 00 00 00 01 40 15 00 04 00   |...@.......@....|
# 000000f0  00 00 00 40 16 00 02 11 94 40 17 00 04 00 00 00   |...@.....@......|
# 00000100  0f 40 18 00 04 00 00 00 3c 00 01 00 04 0a 0a 01   |.@......<.......|
# 00000110  01 00 02 00 04 ff ff ff ff 40 0b 00 04 0a c8 c8   |.........@......|
# 00000120  c8 40 0c 00 1d 43 3a 5c 57 69 6e 64 6f 77 73 5c   |.@...C:\Windows\|
# 00000130  53 79 73 74 65 6d 33 32 5c 63 61 6c 63 2e 65 78   |System32\calc.ex|
# 00000140  65 00 40 0d 00 01 00 40 0e 00 01 00 40 1b 00 01   |e.@....@....@...|
# 00000150  00 40 1c 00 01 00 00 13 00 01 00 00 14 00 01 00   |.@..............|


def load_be32(data):
    return int.from_bytes(data[0:4], "big")


def load_be16(data):
    return int.from_bytes(data[0:2], "big")


def load_le32(data):
    return int.from_bytes(data[0:4], "little")


def load_le16(data):
    return int.from_bytes(data[0:2], "little")


class Attribute:
    def __init__(self, attr_type, attr_len, data):
        self.attr_type = attr_type
        self.attr_len = attr_len
        self.data = data

    def to_dict(self):
        return {"type": self.attr_type, "len": self.attr_len, "data": self.data}


class PulseConfig:
    def __init__(self, data):
        self.data = data
        self.pre_attributes = []
        self.routes = []
        self.post_attributes = []

    def process_attr(self, attr_type, data, attr_len):
        if attr_type == 0x0001:
            ip_address = "%d.%d.%d.%d" % (data[0], data[1], data[2], data[3])
            print("Internal Legacy IP address: %s" % ip_address)
        elif attr_type == 0x0002:
            net_mask = "%d.%d.%d.%d" % (data[0], data[1], data[2], data[3])
            print("Netmask: %s" % net_mask)
        elif attr_type == 0x0003:
            dns_server = "%d.%d.%d.%d" % (data[0], data[1], data[2], data[3])
            print("DNS server: %s" % dns_server)
        elif attr_type == 0x0004:
            wins_server = "%d.%d.%d.%d" % (data[0], data[1], data[2], data[3])
            print("WINS server: %s" % wins_server)
        elif attr_type == 0x0008:
            print("Internal IPv6 address")
        elif attr_type == 0x000A:
            print("DNS server (IPv6)")
        elif attr_type == 0x000F:
            print("IPv6 split include")
        elif attr_type == 0x0010:
            print("IPv6 split exclude")
        elif attr_type == 0x4005:
            mtu = load_be32(data)
            print("MTU %d from server" % mtu)
        elif attr_type == 0x4006:
            print("DNS search domain: %s" % data[0:attr_len].split(b"\x00")[0].decode())
        elif attr_type == 0x401A:
            print("ESP only: %d" % data[0])
        elif attr_type == 0x400B:
            gateway = "%d.%d.%d.%d" % (data[0], data[1], data[2], data[3])
            print("Internal gateway address: %s" % gateway)
        elif attr_type == 0x4017:
            fallback_secs = load_be32(data)
            print("ESP to SSL fallback: %u seconds" % fallback_secs)
        elif attr_type == 0x4010:
            val = load_be16(data)
            if val == ENC_AES_128_CBC:
                enc_type = "AES-128"
            elif val == ENC_AES_256_CBC:
                enc_type = "AES-256"
            print("ESP encryption: 0x%04x (%s)" % (val, enc_type))
        elif attr_type == 0x4000:
            print("Disconnect when routes changed: %d" % data[0])
        elif attr_type == 0x4011:
            val = load_be16(data)
            if val == HMAC_MD5:
                mactype = "MD5"
            elif val == HMAC_SHA1:
                mactype = "SHA1"
            elif val == HMAC_SHA256:
                mactype = "SHA256"
            else:
                mactype = "unknown"
            print("ESP HMAC: 0x%04x (%s)" % (val, mactype))
        elif attr_type == 0x4001:
            print("Tunnel routes take precedence: %d" % data[0])
        elif attr_type == 0x401F:
            print("Tunnel routes with subnet access (also 4001 set): %d" % data[0])
        elif attr_type == 0x4020:
            print("Enforce IPv4: %d" % data[0])
        elif attr_type == 0x4021:
            print("Enforce IPv6: %d" % data[0])
        elif attr_type == 0x4012:
            lifetime_secs = load_be32(data)
            print("ESP key lifetime: %u seconds" % lifetime_secs)
        elif attr_type == 0x4013:
            lifetime_bytes = load_be32(data)
            print("ESP key lifetime: %u bytes" % lifetime_bytes)
        elif attr_type == 0x4014:
            esp_replay_protect = load_be32(data)
            print("ESP replay protection: %d" % esp_replay_protect)
        elif attr_type == 0x4015:
            tos_copy = load_be32(data)
            print("TOS copy: %d" % tos_copy)
        elif attr_type == 0x4016:
            i = load_be16(data)
            print("ESP port: %d" % i)
        elif attr_type == 0x400C:
            logon_script = data[0:attr_len].split(b"\x00")[0].decode()
            print("Logon script: %s" % logon_script)
        elif attr_type == 0x4024:
            print("Pulse ESP tunnel allowed to carry 6in4 or 4in6 traffic: %d" % data[0])
        else:
            print("Unknown attr 0x%x len %d: %s" % (attr_type, attr_len, data[0:attr_len].hex()))

    def handle_attr_elements(self, data, attr_len, attrs):
        l = attr_len
        p = data
        if l < 8 or load_be32(p[4:]) != 0x03000000:
            print("Bad attribute header")
            return 1

        p = p[8:]
        l -= 8

        while l > 4:
            attr_type = load_be16(p)
            attr_len = load_be16(p[2:])

            if attr_len + 4 > l:
                print("Bad attribute length")
                return 1

            p = p[4:]
            l -= 4

            # append to list as a dict so we can reconstruct later
            attrs.append(Attribute(attr_type, attr_len, p[:attr_len]).to_dict())

            # process attribute
            self.process_attr(attr_type, p, attr_len)

            p = p[attr_len:]
            l -= attr_len

        return 0

    def parse(self):
        if len(self.data) < 0x31:
            raise ValueError("Config data too short")

        offset = 0x2C

        config_type = load_be32(self.data[0x20:])
        print(f"Config type: {config_type:08x}")

        if config_type == 0x2E20F000:
            if len(data) < offset + 4:
                raise ValueError("Config data too short (2)")

            attr_flag = 0
            while attr_flag != 0x2C00:
                attr_flag = load_be16(self.data[offset:])
                attr_len = load_be16(self.data[offset + 2 :])

                if attr_flag == 0x2C00:
                    print("attr_flag 0x2c00: known for Pulse version >= 9.1R14")
                elif attr_flag == 0x2E00:
                    print("attr_flag 0x2e00: known for Pulse version >= 9.1R16")
                else:
                    print("unknown Pulse version")

                if len(self.data) < offset + attr_len or self.handle_attr_elements(
                    self.data[offset:], attr_len, self.pre_attributes
                ):
                    raise ValueError("Bad config")

                offset += attr_len

        elif config_type == 0x2C20F000:
            print("Processing Pulse main config data for server version < 9.1R14")
        else:
            raise ValueError("Unrecognised data type")

        assert offset == 0x46
        routes_len = load_be16(self.data[offset + 2 :])

        # parse routing info
        p = self.data[offset + 8 :]
        routes_len -= 8

        while routes_len:
            route_type = load_be32(p)
            ffff = load_be32(p[4:])

            if ffff != 0xFFFF:
                raise ValueError("Bad config: ffff != 0xffff")

            route = "%d.%d.%d.%d/%d.%d.%d.%d" % (
                p[8],
                p[9],
                p[10],
                p[11],
                255 ^ (p[8] ^ p[12]),
                255 ^ (p[9] ^ p[13]),
                255 ^ (p[10] ^ p[14]),
                255 ^ (p[11] ^ p[15]),
            )

            if route_type == 0x07000010:
                print("Received split include route %s" % route)
            elif route_type == 0xF1000010:
                print("Received split exclude route: %s" % route)
            else:
                print("Receive route of unknown type %s" % hex(route_type))

            p = p[0x10:]
            routes_len -= 0x10

        l = load_be16(p[4:])
        p = p[2:]  # fix alignment
        self.handle_attr_elements(p, l, self.post_attributes)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s <config_file>" % sys.argv[0])
        sys.exit(1)

    with open(sys.argv[1], "rb") as f:
        data = f.read()

    config = PulseConfig(data)
    config.parse()
