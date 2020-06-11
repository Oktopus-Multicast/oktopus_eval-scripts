"""The dataset command."""

import os, itertools
from math import ceil
from multiprocessing import Pool, cpu_count

from base import Base # cli
from utils import redirect_stdout

from oktopus.dataset import ensure_dir
from okdatasetgen.commands import GetDatasetSfc

from ..eval_param import *

def _generate_sfc_dataset_files(params):
    topo_name = params.get("topo_name", "")
    res_file = params.get("res_file", "")
    dataset_input_dir = params.get("dataset_input_dir", "")
    sessions_count = params.get("session_count", 0)
    aux_ser_avail_p = params.get("aux_ser_avail_p", 0)
    ord_type = params.get("ord_type", 0)
    sfc_len = params.get("sfc_len", 0)
    sessions_with_services = params.get("sessions_with_services", 0)
    sub_output_dir = params.get("sub_output_dir", "")

    dataset_out = os.path.join(sub_output_dir, 'dataset.log')

    options = {'-i': res_file,
                '-t': topo_name,
                '-d': dataset_input_dir,
                '-o': sub_output_dir,
                '-s': str(sessions_count),
                '--aux_ser_avail_p': str(aux_ser_avail_p),
                '--ord_type': str(ord_type),
                '--sfc_len': str(sfc_len),
                '--sessions-with-services': str(sessions_with_services)}

    cmd = GetDatasetSfc(options)
    print('Running GetDatasetSfc', options)

    with open(dataset_out, 'wb') as log_file:
        with redirect_stdout(log_file):
            cmd.run() # run command

class GenerateSFC(Base):
    """GenerateSFC"""

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
            output_topo_dir = os.path.join(output_dir, topo_name)
            ensure_dir(output_topo_dir)

            for control_params in itertools.product(LENGTH_SER_CHAIN, PER_SESSIONS_WITH_SFC, ORD_TYPE, AUXILIARY_SER_AVAIL_P, EXP_MCAST_SESSIONS, EXPS, EXP_MCAST_REC, EXP_MCAST_BW):
                sfc_len, per_ser, ord_type, aux_ser_avail_p, session_count, exp_idx, recs, bw = control_params
                res_file = os.path.join(output_topo_dir, topo_name + '_resources.graphml')
                exp_dir = os.path.join(output_topo_dir, str(session_count), str(recs), str(bw), 'exp_%s' % str(exp_idx + 1))
                sub_output_dir = os.path.join(output_topo_dir, str(session_count), str(recs), str(bw), 'exp_%s' % str(exp_idx + 1) , \
                    'service_chain', str(sfc_len), str(per_ser), str(ord_type), str(aux_ser_avail_p))
                ensure_dir(sub_output_dir)

                params = {
                    "topo_name": topo_name,
                    "res_file": res_file,
                    "dataset_input_dir": exp_dir,
                    "session_count": session_count,
                    "receivers_per": recs,
                    "bandwidth_per": bw,
                    "aux_ser_avail_p": aux_ser_avail_p,
                    "ord_type": ord_type,
                    "sfc_len": sfc_len,
                    "sessions_with_services": int(ceil((per_ser/100.0)*session_count)),
                    "sub_output_dir": sub_output_dir
                }


                result = pool.apply_async(_generate_sfc_dataset_files, args=(params, ))
                print("Submitted %s-%s-%s-%s tasks to pool generate data" % (topo_name, str(session_count), str(sfc_len), str(per_ser)))
                results.append(result)

        results = [r.get() for r in results]
        pool.close()
        pool.join()
        print("GenerateSFC Done!")



