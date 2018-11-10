"""
Line plots in matplotlib
"""
import itertools
import matplotlib.pyplot as plt
import numpy as np
from .base import plotting_base

COLORS = {
    "red": (0.7176, 0.1098, 0.1098),
    "green": (0.65 * 0.298, 0.65 * 0.6863, 0.65 * 0.3137),
    "blue": (0.9 * 0.0824, 0.9 * 0.3961, 0.9 * 0.7529),
    "orange": (0.85 * 1.0, 0.85 * 0.5961, 0.0),
    "purple": (0.49412, 0.3412, 0.7608),
    "grey": (0.45, 0.45, 0.45),
    "cyan": (0.0, 0.7373, 0.8314),
    "teal": (0.0, 0.5882, 0.5333),
    "lime": (0.8039, 0.8627, 0.2235),
    "brown": (0.4745, 0.3333, 0.2824),
    "black": (0.0, 0.0, 0.0)
}


def get_COLORS(colors, n=None):
    """
    Parameters
    ----------
    colors : 'list'
        List of strings of color names
    n : 'int'
        repeat each color in colors n times
    Returns
    -------
    RGB color codes for plotting functions
    """
    if n is not None:
        colors = np.asarray([[color, ] * n for color in colors]).flatten()

    return [COLORS[color] for color in colors]


def_linestyles = ('-', '--', '-.', ':')
def_markers = (u'o', u'v', u'^', u'<', u'>', u'8', u's', u'p', u'*', u'h',
               u'H', u'D', u'd')


def riffle_lines(*args):
    """
    Parameters
    ----------
    *args : 'Tuple'
        set of lists to be riffled together
    Returns
    -------
    Flattened list of lists such that entries are riffled
    """
    return [item for sublist in zip(*args) for item in sublist]


def get_line_styles(colors=None, linestyles=None, markers=None):
    if colors is not None:
        colors = itertools.cycle(colors)
    else:
        colors = itertools.cycle((COLORS["blue"],
                                  COLORS["green"],
                                  COLORS["red"],
                                  COLORS["orange"],
                                  COLORS["purple"],
                                  COLORS["grey"],
                                  COLORS["cyan"],
                                  COLORS["teal"],
                                  COLORS["lime"],
                                  COLORS["brown"]))

    if linestyles is None:
        linestyles = itertools.cycle(('',))
    elif linestyles == 'Automatic':
        linestyles = itertools.cycle(def_linestyles)
    else:
        linestyles = itertools.cycle(linestyles)

    if markers is None:
        markers = itertools.cycle(('',))
    elif markers == 'Automatic':
        markers = itertools.cycle(def_markers)
    else:
        markers = itertools.cycle(markers)

    return colors, linestyles, markers


def line_plot(*lines, legend=None, **kwargs):
    """
    Parameters
    ----------
    *lines : 'ndarray', shape(line) = (n,2)
        each line in lines must be a nx2 array or nx2 list
    colors : 'ndarray'
        Iterable list of colors to plot for each line in 'data'.
        Will be cycled if fewer entries are specified than the number of lines
        in 'data'.
    linestyles : 'ndarray'
        Iterable list of Matplotlib designations for the linestyle for each
        line in 'data'.
        Will be cycled if fewer entries are specified than the number of lines
        in 'data'.
    linewidth : 'Int'
        Line width for each line in 'data'.
    markersize : 'Float'
        Marker size for each marker in 'data'.
    markeredge : 'list'
        [marker edge color, marker edge width]
    markers : 'ndarray'
        Iterable list of Matplotlib designations for the marker for each line
        in 'data'.
        Will be cycled if fewer entries are specified than the number of lines
        in 'data'.
    """

    def plot_func(axis, *lines,
                  colors=None, linestyles='Automatic', linewidth=2,
                  markers=None, markersize=5, markeredge=['k', 0.5], **kwargs):

        colors, linestyles, markers = get_line_styles(colors=colors,
                                                      linestyles=linestyles,
                                                      markers=markers)

        if markeredge is not None:
            mec, mew = markeredge
        else:
            mec = None
            mew = None

        for line in lines:
            if not isinstance(line, np.ndarray):
                line = np.array(line)

            axis.plot(line[:, 0], line[:, 1],
                      markersize=markersize, marker=next(markers),
                      mec=mec, mew=mew, color=next(colors),
                      linestyle=next(linestyles), linewidth=linewidth)

    plotting_base(plot_func, *lines, legend=legend, **kwargs)


def error_plot(data, legend=None, **kwargs):
    """
    Parameters
    ----------
    data : 'ndarray', shape(data[i]) = (n,2)
        Either a tuple or list of nx2 arrays or a single nx2 array.
    colors : 'ndarray'
        Iterable list of colors to plot for each line in 'data'.
        Will be cycled if fewer entries are specified than the number of lines
        in 'data'.
    linestyles : 'ndarray'
        Iterable list of Matplotlib designations for the linestyle for each
        line in 'data'.
        Will be cycled if fewer entries are specified than the number of lines
        in 'data'.
    linewidth : 'Int'
        Line width for each line in 'data'.
    markersize : 'Float'
        Marker size for each marker in 'data'.
    markeredge : 'list'
        [marker edge color, marker edge width]
    markers : 'ndarray'
        Iterable list of Matplotlib designations for the marker for each line
        in 'data'.
        Will be cycled if fewer entries are specified than the number of lines
        in 'data'.
    """

    def plot_func(axis, data_error,
                  colors=None, linestyles='Automatic', linewidth=2, capsize=6,
                  markers=None, markersize=5, markeredge=['k', 0.5], **kwargs):
        assert isinstance(data_error, (list, tuple)), 'Input data needs to be in \
    (data, error) pairs'

        colors, linestyles, markers = get_line_styles(colors=colors,
                                                      linestyles=linestyles,
                                                      markers=markers)

        if markeredge is not None:
            mec, mew = markeredge
        else:
            mec = None
            mew = None

        for data, error in data_error:
            x = data[:, 0]
            x_error = error[:, 0]
            if np.isnan(x_error).all():
                x_error = None

            y = data[:, 1]
            y_error = error[:, 1]
            if np.isnan(y_error).all():
                y_error = None

            axis.errorbar(x, y, xerr=x_error, yerr=y_error,
                          linewidth=linewidth, markersize=markersize,
                          marker=next(markers), color=next(colors),
                          linestyle=next(linestyles), mec=mec, mew=mew,
                          capsize=capsize, capthick=linewidth)

    plotting_base(plot_func, data, legend=legend, **kwargs)


def dual_plot(data1, data2,
              xlabel=None, ylabel=None, xlim=None, ylim=None,
              xticks=None, yticks=None, ticksize=(6, 1),
              xtick_labels=None, ytick_labels=None, axis_colors='k',
              colors=None, linestyles='Automatic', linewidth=1,
              markers=None, markersize=5, markeredge=['k', 0.5],
              fontsize=16, borderwidth=1, title=None,
              legend=None, figsize=(6, 5), dpi=100, filename=None):
    """

    Parameters
    ----------
    data1 : 'ndarray', shape(data2[i]) = (n,2)
        Either a tuple or list of nx2 arrays or a single nx2 array.
    data2 : 'ndarray', shape(data2[i]) = (n,2)
        Either a tuple or list of nx2 arrays or a single nx2 array.
    xlabel : 'String'
        Label for x-axis.
    ylabel : 'String'
        Label for y-axis.
    xlim : 'tuple', len(xlim) == 2
        Upper and lower limits for the x-axis.
    ylim : 'tuple', len(ylim) == 2
        Upper and lower limits for the y-axis.
    xticks : 'ndarray'
        List of ticks to use on the x-axis. Should be within the bounds set by
        xlim.
    yticks : 'ndarray'
        List of ticks to use on the y-axis. Should be within the bound set by
        ylim.
    ticksize : 'ndarray', default '[8,2]'
        Length and width of ticks.
    xtick_labels : 'list'
        List of custome xticks. Note len(xticks) == len(xtick_labels)
    ytick_labels : 'list'
        List of custome yticks. Note len(yticks) == len(ytick_labels)
    axis_colors : 'string', 'tuple'
        string indicating y-axis colors, tuple of strings indicates color of
        each y-axis
    colors : 'ndarray'
        Iterable list of colors to plot for each line in 'data'.
        Will be cycled if fewer entries are specified than the number of lines
        in 'data'.
    linestyles : 'ndarray'
        Iterable list of Matplotlib designations for the linestyle for each
        line in 'data'. Will be cycled if fewer entries are specified than the
        number of lines in 'data'.
    linewidth : 'Int'
        Line width for each line in 'data'.
    markersize : 'Float'
        Marker size for each marker in 'data'.
    markeredge : 'list'
        [marker edge color, marker edge width]
    markers : 'ndarray'
        Iterable list of Matplotlib designations for the marker for each line
        in 'data'.
        Will be cycled if fewer entries are specified than the number of lines
        in 'data'.
    fontsize : 'Int'
        Font size to be used for axes labels.
    boarderwidth : 'Int'
        Linewidth of plot frame
    add_legend : 'Bool', default = 'False'
        If 'True' a legend will be added at 'legendlocation'.
    figsize : 'Tuple', default = '(8,6)'
        Width and height of figure
    dpi : 'Int', default = '300'
        DPI resolution of figure.
    filename : 'String', default = None.
        Name of file/path to save the figure to.
    """
    if not isinstance(data1, (list, tuple)):
        lines1 = (data1,)
    else:
        lines1 = data1

    if not isinstance(data2, (list, tuple)):
        lines2 = (data2,)
    else:
        lines2 = data2

    if colors is not None:
        if isinstance(colors[0], list):
            colors1 = itertools.cycle(colors[0])
            colors2 = itertools.cycle(colors[1])
        else:
            colors1 = itertools.cycle(colors[::2])
            colors2 = itertools.cycle(colors[1::2])
    else:
        colors1 = itertools.cycle((COLORS["blue"],
                                  COLORS["red"],
                                  COLORS["purple"],
                                  COLORS["cyan"],
                                  COLORS["lime"]))

        colors2 = itertools.cycle((COLORS["green"],
                                  COLORS["orange"],
                                  COLORS["grey"],
                                  COLORS["teal"],
                                  COLORS["brown"]))

    if linestyles is None:
        linestyles1 = itertools.cycle(('',))
        linestyles2 = itertools.cycle(('',))
    elif linestyles == 'Automatic':
        linestyles1 = itertools.cycle(def_linestyles[::2])
        linestyles2 = itertools.cycle(def_linestyles[1::2])
    else:
        if isinstance(linestyles[0], (list, tuple)):
            linestyles1 = itertools.cycle(linestyles[0])
            linestyles2 = itertools.cycle(linestyles[1])
        else:
            linestyles1 = itertools.cycle(linestyles[::2])
            linestyles2 = itertools.cycle(linestyles[1::2])

    if markers is None:
        markers1 = itertools.cycle(('',))
        markers2 = itertools.cycle(('',))
    elif markers == 'Automatic':
        markers1 = itertools.cycle(def_markers[::2])
        markers2 = itertools.cycle(def_markers[1::2])
    else:
        if isinstance(markers[0], (list, tuple)):
            markers1 = itertools.cycle(markers[0])
            markers2 = itertools.cycle(markers[1])
        else:
            markers1 = itertools.cycle(markers[::2])
            markers2 = itertools.cycle(markers[1::2])

    if len(axis_colors) == 1:
        axis_color1 = axis_colors
        axis_color2 = axis_colors
    else:
        axis_color1 = axis_colors[0]
        axis_color2 = axis_colors[1]

    if markeredge is not None:
        mec, mew = markeredge
    else:
        mec = None
        mew = None

    fig = plt.figure(figsize=figsize, dpi=dpi)
    axis1 = fig.add_subplot(111)

    if title is not None:
        axis1.set_title(title, fontsize=fontsize + 2)

    for line in lines1:
        axis1.plot(line[:, 0], line[:, 1], linewidth=linewidth,
                   markersize=markersize, marker=next(markers1),
                   color=next(colors1), linestyle=next(linestyles1),
                   mec=mec, mew=mew)

    axis2 = axis1.twinx()

    for line in lines2:
        axis2.plot(line[:, 0], line[:, 1], linewidth=linewidth,
                   markersize=markersize, marker=next(markers2),
                   color=next(colors2), linestyle=next(linestyles2),
                   mec=mec, mew=mew)

    # update plot labels and format based on user input
    for ax in ['top', 'bottom', 'left', 'right']:
        axis1.spines[ax].set_linewidth(borderwidth)
        axis2.spines[ax].set_linewidth(borderwidth)

    if xlabel is not None:
        axis1.set_xlabel(xlabel, fontsize=fontsize)

    if ylabel is not None:
        if len(ylabel) == 1:
            axis1.set_ylabel(ylabel, fontsize=fontsize, color=axis_color1)
            axis2.set_ylabel(ylabel, fontsize=fontsize, color=axis_color2)
        else:
            axis1.set_ylabel(ylabel[0], fontsize=fontsize,
                             color=axis_color1)
            axis2.set_ylabel(ylabel[1], fontsize=fontsize,
                             color=axis_color2)

    if xlim is not None:
        axis1.set_xlim(xlim)

    if ylim is not None:
        if len(np.asarray(ylim).shape) == 1:
            axis1.set_ylim(ylim)
            axis2.set_ylim(ylim)
        else:
            axis1.set_ylim(ylim[0])
            axis2.set_ylim(ylim[1])

    if xticks is not None:
        axis1.set_xticks(xticks)
        if xtick_labels is not None:
            axis1.set_xticklabels(xtick_labels)

    if yticks is not None:
        if len(np.asarray(yticks).shape) == 1:
            axis1.set_set_yticks(yticks)
            axis2.set_set_yticks(yticks)
        else:
            axis1.set_set_yticks(yticks[0])
            axis2.set_set_yticks(yticks[1])
        if ytick_labels is not None:
            if len(np.asarray(ytick_labels).shape) == 1:
                axis1.set_set_yticklabels(ytick_labels)
                axis2.set_set_yticklabels(ytick_labels)
            else:
                axis1.set_set_yticklabels(ytick_labels[0])
                axis2.set_set_yticklabels(ytick_labels[1])

    axis1.tick_params(axis='x', labelsize=fontsize - 2, width=ticksize[1],
                      length=ticksize[0], color='k')
    axis1.tick_params(axis='y', labelsize=fontsize - 2, width=ticksize[1],
                      length=ticksize[0], color=axis_color1)
    axis2.tick_params(axis='y', labelsize=fontsize - 2, width=ticksize[1],
                      length=ticksize[0], color=axis_color2)

    if len(axis_colors) == 2:
        for tl in axis1.get_yticklabels():
            tl.set_color(axis_colors[0])
        for t2 in axis2.get_yticklabels():
            t2.set_color(axis_colors[1])

    if legend:
        if isinstance(legend, list):
            plt.legend(legend, bbox_to_anchor=(1.05, 1), loc=2,
                       borderaxespad=0., prop={'size': fontsize - 2})
        else:
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2,
                       borderaxespad=0., prop={'size': fontsize - 2})

    fig.tight_layout()
    if filename is not None:
        plt.savefig(filename, dpi=dpi, transparent=True,
                    bbox_inches='tight')
    else:
        plt.show()

    plt.close()
