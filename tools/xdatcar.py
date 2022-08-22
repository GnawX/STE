from ase import io
from ase.io.vasp import write_vasp_xdatcar

nimages = 13
a = []
for i in range(1,nimages+1):
    st = str(i)
    a.append(io.read('POSCAR'+st))

write_vasp_xdatcar('XDATCAR',a)
