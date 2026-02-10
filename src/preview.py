import matplotlib.pyplot as plt
import numpy as np

def Courbe(data, grid, equal,
            x_min, x_max, y_min, y_max,
            caption, legend, legend_title,
            plot = None):

    if plot is not None:
        axis = plot
    else:
        axis = plt

    for eq_x, eq_y, color, domain, style, legendentry, borders in data:
        if ':' in domain:
            from_, to = domain.split(':')
        else:
            continue

        x = np.linspace(float(from_), float(to), 500)
        abscisses = eval(eq_x)
        ordonnees = eval(eq_y)
        style = style.replace('thick', 'solid')
        if style not in ('-', '--', '-.', ':', 'None', ' ', '', 'solid', 'dashed', 'dashdot', 'dotted'):
            style = 'solid'

        axis.plot(abscisses, ordonnees,
                 color = color,
                 label = legendentry,
                 linestyle = style)

    if grid:
        axis.grid()

    if plot is not None:
        axis.set(xlim = (float(x_min), float(x_max)),
                 ylim = (float(y_min), float(y_max)))

        axis.set_title(caption)

    else:
        axis.xlim(float(x_min), float(x_max))
        axis.ylim(float(y_min), float(y_max))

        axis.title(caption)

    if legend:
        axis.legend()

    if plot is None:
        plt.show()
