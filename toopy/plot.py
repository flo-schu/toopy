import numpy as np
from matplotlib.ticker import Formatter, FixedLocator
from datetime import timedelta
from matplotlib.dates import num2date, datestr2num, drange
import numpy as np
from matplotlib import transforms
from matplotlib import ticker
from matplotlib.patches import Rectangle
from copy import copy

def create_axes(gs, fig, ncol, nrow, rstart=0, cstart=0):
    """
    this function creates axes in some area of the gridspec. It is useful
    if the the figure consits of many panels and it has to be subdivided
    into subfigures without using subfigure. It returns np.arrays of the 
    figures that are consistend with pyplot 2-D subplots
    see https://gist.githubusercontent.com/flo-schu/1e2a87f9cfa217ce488dabba2597f027/raw/175897dbae07187ca88328fd36d77d4bc76d90aa/multipanel_figure.py

    for an implementation example
    """
    axes = np.empty((nrow,ncol), dtype=object)
    for ci, c in enumerate(range(cstart, ncol+cstart)):
        for ri, r in enumerate(range(rstart, nrow+rstart)):
            axes[ri, ci] = fig.add_subplot(gs[r,c])
    
    return axes


class Date2DaysFormatter(Formatter):
    """
    provide origin of axis as a date in the form of 'YYYY-MM-DD'
    """
    def __init__(self, origin):
        self.origin = datestr2num(origin)

    def __call__(self, x, _):
        """Return the label for time x at position pos."""
        return str(int(x - self.origin))


# on axis of a plot use like this:
def interval_locator(
    ax, 
    interval=timedelta(days=7), 
    start=None, 
    end=None
):
    xl, xu = ax.get_xlim()
    
    if start is not None:
        start = datestr2num(start)
    else:
        start = xl

    if end is not None:
        end = datestr2num(end)
    else:
        end = xu

    locs = drange(dstart=num2date(start), dend=num2date(end), delta=interval)
    return FixedLocator(locs)
    



def replace_pos_with_label(pos, label, axis):
    fig = axis.figure
    fig.canvas.draw()  # this is needed to set up the x-ticks
    labs = axis.get_xticklabels()
    labels = []
    locs = []
    for text in labs:
        x = text._x
        lab = text._text

        if x == pos:
            lab = label

        labels.append(lab)
        locs.append(x)

    axis.xaxis.set_major_locator(ticker.FixedLocator(locs))
    axis.set_xticklabels(labels)

def line_break(line, break_from=0.0002, break_until=0.002, 
    break_width=0.1, slant=1.5, plot_line_break=True):
    assert isinstance(line, list), "line must be a list, just use the output of plt.plot(...)"
    axis = line[0]._axes
    fig = axis.figure

    ymin_orig, _ = copy(axis.get_xlim())

    for l in line:
        x = l.get_xdata()
        before = np.where(x < break_from)[0]
        after = np.where(x >= break_until)[0]
        x_before_break = x[before]
        x_after_break = x[after]

        x_min_new = 10 ** np.round(np.log10(x_after_break[0] / 2))
        x_max_new = x_after_break[0]
        x_new_before_break = np.linspace(
            x_min_new, x_max_new, len(x_before_break))

        y = l.get_ydata()
        y_before_break = y[before]
        y_after_break = y[after]

        l.set_xdata(np.concatenate([x_new_before_break, x_after_break]))
        l.set_ydata(np.concatenate([y_before_break, y_after_break]))

        # line_props = dict(
        #     color=l.get_color(),
        #     linestyle=l.get_linestyle(),
        #     alpha=l.get_alpha()
        # )
        # l.remove()
        # lbb = axis.plot(x_new_before_break, y_before_break, **line_props)
        # lab = axis.plot(x_after_break, y_after_break, **line_props)
        if plot_line_break:
            line_break_xl = break_until * 0.9
            line_break_xr = break_until * 1.1
            line_break_width = line_break_xr - line_break_xl

            line_break_yl = y_before_break[-1] * 0.9
            line_break_yu = y_after_break[0] * 1.1
            line_break_height = line_break_yu - line_break_yl

            # add line break
            axis.add_patch(Rectangle(
                xy=(line_break_xl, line_break_yl), 
                width=line_break_width, 
                height=line_break_height, 
                fill=True, color="white",
                clip_on=False, zorder=3)
            )
            _ = axis.vlines(
                [line_break_xl, line_break_xr], line_break_yl, line_break_yu,
                linewidth=.5, 
                color="black", zorder=3.1)

    ymin_new, _ = axis.get_xlim()
    replace_pos_with_label(pos=ymin_new, label=0.0, axis=axis)

    # add axis break
    # transform uses real x coordinates and axis-fractional y-coordinates
    trans = transforms.blended_transform_factory(
        axis.transData, axis.transAxes)

    # draw white box over x-axis spine
    _ = axis.add_patch(Rectangle(
        xy=(break_until * 0.9, -0.05), 
        width=break_until * 0.2, 
        height=0.1, 
        fill=True, color="white",
        transform=trans,
        clip_on=False, zorder=3)
    )
    
    # draw black bars
    _ = axis.vlines(
        [break_until*0.9, break_until*1.1], -0.025, 0.025,
        transform=trans, linewidth=.5,
        color="black", zorder=3.1, clip_on=False)
