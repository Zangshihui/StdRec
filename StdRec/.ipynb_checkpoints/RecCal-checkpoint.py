import sys
import time
import numpy as np
from CosCalNL.Reconstruct import Reconstruct

NMesh = 512
BoxSize = 1000
R_init = 20
R_min = 2
Para = sys.argv[1]
Num = sys.argv[2]

def main():
    snapPATH = '/mnt/scratch-lustre/zangsh/Quijote_Simulations/Snapshots/' + Para + '/' + Num + '/snapdir_004/snap_004'
    savePATH = '/mnt/scratch-lustre/zangsh/NLRec_Marcel/Density/' + Para + '/' + Num + '/Den_Rec.bin'
    MyRec = Reconstruct(NMesh = NMesh, BoxSize = BoxSize)
    MyRec.Readsnapshots(snapPATH = snapPATH)

    # Loop to iterate
    for i in range(8):
        # Paint the catalog on the mesh using cic
        MyRec.Paint()
        R = max(0.5**i*R_init, R_min)
        MyRec.Gaussian_Window(R)
        MyRec.Zeldovich_Approx()
        MyRec.Shift()
    # Generate the displacement field
    MyRec.Paint()
    MyRec.Displace_Reconstruct()
    den = MyRec.GetRecDensity()
    den.astype(np.float32).tofile(savePATH)
        
if __name__ == '__main__':
    main()