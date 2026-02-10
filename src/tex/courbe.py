def format_syntax(formula):
    f = formula#.replace('sin(', 'sin(deg(')
    #f = f.replace('cos(', 'cos(deg(')
    return f

def line_curb_2d(x, y, color, domain, style, legend, bords):
    x = format_syntax(x)
    y = format_syntax(y)

    args = []
    if color:
        args.append(color)
    if style:
        args.append(style)
    if domain:
        t = 'domain={}'.format(domain)
        args.append(t)
    else:
        #txt = rf'\addplot[mark=*] coordinates {{({x}, {y})}};'
        args = ', '.join(args)
        txt = rf'\node[label={{\hspace{{-0.3cm}}{legend}}}, circle, fill, inner sep=2pt, {args}] at (axis cs:{x}, {y}) {{}};'
        return txt + '\n'

    if bords:
        args.append(bords)

    args.append('samples=100')
    args = ', '.join(args)

    txt = rf'\addplot[{args}] ({{{x}}}, {{{y}}});'
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
    txt = r'''\begin{figure}
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
