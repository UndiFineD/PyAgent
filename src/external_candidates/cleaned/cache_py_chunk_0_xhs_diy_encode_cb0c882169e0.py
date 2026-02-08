# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\cache.py\work.py\copilot_tmp.py\chunk_0_xhs_diy_encode_cb0c882169e0.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\cache\work\copilot_tmp\chunk_0_xhs_diy_encode.py

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\chocomintx\xiaohongshutools\scripts\request\web\encrypt\xhs_diy_encode.py

# NOTE: extracted with static-only rules; review before use


def triplet_to_base64(a, c):
    return c[(a >> 18) & 63] + c[(a >> 12) & 63] + c[(a >> 6) & 63] + c[a & 63]


def encode_chunk(a, e, r, c):
    d = []

    for f in range(e, r, 3):
        c_val = ((a[f] << 16) & 0xFF0000) + ((a[f + 1] << 8) & 0xFF00) + (a[f + 2] & 0xFF)

        d.append(triplet_to_base64(c_val, c))

    return "".join(d)


def b64_encode(a, CUSTOM_BASE64_ALPHABET):
    c = CUSTOM_BASE64_ALPHABET

    r = len(a)

    d = r % 3

    f = []

    s = 16383

    u = 0

    l = r - d

    while u < l:
        end = min(u + s, l)

        f.append(encode_chunk(a, u, end, c))

        u += s

    if d == 1:
        e = a[r - 1]

        f.append(c[e >> 2] + c[(e << 4) & 63] + "==")

    elif d == 2:
        e = (a[r - 2] << 8) + a[r - 1]

        f.append(c[e >> 10] + c[(e >> 4) & 63] + c[(e << 2) & 63] + "=")

    return "".join(f)


def encode_utf8(a):
    # 首先进行URL编码

    url_encoded = a

    result = []

    i = 0

    while i < len(url_encoded):
        c = url_encoded[i]

        if c == "%":
            # 处理%编码的字符

            hex_str = url_encoded[i + 1 : i + 3]

            char_code = int(hex_str, 16)

            result.append(char_code)

            i += 3

        else:
            # 处理普通ASCII字符

            result.append(ord(c))

            i += 1

    return result
