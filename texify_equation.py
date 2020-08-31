"""Example of how to use this file:
python compile_math.py 'ax^2 + bx + c'
"""

import argparse

# package import
from texifier import equation


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('tex', default='', action='store',
                        help='filename used to store the build output file.')
    parser.add_argument('-f', '--filename', default='math.pdf', action='store',
                        help='filename used to store the build output file.')

    args = parser.parse_args()

    equation.to_pdf(args.tex, filename=args.filename)


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
