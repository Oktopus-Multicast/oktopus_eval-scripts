"""The dataset command."""

import os, itertools, time, re, csv, subprocess, copy

from math import ceil
from collections import OrderedDict 

from base import Base # cli
from utils import redirect_stdout

from oktopus.dataset import ensure_dir

from . import *
from multiprocessing import Pool, cpu_count

def _generate_solutions_sfc(date, csv_name, exp_id, dataset_dir, app, topo_name, graph_path, input_dir, sessions_count, algorithm_name, objective, sfc_len, per_ser, ord_type, aux_ser_avail_p, receivers_per, bandwidth_per):
    curr_dir =  os.path.dirname(__file__)
    alg_cmd = ['python', '-u', "%s/sdn_app/%s.py" % (os.path.dirname(curr_dir), app), topo_name, graph_path, input_dir, str(sessions_count), algorithm_name, objective]

    log_dir = os.path.join(dataset_dir, 'log', algorithm_name, date)
    log_file = os.path.join(log_dir, 'output.log')
    ensure_dir(log_dir)

    sess_file = os.path.join(log_dir, 'sess.csv')
    bandwidth_cost = max_link_load = runtime = is_complete = False

    data_log_file =  open(log_file, mode='wb')
    csv_sess_file =  open(sess_file, mode='wb')
    csv_sess_writer = csv.writer(csv_sess_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_sess_writer.writerow(['addr', 'cost', 'exp_id','date','num_sessions', 'receivers_per', 'bandwidth_per', 'objective', 'algorithm', 'topology', 'service_chain_len', 'percentage_sessions_with_services', 'chain_order_type', 'aux_ser_avail_p', 'time', 'allo_order'])

    print('Running', ' '.join(alg_cmd))
    proc = subprocess.Popen(alg_cmd, stdout=data_log_file, stderr=data_log_file)
    proc.communicate()
    with open(log_file) as data_log_file:
        for line in data_log_file.readlines():    
            b = re.findall("Total bandwidth cost    = (\d*.*)", line)
            ll = re.findall("Max. link load value    = (\d*.\d*)", line) 
            rt = re.findall("Optimization time       = (\d*.\d*)", line)
            complete = re.findall("All DONE: (\d*.\d*)", line)

            if b:
                bandwidth_cost = b[0]
            if ll:
                max_link_load = ll[0]
            if rt:
                runtime = rt[0]
            if complete:
                is_complete = complete[0]

            sess = re.findall("Session Cost: (\d*.\d*.\d*.\d*), (\d*), (\d*.\d*), (\d*)", line)
            
            if sess and is_complete != False:
                csv_sess_writer.writerow([sess[0][0], sess[0][1], str(exp_id), date, str(sessions_count), str(receivers_per), str(bandwidth_per), objective, algorithm_name, topo_name, sfc_len, per_ser, ord_type, aux_ser_avail_p, sess[0][2], sess[0][3]])


    with open('%s'%csv_name, mode='a') as data_file:
        data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow([str(exp_id), date, str(sessions_count), str(receivers_per), str(bandwidth_per), objective, algorithm_name, topo_name, sfc_len, per_ser, ord_type, aux_ser_avail_p, runtime, max_link_load, bandwidth_cost, is_complete])
    
    return (is_complete, topo_name, algorithm_name, sessions_count, objective, app, sfc_len, per_ser, ord_type, aux_ser_avail_p, exp_id)

class RunSFC(Base):
    """RunSFC"""

    def run(self):
        output_dir = self.options.get('-o', None)
        num_cpus = float(self.options.get('--num_cpus', None))
        csv_name = self.options.get('--csv_name', None)

        date = 'data_%sy_%sm_%sd_%sh_%sm_%ss' % (time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)

        #csv file
        if csv_name == "date":
            csv_name = 'output/%s.csv'%date
            ensure_dir('output')

        # CPU
        cpu_util = int(ceil((0.95 * cpu_count())))
        cpu_util = int(num_cpus) if num_cpus < cpu_util else cpu_util
        pool = Pool(cpu_util)

        if not os.path.exists('%s'%csv_name):
            with open('%s'%csv_name, mode='w') as data_file:
                data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data_writer.writerow(['exp_id','date','num_sessions', 'receivers_per', 'bandwidth_per', 'objective', 'algorithm', 'topology', 'service_chain_len', 'percentage_sessions_with_services', 'chain_order_type', 'aux_ser_avail_p', 'runtime', 'max_link_load', 'total_bandwidth_cost', 'complete_sessions'])

        results = []

        crl_param = OrderedDict()
        crl_param['num_sessions']  = EXP_MCAST_SESSIONS
        crl_param['service_chain_len'] = LENGTH_SER_CHAIN
        crl_param['percentage_sessions_with_services'] = PER_SESSIONS_WITH_SFC
        crl_param['chain_order_type'] = ORD_TYPE
        crl_param['receivers_per'] = EXP_MCAST_REC
        crl_param['bandwidth_per'] = EXP_MCAST_BW
        crl_param['aux_ser_avail_p'] = AUXILIARY_SER_AVAIL_P

        # param for all repre sample experiment
        for topo_name, exp_idx, app, objective, algo in itertools.product(TOPO, EXPS, SDN_APP, OBJECTIVES, ALGORITHMS):
            output_topo_dir = os.path.join(output_dir, topo_name)
            ensure_dir(output_topo_dir)

            # control param
            cp_repre = copy.deepcopy(crl_param)
            for repre_k, repre_v in REPRE_SAMPLE.items():
                for sample_k, sample_v in repre_v.items():
                    if repre_k != sample_k:
                        cp_repre[sample_k] = sample_v
                
                # check topo
                if topo_name not in repre_v['topo']:
                    continue
                
                # fix the rest of control param
                for param_combi in itertools.product(*cp_repre.values()):
                    session_count, sfc_len, per_ser, ord_type, recs, bw, aux_ser_avail_p, _ = param_combi
                    res_file = os.path.join(output_topo_dir, topo_name + '_resources.graphml')
                    exp_id = 'exp_%s' % str(exp_idx + 1)
                    exp_dir = os.path.join(output_topo_dir,  str(session_count), str(recs), str(bw),  exp_id,  'service_chain', str(sfc_len), str(per_ser), str(ord_type), str(aux_ser_avail_p))
                    ensure_dir(exp_dir)
                    result = pool.apply_async(_generate_solutions_sfc, args=(date, csv_name, exp_idx+1, exp_dir, app, topo_name, res_file, exp_dir, session_count, algo, objective, sfc_len, per_ser, ord_type, aux_ser_avail_p, recs, bw))
                    print("Submitted {}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{}-{} tasks to pool".format(topo_name, exp_idx, app, objective, algo, session_count, sfc_len, per_ser, ord_type, recs, bw, aux_ser_avail_p))
                    results.append(result)

            break

        results = [r.get() for r in results]
        pool.close()
        pool.join()
        print("RunSFC Done!")



            

