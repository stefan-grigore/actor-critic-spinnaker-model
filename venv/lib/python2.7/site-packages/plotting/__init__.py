from .lines import (COLORS, riffle_lines, get_COLORS,
                    line_plot, error_plot, dual_plot)
from .dataframes import (pivot_timeseries, pivot_df, box_plot, point_plot,
                         dist_plot, bar_plot, df_line_plot, df_error_plot)

import matplotlib as mpl
import seaborn as sns

sns.set_style("white")
sns.set_style("ticks")
mpl.rcParams['font.sans-serif'] = 'Arial'
mpl.rcParams['pdf.fonttype'] = 42


def change_tick_style(style):
    if style == 'classic':
        mpl.rcParams['xtick.direction'] = 'in'
        mpl.rcParams['ytick.direction'] = 'in'
        mpl.rcParams['xtick.top'] = True
        mpl.rcParams['ytick.right'] = True
    else:
        mpl.rcParams['xtick.direction'] = 'out'
        mpl.rcParams['ytick.direction'] = 'out'
        mpl.rcParams['xtick.top'] = False
        mpl.rcParams['ytick.right'] = False
