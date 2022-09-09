import numpy as np

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
