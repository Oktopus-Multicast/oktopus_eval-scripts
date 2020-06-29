CMD_CONSTANTS = {'create_plot': CreatePlot,
        'generate_res': GenerateRes,
        'generate_dataset': GenerateDataset,
        'generate_sfc': GenerateSFC,
        'run_sfc': RunSFC}


REPRE_SAMPLE = {
    'num_sessions':{'num_sessions': True, 
            'service_chain_len': ['variable'], 
            'percentage_sessions_with_services':[100], 
            'chain_order_type':[1], 
            'receivers_per':['variable'], 
            'bandwidth_per':['variable'], 
            'aux_ser_avail_p':[0.25]},
    'service_chain_len':{'num_sessions': [4000], 
            'service_chain_len': True, 
            'percentage_sessions_with_services':[100], 
            'chain_order_type':[1], 
            'receivers_per':['variable'], 
            'bandwidth_per':['variable'], 
            'aux_ser_avail_p':[0.25]},
    'percentage_sessions_with_services':{'num_sessions': [4000], 
            'service_chain_len': ['variable'], 
            'percentage_sessions_with_services':True, 
            'chain_order_type':[1], 
            'receivers_per':['variable'], 
            'bandwidth_per':['variable'], 
            'aux_ser_avail_p':[0.25]},
    'chain_order_type':{'num_sessions': [4000], 
            'service_chain_len': ['variable'], 
            'percentage_sessions_with_services':[100], 
            'chain_order_type':True, 
            'receivers_per':['variable'], 
            'bandwidth_per':['variable'], 
            'aux_ser_avail_p':[0.25]},
    'receivers_per':{'num_sessions': [4000], 
            'service_chain_len': ['variable'], 
            'percentage_sessions_with_services':[100], 
            'chain_order_type':[1], 
            'receivers_per':True, 
            'bandwidth_per':['variable'], 
            'aux_ser_avail_p':[0.25]},
    'bandwidth_per':{'num_sessions': [4000], 
            'service_chain_len': ['variable'], 
            'percentage_sessions_with_services':[100], 
            'chain_order_type':[1], 
            'receivers_per':['variable'], 
            'bandwidth_per':True, 
            'aux_ser_avail_p':[0.25]},
    'aux_ser_avail_p':{'num_sessions': [4000], 
            'service_chain_len': ['variable'], 
            'percentage_sessions_with_services':[100], 
            'chain_order_type':[1], 
            'receivers_per':['variable'], 
            'bandwidth_per':['variable'], 
            'aux_ser_avail_p':True},
}

OBJECTIVES=['routing']
NUM_OF_SER_PER_NODE = 6
EXP_MCAST_SESSIONS = [50, 100, 500, 1000, 1500, 2000, 3000, 4000]
NUM_OF_AVAILABLE_SERVICES = 6
PER_SESSIONS_WITH_SFC = [100]
LENGTH_SER_CHAIN = [2, 3, 4, 5, 6, "variable"]
ORD_TYPE = [1, 2]
AUXILIARY_SER_AVAIL_P = [0.25, 0.05, 0.15, 0.35, 0.45] 
EXP_MCAST_REC = ['variable', 0.1, 0.2, 0.3, 0.4] 
EXP_MCAST_BW = ['variable'] 
ALGORITHMS = ['oktopus', 'msa'] # ['cplex_sc']
SDN_APP = ['min_mlu_service_chaining']
EXPS = [0]


from create_plot import CreatePlot

from generate_res import GenerateRes
from generate_dataset import GenerateDataset
from generate_sfc import GenerateSFC
from run_sfc import RunSFC

__all__ = ['CreatePlot', 'GenerateRes', 'GenerateDataset', 'GenerateSFC', 'RunSFC', 'CMD_CONSTANTS',
'REPRE_SAMPLE', 'OBJECTIVES', 'NUM_OF_SER_PER_NODE', 'EXP_MCAST_SESSIONS', 'NUM_OF_AVAILABLE_SERVICES', 'PER_SESSIONS_WITH_SFC',
'LENGTH_SER_CHAIN', 'ORD_TYPE', 'AUXILIARY_SER_AVAIL_P', 'EXP_MCAST_REC', 'EXP_MCAST_BW', 'ALGORITHMS', 'SDN_APP', 'EXPS']


