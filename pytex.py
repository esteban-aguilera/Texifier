"""Example of how to use this file:
python compile_math.py 'example.tex'
"""

import argparse
import os
import sys

# package import
from texifier import utils
from texifier import texifier


# --------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Compile LaTeX file with custom Python macros')
    parser.add_argument('input', default='', action='store',
                        help='filename of the document to preprocess.')
    parser.add_argument('--macros', default='macros', action='store',
                        help='filename with the Python macros for LaTeX.')
    parser.add_argument('--output', default='pymain.tex', action='store',
                        help='filename of the preprocessed document.')
    parser.add_argument('--pdf', default='pymain.pdf', action='store',
                        help='filename of the preprocessed document.')
    parser.add_argument('--bib', default='bibliography.bib', action='store',
                        help='filename of the bibliography')
    parser.add_argument('--build', default='build', action='store',
                        help='directory used to store the build output files')
    parser.add_argument('-b', '--block_terminal', default=False, action='store_true',
                        help='latex compiler will now show output')
    parser.add_argument('-c', '--compile', default=False, action='store_true',
                        help='compiles the generated tex file.')
    parser.add_argument('-o', '--open', default=False, action='store_true',
                        help='opens built pdf file in default\'s browser')
    args = parser.parse_args()

    if(args.input == ''):
        raise Exception('input filename must be specified.')

    with open(args.input) as f:
        line = ''
        while('\\documentclass' not in line):
            line = f.readline()
            if('!TeX root' in line):
                args.output = line[line.find('=')+1:-1].replace(' ', '')

    if(args.output == 'pymain.tex'):
        args.output = f'main/{args.input[:-4]}.tex'

    if(args.pdf == 'pymain.pdf'):
        args.pdf = f'{args.input[:-4]}.pdf'
    

    # append working directory to path
    sys.path.append(os.getcwd())

    # format tex with the Python macros.
    texifier.format_tex(args.input, args.output, __import__(args.macros))

    # compile latex
    if(args.compile is True):
        texifier.build_pdf(args.input, args.output, args.pdf,
            build=args.build, block_terminal=args.block_terminal)

    # open pdf
    if(args.open is True):
        os.system(f'xdg-open \'{args.pdf}\'')


# --------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------
if __name__ == '__main__':
    utils.mkdir('img')
    utils.mkdir('build')
    utils.mkdir('main')
    main()
