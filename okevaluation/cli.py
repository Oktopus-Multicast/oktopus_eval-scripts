"""
okevaluation

Usage:
  okevaluation generate_res  -o <output_dir>  [--topology=<topologies_dir>]  [--link_bw_cap=<link_bw_cap>] [--medium=<medium>]  [--topo_run=<topo_run>]
  okevaluation generate_dataset  -o <output_dir>   [--topology=<topologies_dir>] [--num_cpus=<num_cpus>] [--topo_run=<topo_run>]
  okevaluation generate_sfc  -o <output_dir>  [--topology=<topologies_dir>]   [--num_cpus=<num_cpus>] [--topo_run=<topo_run>]
  okevaluation run_sfc -o <output_dir>  [--topology=<topologies_dir>] [--num_cpus=<num_cpus>] [--topo_run=<topo_run>] [--csv_name=<csv_name>]
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
  okevaluation hello

Help:
  For help using this tool, please open an issue on the Github repository:
  https://cs-git-research.cs.surrey.sfu.ca/nsl/ISP/oktopus/eval-scripts
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
