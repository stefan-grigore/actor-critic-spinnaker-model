"""
Plotting dataframe data with seaborn and pandas
"""
import itertools
import pandas as pd
import seaborn as sns
from .base import plotting_base


def pivot_timeseries(df, var_name, timezone=None):
    sns_df = []
    for name, col in df.iteritems():
        col = col.to_frame()
        col.columns = [var_name]
        col['source'] = name
        col['year'] = col.index.year
        col['month'] = col.index.month
        col['hour'] = col.index.hour
        if timezone is not None:
            td = pd.to_timedelta('{:}h'.format(timezone))
            col['local_hour'] = (col.index + td).hour

        sns_df.append(col)

    return pd.concat(sns_df)


def pivot_df(df, var_name):
    sns_df = []
    for name, col in df.iteritems():
        col = col.to_frame()
        col.columns = [var_name]
        col['source'] = name
        sns_df.append(col)

    return pd.concat(sns_df)


def box_plot(df, **kwargs):
    def plot_func(axis, df, **kwargs):
        meanprops = dict(marker='o', markeredgecolor='black',
                         markerfacecolor="None", markersize=5)
        sns.boxplot(data=df, ax=axis, meanprops=meanprops, **kwargs)

    plotting_base(plot_func, df, **kwargs)


def dist_plot(df, **kwargs):
    def plot_func(axis, df, **kwargs):
        fit = kwargs.get('fit', None)
        palette = itertools.cycle(sns.color_palette())
        if isinstance(df, pd.DataFrame):
            for label, series in df. iteritems():
                if fit is not None:
                    sns.distplot(series, kde=False,
                                 fit_kws={"color": next(palette)},
                                 label=label, **kwargs)
                else:
                    sns.distplot(series, label=label, **kwargs)
        else:
            if fit is not None:
                sns.distplot(df, kde=False,
                             fit_kws={"color": next(palette)},
                             **kwargs)
            else:
                sns.distplot(df, **kwargs)

    plotting_base(plot_func, df, **kwargs)


def point_plot(df, **kwargs):
    def plot_func(axis, df, **kwargs):
        sns.pointplot(data=df, ax=axis, **kwargs)

    plotting_base(plot_func, df, **kwargs)


def bar_plot(df, **kwargs):
    def plot_func(axis, df, **kwargs):
        sns.barplot(data=df, ax=axis, **kwargs)

    plotting_base(plot_func, df, **kwargs)


def df_line_plot(df, **kwargs):
    def plot_func(axis, df, **kwargs):
        df.plot(ax=axis, **kwargs)

    plotting_base(plot_func, df, **kwargs)


def df_error_plot(df, error, **kwargs):
    def plot_func(axis, df, error, **kwargs):
        error.columns = df.columns
        error.index = df.index
        df.plot(yerr=error, ax=axis, **kwargs)

    plotting_base(plot_func, df, error, **kwargs)
