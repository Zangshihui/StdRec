import time
import numpy as np
from CosCalNL_multi.Fast import Fast
from CosCalNL_multi.FastLoop_multi import FastLoop_multi

class Reconstruct(Fast):
    def __init__(self, BoxSize = 1000, NMesh = 512, Omega_m0 = 0.3175, Hubble0 = 67.11, redshift = 0, RSD = False, *args, **kwargs):
        super(Reconstruct, self).__init__(BoxSize, NMesh, Omega_m0, Hubble0, redshift, RSD)

    
    def Gaussian_Window(self, R):
        """
        Return a Gaussian window with scale R
        """
        self.deltaK = np.fft.rfftn(self.deltaX)
        window = np.exp(-0.5 * (self.k_ind * self.Kf) ** 2. * R**2.).astype(np.float32)
        self.deltaK *= window
        self.deltaK = self.Truncate(self.deltaK)
    
    def Zeldovich_Approx(self, bias = 1):
        """
        Return the displacement result by Zeldovich's approximation
        """
        self.k_ind[0,0,0] = 1
        if self.RSD == True:
            temp = -1j*self.deltaK/self.k_ind**2/(bias + self.f*self.mu_ind**2)/self.Kf
        else:
            temp = -1j*self.deltaK/self.k_ind**2/(bias)/self.Kf
        self.k_ind[0,0,0] = 0
        self.Dis = np.empty([self.NMesh, self.NMesh, self.NMesh, 3], dtype = np.float32)
        self.Dis[:, :, :, 0]= np.fft.irfftn(temp*self.fnx).real.astype(np.float32)
        self.Dis[:, :, :, 1] = np.fft.irfftn(temp*self.fny).real.astype(np.float32)
        self.Dis[:, :, :, 2] = np.fft.irfftn(temp*self.fnz).real.astype(np.float32)
        del temp
        
    def StdRec(self):
        """
        Carry on standard reconstruction
        """
        # Add anisotropic displacement
        if self.RSD == True:
            self.Dis[:, :, :, 2] += self.Dis[:, :, :, 2]*self.f
        # Move the particles
        self.Position = FastLoop_multi.Shift_multi(self.Position.astype(np.float32), self.Dis.astype(np.float32), self.NMesh, self.BoxSize, self.Size)
        self.delta_d1 = FastLoop_multi.CICPaint_multi(self.Position, self.NMesh, self.BoxSize, self.Size) 
        self.delta_d2 = FastLoop_multi.CICPaint_multi(self.Position + 0.5*self.H, self.NMesh, self.BoxSize, self.Size) 
        self.delta_d = 0.5*(self.delta_d1 + self.delta_d2) - 1
        del self.delta_d1, self.delta_d2
        del self.Position
        
        # Generate referenced particles and move them.
        self.Position_Grid = FastLoop_multi.Grid(self.BoxSize, self.NMesh)
        self.Position_Grid = FastLoop_multi.Shift_multi(self.Position_Grid.astype(np.float32), self.Dis.astype(np.float32), self.NMesh, self.BoxSize, self.NMesh**3)
        self.delta_s1 = FastLoop_multi.CICPaint_multi(self.Position_Grid, self.NMesh, self.BoxSize, self.NMesh**3)
        self.delta_s2 = FastLoop_multi.CICPaint_multi(self.Position_Grid + 0.5*self.H, self.NMesh, self.BoxSize, self.NMesh**3)
        self.delta_s = 0.5*(self.delta_s1 + self.delta_s2) - 1
        del self.delta_s1, self.delta_s2
        del self.Position_Grid, self.Dis
        
        # Calculate the difference between two fields
        self.deltaX0 = self.delta_d - self.delta_s
        del self.delta_d, self.delta_s
        self.deltaX0k = np.fft.rfftn(self.deltaX0)
        self.deltaX0k = self.DeConvolution(self.deltaX0k, 2)
        self.deltaX0 = np.fft.irfftn(self.deltaX0k).real
        
        
    def DeConvolution(self, data, p):
        """
        DeConvolution for Window Kernel in Fourier Space
        Here's the algorith for CIC Kernel (p = 2)
        """
        self.dn = np.sinc(self.Kf*self.fn/(2*self.Knyq))**(-p)
        self.rdn = np.sinc(self.Kf*self.rfn/(2*self.Knyq))**(-p)
        self.d_ind = self.dn[:, None, None]*self.dn[None, :, None]*self.rdn[None, None, :]
        data *= self.d_ind
        del self.dn, self.d_ind
        return data
        
        
        
    
   
