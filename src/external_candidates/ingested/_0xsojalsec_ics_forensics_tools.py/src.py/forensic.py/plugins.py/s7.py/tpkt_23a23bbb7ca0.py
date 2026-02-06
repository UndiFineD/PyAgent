# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ics-forensics-tools\src\forensic\plugins\s7\tpkt.py
from forensic.common.stream.stream import (
    BinaryReader,
    BinaryWriter,
    DataStruct,
    dynamic,
    ubyte,
    uint16be,
)

SIZE_OF_HEADER = 4


class TPKTLayer(DataStruct):
    version = ubyte
    reserved = ubyte
    length = uint16be
    real_length = dynamic


class TPKT:
    def parse(self, br: BinaryReader) -> TPKTLayer:
        res = TPKTLayer(br)

        if res.length:
            res.real_length = res.length - SIZE_OF_HEADER

        return res

    def write(self, version: int, bw_cotp: BinaryWriter) -> BinaryWriter:
        bw = BinaryWriter()
        bw.write_struct(
            TPKTLayer,
            {
                "version": version,
                "reserved": 0,
                "length": len(bw_cotp) + SIZE_OF_HEADER,
            },
        )
        return bw + bw_cotp
