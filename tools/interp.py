#linear interpolation of the coordinates between GS (POSCAR_I) and STE(POSCAR_F)

from ase import atoms
from ase import io

nimgs = 7

initial = io.read('POSCAR_I')

final = io.read('POSCAR_F')

images = [initial]

images += [initial.copy() for i in range(nimgs-2)]

images += [final]

images += [final.copy() for i in range(nimgs-1)]

pos0 = initial.get_positions()

pos1 = final.get_positions()

dist = (pos1 - pos0)/(nimgs - 1)

for i in range(nimgs*2-1):

    images[i].set_positions(pos0 + i*dist)

    fil = 'POSCAR'+ str(i+1)

    io.write(fil, images[i])
