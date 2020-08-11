import argparse
import os
import pathlib
import string
import sys


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# main
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('input', default='', action='store',
                        help='filename of the document to preprocess.')
    parser.add_argument('--macros', default='macros', action='store',
                        help='filename of the document to preprocess.')
    parser.add_argument('--output', default='pymain.tex', action='store',
                        help='filename of the already preprocessed document.')
    parser.add_argument('--bib', default='bibliography.bib', action='store',
                        help='filename of the bibliography')
    parser.add_argument('--dir', default='build', action='store',
                        help='directory used to store the build output files')
    parser.add_argument('-b', '--block_terminal', default=False, action='store_true',
                        help='latex compiler will now show output')
    parser.add_argument('-c', '--compile', default=False, action='store_true',
                        help='compiles the generated tex file.')
    parser.add_argument('-o', '--open', default=False, action='store_true',
                        help='opens built pdf file in default\'s browser')
    args = parser.parse_args()

    if(args.input == ''):
        raise ValueError('\'input\' must be specified.')

    with open(args.input) as f:
        line = ''
        while('\\documentclass' not in line):
            line = f.readline()
            if('!TeX root' in line):
                args.output = line[line.find('=')+1:-1].replace(' ', '')

    if(args.output == 'pymain.tex'):
        args.output = f'main/{args.input[:-4]}.tex'

    kwargs = {
        'input':args.input,
        'output': args.output,
        'bib':args.bib,
        'dir':args.dir,
        'block_terminal':args.block_terminal,
        'compile':args.compile,
        'open':args.open
    }

    sys.path.append(os.getcwd())  # append to path the working directory
    format_tex(__import__(args.macros), **kwargs)
    if(args.compile is True):
        build_pdf(**kwargs)
    if(args.open is True):
        os.system(f'xdg-open \'{args.output[:-4]}.pdf\'')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# builder
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def build_pdf(**kwargs):
    input = kwargs.get('input')
    dir = kwargs.get('dir')
    output = kwargs.get('output')
    block_terminal = kwargs.get('block_terminal')

    options =  '-pdf '
    options += '-interaction=nonstopmode '
    options += '-synctex=1 '
    options += '-file-line-error '
    if(type(dir) == str and dir not in ['']):
        options += f'--output-directory=\"{dir}\" '

    sufix = ''
    if(block_terminal is True):
        sufix += '>/dev/null 2>&1'

    mkdir(dir)

    # compile latex
    os.system(f'latexmk {options} {output} {sufix}')
    os.system(f'latexmk {options} {output} >/dev/null 2>&1')
    
    filename = input[:-4].split('/')[-1]
    num = len('main/')
    os.system(f'cp \'{dir}/{output[num:-4]}.pdf\' \'{output[:-4]}.pdf\'')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# formatter
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def format_tex(macros_module, **kwargs):
    input = kwargs.get('input')
    output = kwargs.get('output')

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


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# utils
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def mkdir(dir):
    if(os.path.exists(dir) is False and dir not in ['']):
        os.mkdir(dir)


def find_closing_parentheses(text, p):
    ii, kk = (text[0] == p[0]) - 1, text.find(p[1])   # indices

    while(kk != -1):
        ii = text.find(p[0], ii+1)  # find next opening parentheses
        if(ii != -1):   # if there is a next opening parentheses
            if(ii < kk):  # if the opening parentheses is before the closing one.
                kk = text.find(p[1], kk+1)  # find next closing parentheses
            else:
                return kk
        else:
            return kk  # there is no other opening parentheses

    return -1


def find_opening_parentheses(text, p):
    ii, kk = len(text) - (text[-1] == p[1]), text.rfind(p[0])   # indices

    while(kk != -1):
        ii = text.rfind(p[1], 0, ii)  # find next closing parentheses
        if(ii != -1):  # if there is a next closing parentheses
            if(kk < ii):  # if there is a next opening parentheses
                kk = text.rfind(p[0], 0, kk)  # find next opening parentheses
            else:
                return kk
        else:
            return kk  # there is no other parentheses

    return -1


def find_all(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def check_parentheses(text):
    for p in ['()', '[]', '{}']:
        for i in find_all(text, p[0]):
            k = find_closing_parentheses(text[i:], p)
            if(k == -1):
                nline = text[:i].count('\n') + 1
                start, end = text[:i].rfind('\n') , text.find('\n', i)
                print()
                raise ValueError(f"""Parentheses {p[0]} in line {nline} does not close:
                    {text[start:i]}\033[4m{p[0]}\033[0m{text[i+1:end]}
                """)

        for i in find_all(text, p[1]):
            k = find_opening_parentheses(text[:i], p)
            if(k == -1):
                nline = text[:i].count('\n') + 1
                start, end = text[:i].rfind('\n'), text.find('\n', i)
                print()
                raise ValueError(f"""Parentheses {p[1]} in line {nline} does not open:
                    {text[start:i]}\033[4m{p[1]}\033[0m{text[i+1:end]}
                """)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# main
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    mkdir('img')
    mkdir('build')
    mkdir('main')
    main()
