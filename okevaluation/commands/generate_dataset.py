"""The dataset command."""

import os, itertools
from math import ceil
from multiprocessing import Pool, cpu_count

from base import Base # cli
from utils import redirect_stdout

from oktopus.dataset import ensure_dir
from okdatasetgen.commands import GetDataset

from ..eval_param import *

def _generate_dataset_files(isp_topo_resources_file, out_dir, sessions_count, receivers_per, bandwidth_per):
    dataset_out = os.path.join(out_dir, 'dataset.log')
    options = {'-i': isp_topo_resources_file,
                '-o': out_dir,
                '-s': str(sessions_count),
                '-r': str(receivers_per),
                '-b': str(bandwidth_per)}
    cmd = GetDataset(options)
    print('Running GetDataset', options)

    with open(dataset_out, mode='w') as log_file:
        with redirect_stdout(log_file):
            cmd.run() # run command

class GenerateDataset(Base):
    """GenerateDataset"""

    def run(self):
        output_dir = self.options.get('-o', None)
        num_cpus = float(self.options.get('--num_cpus', None))
        topo_run = self.options.get('--topo_run', None)

        # CPU
        cpu_util = int(ceil((0.95 * cpu_count())))
        cpu_util = int(num_cpus) if num_cpus < cpu_util else cpu_util
        pool = Pool(cpu_util)

        results = []

        for topo_name in [topo_run]:
            sub_output_dir = os.path.join(output_dir, topo_name)
            ensure_dir(sub_output_dir)

            for control_params in itertools.product(EXP_MCAST_SESSIONS, EXP_MCAST_REC, EXP_MCAST_BW, EXPS):
                session_count, recs, bw, exp_idx = control_params
                res_file = os.path.join(sub_output_dir, topo_name + '_resources.graphml')
                exp_dir = os.path.join(sub_output_dir, 
                                        str(session_count), 
                                        str(recs),
                                        str(bw),
                                        'exp_%s' % str(exp_idx + 1))
                ensure_dir(exp_dir)

                result = pool.apply_async(_generate_dataset_files, args=(res_file, exp_dir, session_count, recs, bw))
                print("Submitted %s-%s tasks to pool generate data" % (topo_name, str(session_count)))
                results.append(result)

        results = [r.get() for r in results]
        pool.close()
        pool.join()
        print("GenerateDataset Done!")


