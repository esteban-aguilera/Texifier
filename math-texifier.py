import argparse
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'text.usetex': True})
matplotlib.rc('text.latex', preamble=r"\usepackage{amsmath}  \usepackage{xcolor}")


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('tex', default='', action='store',
                        help='filename used to store the build output file.')
    parser.add_argument('-f', '--filename', default='math', action='store',
                        help='filename used to store the build output file.')

    args = parser.parse_args()

    # check args
    if(args.tex == ''):
        raise ValueError('argument is missing.')

    fig = plt.figure()

    dpi = fig.get_dpi()
    renderer = fig.canvas.get_renderer()
    text = fig.text(0, 0, f'$\\displaystyle \\textcolor{{white}}{{.}}{args.tex}$', va='bottom', ha='left',
        bbox=dict(facecolor='red', alpha=0.0))

    bbox = text.get_window_extent(renderer=renderer)
    x0, y0, x1, y1 = bbox.x0, bbox.y0, bbox.x1, bbox.y1

    fig.set_size_inches(1.1*x1/float(dpi), 2*y1/float(dpi))

    fig.savefig(f'{args.filename}.pdf')

    plt.close(fig)


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
