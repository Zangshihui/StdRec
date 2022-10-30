source $HOME/ENV/nbodykit/bin/activate
module load gcc
module load openmpi

Para='fiducial'
for ((i=0;i<250;i++))
do
    Simu_Start=$(($i*2))
    (python -u RecCal_multi.py $Para $(($Simu_Start+0))) &
    (python -u RecCal_multi.py $Para $(($Simu_Start+1))) &
    wait
done