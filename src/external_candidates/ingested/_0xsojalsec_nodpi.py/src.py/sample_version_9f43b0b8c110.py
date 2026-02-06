# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-NoDPI\src\sample_version.py
import asyncio
import logging
import random

BLOCKED = [
    line.rstrip().encode() for line in open("blacklist.txt", "r", encoding="utf-8")
]
TASKS = []


async def main(host, port):

    server = await asyncio.start_server(new_conn, host, port)
    await server.serve_forever()


async def pipe(reader, writer):

    while not reader.at_eof() and not writer.is_closing():
        try:
            writer.write(await reader.read(1500))
            await writer.drain()
        except Exception as e:
            logging.error(e)
            break

    writer.close()


async def new_conn(local_reader, local_writer):

    http_data = await local_reader.read(1500)

    if not http_data:
        local_writer.close()

        return

    try:
        type, target = http_data.split(b"\r\n")[0].split(b" ")[0:2]
        host, port = target.split(b":")
    except Exception as e:
        logging.error(e)
        local_writer.close()
        return

    if type != b"CONNECT":
        local_writer.close()
        return

    local_writer.write(b"HTTP/1.1 200 OK\n\n")
    await local_writer.drain()

    try:
        remote_reader, remote_writer = await asyncio.open_connection(host, port)
    except Exception as e:
        logging.error(e)
        local_writer.close()
        return

    if port == b"443":
        await fragment_data(local_reader, remote_writer)

    TASKS.append(asyncio.create_task(pipe(local_reader, remote_writer)))
    TASKS.append(asyncio.create_task(pipe(remote_reader, local_writer)))


async def fragment_data(local_reader, remote_writer):

    try:
        head = await local_reader.read(5)
        data = await local_reader.read(2048)
    except Exception as e:
        logging.error(e)
        local_reader.close()
        return

    parts = []

    if all(data.find(site) == -1 for site in BLOCKED):
        remote_writer.write(head + data)
        await remote_writer.drain()
        return

    host_end_index = data.find(b"\x00")
    if host_end_index != -1:
        parts.append(
            bytes.fromhex("160304")
            + int(host_end_index + 1).to_bytes(2, byteorder="big")
            + data[: host_end_index + 1]
        )
        data = data[host_end_index + 1 :]

    while data:
        part_len = random.randint(1, len(data))
        parts.append(
            bytes.fromhex("160304")
            + int(part_len).to_bytes(2, byteorder="big")
            + data[0:part_len]
        )
        data = data[part_len:]

    remote_writer.write(b"".join(parts))
    await remote_writer.drain()


print("Наслаждайтесь просмотром! Прокси запущен на 127.0.0.1:8881")
asyncio.run(main(host="127.0.0.1", port=8881))
