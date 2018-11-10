import matplotlib.pyplot as plt
import seaborn as sns


def plotting_base(plot_func, *args, despine=True, axes=True,
                  figsize=(6, 4), dpi=100, fontsize=14,
                  xlabel=None, ylabel=None, xlim=None, ylim=None,
                  xticks=None, yticks=None, ticksize=(6, 1),
                  xtick_rotation=None, ytick_rotation=None,
                  xtick_labels=None, ytick_labels=None, borderwidth=1,
                  title=None, legend=True, filename=None, showplot=True,
                  **kwargs):
    """
    Parameters
    ----------
    plot_func : 'function'
        Plotting function
    * args
        Args for plot_func
    despine : 'bool'
        Despine axis in seaborn
    axes : 'bool'
        Show axes, default=True
    figsize : 'Tuple', default = '(8,6)'
        Width and height of figure
    dpi : 'int', default = '100'
        DPI resolution of figure.
    fontsize : 'int'
        Font size to be used for axes labels, ticks will be 2 points smaller
    xlabel : 'str'
        Label for x-axis.
    ylabel : 'str'
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
    xtick_rotation : 'int'
        Degree to rotate xtick labels
    ytick_rotation : 'int'
        Degree to rotate ytick labels
    xtick_labels : 'list'
        List of custome xticks. Note len(xticks) == len(xtick_labels)
    ytick_labels : 'list'
        List of custome yticks. Note len(yticks) == len(ytick_labels)
    boarderwidth : 'int'
        Linewidth of plot frame
    title : 'str'
        Plot title
    legend : 'bool'|'list'
        If True, use df labels, or list of legend labels
    filename : 'str', default = None.
        Name of file/path to save the figure to
    showplot : 'bool'
        Display plot
    **kwargs
        kwargs for plot_func
    """
    fig = plt.figure(figsize=figsize, dpi=dpi)
    axis = fig.add_subplot(111)

    if legend is False:
        kwargs['legend'] = legend

    plot_func(axis, *args, **kwargs)

    if despine:
        sns.despine(offset=10, trim=False)

    if title is not None:
        axis.set_title(title, fontsize=fontsize + 2)

    if xlabel is not None:
        axis.set_xlabel(xlabel, fontsize=fontsize)
    else:
        axis.xaxis.label.set_size(fontsize)

    if ylabel is not None:
        axis.set_ylabel(ylabel, fontsize=fontsize)
    else:
        axis.yaxis.label.set_size(fontsize)

    if xlim is not None:
        axis.set_xlim(xlim)

    if ylim is not None:
        axis.set_ylim(ylim)

    axis.tick_params(axis='both', labelsize=fontsize - 2,
                     width=ticksize[1], length=ticksize[0])

    if xticks is not None:
        axis.set_xticks(xticks)
        if xtick_labels is not None:
            axis.set_xticklabels(xtick_labels)

    if xtick_rotation is not None:
        for tick in axis.get_xticklabels():
            tick.set_rotation(xtick_rotation)

    if yticks is not None:
        axis.set_yticks(yticks)
        if ytick_labels is not None:
            axis.set_yticklabels(ytick_labels)

    if ytick_rotation is not None:
        for tick in axis.get_yticklabels():
            tick.set_rotation(ytick_rotation)

    for ax in ['top', 'bottom', 'left', 'right']:
        axis.spines[ax].set_linewidth(borderwidth)

    if legend:
        if isinstance(legend, list):
            plt.legend(legend, bbox_to_anchor=(1.05, 1), loc=2,
                       borderaxespad=0., prop={'size': fontsize - 2})
        else:
            plt.legend(bbox_to_anchor=(1.05, 1), loc=2,
                       borderaxespad=0., prop={'size': fontsize - 2})

    if not axes:
        plt.axis('off')

    fig.tight_layout()
    if filename is not None:
        plt.savefig(filename, dpi=dpi, transparent=True,
                    bbox_inches='tight')

    if showplot:
        plt.show()

    plt.close()
