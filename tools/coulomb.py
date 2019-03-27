import numpy as np                                                                                                          
from ase.io import read                                                                                                     
from ase.io.cube import read_cube_data                                                                                      
from timeit import default_timer as timer                                                                                   

start = timer()

homo = read_cube_data('homo.cube')[0]
lumo = read_cube_data('lumo.cube')[0]

epsilon = 3.28

with open('homo.cube','r') as f:
     f.readline()               
     f.readline()               
     f.readline()               
     line1 = f.readline().split()
     line2 = f.readline().split()
     line3 = f.readline().split()

n1,n2,n3 = int(line1[0]),int(line2[0]),int(line3[0])
n = n1*n2*n3                                        
x1,y1,z1 = [float(s) for s in line1[1:]]            
x2,y2,z2 = [float(s) for s in line2[1:]]            
x3,y3,z3 = [float(s) for s in line3[1:]]            
vec = np.array([[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]])  
dx = x1+x2+x3
dy = y1+y2+y3
dz = z1+z2+z3
da = np.linalg.norm(vec[0])
db = np.linalg.norm(vec[1])
dc = np.linalg.norm(vec[2])

a,b,c = np.meshgrid(range(n1),range(n2),range(n3),indexing='ij')
r = np.vstack((a.flatten(),b.flatten(),c.flatten())).T
r = np.dot(r,vec)
homo = homo.flatten()
homo = np.square(homo)
lumo = lumo.flatten()
lumo = np.square(lumo)

coulb = 0.0
for i in range(1,n):
    lumotmp = np.roll(lumo,i)
    r2 = np.roll(r,i,axis=0)
    rtmp = np.linalg.norm(r - r2, axis=1)
    lumotmp = np.divide(lumotmp,rtmp)
    coulb += np.multiply(homo,lumotmp)
    print 'The step:', i, 'of', n
coulb = coulb*da*da*dc*da*db*dc/epsilon


print 'Exciton binding energy', coulb*27.211, 'eV'

end = timer()
print 'elapsed time:', end - start, 'seconds.'
