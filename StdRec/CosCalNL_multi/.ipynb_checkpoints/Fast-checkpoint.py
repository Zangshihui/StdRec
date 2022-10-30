import time
import numpy as np
from CosCalNL_multi.Base import Base
from CosCalNL_multi.FastLoop_multi import FastLoop_multi

class Fast(Base):
    def __init__(self, BoxSize = 1000, NMesh = 512, Omega_m0 = 0.3175, Hubble0 = 67.11, redshift = 0, RSD = False, *args, **kwargs):
        super(Fast, self).__init__(BoxSize, NMesh, Omega_m0, Hubble0, redshift, RSD)

    def Paint(self, window = 'cic'):
        """
        Mapping the catalog onto the mesh. Both deconvolution and interlacing is operated.
        """
        if window == 'cic':
            self.Density1 = FastLoop_multi.CICPaint_multi(self.Position, self.NMesh, self.BoxSize, self.Size)
            self.Density2 = FastLoop_multi.CICPaint_multi(self.Position + 0.5*self.H, self.NMesh, self.BoxSize, self.Size)
            self.Density = 0.5*(self.Density1 + self.Density2)
            self.deltaX = self.Density - 1
        self.deltaK = np.fft.rfftn(self.deltaX)
        self.deltaK = self.DeConvolution(self.deltaK, 2)
        
    def Truncate(self, data):
        kmax = self.NMesh/2
        data[self.k_ind > kmax] = 0
        return data

    
