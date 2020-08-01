"""
okevaluation

Usage:
  okevaluation generate_res  -o <output_dir>  --topology=<topologies_dir>  --topo_run=<topo_run> [--link_bw_cap=<link_bw_cap>] [--medium=<medium>]  
  okevaluation generate_dataset  -o <output_dir>   --topology=<topologies_dir> --topo_run=<topo_run> [--num_cpus=<num_cpus>]
  okevaluation generate_sfc  -o <output_dir>  --topology=<topologies_dir>  --topo_run=<topo_run> [--num_cpus=<num_cpus>] 
  okevaluation run_sfc -o <output_dir>  --topology=<topologies_dir> [--topo_run=<topo_run>] [--num_cpus=<num_cpus>]  [--csv_name=<csv_name>]
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

Examples:
  okevaluation generate_res  -o example/ --topology=oktopus_dataset-gen/data/topology_zoo/ --topo_run=AttMpls
  okevaluation generate_dataset  -o example/ --topology=oktopus_dataset-gen/data/topology_zoo/ --topo_run=AttMpls
  okevaluation generate_sfc  -o example/ --topology=oktopus_dataset-gen/data/topology_zoo/ --topo_run=AttMpls
  okevaluation run_sfc  -o example/ --topology=oktopus_dataset-gen/data/topology_zoo/ --topo_run=AttMpls
  okevaluation create_plot --csv=output/data_2020y_6m_29d_17h_5m_1s.csv --dir=example/ -o example/plot

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/Oktopus-Multicast/oktopus_eval-scripts.git
"""
 
 
from inspect import getmembers, isclass
from docopt import docopt
 
from commands import CMD_CONSTANTS
 
from . import __version__ as VERSION

def main():
    """Main CLI entrypoint."""    
    options = docopt(__doc__, version=VERSION)
 
    for cmd in options.keys():
      if cmd in CMD_CONSTANTS and options[cmd]:
        command = CMD_CONSTANTS[cmd](options)
        command.run()
