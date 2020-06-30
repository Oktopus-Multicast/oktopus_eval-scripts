"""The create_plot command."""

import docopt, pandas, itertools, os, numpy, collections, statistics, copy
from sciplot.line import plot_line
from sciplot.bar import plot_two_bars, plot_n_bars
from sciplot import  DEFAULT_RC

from oktopus.dataset import ensure_dir

from . import REPRE_SAMPLE

from base import Base # cli

class _Metric:
    @staticmethod
    def mean_size(data):
        if len(data['num_links']) > 1:
            return statistics.mean(data['num_links'])
        else:
            return 0

    @staticmethod
    def std_hop(data):
        if len(data['num_links']) > 1:
            return statistics.stdev(data['num_links'])
        else:
            return 0

    @staticmethod
    def std_cost(data):
        if len(data['costs']) > 1:
            return statistics.stdev(data['costs'])
        else:
            return 0

    @staticmethod
    def runtime(data):
        return data['runtime']

    @staticmethod
    def avg_cost(data):
        if len(data['costs']) > 1:
            return statistics.mean(data['costs'])
        else:
            return 0

    @staticmethod
    def allc_sess(data):
        return data['complete_sessions'] * 100

    @staticmethod
    def total_bandwidth_cost(data):
        return data['total_routing_cost']

class _Constant:
    XAXIS_LABEL = {'num_sessions': 'Number of Sessions',
                'service_chain_len': 'Service Chain Length', 
                'percentage_sessions_with_services': '% Sessions with Service Chain', 
                'chain_order_type': 'Order Type of Service Chain', 
                'aux_ser_avail_p': '% Auxiliary Services',
                'receivers_per': '% Receivers',
                'bandwidth_per': '% Bandwidth',
                'paths': 'Number of Paths'}

    YAXIS_LABEL = {'total_bandwidth_cost': 'Total Routing Cost', 
                    'max_link_load': 'Max. Link Load %',
                    'runtime':'second',
                    'cost':'Avg Hops/Session',
                    'mean_size': 'Avg Size/Session',
                    'std_hop': 'STDEV Size/Session',
                    'std_cost': 'STDEV Cost/Session',
                    'avg_cost': 'Avg Cost/Session',
                    'allc_sess': '% Allocated Sessions'}
                    
    LABEL_ALGO = {'cplex_sc': 'OPT', 
                    'cplex_mte': 'OPT', 
                    'oktopus': 'Oktopus', 
                    'msa': 'MSA', 
                    'mtrsa': 'MTRSA',  
                    'mldp': 'mLDP'}

    METRIC_SET = {'mean_size': _Metric.mean_size,
                'std_hop': _Metric.std_hop,
                'std_cost': _Metric.std_cost,
                'runtime': _Metric.runtime,
                'avg_cost': _Metric.avg_cost,
                'allc_sess': _Metric.allc_sess,
                'total_bandwidth_cost': _Metric.total_bandwidth_cost}


class CreatePlot(Base):
    """CreatePlot"""

    def run(self):
        output_dir = self.options.get('-o', None)
        dir = self.options.get('--dir', None)
        csv_file = self.options.get('--csv', None)

        ensure_dir(output_dir)

        df = pandas.read_csv(csv_file)
        topo_set = set(df['topology'])
        objective_set = set(df['objective'])
        algo_set = set(df['algorithm'])
        ser_len_set = set(df['service_chain_len'])
        per_set = set(df['percentage_sessions_with_services'])
        ord_set = set(df['chain_order_type'])
        aux_set = set(df['aux_ser_avail_p'])
        num_set = set(df['num_sessions'])
        recs_set = set(df['receivers_per'])
        bw_set = set(df['bandwidth_per'])

        crl_param = {'num_sessions':num_set, 
            'service_chain_len':ser_len_set, 
            'percentage_sessions_with_services':per_set, 
            'chain_order_type':ord_set, 
            'receivers_per':recs_set, 
            'bandwidth_per':bw_set, 
            'aux_ser_avail_p':aux_set}


        param_keys = list(crl_param.keys())
        print "param_keys", param_keys
        param_values = [crl_param[param_key] for param_key in param_keys]
        print "param_values", param_values

        # control param
        for param_id, param_key in enumerate(param_keys):
            cp_param_values = copy.deepcopy(param_values)
            cp_param_values[param_id] = [0]
            # representative sample
            repre_sample = REPRE_SAMPLE[param_key]
            for p_id, p_k in enumerate(param_keys):
                if p_k == param_key:
                    continue
                else:
                    cp_param_values[p_id] = repre_sample[p_k]
            
            # fix the rest of control param
            for param_combi in itertools.product(*cp_param_values):
                ensure_dir(output_dir+"/" + '_'.join(map(str, _Constant.XAXIS_LABEL[param_key].split())))
                # for each topo
                for topo in topo_set:
                    y, x, max_y = dict(), dict(), dict()

                    for metric_key, metric_v in _Constant.METRIC_SET.items():
                        y[metric_key] = collections.defaultdict(list)
                        x[metric_key] = collections.defaultdict(list)
                        max_y[metric_key] = 0
                    # for each val of target control param
                    for param_var in param_values[param_id]:
                        if param_var == 'variable':
                            continue 
                        
                        # for each algo
                        for algo in algo_set:
                            param_combi_lst = list(param_combi)
                            param_combi_lst[param_id] = param_var
                            param_combi = tuple(param_combi_lst)

                            algo_df = df.loc[df['topology'] == topo]
                            algo_df = algo_df.loc[algo_df['algorithm'] == algo]
                            for id, k in enumerate(param_keys):
                                algo_df = algo_df.loc[algo_df[k] == param_combi[id]]

                            if algo_df.empty:
                                continue
                            algo_df = {k:list(v)[-1] for k, v in algo_df.items()}

                            data = dict()
                            try:
                                data['num_links'] = []
                                data['costs'] = []
                                data['total_routing_cost'] = float(algo_df['total_bandwidth_cost'])
                                data['runtime'] = float(algo_df['runtime'])
                                data['complete_sessions'] = float(algo_df['complete_sessions'])
                                data['num_sessions'] = float(algo_df['num_sessions'])
                            except ValueError:
                                data['total_routing_cost'] = 0
                                data['runtime'] = 0
                                data['complete_sessions'] = 1
                                data['num_sessions'] = float(algo_df['num_sessions'])

                            
                            # get data of each session
                            try:
                                sess_csv = pandas.read_csv("{}/{}/{}/exp_{}/service_chain/{}/{}/{}/{}/log/{}/{}/sess.csv".format(
                                                dir, 
                                                algo_df['topology'], 
                                                algo_df['num_sessions'], 
                                                algo_df['exp_id'], 
                                                algo_df['service_chain_len'],
                                                algo_df['percentage_sessions_with_services'],
                                                algo_df['chain_order_type'],
                                                algo_df['aux_ser_avail_p'],
                                                algo_df['algorithm'],
                                                algo_df['date']), 
                                                dtype={"cost": float})

                                sess_serv_csv = pandas.read_csv("{}/{}/{}/exp_{}/service_chain/{}/{}/{}/{}/sessions_{}_services.csv".format(
                                                dir, 
                                                algo_df['topology'], 
                                                algo_df['num_sessions'],
                                                algo_df['exp_id'], 
                                                algo_df['service_chain_len'],
                                                algo_df['percentage_sessions_with_services'],
                                                algo_df['chain_order_type'],
                                                algo_df['aux_ser_avail_p'],
                                                algo_df['num_sessions']))

                                sess = sess_csv.merge(sess_serv_csv, left_on='addr', right_on='addr', suffixes=('_left', '_right'))

                                cost, bw, num_receivers = list(sess['cost']), list(sess['bw']), [len(dsts.split(',')) for dsts in list(sess['dsts'])]
                                num_links = [c/b for c, b in zip(cost, bw)]
                                data['num_links'] = num_links
                                data['costs'] = cost

                            except Exception as e:
                                print "Check new format output location:"

                            if len(data['num_links']) == 0:
                                try:
                                    sess_csv = pandas.read_csv("{}/{}/{}/{}/{}/exp_{}/service_chain/{}/{}/{}/{}/log/{}/{}/sess.csv".format(
                                                    dir, 
                                                    algo_df['topology'], 
                                                    algo_df['num_sessions'], 
                                                    algo_df['receivers_per'], 
                                                    algo_df['bandwidth_per'], 
                                                    algo_df['exp_id'], 
                                                    algo_df['service_chain_len'],
                                                    algo_df['percentage_sessions_with_services'],
                                                    algo_df['chain_order_type'],
                                                    algo_df['aux_ser_avail_p'],
                                                    algo_df['algorithm'],
                                                    algo_df['date']), 
                                                    dtype={"cost": float})

                                    sess_serv_csv = pandas.read_csv("{}/{}/{}/{}/{}/exp_{}/service_chain/{}/{}/{}/{}/sessions_{}_services.csv".format(
                                                    dir, 
                                                    algo_df['topology'], 
                                                    algo_df['num_sessions'], 
                                                    algo_df['receivers_per'], 
                                                    algo_df['bandwidth_per'], 
                                                    algo_df['exp_id'], 
                                                    algo_df['service_chain_len'],
                                                    algo_df['percentage_sessions_with_services'],
                                                    algo_df['chain_order_type'],
                                                    algo_df['aux_ser_avail_p'],
                                                    algo_df['num_sessions']))

                                    sess = sess_csv.merge(sess_serv_csv, left_on='addr', right_on='addr', suffixes=('_left', '_right'))

                                    cost, bw, num_receivers = list(sess['cost']), list(sess['bw']), [len(dsts.split(',')) for dsts in list(sess['dsts'])]
                                    num_links = [c/b for c, b in zip(cost, bw)]
                                    data['num_links'] = num_links
                                    data['costs'] = cost

                                except Exception as e:
                                    print e

                            for metric_key, metric_v in _Constant.METRIC_SET.items():
                                y_var, x_var = metric_v(data), param_var
                                if param_key in ['receivers_per', 'aux_ser_avail_p']:
                                    x_var = float(param_var)*100

                                y[metric_key][algo_df['algorithm']].append(y_var)
                                x[metric_key][algo_df['algorithm']].append(x_var)
                                max_y[metric_key] = max(max_y[metric_key], y_var)
                    
                    # for each metric
                    for metric_key in _Constant.METRIC_SET.keys():
                        ys, xs, line_labels = [], [], []
                        for algo in y[metric_key].keys():
                            z = sorted(zip(x[metric_key][algo], y[metric_key][algo]))
                            if len(x[metric_key][algo]) < 1:
                                continue
                            xx, yy = zip(*z)
                            ys.append(list(yy))
                            xs.append(list(map(int, xx)))
                            line_labels.append(_Constant.LABEL_ALGO[algo])
                        
                        if len(xs) < 2:
                            continue

                        # Create graph
                        param_combi_lst = list(param_combi)
                        param_combi_lst[param_id] = 'vary'
                        title = topo + '_' + metric_key + '_' + '_'.join(map(str, param_combi_lst)).replace('.', '')
                        print title

                        filename = os.path.join(output_dir+"/" + '_'.join(map(str, _Constant.XAXIS_LABEL[param_key].split())), title)
                        
                        yaxis_label = _Constant.YAXIS_LABEL[metric_key]
                        y_range = [0, max_y[metric_key]*2]
                        x_range = [min(xs[0]), max(xs[0])]
                        legend_bbox = (0.01, 0.25, 0.45, 0.08) # bottom left

                        if metric_key == 'allc_sess':
                            if param_key == 'num_sessions':
                                y_range = [20, 100]
                            else:
                                y_range = [20, 80]

                        if param_key == 'num_sessions':
                            x_range = [min(xs[0]), max(xs[0])]
                            if max(xs[0]) < 4000:
                                x_range = [0, 1000]
                        else:
                            legend_bbox = (0.6, 0.9, 0.4, 0.08) # uppder right

                        if param_key in ['chain_order_type']:
                            xname = ['partial', 'random']
                            y_range = [0, 60]
                            plot_n_bars(ys,
                                line_labels,
                                xticks = xname,
                                legend=True,
                                xaxis_label=_Constant.XAXIS_LABEL[param_key],
                                yaxis_label=yaxis_label,
                                x_sci=False, y_sci=False,
                                y_lim=y_range,
                                hatch=True,
                                name=filename)
                        else:
                            plot_line(xs,
                                ys,
                                xaxis_label=_Constant.XAXIS_LABEL[param_key],
                                yaxis_label=yaxis_label,
                                line_labels=line_labels,
                                x_lim=x_range,
                                y_lim=y_range,
                                legend_top=False,
                                legend_bbox=legend_bbox,
                                legend_font_size=24,
                                ls_cycle=True,
                                x_sci=False,
                                y_sci=False,
                                name=filename
                            )