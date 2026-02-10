def format_syntax(formula):
    f = formula#.replace('sin(', 'sin(deg(')
    #f = f.replace('cos(', 'cos(deg(')
    return f

def line_curb_2d(x, y, z, color, domain, style, legend, bords):
    x = format_syntax(x)
    y = format_syntax(y)
    z = format_syntax(z)

    args = []
    if color:
        pass#args.append(color)
    if style:
        args.append(style)
    if domain:
        t = 'domain={0}, domain y={1}'.format(*domain.split(';'))
        args.append(t)
    else:
        #txt = rf'\addplot[mark=*] coordinates {{({x}, {y})}};'
        #args = ', '.join(args)
        #txt = rf'\node[label={{\hspace{{-0.3cm}}{legend}}}, circle, fill, inner sep=2pt, {args}] at (axis cs:{x}, {y}) {{}};'
        return '% points\n'#txt + '\n'

    if bords:
        pass#args.append(bords)

    args = ', '.join(args)

    txt = rf'\addplot3+ [{args}] ({{{x}}}, {{{y}}}, {{{z}}});'
    if legend:
        txt += '\n' + r'\addlegendentry{{{}}}'.format(legend) + '\n'

    return txt

def axeplot(curbs, arguments, legend, legendtitle, axiseq):
    txt = r'\begin{axis}['
    for k, v in arguments.items():
        if not v:
            continue

        txt += '\n    ' + str(k) + '=' + str(v) + ','

    if not legend:
        txt += '\n' + r'every axis legend/.code={\let\addlegendentry\relax},' + '% Commenter cette ligne pour afficher la légende !\n'

    if axiseq:
        txt += 'axis equal'

    txt += ']\n'
    if legendtitle:
        txt += r'\addlegendimage{empty legend}' + '\n'
        txt += r'\addlegendentry{\hspace{-.6cm}\textbf{' + legendtitle + '}}\n'

    for curb in curbs:
        txt += curb + '\n'

    txt += r'\end{axis}' + '\n'
    return txt

def figure(curbs, arguments, caption, legend, legendttle, axiseq):
    txt = r'''\begin{figure}[h]
\centering
\begin{tikzpicture}
'''
    txt += axeplot(curbs, arguments, legend, legendttle, axiseq)
    txt += r'\end{tikzpicture}' + '\n'
    if caption:
        txt += r'\caption{' + caption + '}\n'

    txt += r'\end{figure}' + '\n'
    return txt

if __name__ == '__main__':
    line = line_curb_2d(
        ('x', '2*x'),
        color = 'red')
    print(figure([line], 'premiers tests...'))
