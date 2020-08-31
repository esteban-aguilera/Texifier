# -----------------------------------------------------------------------------
# macros with zero variables
# -----------------------------------------------------------------------------
def newpar(*args):
    if(len(args) == 0):
        return r'\vspace{15pt}'


def d(*args):
    if(len(args) == 0):
        return r'{\text{d}}'


def ii(*args):
    if(len(args) == 0):
        return r'{\mathfrak{i}}'


def dagg(*args):
    if(len(args) == 0):
        return r'^{\dagger}'


def H(*args):
    if(len(args) == 0):
        return r'{\mathcal{H}}'


def Hi(*args):
    if(len(args) == 0):
        return r'H^{(i)}'


# -----------------------------------------------------------------------------
# macros with one variable
# -----------------------------------------------------------------------------
def Question(*args):
    if(len(args) == 1):
        return r'\textcolor{red}{ %s }' % args


def bm(*args):
    if(len(args) == 1):
        return r'\boldsymbol{%s}' % args


def rvec(*args):
    if(len(args) == 1):
        return r'\reflectbox{\ensuremath{\vec{\reflectbox{\ensuremath{%s}}}}}' % args


# -----------------------------------------------------------------------------
# macros with two variables
# -----------------------------------------------------------------------------
def partial(*args):
    if(len(args) == 0):
        return r'\oldpartial'
    elif(len(args) == 1):
        return r'\oldpartial_{%s}' % args
    elif(len(args) == 2):
        return r'\frac{\oldpartial %s}{\oldpartial %s}' % args


def Tr(*args):
    if(len(args) == 1):
        return r'\text{Tr}\left(%s \right)' % args
    elif(len(args) == 2):
        return r'\text{Tr}%s(%s%s)' % (args[0], args[1], args[0])


def bra(*args):
    if(len(args) == 1):
        return f'\\left\\langle {args[0]} \\right|'
    elif(len(args) == 2):
        return f'{args[0]}\\langle {args[1]} {args[0]}|'


def ket(*args):
    if(len(args) == 1):
        return f'\\left| {args[0]} \\right\\rangle'
    elif(len(args) == 2):
        return f'{args[0]}| {args[1]} {args[0]}\\rangle'


def braket(*args):
    if(len(args) == 1):
        return f'\\left\\langle {args[0]} \\right\\rangle'
    elif(len(args) == 2):
        return f'{args[0]}\\langle {args[1]} {args[0]}\\rangle'


def EinsteinSummation(*args):
    if(len(args) == 2):
        variables = args[1].split()

        coords = ['x', 'y', 'z']
        permutations = None
        for _ in range(len(args)):
            if(permutations is None):
                permutations = coords
            else:
                permutations = [x+y for x in permutations for y in coords]

        s = ''
        for p in permutations:
            p = list(p)

            aux = args[0]
            for i, var in enumerate(variables):
                aux = aux.replace(var, p[i])

            if(s == ''):
                s = aux
            else:
                s = f'{s} \n\t\t+ {aux}'

        return s


# -----------------------------------------------------------------------------
# macros with three variables
# -----------------------------------------------------------------------------
def replace(*args):
    if(len(args) == 3):
        return args[0].replace(args[1], args[2])


def Commutator(*args):
    if(len(args) == 2):
        return f'\\left[ {args[0]}, {args[1]} \\right]'
    elif(len(args) == 3):
        return f'{args[0]}[ {args[1]}, {args[2]} {args[0]}]'


def T(*args):
    """Time ordering operator
    """
    if(len(args) == 1):
        return r'T \bigg(%s \bigg)' % args
    elif(len(args) == 2):
        return r'T_{%s} \bigg(%s \bigg)' % (args[0], args[1])
    elif(len(args) == 3):
        return r'T_{%s} %s(%s %s)' % (args[0], args[1], args[2], args[1])


def U(*args):
    args = list(args)

    if('+' in args[-1]):
        aux = [f'{x}(\\tau)' for x in args[-1].split('+')]
        args[-1] = '+'.join(aux)
    else:
        args[-1] = f'{args[-1]}(\\tau)'

    args = tuple(args)

    if(len(args) == 1):
        return r'e^{-\frac{\ii}{\hbar} \int_{t_0}^{t} %s \d\tau}' % args
    elif(len(args) == 2):
        if(args[0][0].lower() == 'c'):
            return r'e^{-\frac{\ii}{\hbar} \int_{%s} %s \d\tau}' % args
        else:
            return r'e^{-\frac{\ii}{\hbar} \int_{t_0}^{%s} %s \d\tau}' % args
    elif(len(args) == 3):
        return r'e^{-\frac{\ii}{\hbar} \int_{%s}^{%s} %s \d\tau}' % args


def Uinv(*args):
    args = list(args)

    if('+' in args[-1]):
        aux = [f'{x}(\\tau)' for x in args[-1].split('+')]
        args[-1] = '+'.join(aux)
    else:
        args[-1] = f'{args[-1]}(\\tau)'

    args = tuple(args)

    if(len(args) == 1):
        return r'e^{\frac{\ii}{\hbar} \int_{t_0}^{t} %s \d\tau}' % args
    elif(len(args) == 2):
        if(args[0][0] == 'c'):
            return r'e^{-\frac{\ii}{\hbar} \int_{%s} %s \d\tau}' % args
        else:
            return r'e^{\frac{\ii}{\hbar} \int_{t_0}^{%s} %s \d\tau}' % args
    elif(len(args) == 3):
        return r'e^{\frac{\ii}{\hbar} \int_{%s}^{%s} %s \d\tau}' % args


def UTimeIndependent(*args):
    args = list(args)

    if('+' in args[-1]):
        args[-1] = f'({args[-1]})'

    args = tuple(args[::-1])

    if(len(args) == 1):
        return r'e^{-\frac{\ii}{\hbar} %s (t-t_0)}' % args
    elif(len(args) == 2):
        return r'e^{-\frac{\ii}{\hbar} %s (%s-t_0)}' % args
    elif(len(args) == 3):
        return r'e^{-\frac{\ii}{\hbar} %s (%s-%s)}' % args


def UinvTimeIndependent(*args):
    args = list(args)

    if('+' in args[-1]):
        args[-1] = f'({args[-1]})'

    args = tuple(args[::-1])

    if(len(args) == 1):
        return r'e^{\frac{\ii}{\hbar} %s (t-t_0)}' % args
    elif(len(args) == 2):
        return r'e^{\frac{\ii}{\hbar} %s (%s-t_0)}' % args
    elif(len(args) == 3):
        return r'e^{\frac{\ii}{\hbar} %s (%s-%s)}' % args


def UTimeOrdered(*args):
    args = list(args)

    if('+' in args[-1]):
        aux = [f'{x}(\\tau)' for x in args[-1].split('+')]
        args[-1] = '+'.join(aux)
    else:
        args[-1] = f'{args[-1]}(\\tau)'

    args = tuple(args)

    if(len(args) == 1):
        return r'T\Big( e^{-\frac{\ii}{\hbar} \int_{t_0}^{t} %s \d\tau} \Big)' % args
    elif(len(args) == 2):
        if(args[0][0] == 'c'):
            return r'T_{%s}\Big( e^{-\frac{\ii}{\hbar} \int_{%s} %s \d\tau} \Big)' % (args[0], *args)
        else:
            return r'T\Big( e^{-\frac{\ii}{\hbar} \int_{t_0}^{%s} %s \d\tau} \Big)' % args
    elif(len(args) == 3):
        return r'T\Big( e^{-\frac{\ii}{\hbar} \int_{%s}^{%s} %s \d\tau} \Big)' % args


def UinvTimeOrdered(*args):
    args = list(args)

    if('+' in args[-1]):
        aux = [f'{x}(\\tau)' for x in args[-1].split('+')]
        args[-1] = '+'.join(aux)
    else:
        args[-1] = f'{args[-1]}(\\tau)'

    args = tuple(args)

    if(len(args) == 1):
        return r'T\Big( e^{\frac{\ii}{\hbar} \int_{t_0}^{t} {%s}(\tau) \d\tau} \Big)' % args
    elif(len(args) == 2):
        if(args[0][0] == 'c'):
            return r'T_{%s}\Big( e^{-\frac{\ii}{\hbar} \int_{%s} %s \d\tau} \Big)' % (args[0], *args)
        else:
            return r'T\Big( e^{-\frac{\ii}{\hbar} \int_{t_0}^{%s} %s \d\tau} \Big)' % args
    elif(len(args) == 3):
        return r'T\Big( e^{\frac{\ii}{\hbar} \int_{%s}^{%s} {%s}(\tau) \d\tau} \Big)' % args


# -----------------------------------------------------------------------------
# macros with four variables
# -----------------------------------------------------------------------------
def HeisenbergPicture(*args):
    if(len(args) == 2):
        U = UTimeOrdered('t_0', 't', args[1])
        Uinv = UinvTimeOrdered('t_0', 't', args[1])
        return f'{Uinv}~{args[0]}~{U}'
    elif(len(args) == 3):
        U = UTimeOrdered('t_0', args[0], args[2])
        Uinv = UinvTimeOrdered('t_0', args[0], args[2])
        return f'{Uinv}~{args[1]}~{U}'
    elif(len(args) == 4):
        U = UTimeOrdered(args[0], args[1], args[3])
        Uinv = UinvTimeOrdered(args[0], args[1], args[3])
        return f'{Uinv}~{args[2]}~{U}'


def HeisenbergPictureTimeIndependent(*args):
    if(len(args) == 2):
        U = UTimeIndependent('t_0', 't', args[1])
        Uinv = UinvTimeIndependent('t_0', 't', args[1])
        return f'{Uinv}~{args[0]}~{U}'
    elif(len(args) == 3):
        U = UTimeIndependent('t_0', args[0], args[2])
        Uinv = UinvTimeIndependent('t_0', args[0], args[2])
        return f'{Uinv}~{args[1]}~{U}'
    elif(len(args) == 4):
        U = UTimeIndependent(args[0], args[1], args[3])
        Uinv = UinvTimeIndependent(args[0], args[1], args[3])
        return f'{Uinv}~{args[2]}~{U}'


def SchrodingerPicture(*args):
    if(len(args) == 2):
        U = UTimeOrdered('t_0', 't', args[1])
        Uinv = UinvTimeOrdered('t_0', 't', args[1])
        return f'{U}~{args[0]}~{Uinv}'
    elif(len(args) == 3):
        U = UTimeOrdered('t_0', args[0], args[2])
        Uinv = UinvTimeOrdered('t_0', args[0], args[2])
        return f'{U}~{args[1]}~{Uinv}'
    elif(len(args) == 4):
        U = UTimeOrdered(args[0], args[1], args[3])
        Uinv = UinvTimeOrdered(args[0], args[1], args[3])
        return f'{U}~{args[2]}~{Uinv}'


def SchrodingerPictureTimeIndependent(*args):
    if(len(args) == 2):
        U = UTimeIndependent('t_0', 't', args[1])
        Uinv = UinvTimeIndependent('t_0', 't', args[1])
        return f'{U}~{args[0]}~{Uinv}'
    elif(len(args) == 3):
        U = UTimeIndependent('t_0', args[0], args[2])
        Uinv = UinvTimeIndependent('t_0', args[0], args[2])
        return f'{U}~{args[1]}~{Uinv}'
    elif(len(args) == 4):
        U = UTimeIndependent(args[0], args[1], args[3])
        Uinv = UinvTimeIndependent(args[0], args[1], args[3])
        return f'{U}~{args[2]}~{Uinv}'


# -----------------------------------------------------------------------------
# tikz macros
# -----------------------------------------------------------------------------
def TikzFermion(*args):
    if(len(args) == 2):
        return r'\draw[decoration={markings, mark=at position 0.5 with {\arrow{> }}}, postaction={decorate}] (%s) -- (%s)' % args
