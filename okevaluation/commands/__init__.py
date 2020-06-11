from create_plot import CreatePlot

from generate_res import GenerateRes
from generate_dataset import GenerateDataset
from generate_sfc import GenerateSFC
from run_sfc import RunSFC

__all__ = ['CreatePlot', 'GenerateRes', 'GenerateDataset', 'GenerateSFC', 'RunSFC']


CMD_CONSTANTS = {'create_plot': CreatePlot,
        'generate_res': GenerateRes,
        'generate_dataset': GenerateDataset,
        'generate_sfc': GenerateSFC,
        'run_sfc': RunSFC}

