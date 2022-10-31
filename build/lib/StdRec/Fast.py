import time
import numpy as np
from StdRec.Base import Base
import FastLoop_multi

class Fast(Base):
    def __init__(self, BoxSize = 1000, NMesh = 512, Omega_m0 = 0.3175, Hubble0 = 67.11, redshift = 0, *args, **kwargs):
        super(Fast, self).__init__(BoxSize, NMesh, Omega_m0, Hubble0, redshift)

    def Paint(self, window = 'cic'):
        """
        Mapping the catalog onto the mesh. Both deconvolution and interlacing is operated.
        """
        if window == 'cic':
            self.Density = FastLoop_multi.CICPaint_multi(self.Position, self.NMesh, self.BoxSize, self.Size)
            self.deltaX = self.Density - 1
        self.deltaK = np.fft.rfftn(self.deltaX)
        self.deltaK = self.DeConvolution(self.deltaK, 2)
        
    def Truncate(self, data):
        kmax = self.NMesh/2
        data[self.k_ind > kmax] = 0
        return data

    
