# StdRec
**StdRec** is a python package to perform [the standard reconstruction](https://iopscience.iop.org/article/10.1086/518712/meta) algorithm on particle catalogs.

## Dependences

### GCC

gcc is required to compile the cython files.

### Other python pkgs
requirement.txt has listed all required python packages. They can be installed using the setup.py. Virtual environment is recommended to avoid collisions with other existed pkgs.

## install StdRec
```
git clone https://github.com/Zangshihui/StdRec
cd ./StdRec
python setup.py build_ext
python setup.py install
```

## Tutorial
### Set the cosmology
```
from StdRec import Reconstruct
MyRec = Reconstruct(NMesh = NMesh, BoxSize = BoxSize, Omega_m0 = 0.3175, redshift = 0.5)
```
NMesh decides the mesh grid where the reconstruction is going to perform. BoxSize is the size of the simulation. Omega_m0 is the matter density at $z = 0$. 
### Read the snapshot files
```
MyRec.Readsnapshots(snapPATH = snapPATH)
```
We quote the readgadget.py and readfof.py program in [Pylians3](https://github.com/franciscovillaescusa/Pylians3). Gadget format snapshots are supported here. You can also read Quijote halos like
```
MyRec.Readhalo(mode = 'Quijote', HaloPATH = HaloPATH)
```

### Apply RSD
```
MyRec.RSD(los = 2)
```
You can map your catalog into the redshift space.

### Perform the reconstruction
```
MyRec.StdRec(bias = bias, Filter = R)
```
The linear bias and Filter scale are required in this step.

### Get the result
```
den = MyRec.GetRecDensity()
```