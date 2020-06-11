#!/bin/bash 

TEST_DIR="/local-scratch/carlosl/vod"
CSV_FILENAME="output/vod.csv"
CHART_DIR="/local-scratch/carlosl/opt"
declare -a topo=(AttMpls Dfn Columbus Ion Colt)
declare -a topo=(Colt)
declare -a exps=(0)

# Create graph file
for t in ${topo[@]}
do
    python parallel_run_distributed.py res -o $TEST_DIR --topo_run=$t
done
wait

# Create sessions
for t in ${topo[@]}
do
    for e in ${exps[@]}
    do
        python parallel_run_distributed.py dataset -o $TEST_DIR --topo_run=$t --exps_id=$e &
    done
done
wait

# Create service chain
for t in ${topo[@]}
do
    for e in ${exps[@]}
    do
        echo python parallel_run_distributed.py dataset_sfc -o $TEST_DIR --topo_run=$t --exps_id=$e 
        python parallel_run_distributed.py dataset_sfc -o $TEST_DIR --topo_run=$t --exps_id=$e &
    done
done
wait

# Run algo
for t in ${topo[@]}
do
    for e in ${exps[@]}
    do
        echo python parallel_run_distributed.py exps_sfc -o $TEST_DIR --csv_name=$CSV_FILENAME --topo_run=$t --exps_id=$e 
        python parallel_run_distributed.py exps_sfc -o $TEST_DIR --csv_name=$CSV_FILENAME --topo_run=$t --exps_id=$e &
        sleep 1
    done
done
wait

# # Create graph
# python create_graph.py sc --csv $CSV_FILENAME -o $CHART_DIR
# wait

echo "DONE." "TOPO=[${topo[*]}] EXPS=[${exps[*]}] TEST_DIR=$TEST_DIR"