"""The dataset command."""

import docopt, csv, os, sys, time, subprocess, re, json, pandas, statistics, itertools
from math import ceil

from base import Base # cli
from utils import redirect_stdout

from oktopus.dataset import ensure_dir
from okdatasetgen.commands import GetIsp


class GenerateRes(Base):
    """GenerateRes"""

    def _generate_resources_file(self, params):
        topo_out = os.path.join(params.get("out_dir", ""), 'topo.log')
        options =  {'-i':  params.get("isp_topo_file", ""),
                        '-o':  params.get("out_dir", ""),
                        '--link' :  params.get("link_capacity", 10000),
                        '--medium' :  params.get("medium",  'copper')}
        cmd = GetIsp(options)

        with open(topo_out, mode='w') as log_file:
            with redirect_stdout(log_file):
                cmd.run() # run command

    def run(self):
        output_dir = self.options.get('-o', None)
        topo_dir = self.options.get('--topology', None)
        link_bw_cap = int(self.options.get('--link_bw_cap', None))
        topo_run = self.options.get('--topo_run', None)
        medium = self.options.get('--medium', None)

        ensure_dir(output_dir)

        topo_file = os.path.join(topo_dir, topo_run + '.graphml')
        output_topo_dir = os.path.join(output_dir, topo_run)
        ensure_dir(output_topo_dir)
        params = {
            "isp_topo_file": topo_file,
            "out_dir": output_topo_dir,
            "link_capacity": link_bw_cap,
            "medium":  medium
        }
        self._generate_resources_file(params=params)
        print("GenerateRes Done!")
