import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns

__author__ = 'Khaled Diab (kdiab@sfu.ca)'

# Line Styles
DEFAULT_LINE_WIDTH = 4
ALTERNATIVE_LINE_WIDTH = 5
SMALL_LINE_WIDTH = 2
LINE_STYLES = ['-', '--', '-.', ':']

# Font
TEX_ENABLED = False
TICK_FONT_SIZE = 26
AXIS_FONT_SIZE = 26
LEGEND_FONT_SIZE = 28

# COLOR
bar_colors1 = ['#e66101', '#fdb863', '#b2abd2', '#5e3c99']
bar_colors2 = ['#ffffcc', '#c2e699', '#78c679', '#31a354', '#006837']
flatui = ["#0072B2", "#D55E00", "#009E73", "#3498db", "#CC79A7", "#F0E442", "#56B4E9"] # ["#3498db", "#2ecc71"]  # , "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
blue_red = ["#0000ff", "#ff0000"]
DEFAULT_PALETTE = sns.color_palette(blue_red)  # sns.color_palette(palette='colorblind')
ALTERNATIVE_PALETTE = sns.color_palette(flatui)  # sns.color_palette(palette='pastel')
# BAR_PALETTE = list(reversed(sns.color_palette("cubehelix", 8)))
# BAR_PALETTE = sns.color_palette(bar_colors1[:3] + bar_colors2)
# Helix
# BAR_PALETTE = sns.color_palette([bar_colors2[-1], bar_colors2[1]])
# STEM
# BAR_PALETTE = sns.color_palette([bar_colors2[2], bar_colors2[-1]])
# BAR_PALETTE = sns.color_palette(['#ff0000', '#00ff00', '#0000ff', '#ff00ff'])
BAR_PALETTE = sns.color_palette(blue_red)


DEFAULT_RC = {'lines.linewidth': DEFAULT_LINE_WIDTH,
              'axes.labelsize': AXIS_FONT_SIZE,
              'xtick.labelsize': TICK_FONT_SIZE,
              'ytick.labelsize': TICK_FONT_SIZE,
              'legend.fontsize': LEGEND_FONT_SIZE,
              'text.usetex': TEX_ENABLED,
              # 'ps.useafm': True,
              # 'ps.use14corefonts': True,
              'font.family': 'sans-serif',
              # 'font.serif': ['Helvetica'],  # use latex default serif font
              }

ALTERNATIVE_RC = {'lines.linewidth': ALTERNATIVE_LINE_WIDTH,
                  'axes.labelsize': AXIS_FONT_SIZE,
                  'xtick.labelsize': TICK_FONT_SIZE,
                  'ytick.labelsize': TICK_FONT_SIZE,
                  'legend.fontsize': LEGEND_FONT_SIZE,
                  'text.usetex': TEX_ENABLED,
                  'font.family': 'sans-serif',
                  # 'font.family': 'serif',
                  # 'font.serif': ['Helvetica'],  # use latex default serif font
                 }

SMALL_RC = {'lines.linewidth': SMALL_LINE_WIDTH,
            'axes.labelsize': AXIS_FONT_SIZE,
            'xtick.labelsize': TICK_FONT_SIZE,
            'ytick.labelsize': TICK_FONT_SIZE,
            'legend.fontsize': LEGEND_FONT_SIZE,
            'text.usetex': TEX_ENABLED,
            'font.family': 'sans-serif',
            # 'font.family': 'serif',
            # 'font.serif': ['Helvetica'],  # use latex default serif font
            }

sns.set_context(context='paper', rc=DEFAULT_RC)
sns.set_style(style='ticks')
sns.set_palette(DEFAULT_PALETTE)
plt.rc('text', usetex=TEX_ENABLED)
plt.rc('ps', **{'fonttype': 42})
# plt.rc('mathtext', **{'fontset': 'stix'})
# plt.rc('axes.formatter', **{'use_mathtext': True})
# plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
# plt.rc('font', **{'family': 'serif', 'serif': ['Times']})
plt.rc('legend', handlelength=1., handletextpad=0.1)
