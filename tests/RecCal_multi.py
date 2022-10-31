import sys
import time
import numpy as np
from StdRec import Reconstruct

NMesh = 512
BoxSize = 1000
bias = 1
R = 5

def main():
    start = time.time()
    
    snapPATH = '/scratch/p/pen/zangsh/Quijote_Simulations/Snapshots/fiducial/0/snapdir_004/snap_004'
    MyRec = Reconstruct(NMesh = NMesh, BoxSize = BoxSize, Omega_m0 = 0.3175, redshift = 0.5)
    # Read the snapshot
    MyRec.Readsnapshots(snapPATH = snapPATH)
    # Apply the RSD
    MyRec.RSD(los = 2)
    
    # Generate the displacement field
    MyRec.StdRec(bias = bias, Filter = R)    
    den = MyRec.GetRecDensity()
    
    end = time.time()
    print('StdRec finished, costs %f s.'%(end - start))
        
if __name__ == '__main__':
    main()