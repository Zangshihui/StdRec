Para=fiducial

for ((i=2000;i<2001;i++))
do
    Simu_Start=$(($i*1))
    
    source ~/.globus.sh
    globus transfer $Quijote3:/$Para/$(($Simu_Start+0))/snapdir_004 $Niagara:/scratch/p/pen/zangsh/Quijote_Simulations/Snapshots/$Para/$(($Simu_Start+0))/snapdir_004 --label "Snapshots StdRec" --recursive 
    sleep 1m
    
    source $HOME/ENV/nbodykit/bin/activate
    cd /scratch/p/pen/zangsh/StdRec
    (python RecCal_multi.py $Para $(($Simu_Start+0))) &
    wait
    (python ../NLR/Power/Power.py fiducial $(($Simu_Start+0))) &
    wait
    
    snapPATH=/scratch/p/pen/zangsh/Quijote_Simulations/Snapshots/$Para
    rm -rf $snapPATH/$(($Simu_Start+0))/snapdir_004/snap_004*
    
    echo $Para $i

done