#!/bin/bash 
#SBATCH --nodes=1
#SBATCH --ntasks=40
#SBATCH --time=23:00:00
#SBATCH --job-name MRec
#SBATCH --output=MRec_output_%j.txt
#SBATCH --mail-type=FAIL

Start=$1
End=$2
Para=$3
cd /scratch/p/pen/zangsh/MLR
source $HOME/ENV/nbodykit/bin/activate
module load gcc
module load openmpi

for ((i=$Start;i<$End;i++))
do
    python -u RecCal_multi.py $Para $i
    CatPATH=/project/p/pen/zangsh/Quijote_Simulations/Snapshots/$Para/$i/snapdir_004
    rm -rf $CatPATH/snap*
done
