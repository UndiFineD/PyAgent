# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-NotelyVoice\lib\src\main\jni\ggml\src\ggml-opencl\kernels\embed_kernel.py
#

import logging
import sys

logger = logging.getLogger("opencl-embed-kernel")


def main():
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) != 3:
        logger.info("Usage: python embed_kernel.py <input_file> <output_file>")
        sys.exit(1)

    ifile = open(sys.argv[1], "r")
    ofile = open(sys.argv[2], "w")

    for i in ifile:
        ofile.write('R"({})"\n'.format(i))

    ifile.close()
    ofile.close()


if __name__ == "__main__":
    main()
