"""
Plotting of 3D arrays in 2D plots
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import numpy.ma as ma


def add_colorbar(axis, cf, ticks, size, padding,
                 location='right', label=None, lines=None, fontsize=14):
    divider = make_axes_locatable(axis)

    caxis = divider.append_axes(location, size=size,
                                pad=padding)

    if location in ['top', 'bottom']:
        orientation = 'horizontal'
    else:
        orientation = 'vertical'

    cbar = plt.colorbar(cf, ticks=ticks, cax=caxis,
                        orientation=orientation,
                        ticklocation=location)

    cbar.ax.tick_params(labelsize=fontsize - 2)

    if label is not None:
        cbar.set_label(label, size=fontsize)

    if lines is not None:
        cbar.add_lines(lines)


def contour_plot(axis, data, **kwargs):
    def plot_func(data, figsize, fontsize, zlim=None, major_spacing=None,
                  minor_spacing=None, contour_width=1, contour_color='k',
                  opacity=1., colorbar_on=True, colorbar_location='right',
                  colorbar_label=None, colorbar_lines=True,
                  colorbar_ticks=None, colormap='jet', **kwargs):
        assert len(data) == 3, 'Data must equal (x, y, data)'

        x, y, z = data
        z_m = ma.masked_invalid(z)

        a_ratio = z.shape
        a_ratio = a_ratio[1] / a_ratio[0]

        if isinstance(figsize, (int, float)):
            figsize = [figsize * a_ratio, figsize]
        else:
            figsize = max(figsize)
            figsize = [figsize * a_ratio, figsize]

        if zlim is None:
            zmin, zmax = np.nanmin(z), np.nanmax(z)
        else:
            zmin, zmax = zlim

        if major_spacing is None:
            major_spacing = (zmax - zmin) / 10
        if minor_spacing is None:
            minor_spacing = major_spacing / 10

        cl_levels = np.arange(zmin, zmax + major_spacing, major_spacing)
        cf_levels = np.arange(zmin, zmax + minor_spacing, minor_spacing)

        if colorbar_ticks is None:
            l_levels = cl_levels[::2]
        else:
            l_levels = (zmax - zmin) / colorbar_ticks
            l_levels = np.arange(zmin, zmax + l_levels, l_levels)

        orientation = 'vertical'
        if colorbar_location in ['top', 'bottom']:
            orientation = 'horizontal'

        cf = plt.contourf(x, y, z_m, alpha=opacity, levels=cf_levels,
                          extend='both', antialiased=True)

        if contour_color is not None:
            cl = plt.contour(cf, levels=cl_levels, colors=(contour_color,),
                             linewidths=(contour_width,))

        if colormap is not None:
            cf.set_cmap(colormap)

        if colorbar:
            cbar_padding = 0.1
            if colorbar_location in ['top', 'bottom']:
                figsize[1] += figsize[1] / 10
                cbar_size = figsize[0] / 20
            else:
                figsize[0] += figsize[0] / 10
                cbar_size = figsize[1] / 20

            divider = make_axes_locatable(axis)

            caxis = divider.append_axes(colorbar_location, size=cbar_size,
                                        pad=cbar_padding)

            cbar = plt.colorbar(cf, ticks=l_levels, cax=caxis,
                                orientation=orientation,
                                ticklocation=colorbar_location)

            cbar.ax.tick_params(labelsize=fontsize - 2)

            if colorbar_label is not None:
                cbar.set_label(colorbar_label, size=fontsize)

            if colorbar_lines is not None:
                if contour_color is not None:
                    cbar.add_lines(cl)


def colorbar(zlim, ticks=None, lines=None, line_color='k', linewidth=1,
             colormap='jet', extend='neither', ticklocation='right',
             fontsize_other=18, label=None, fontsize_label=21, figsize=6,
             dpi=100, showfig=True, filename=None):

    """
    Parameters
    ----------
    zlim : 'tuple'
        List or tuple indicating zmin and zmax.
    tick : 'Int'
        Number of ticks to label.
    lines : 'Int'
        Number of lines to draw on colorbar.
    line_color : 'String'
        Color of lines drawn on colorbar.
    linewidth : 'Int'
        Line width for each line drawn on colorbar.
    colormap : 'String'
        Color scheme for colorbar.
    extend : 'String'
        Direction to extend colors beyond zmin and zmax.
    ticklocation : 'String'
        Orientation of colorbar and location of tick marks.
    fontsize_other : 'Int'
        Font size of tick numbers.
    label : 'String'
        Label for colorbar
    fontsize_label : 'Int'
        Font size of label.
    figsize : 'Tuple', default = '(8,6)'
        Width and height of figure
    dpi : 'Int', default = '300'
        DPI resolution of figure.
    showfig : 'Bool', default = 'True'
        Whether to show figure.
    filename : 'String', default = None.
        Name of file/path to save the figure to.

    Returns
    -------
    Plot custom colorbar
    """

    a_ratio = 20

    if isinstance(figsize, (list, tuple)):
        figsize = max(figsize)

    if ticklocation in ['right', 'left']:
        figsize = (figsize / a_ratio, figsize)
        orientation = 'vertical'
    else:
        figsize = (figsize, figsize / a_ratio)
        orientation = 'horizontal'

    if ticks is not None:
        ticks = (zlim[1] - zlim[0]) / ticks
        ticks = np.arange(zlim[0], zlim[1] + ticks, ticks)

    fig = plt.figure(figsize=figsize, dpi=dpi)
    axis = fig.add_axes([0.0, 0.0, 1.0, 1.0])

    norm = mpl.colors.Normalize(vmin=zlim[0], vmax=zlim[1])

    cb = mpl.colorbar.ColorbarBase(axis, cmap=colormap, norm=norm,
                                   orientation=orientation, extend=extend,
                                   ticks=ticks, ticklocation=ticklocation)
    cb.ax.tick_params(labelsize=fontsize_other)

    if label is not None:
        cb.set_label(label, size=fontsize_label)

    if lines is not None:
        lines = (zlim[1] - zlim[0]) / lines
        lines = np.arange(zlim[0], zlim[1] + lines, lines)
        cb.add_lines(lines, colors=(line_color,) * len(lines),
                     linewidths=(linewidth,) * len(lines))

    if filename is not None:
        plt.savefig(filename, dpi=dpi, transparent=True,
                    bbox_inches='tight')

    if showfig:
        plt.show()

    plt.close()
