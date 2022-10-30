import sys
import time
import numpy as np
from CosCalNL_multi.Reconstruct import Reconstruct
from CosCal.CPower import CPower
from CosCal.FastLoop import Dimension

NMesh = 512
BoxSize = 1000
bias = 1
Para = sys.argv[1]
Num = sys.argv[2]
R = 5

# R = np.array(sys.argv[3]).astype(np.float32)
# snapnum = str(sys.argv[4])
# bias = float(sys.argv[5])
# Name = sys.argv[6]
# print(R)

def main():
    start = time.time()
    
    snapPATH = '/scratch/p/pen/zangsh/Quijote_Simulations/Snapshots/' + Para + '/' + Num + '/snapdir_004/snap_004'
#     HaloPATH = '/scratch/p/pen/zangsh/Quijote_Simulations/Halos/' + Para + '/' + str(Num) + '/'
    MyRec = Reconstruct(NMesh = NMesh, BoxSize = BoxSize, Omega_m0 = 0.3175, redshift = 0, RSD = False)
    MyRec.Readsnapshots(snapPATH = snapPATH)
#     MyRec.Readhalo(mode = 'Quijote', HaloPATH = HaloPATH)

    # Paint the catalog on the mesh using cic
    MyRec.Paint()
    # Smooth the field
    MyRec.Gaussian_Window(R)
    # Calculate the Displacement field
    MyRec.Zeldovich_Approx(bias = bias) 
    
    # Generate the displacement field
    MyRec.StdRec()
    den = MyRec.GetRecDensity()

    # Calculating power
    DenSavePATH = '/scratch/p/pen/zangsh/Quijote_Simulations/Density/' + Para + '/' + str(Num) + '/Den_DMStdRec_R5.bin'
    den.astype(np.float32).tofile(DenSavePATH)
    
    end = time.time()
    print('%s %s finished, costs %f s.'%(Para, Num, end - start))
        
if __name__ == '__main__':
    main()