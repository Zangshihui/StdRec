import sys
import numpy as np

Para = sys.argv[1]
z = sys.argv[2]

def main():
    k_InterPATH = '/project/p/pen/zangsh/Quijote_Simulations/Power/fiducial/0/k.bin'
#     Pk_linPATH = '/project/p/pen/zangsh/Quijote_Simulations/Power/Linear_Pk/' + Para + '/CAMB_TABLES/CAMB_matterpow_' + z + '.dat' 
    Pk_linPATH = '/project/p/pen/zangsh/Quijote_Simulations/Power/Linear_Pk/Mnu_p/ICs/0.10eV_Pcb_rescaled_z0.0000.txt'
    Pk_InterPATH = '/project/p/pen/zangsh/Quijote_Simulations/Power/' + Para + '/Average/Pk_IC.bin'
    k_lin, Pk_lin = np.loadtxt(Pk_linPATH, unpack = True)
    k_Inter = np.fromfile(k_InterPATH, dtype = np.float32)
    Pk_Inter = np.zeros(256)
    k_Inter *= 2*np.pi/1000
    
    for I in range(1, 256):
        k_local = k_Inter[I]
        xi = (k_lin < k_local).sum() - 1
        xj = xi + 1
        ki = (k_lin[xj] - k_local)/(k_lin[xj] - k_lin[xi])
        kj = (k_local - k_lin[xi])/(k_lin[xj] - k_lin[xi])
        Pk_Inter[I] = ki*Pk_lin[xi] + kj*Pk_lin[xj]
        
    Pk_Inter.astype(np.float32).tofile(Pk_InterPATH)
    

main()