import argparse
import matplotlib
import matplotlib.pyplot as plt


# -----------------------------------------------------------------------------
# matplotlib options
# -----------------------------------------------------------------------------
matplotlib.rcParams.update({'text.usetex': True})
matplotlib.rc('text.latex', preamble=r"\usepackage{amsmath}  \usepackage{xcolor}")


# -----------------------------------------------------------------------------
# functions
# -----------------------------------------------------------------------------
def to_pdf(tex, filename='math.pdf'):
    """Compiles a LaTeX math command to a pdf through matplotlib.pyplot.

    Parameters
    ----------
    tex: str
        Math symbol written in latex.  It will be assumed that everything
        in this string is already in math mode.
    
    filename: str, optional
        filename of the compiled output.
    """
    fig = plt.figure()
    
    # insert tex con figure
    dpi = fig.get_dpi()
    renderer = fig.canvas.get_renderer()
    text = fig.text(0, 0, f'$\\displaystyle \\textcolor{{white}}{{.}}{tex}$',
        va='bottom', ha='left', bbox={'facecolor':'red', 'alpha':0.0})
    
    # setup a box
    bbox = text.get_window_extent(renderer=renderer)
    x0, y0, x1, y1 = bbox.x0, bbox.y0, bbox.x1, bbox.y1
    
    # resize figure
    fig.set_size_inches(1.1*x1/float(dpi), 2*y1/float(dpi))
    
    # save and close figure
    fig.savefig(filename)
    plt.close(fig)
