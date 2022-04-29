import numpy as np
import matplotlib.pyplot as plt

def plot_barcodes(dgms,titulo_frag='',titulo_graf='',color='indigo'):
    concat_dgms = np.concatenate(dgms).flatten()
    has_inf = np.any(np.isinf(concat_dgms))
    finite_dgms = concat_dgms[np.isfinite(concat_dgms)]
    if has_inf: #esto debe hacerse para poder graficar los valores "hasta el infinito" inf; está hecho imitando lo que aparece en el módulo persim.plot_diagrams, asociado a ripser, que es el que grafica los diagramas de persistencia
        ax_min, ax_max = np.min(finite_dgms), np.max(finite_dgms)
        buffer=(ax_max - ax_min)/5
        y_down = ax_min - buffer / 2
        y_up = ax_max + buffer
        yr = y_up - y_down
        b_inf = y_down + yr * 0.95
    L=len(dgms)
    fig, ax=plt.subplots()
    for i in range(L):
        l=len(dgms[i])
        for j in range(l):
            p=dgms[i][j]
            if p[1] != np.inf:
                ax.hlines(y=i-j/l,xmin=p[0],xmax=p[1],linewidth=2,color=color)
            else:
                ax.hlines(y=i-j/l,xmin=p[0],xmax=b_inf,linewidth=2,color=color)
    ax.set_yticks([i for i in range(-1,L)])
    ax.set_yticklabels(['']+[r'$\beta_{{{}}}$'.format(str(i)) for i in range(L)]) #se necesitan 3 pares de llaves en '$H_{{{}}}$'.format(str(i)) pues con uno solo únicamente toma como subíndice un dígito (no dos, en el caso de H_10 y H_11)
    plt.title(titulo_frag+' '+'-'+' '+titulo_graf) #aquí hay que poner dobles llaves a la K dentro de mathcal, pues no representa una clave (Key) de .format
    fig.tight_layout()
    plt.show()
