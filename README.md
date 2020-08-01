# Oktopus Evaluation Scripts


This repository contain scripts to run the evaluation experiments of Oktopus.

## Install
First install the Oktopus [Framework](https://github.com/Oktopus-Multicast/oktopus_framework) and [Dataset Generation](https://github.com/Oktopus-Multicast/oktopus_dataset-gen) packages.
Then install the Oktopus Evaluation Scripts module by running:

    pip install -e .

## Usage

Oktopus Evaluation Scripts contain a set of commands which can be view by running:

    okevaluation -h

It should output:

```
okevaluation

Usage:
  okevaluation generate_res  -o <output_dir>  --topology=<topologies_dir>  --topo_run=<topo_run> [--link_bw_cap=<link_bw_cap>] [--medium=<medium>]  
  okevaluation generate_dataset  -o <output_dir>   --topology=<topologies_dir> --topo_run=<topo_run> [--num_cpus=<num_cpus>]
  okevaluation generate_sfc  -o <output_dir>  --topology=<topologies_dir>  --topo_run=<topo_run> [--num_cpus=<num_cpus>] 
  okevaluation run_sfc -o <output_dir>  --topology=<topologies_dir> [--num_cpus=<num_cpus>]  [--csv_name=<csv_name>]
  okevaluation create_plot --csv <csv_file> --dir <dir> -o <output_dir>

Arguments:
  -o <output_dir>                    Output directory                         
  --topology=<isp_topology>          ISP topology (without resources)          
  --link_bw_cap=<link_bw_cap>        Link bandwidth capacity                   [default: 10000]
  --medium=<medium>                  Medium of the link                        [default: copper]
  --num_cpus=<num_cpus>              Number of parallel tasks                  [default: inf]
  --topo_run=<topo_run>              Choose a topology                         
  --csv_name=<csv_name>              csv file name                             [default: date]
  
  --csv <csv_file>    CSV File
  --dir <dir>         Data directory
  
Options:
  -h --help     Displays this message
  -v --version  Displays script version


```

## Experiment Control Parameters

The commands uses default parameters found in this [file](https://github.com/oktopus-multicast/oktopus_eval-scripts/blob/master/okevaluation/commands/__init__.py) of the repository.

## Commands

* ###  okevaluation generate_res

   It generates the ISP files for the experiment.

   Example:

  ```bash
  okevaluation generate_res  -o example/ --topology=oktopus_dataset-gen/data/topology_zoo/ --topo_run=AttMpls
  ```

  Given the specified `AttMpls` topology and the `oktopus_dataset-gen/data/topology_zoo/` directory, where it stores the Internet Topology Zoon AttMpls graphml file. It generates a AttMpls ISP graph file in `example/` with the given control parameter link capacity.

* ###  okevaluation generate_dataset

   It generates the multicast sessions for the experiment.

   Example:

  ```bash
  okevaluation generate_dataset  -o example/ --topology=oktopus_dataset-gen/data/topology_zoo/ --topo_run=AttMpls
  ```

  Given the specified `AttMpls` topology and the `oktopus_dataset-gen/data/topology_zoo/` directory, where it stores the Internet Topology Zoon AttMpls graphml file. It generates CSV files containing the multicast sessions in `example/` directory.

* ###  okevaluation generate_sfc

   It generates the service chain requirement for the multicast sessions for the experiment.

   Example:

  ```bash
  okevaluation generate_sfc  -o example/ --topology=oktopus_dataset-gen/data/topology_zoo/ --topo_run=AttMpls
  ```

  Given the specified `AttMpls` topology and the `oktopus_dataset-gen/data/topology_zoo/` directory, where it stores the Internet Topology Zoon AttMpls graphml file. It generates CSV files containing the service chain for the multicast sessions in `example/` directory.

* ###  okevaluation run_sfc

   It generates the results of the experiment.

   Example:

  ```bash
  okevaluation run_sfc  -o example/ --topology=oktopus_dataset-gen/data/topology_zoo/
  ```

  Given the specified control parameters in the setting [file](https://github.com/oktopus-multicast/oktopus_eval-scripts/blob/master/okevaluation/commands/__init__.py) and the `oktopus_dataset-gen/data/topology_zoo/` directory, where it stores the Internet Topology Zoo graphml file. It generates the results of the experiment in `example/` directory and it output a summary of the results in CSV format under the `output` directory of the current path.

* ###  okevaluation create_plot

   It generates the plot of the experiment results.

   Example:

  ```bash
  okevaluation create_plot --csv=output/data_2020y_6m_29d_17h_5m_1s.csv --dir=example/ -o example/plot
  ```

  Given the summary result file `output/data_2020y_6m_29d_17h_5m_1s.csv` and results directory `example/`. It generates plots of the results in the `example/plot` directory.