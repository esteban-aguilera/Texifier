import argparse
import os
import pathlib
import string
import sys

# package imports
from .utils import mkdir, find_closing_parentheses, find_opening_parentheses, \
    find_all, check_parentheses


# --------------------------------------------------------------------------------
# builder
# --------------------------------------------------------------------------------
def build_pdf(input, output, pdf, build='build', block_terminal=False):
    options =  '-pdf '
    options += '-interaction=nonstopmode '
    options += '-synctex=1 '
    options += '-file-line-error '
    if(type(build) == str and build not in ['']):
        options += f'--output-directory=\"{build}\" '

    sufix = ''
    if(block_terminal is True):
        sufix += '>/dev/null 2>&1'

    mkdir(build)

    # compile latex
    os.system(f'latexmk {options} {output} {sufix}')
    os.system(f'latexmk {options} {output} >/dev/null 2>&1')
    
    print(f'cp \'{build}/{pdf}\' \'{pdf}\'')
    os.system(f'cp \'{build}/{pdf}\' \'{pdf}\'')


# --------------------------------------------------------------------------------
# formatter
# --------------------------------------------------------------------------------
def format_tex(input, output, macros_module):
    oldmacros = ''
    macros = [macro for macro in dir(macros_module) if '__' not in macro]
    for macro in macros:
        oldmacros += f'\\ifdefined\\{macro}\\let\\old{macro}\\{macro}\\fi \n'
    oldmacros += 4 * '\n'

    f = open(f'{input}', 'r')
    tex = f.read()
    f.close()

    check_parentheses(tex)
    tex = format_macros(tex, macros_module)
    tex = append_subfiles(tex, macros_module)

    ii = tex.find('\\begin{document}')
    tex = tex[tex.find('\\documentclass'):ii] + oldmacros + tex[ii:]

    if('/' in output):
        outdir = output.split('/')
        for i in range(len(outdir)):
            mkdir('/'.join(outdir[:i]))

    with open(f'{output}', 'w+') as main:
        main.write(tex)


def format_macros(text, macros_module):
    macros = [macro for macro in dir(macros_module) if '__' not in macro]
    for macro in macros:
        func = getattr(macros_module, macro)

        ii, jj, kk = 0, 0, 0
        while(ii < len(text)):
            ii = text.find(f'\\{macro}', kk)  # macro's first char.
            if(ii == -1):
                break

            jj = ii + len(macro) + 1  # first char after macro's tag.
            kk = jj - 1 # macro's last char, variables included.

            args = ()
            get_more_parameters = True
            while(get_more_parameters is True):
                if(text[jj] in string.ascii_letters and args == ()):
                    get_more_parameters = False  # macro with no arguments
                elif(text[jj] == '['):
                    kk = jj+find_closing_parentheses(text[jj:], '[]')
                    if(kk == -1):
                        raise ValueError(f'{macro} did not close parentheses ].')
                    args += (text[jj+1:kk],)
                elif(text[jj] == '{'):
                    kk = jj+find_closing_parentheses(text[jj:], '{}')
                    if(kk == -1):
                        raise ValueError(f'{macro} did not close parentheses }}.')
                    args += (text[jj+1:kk],)
                else:
                    new_text = func(*args)
                    if(new_text is None):
                        nline = text[:ii].count('\n') + 1
                        raise ValueError(f'\n\n\t\tWrong number of variables in \\{func.__name__} of line {nline}\n')
                    else:
                        new_text = format_macros(new_text, macros_module)
                        text = text[:ii] + new_text + text[kk+1:]
                        get_more_parameters = False

                jj = kk + 1
            
            kk = ii + len(macro) + 1
            
    return text


def append_subfiles(text, macros_module):
    i, j, k = 0, 0, 0
    length = len(f'\\subfile')

    while(i < len(text)):
        i = text.find(f'\\subfile', k+1)

        if(i == -1):
            break
        else:
            j = i + length
            if(text[j] in ['{', '[']):
                k = j+find_closing_parentheses(text[j:], '{}')
                filename = text[j+1:k]

                print(f'{filename}.tex')
                with open(f'{filename}.tex', 'r') as f:
                    new_text = f.read()
                
                check_parentheses(new_text)
                new_text = format_macros(new_text, macros_module)
                text = text[:i] + new_text + text[k+1:]

    return text
