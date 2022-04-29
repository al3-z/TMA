import music21 as m21
import copy
#import simplicial as simpl
#import mogutda as mtda
from mogutda import SimplicialComplex
from ripser import ripser
from persim import plot_diagrams
import numpy as np
import matplotlib.pyplot as plt
from plot_barcodes_ripser import plot_barcodes
from transpBajoFin import transpBajoFin

titulo="ALP-Graffiti8_FJH.mxl"
score=m21.converter.parse('/Users/alberto/Documents/doc/partituras_doc/{}'.format(titulo))#NOTA: hay que quitar en el archivo .xml o .mxl, etc los pentagramas que sean de percusiones no afinadas
#print("Haydn Cuarteto de Cuerdas op.74 no.1 en Do Mayor, III - Minueto")
eventos=[]
eventosTDA=[]
eventosB=[]
#score.measures(0,5).show()
#acs=score.chordify() #esta instruccion es para considerar TODO el archivo.
inicio=1
fin=4
titulo_frag="{}, cc.{}-{}".format(titulo,str(inicio),str(fin))
acs=score.measures(inicio,fin).chordify() #si no se quiere todo el score, hay que poner score.measures(a,b).chordify()
#acs.show()#hay una incongruencia entre el score original y el que genera music21. en el primer piano se recorre la primera figura.(esto aplica para el son de la noche para piano a 4 manos)
#acs=transpBajoFin(score,acs)[0] #Esto transpone el fragmento acs a do, tomando en cuenta la última nota del bajo.
for ac in acs.flat.recurse().getElementsByClass('Chord'):
    eventos.append([tuple(ac.normalOrder),float(ac.quarterLength)])#aquí se quitan las repeticiones de octavas en los acordes.
    eventosTDA.append([tuple(ac.normalOrder),float(ac.quarterLength),float(ac.offset)])
    eventosB.append([tuple(ac.intervalVector),float(ac.quarterLength),float(ac.offset)])
print("\n# eventos :", len(eventos))
print(eventos)#aqui puede haber acordes repetidos. aqui habria que hacer las conexiones entre acordes y ritmos, antes de sumar las duraciones. la lista "eventos" se quedará intacta para poder contar ritmos (no sumar duraciones, lo cual se hará en la lista eventos2).
print("\n# eventosTDA :", len(eventosTDA))
print(eventosTDA)
print("\n# eventos :", len(eventosB))
print(eventosB)

found=set()
eventos2=copy.deepcopy(eventos) #es necesario importar la librería copy (python)y usar la función deepcopy, pues se trata de pegar una lista de listas. se pueden usar distintos métodos para copiar listas no anidadas o listas superfluas con new_list=old_list[:] (según este método sería el más rápido)
#pero también hay otros métodos: new_list=list(old_list), ver por ejemplo https://stackoverflow.com/questions/2612802/list-changes-unexpectedly-after-assignment-how-do-i-clone-or-copy-it-to-prevent
for i in range(len(eventos2)):#define el conjunto found como las tuplas de acordes, sumando su duración y quitando repeticiones
    eventos2[i][0]=tuple(eventos2[i][0])
    if any([eventos2[i][0] in list(found)[j] for j in range(len(list(found)))]) == False:
        found.add((eventos2[i][0],i))
    else:
        for j in range(len(list(found))):
            if eventos2[i][0] in list(found)[j]:
                eventos2[list(found)[j][1]][1] += eventos2[i][1] #se suman las duraciones de los acordes repetidos
#print("eventos con duraciones totales en la primera aparición: ", len(eventos2))#falta hacer que todos los acordes iguales tengan la misma duración(??)
#print(eventos2)#la lista eventos 2 contiene las tuplas de acordes junto con su duración total sumada la primera vez que aparece el acorde en la lista.
from collections import Counter
ac_counts=Counter(ac for ac, _ in eventos2) #contador (tipo de diccionario) de elementos en la primera entrada (acordes) de la lista eventos2
for i in range(len(eventos2)):#agregar la cuenta de cada acorde
    eventos2[i].append(ac_counts[eventos2[i][0]])
print("\neventos con duraciones totales en la primera aparición, con cuenta de ocurrencias:")
print("# eventos2: ", len(eventos2))
print(eventos2)



eventos2_cons=[[(eventos2[i][0],eventos2[i+1][0]),0] for i in range(len(eventos2)-1)]
par_counts=Counter(par for par, _ in eventos2_cons)
l=[]
for par in eventos2_cons:
    par[1]+=par_counts[par[0]]
    if par not in l:
        l.append(par)
eventos2_cons=l
print("\npares de eventos consecutivos, con cuenta de ocurrencias:")
print(eventos2_cons)


#crear lista sin acordes repetidos, junto con su duración total y ocurrencias totales
acsdifs=[]
for i in range(len(eventos2)):#obtiene lista de acordes sin repetición, junto con sus duraciones totales y repeticiones totales
    if any([eventos2[i][0] in acsdifs[j] for j in range(len(acsdifs))])==False:
        acsdifs.append(eventos2[i])
print("\n# conjuntos de alturas (acordes) distintos con duraciones totales y cuenta de ocurrencias:", len(acsdifs))
print(acsdifs)
notas=[]
acordes=[]
intervalos={}
intervalos_acs=[]
ritmos=[]
for i in range(len(eventos2)):#crea una lista con clase de altura, su duracion total y numero de ocurrencias en todos los acordes
    for n in eventos2[i][0]:
        if n not in [item[0] for item in notas]:
            dur=0
            times=0
            for j in range(len(eventos2)):
                if n in eventos2[j][0]:
                    dur+=eventos2[j][1]
                    times+=eventos2[j][2]
            notas.append((n,dur,times))
print("\n# clases de altura: ", len(notas)," : ", notas)

for i in range(len(acsdifs)):
    intervalos_acorde=[]
    for j in range(len(acsdifs[i][0])-1):
        intervalos_acorde.append((acsdifs[i][0][j+1]-acsdifs[i][0][j])%12)
    intervalos_acs.append([tuple(intervalos_acorde),acsdifs[i][1],acsdifs[i][2]])
    #se agrega la duración total del acorde al que pertenecen los intervalos y el num de ocurrencias
    #NOTA: otra opcion es usar la funcion de music21: vector de intervalos
print("\n# acordes como n-adas de intervalos con duraciones totales y cuenta de ocurrencias: ", len(intervalos_acs) , ':')
print(intervalos_acs)

#diccionario de intervalos por separado (no como tupla)
for t in intervalos_acs:
    if len(t[0])>0:
        for i in t[0]:
            if i in intervalos:
                intervalos[i][0]+=t[1]
                intervalos[i][1]+=t[2]
            else:
                intervalos[i]=[t[1],t[2]]

print("\n# intervalos con duraciones y ocurrencias totales: ", len(intervalos) , ':')
print(intervalos)



for i in range(len(acsdifs)):
    acordes.append(tuple((tuple(m21.chord.Chord(acsdifs[i][0]).normalOrder),acsdifs[i][1],acsdifs[i][2])))#la hacemos tupla para añadirla directamente como nodo en la grafica (hashable)
print("\n# acordes: ", len(acordes) , ':')
print(acordes)


for i in range(len(eventos)):
    #print(eventos2[i][1]) #lista de duraciones totales
    if eventos[i][1] not in ritmos:#esto agrega un ritmo cada que aparece en la lista eventos, pues eventos[i][1] nunca pertenece tal cual a la lista ritmos (la lista ritmos tiene como elementos listas cuya entrada [0][0] tiene el ritmo en cuestión)
        ritmos.append([(eventos[i][1],'qL'),0])#agrega a la lista ritmos los ritmos de los acordes de la lista original, "eventos"
#print("# ritmos: ", len(ritmos) , ':', ritmos)
rit_counts=Counter(rit for rit, _ in ritmos)
for i in range(len(ritmos)):#agregar a cada entrada de la lista ritmos2 el número de veces que aparece en la lista original, "eventos". así se puede obtener también la suma de duraciones de cada ritmo (lo cual es desechable, al tener en cuenta que al ser ritmos ya son duraciones).
    ritmos[i][1]=rit_counts[ritmos[i][0]]
    ritmos[i]=tuple(ritmos[i])
ritmos=list(set(ritmos))
print("\n# ritmos con contador: ", len(ritmos) , ':', ritmos)








#A partir de aquí comienza Topología Algebraica (Homología simplicial y TDA)

#TDA sobre los eventosTDA: (acorde, duración, offset)    NOTA: faltaría incluir timbre, dinámica...
for ind , ev in enumerate(eventosTDA):
    x=[0]*12
    for i in range(len(ev[0])):
        x[i]=ev[0][i]+12 #se consideran clases de altura 12-23 para poder agregar coordenadas 0 en R^12
    ev.remove(ev[0])
    eventosTDA[ind]=x+ev

dataeventosTDA=np.array(eventosTDA)
print("\ndataeventosTDA:")
print(dataeventosTDA)
print("\n hasta aquí dataeventosTDA \n")
dgms = ripser(dataeventosTDA, maxdim=3, metric='euclidean')['dgms']
l=[]
Pers_entr=0
D=0
for i in dgms:
    for j in i:
        print(j)
        x=j[1]-j[0]
        l.append(x)
        if x!=np.inf:
            D+=x
    print("\n")
print(l)

print("D: ", D)
for x in l:
    if x!=np.inf:
        p=x/D
        Pers_entr-=(p)*(np.log(p))
    else:
        continue
print("entropía pesistente de eventosTDA: ", Pers_entr)
print("\n")




plot_diagrams(dgms, title=titulo_frag+' '+'-'+' '+'$(ac(\overline {12} , \, ... \, , \overline {23}), dur , pos)$', colormap='default', show=True)
plot_diagrams(dgms, title=titulo_frag+' '+'-'+' '+'$(ac(\overline {12} , \, ... \, , \overline {23}), dur , pos)$', colormap='default', lifetime=True, show=True)

plot_barcodes(dgms,titulo_frag,"Barcodes for $(ac(\overline {12} , \, ... \, , \overline {23}), dur , pos)$",'teal')




#TDA sobre los eventosB: (vector de intervalos del acorde, duración, offset)    NOTA: faltaría incluir timbre, dinámica...

dataeventosB=np.array([list(ev[0])+[ev[1],ev[2]] for ev in eventosB])
print("dataeventosB")
print(dataeventosB)
dgms = ripser(dataeventosB, maxdim=3, metric='euclidean')['dgms']
for i in dgms:
    for j in i:
        print(j)
    print("\n")
plot_diagrams(dgms, title=titulo_frag+' '+'-'+' '+'$(vectInt(ac), dur , pos)$', colormap='default', show=True)
plot_diagrams(dgms, title=titulo_frag+' '+'-'+' '+'$(vectInt(ac), dur , pos)$', colormap='default', lifetime=True, show=True)

plot_barcodes(dgms,titulo_frag,"Barcodes for $(vectInt(ac), dur , pos)$",'teal')


#TDA sólo sobre los tipos de acordes (vectores de intervalos)
dataeventosB=np.array([ev[0] for ev in eventosB])
print("dataeventosB")
print(dataeventosB)
dgms = ripser(dataeventosB, maxdim=3, metric='euclidean')['dgms']
for i in dgms:
    for j in i:
        print(j)
    print("\n")
plot_diagrams(dgms, title=titulo_frag+' '+'-'+' '+'$vectInt(ac)$', colormap='default', show=True)
plot_diagrams(dgms, title=titulo_frag+' '+'-'+' '+'$vectInt(ac)$', colormap='default', lifetime=True, show=True)

plot_barcodes(dgms,titulo_frag,"Barcodes for $(vectInt(ac))$")





#Se construyen los complejos simpliciales de eventos (acordes), CSEv, por altura y número de voces.
a=0
b=len(eventos)
#b=6

simp=[]
NumsBetti_CSEv_Tot=[]
for i in range(a,b):
    simp.append(eventos[i][0])
    print("Simplejos del CS-Ev", i, ": " , simp  )
    CS=SimplicialComplex(simplices=simp)
    E=0
    NumsBetti_CSEv_i=[]
    for k in range(12):
        bk=CS.betti_number(k)
        print("Número de Betti ", k , ": ", bk)
        NumsBetti_CSEv_i.append(bk)
        Ek=((-1)**k)*bk
        E+=Ek
    print("Característica de Euler del CS-Ev", i,": " ,E)
    NumsBetti_CSEv_Tot.extend([tuple(NumsBetti_CSEv_i) , E])
print(NumsBetti_CSEv_Tot)


#se forman dos listas: una con listas que contienen los números de Betti de los CS-Ev, tomados por dimensión, y otra con los máximos de cada una de esas listas
LstBetti=[]
Maxs=[]
for j in range(12):
    lstBetti=[NumsBetti_CSEv_Tot[i][j] for i in range(0,len(NumsBetti_CSEv_Tot),2)]
    LstBetti.append(lstBetti)
    M=max(lstBetti)
    Maxs.append(M)

fig, ax=plt.subplots()
for j in range(12):
    if LstBetti[j] != [0]*12:
        for i in range(len(LstBetti[j])):
            if LstBetti[j][i]==0:
                continue
            else:
                for k in range(LstBetti[j][i]):
                    ax.hlines(y=j-k/Maxs[j],xmin=i,xmax=i+1,linewidth=2,color='darkgreen')
ax.set_yticks([i for i in range(-1,12)])
ax.set_yticklabels(['']+[r'$\beta_{{{}}}$'.format(str(i)) for i in range(12)]) #se necesitan 3 pares de llaves en '$H_{{{}}}$'.format(str(i)) pues con uno solo únicamente toma como subíndice un dígito (no dos, en el caso de H_10 y H_11)
plt.title(titulo_frag+' '+'-'+' '+r'$\beta (\mathcal{K}(0,i))$')
fig.tight_layout()
plt.show()




"""
#TDA sobre los nums de Betti de los complejos CSEv_i

dataNumsBetti_CSEv=np.array([NumsBetti_CSEv_Tot[i] for i in range(0,len(NumsBetti_CSEv_Tot),2)])
print("dataNumsBetti_CSEv")
print(dataNumsBetti_CSEv)
dgms = ripser(dataNumsBetti_CSEv, maxdim=3, metric='euclidean')['dgms']
for i in dgms:
    for j in i:
        print(j)
    print("\n")
plot_diagrams(dgms, show=True)
plot_diagrams(dgms, lifetime=True, show=True)
"""

r=4 #radio de eventos
print("Homología de los complejos simpliciales asociados a ventanas de eventos de radio =",r)
NumsBetti_CSEv_r_Tot=[]
for i in range(a+r,b-r):
    simp=[eventos[j][0] for j in range(i-r,i+r+1)]
    print("Simplejos del CS-Ev_{}".format(str(r)), i, ": " , simp  )
    CS=SimplicialComplex(simplices=simp)
    E=0
    NumsBetti_CSEv_r=[]
    for k in range(12):
        bk=CS.betti_number(k)
        print("Número de Betti ", k , ": ", bk)
        NumsBetti_CSEv_r.append(bk)
        Ek=((-1)**k)*bk
        E+=Ek
    print("Característica de Euler del CS-Ev_{}".format(str(r)), i,": " ,E)
    NumsBetti_CSEv_r_Tot.extend([tuple(NumsBetti_CSEv_r) , E])
print(NumsBetti_CSEv_r_Tot)



#se forman dos listas: una con listas que contienen los números de Betti de los CS-Ev_r, tomados por dimensión, y otra con los máximos de cada una de esas listas
LstBetti2=[]
Maxs2=[]
for j in range(12):
    lstBetti=[NumsBetti_CSEv_r_Tot[i][j] for i in range(0,len(NumsBetti_CSEv_r_Tot),2)]
    LstBetti2.append(lstBetti)
    if len(lstBetti)!=0:
        M=max(lstBetti)
    else:
        M=0
    Maxs2.append(M)

fig, ax=plt.subplots()
for j in range(12):
    if LstBetti2[j] != [0]*12:
        for i in range(len(LstBetti2[j])):
            if LstBetti2[j][i]==0:
                continue
            else:
                for k in range(LstBetti2[j][i]):
                    ax.hlines(y=j-k/Maxs2[j],xmin=i,xmax=i+1,linewidth=2,color='darkgreen')
ax.set_xticks([i for i in range(a,b-2*r,r)])
ax.set_xticklabels([str(i) for i in range(a+r,b-r,r)])
ax.set_yticks([i for i in range(-1,12)])
ax.set_yticklabels(['']+[r'$\beta_{{{}}}$'.format(str(i)) for i in range(12)]) #se necesitan 3 pares de llaves en '$H_{{{}}}$'.format(str(i)) pues con uno solo únicamente toma como subíndice un dígito (no dos, en el caso de H_10 y H_11)
plt.title(titulo_frag+' '+'-'+' '+r'$\beta (\mathcal{{K}} _{0}(i))$'.format(r)) #aquí hay que poner dobles llaves a la K dentro de mathcal, pues no representa una clave (Key) de .format
fig.tight_layout()
plt.show()




"""
#TDA sobre los nums de Betti de los complejos CSEv_r_i

dataNumsBetti_CSEv_r=np.array([NumsBetti_CSEv_r_Tot[i] for i in range(0,len(NumsBetti_CSEv_r_Tot),2)])
print("dataNumsBetti_CSEv_r")
print(dataNumsBetti_CSEv_r)
dgms = ripser(dataNumsBetti_CSEv_r, maxdim=3, metric='euclidean')['dgms']
for i in dgms:
    for j in i:
        print(j)
    print("\n")
plot_diagrams(dgms, show=True)
plot_diagrams(dgms, lifetime=True, show=True)
"""




eventos3=[] #esta lista almacena los acordes codificados en el cuadrante positivo unitario en R12, agregándoles coordenadas 0 ó 1 en la coordenada x[i] si contienen la clase de altura i

for ac in eventos:
    x=[0]*12
    for n in ac[0]:
        x[n]=1
    eventos3.append(tuple(x))
print("eventos3: ", len(eventos3), " Sin repetición: ", len(set(eventos3)))
print("\nacordes vistos en el cuadrante positivo unitario de R^12:")
print(eventos3)

dataAcsR12_u=np.array(eventos3)
dgms = ripser(dataAcsR12_u, maxdim=3, metric='euclidean')['dgms']
for i in dgms:
    for j in i:
        print(j)
    print("\n")
plot_diagrams(dgms,title=titulo_frag+' '+'-'+' '+"Chords in $I^{12}$", colormap='default',show=True)
plot_diagrams(dgms,title=titulo_frag+' '+'-'+' '+"Chords in $I^{12}$", colormap='default',lifetime=True, show=True)
fig.tight_layout()

plot_barcodes(dgms,titulo_frag,"Barcodes for chords in $I^{12}$")


eventos4=[] #esta lista almacena los acordes codificados en R12, tomando en cuenta las clases de altura 12-23, en lugar de 0-11, agregando coordenadas 0.
for ac in eventos:
    x=[0]*12
    for i in range(len(ac[0])):
        x[i]=ac[0][i]+12
    eventos4.append(tuple(x))
print("eventos4: ", len(eventos4), " Sin repetición: ", len(set(eventos4)))
print("\nacordes vistos en R^12, según número de voces, con clases de altura entre 12 y 23:")
print(eventos4)


dataAcsR12=np.array(eventos4)
dgms = ripser(dataAcsR12, maxdim=3, metric='euclidean')['dgms']
for i in dgms:
    for j in i:
        print(j)
    print("\n")
plot_diagrams(dgms, title=titulo_frag+' '+'-'+' '+'Chords in $\mathbb{R} ^{12} , c.a. \overline {12} - \overline {23}$', colormap='default',show=True)
plot_diagrams(dgms, title=titulo_frag+' '+'-'+' '+'Chords in $\mathbb{R} ^{12} , c.a. \overline {12} - \overline {23}$', colormap='default',lifetime=True, show=True)

plot_barcodes(dgms,titulo_frag,"Barcodes for chords in $\mathbb{R} ^{12} , p.c. \overline {12} - \overline {23}$")


Suc_CS_Acs=[] #esta lista guarda los complejos simpliciales correspondientes a cada acorde, tomando en cuenta alturas e intervalos
Betti_Total_AcsInt=[]
Betti_AcsInt=[]
simpAcsInt=[]
vectAcsInt=[]
for ac in eventos:
    vectAcInt=[0]*12
    simpAcInt=[]
    if len(ac[0])>1:
        for i in range(len(ac[0])-1):
            if ac[0][i]<ac[0][i+1]:
                simpInt=tuple([k for k in range(ac[0][i],1+ac[0][i+1])])
                print("simpInt: ", i, ": ", simpInt)
                simpAcInt.append(simpInt)
                print("simpAcInt: ", i, ": ", simpAcInt)
                simpAcsInt.append(simpInt)
                vectAcInt[ac[0][i]]=ac[0][i+1]-ac[0][i]
            else:
                simpInt=tuple([k%12 for k in range(ac[0][i],1+12+ac[0][i+1])])
                print("simpInt: ", i, ": ", simpInt)
                simpAcInt.append(simpInt)
                print("simpAcInt: ", i, ": ", simpAcInt)
                simpAcsInt.append(simpInt)
                vectAcInt[ac[0][i]]=12+ac[0][i+1]-ac[0][i]
    else:
        simpAcInt.append(ac[0])
        simpAcsInt.append(ac[0])
    vectAcsInt.append(vectAcInt)
    print("vectAcInt:")
    print(vectAcInt)
    print("\n")
    CS_Ac=SimplicialComplex(simplices=simpAcsInt)
    Betti_Ac=[CS_Ac.betti_number(m) for m in range(12)]
    print("Betti_Ac: ", Betti_Ac)
    E=CS_Ac.euler_characteristics()
    print("Característica de Euler del complejo acumulado de acordes por intervalo:", E)
    Betti_AcsInt.extend([Betti_Ac, E])
    Suc_CS_Acs.append(CS_Ac)
    print("\nSimplejos del complejo acumulado de acordes por intervalo: ", simpAcsInt)
print("\nvectAcsInt:", len(vectAcsInt))
print(vectAcsInt)
print("\nBetti_AcsInt: ", Betti_AcsInt)
print("\nTOTAL Simplejos de acordes por intervalo (sin repeticiones): ", len(list(set(simpAcsInt))), ":", list(set(simpAcsInt)))
CS_Acs=SimplicialComplex(simplices=simpAcsInt)
Betti_Total_AcsInt=[CS_Acs.betti_number(m) for m in range(12)]
print("\nBetti_Total_AcsInt: ", Betti_Total_AcsInt)
E_Total_AcsInt=CS_Acs.euler_characteristics()
print("Característica de Euler del complejo TOTAL de acordes por intervalo: ", E_Total_AcsInt)




#TDA sobre los acordes por intervalo y altura vistos en R^12
print("\nTDA sobre los acordes por intervalo y altura vistos en R^12:")
datavectAcsInt=np.array([vectAcsInt[i] for i in range(len(vectAcsInt))])
print("\ndatavectAcsInt: ", len(datavectAcsInt))
print(datavectAcsInt)
dgms = ripser(datavectAcsInt, maxdim=3, metric='euclidean')['dgms']
print("\ndataBetti_AcsInt (parejas (b,d) corr. a la homología persistente del cjto. Betti_AcsInt):")
for i in dgms:
    for j in i:
        print(j)
    print("\n")
plot_diagrams(dgms, title=titulo_frag+' '+'-'+' '+r'$\beta (acs.(alt,int))$', show=True)
plot_diagrams(dgms, title=titulo_frag+' '+'-'+' '+r'$\beta (acs.(alt,int))$', lifetime=True, show=True)

plot_barcodes(dgms,titulo_frag,"Barcodes for chords in $(acs.(alt,int))$")



"""
#TDA sobre los nums de Betti de los Complejos acumulados de acordes por intervalo y altura
dataBetti_AcsInt=np.array([Betti_AcsInt[i] for i in range(0,len(Betti_AcsInt),2)])
dgms = ripser(dataBetti_AcsInt, metric='euclidean')['dgms']
print("dataBetti_AcsInt (parejas (b,d) corr. a la homología persistente del cjto. Betti_AcsInt):")
for i in dgms:
    for j in i:
        print(j)
    print("\n")
plot_diagrams(dgms, show=True)
plot_diagrams(dgms, lifetime=True, show=True)
"""

"""
simpAcs=[]
CS_Acs=SimplicialComplex(simplices=set(simpAcs))
print("\nComplejo simplicial de todos los acordes como clases de alturas:")
for k in range(12):
    bk=CS_Acs.betti_number(k)
    print("Número de Betti ", k , ": ", bk)
    Ek=((-1)**k)*bk
    E+=Ek
print("Característica de Euler del CS-Acs", i,": " ,E)
"""


















#NOTA lo siguiente aparece en el archivo music21_notas_acordes_intervalos_ritmos_sin_octavas_sin_inversiones, donde se construyen y analizan gráficas y redes

"""
#a partir de aquí se construye la gráfica
import networkx as nx
import itertools
import matplotlib.pyplot as plt
from networkx.utils import pairwise
G=nx.Graph()
G.add_nodes_from([item[0] for item in notas])#acordes e intervalos no pueden agregarse con este método, pues contienen listas (unhashable), hay que hacerlas tupla primero (hashable)
#hay que agregar las clases de alturas a partir de las primeras entradas de la lista notas, que contiene duraciones y ocurrencias totales de cada clase de altura
for i in range(len(acordes)):
    #if len(acordes[i][0]) > 1:#esto es para sólo tener los acordes con más de una nota. OJO: habria que activarlo tambien más abajo, al momento de dibujar los nodos
        G.add_node(tuple(acordes[i][0]))
for i in range(len(intervalos_acs)): #esto agrega n-adas de intervalos correspondientes a cada acorde; pero lo que en realidad se quiere es generar los intervalos por separado.
    if len(intervalos_acs[i][0]) > 0:
        G.add_node((intervalos_acs[i][0],'iAc'))
for key in intervalos:
    G.add_node((key,'i'))
def Extract(lst):
    return [item[0] for item in lst]
G.add_nodes_from(Extract(ritmos))
subset_key=[]
nx.set_node_attributes(G,subset_key,"subset")#para dibujar con multipartite_layout hay que poner al diccionario de nodos el atributo "subset"
nx.set_node_attributes(G,subset_key,"node_color")
notas_acs=[]
notas_rit=[]
acs_ints=[]
totalDurNotas=0
totalTimesNotas=0
totalDurAcs=0
totalTimesAcs=0
totalTimesRit=0
totalDegCentr=0
totalDegCentr=0
totalDegCentr=0
totalDurInts=0
totalTimesInts=0
for n in G.nodes():
    if n in [item[0] for item in notas]:
        G.nodes()[n]["subset"]=1
        G.nodes()[n]["node_color"]='c'
        G.nodes()[n]["weight"]=notas[[item[0] for item in notas].index(n)][1]#asigna la duración total de la clase de altura como peso
        G.nodes()[n]["times"]=notas[[item[0] for item in notas].index(n)][2]#asigna el número total de ocurrencias de la clase de altura como otro atributo llamado "times"
        totalDurNotas+=G.nodes()[n]["weight"]
        totalTimesNotas+=G.nodes()[n]["times"]
        for i in range(len(acordes)):
            if n in acordes[i][0]:
                cont_notas_acs=acordes[i][0].count(n) #contar ocurrencias de la nota n en el acorde acordes[i][0]
                notas_acs.append(((n,acordes[i][0]),cont_notas_acs*acordes[i][2]))
                #print("cuenta notas:", n ,"en ", acordes[i][0] ,":", cont_notas_acs)
    elif any([n == tuple(acordes[m][0]) for m in range(len(acordes))])==True:
        G.nodes()[n]["subset"]=2
        G.nodes()[n]["node_color"]='magenta'
        G.nodes()[n]["weight"]=acordes[[item[0] for item in acordes].index(n)][1]#asigna duracion del acorde como peso
        G.nodes()[n]["times"]=acordes[[item[0] for item in acordes].index(n)][2]#asigna el número de repeticiones como "times"
        totalDurAcs+=G.nodes()[n]["weight"]
        totalTimesAcs+=G.nodes()[n]["times"]
        for r in ritmos:
            cont_nota_rit=eventos.count([tuple(n),r[0][0]])
            if cont_nota_rit>0:
                print("acorde: ", n, "ritmo: ", r[0][0], "# veces: ", cont_nota_rit)
                if (n,r[0][0],cont_nota_rit) not in notas_rit:
                    notas_rit.append((n,r[0][0],cont_nota_rit))
            #faltaria guardar este contador en la lista notas_rit y luego generar las aristas con este grosor
    #elif any([n[0] == intervalos_acs[k][0] for k in range(len(intervalos_acs))]) == True:
    #    G.nodes()[n]["subset"]=5
    #    G.nodes()[n]["node_color"]='indianred'
    elif n[1] == 'i':
        G.nodes()[n]["subset"]=3
        G.nodes()[n]["node_color"]='yellowgreen'
        G.nodes()[n]["weight"]=intervalos[n[0]][0]
        G.nodes()[n]["times"]=intervalos[n[0]][1]
        totalDurInts+=G.nodes()[n]["weight"]
        totalTimesInts+=G.nodes()[n]["times"]
        for i in range(len(intervalos_acs)):
            if len(intervalos_acs[i][0])>0:
                if n[0] in intervalos_acs[i][0]:
                    cont_acs_ints=intervalos_acs[i][0].count(n[0])
                    acs_ints.append((n,acordes[i][0],cont_acs_ints*acordes[i][2]))
    elif any([n == ritmos[i][0] for i in range(len(ritmos))])==True: #OJO., para usar multipartite_layout, hay que etiquetar tuplas (hashable), no listas (unhashable)!!
        G.nodes()[n]["subset"]=4
        G.nodes()[n]["node_color"]='teal'
        G.nodes()[n]["times"]=ritmos[[item[0] for item in ritmos].index(n)][1]
        totalTimesRit+=G.nodes()[n]["times"]
print("nodos: ", G.nodes(data=True))

print("totalDurNotas=",totalDurNotas)
print("totalTimesNotas=",totalTimesNotas)
print("totalDurAcs=",totalDurAcs)
print("totalTimesAcs=",totalTimesAcs)
print("totalTimesRit=",totalTimesRit)
print("totalDurInts=",totalDurInts)
print("totalTimesInts=",totalTimesInts)



#poner aristas: hay que poner contadores de número total de repeticiones por tipo de arista y agregarlo como anchura (width) (también hay un parámetro de transparencia para aristas (alpha); sería útil para otra medida de las aristas???; por ahora, sólo para diferenciar mejor las aristas en el dibujo)
for i in range(len(notas_acs)):
    G.add_edge(notas_acs[i][0][0],notas_acs[i][0][1], width=notas_acs[i][1])
for i in range(len(notas_rit)):
    G.add_edge(notas_rit[i][0],(notas_rit[i][1],'qL'), width=notas_rit[i][2])
for i in range(len(acs_ints)):#aristas entre intervalos y acordes
    G.add_edge(acs_ints[i][0],acs_ints[i][1], width=acs_ints[i][2])



#Calcular entropía (de Shannon).

"""
"""


NOTA: La entropía de una gráfica puede definirse de tres modos distintos equivalentes:
la mínima información mutua entre las vars aleatorias X,Y, donde X es un vértice uniformemente distribuido y Y un conjunto independiente de vértices que contiene a X;
el mínimo valor sobre todos los puntos del politopo envolvente de los vértices, de la suma de los productos de la probabilidad de cada vértice
por el logaritmo del inverso de cada coordenada del punto;
o bien como su número cromático
La entropía así definida es un problema NP-hard.


"""

"""
entropiaShannonNotasDur=0
entropiaShannonNotasTimes=0
entropiaShannonAcsDur=0
entropiaShannonAcsTimes=0
entropiaShannonIntsDur=0
entropiaShannonIntsTimes=0
entropiaShannonRitTimes=0
entropiaShannonDegCentr=0

import math
for n in G.nodes():
    if n in [item[0] for item in notas]:
        G.nodes()[n]["p_dur"]=G.nodes()[n]["weight"]/totalDurNotas
        G.nodes()[n]["p_rep"]=G.nodes()[n]["times"]/totalTimesNotas
        G.nodes()[n]["deg_centr"]=nx.degree_centrality(G)[n]
        totalDegCentr+=G.nodes()[n]["deg_centr"]
        entropiaShannonNotasDur+=(-G.nodes()[n]["p_dur"]*math.log(G.nodes()[n]["p_dur"],2))
        entropiaShannonNotasTimes+=(-G.nodes()[n]["p_rep"]*math.log(G.nodes()[n]["p_rep"],2))
    elif any([n == tuple(acordes[m][0]) for m in range(len(acordes))])==True:
        G.nodes()[n]["p_dur"]=G.nodes()[n]["weight"]/totalDurAcs
        G.nodes()[n]["p_rep"]=G.nodes()[n]["times"]/totalTimesAcs
        G.nodes()[n]["deg_centr"]=nx.degree_centrality(G)[n]
        totalDegCentr+=G.nodes()[n]["deg_centr"]
        entropiaShannonAcsDur+=(-G.nodes()[n]["p_dur"]*math.log(G.nodes()[n]["p_dur"],2))
        entropiaShannonAcsTimes+=(-G.nodes()[n]["p_rep"]*math.log(G.nodes()[n]["p_rep"],2))
    elif n[1] == 'i':
        G.nodes()[n]["p_dur"]=G.nodes()[n]["weight"]/totalDurInts
        G.nodes()[n]["p_rep"]=G.nodes()[n]["times"]/totalTimesInts
        G.nodes()[n]["deg_centr"]=nx.degree_centrality(G)[n]
        totalDegCentr+=G.nodes()[n]["deg_centr"]
        entropiaShannonIntsDur+=(-G.nodes()[n]["p_dur"]*math.log(G.nodes()[n]["p_dur"],2))
        entropiaShannonIntsTimes+=(-G.nodes()[n]["p_rep"]*math.log(G.nodes()[n]["p_rep"],2))
    elif any([n == ritmos[i][0] for i in range(len(ritmos))])==True: #OJO., para usar multipartite_layout, hay que etiquetar tuplas (hashable), no listas (unhashable)!!
        G.nodes()[n]["p_rep"]=G.nodes()[n]["times"]/totalTimesRit
        G.nodes()[n]["deg_centr"]=nx.degree_centrality(G)[n]
        totalDegCentr+=G.nodes()[n]["deg_centr"]
        entropiaShannonRitTimes+=(-G.nodes()[n]["p_rep"]*math.log(G.nodes()[n]["p_rep"],2))



for n in G.nodes():
    if n in [item[0] for item in notas]:
        G.nodes()[n]["p_centr"]=G.nodes()[n]["deg_centr"]/totalDegCentr
        entropiaShannonDegCentr+=(-G.nodes()[n]["p_centr"]*math.log(G.nodes()[n]["p_centr"],2))
    elif any([n == tuple(acordes[m][0]) for m in range(len(acordes))])==True:
        G.nodes()[n]["p_centr"]=G.nodes()[n]["deg_centr"]/totalDegCentr
        entropiaShannonDegCentr+=(-G.nodes()[n]["p_centr"]*math.log(G.nodes()[n]["p_centr"],2))
    elif n[1] == 'i':
        G.nodes()[n]["p_centr"]=G.nodes()[n]["deg_centr"]/totalDegCentr
        entropiaShannonDegCentr+=(-G.nodes()[n]["p_centr"]*math.log(G.nodes()[n]["p_centr"],2))
    elif any([n == ritmos[i][0] for i in range(len(ritmos))])==True: #OJO., para usar multipartite_layout, hay que etiquetar tuplas (hashable), no listas (unhashable)!!
        G.nodes()[n]["p_centr"]=G.nodes()[n]["deg_centr"]/totalDegCentr
        entropiaShannonDegCentr+=(-G.nodes()[n]["p_centr"]*math.log(G.nodes()[n]["p_centr"],2))

print("nodos: ", G.nodes(data=True))
print("\n Entropía de Shannon de Notas c.r. a la duración: ",entropiaShannonNotasDur)
print(" Entropía de Shannon de Notas c.r. a las repeticiones: ",entropiaShannonNotasTimes)
print("\n Entropía de Shannon de Acordes c.r. a la duración: ",entropiaShannonAcsDur)
print(" Entropía de Shannon de Acordes c.r. a las repeticiones: ",entropiaShannonAcsTimes)
print("\n Entropía de Shannon de Ritmos (c.r. a las repeticiones): ",entropiaShannonRitTimes)
print("\n Entropía de Shannon c.r. a la centralidad de grado: ",entropiaShannonDegCentr)
"""

"""
#Verificar que las distribuciones de probabilidad en realidad sumen 1: (en efecto suman 1)
suma=0
for n in G.nodes():
    suma+=G.nodes()[n]["p_centr"]
print("Suma de centralidades: ", suma)
suma2=0
suma3=0
suma4=0
for n in G.nodes():
    if n in [item[0] for item in notas]:
        suma2+=G.nodes()[n]["p_rep"] #cambiar tambien por p_dur
    elif any([n == tuple(acordes[m][0]) for m in range(len(acordes))])==True:
        suma3+=G.nodes()[n]["p_rep"] #cambiar tambien por p_dur
    elif any([n == ritmos[i][0] for i in range(len(ritmos))])==True: #OJO., para usar multipartite_layout, hay que etiquetar tuplas (hashable), no listas (unhashable)!!
        suma4+=G.nodes()[n]["p_rep"] #recuerda que los ritmos NO tienen atributo de duracion (sólo repeticiones)
print("Suma notas: ", suma2)
print("Suma acordes: ", suma3)
print("Suma ritmos: ", suma4)
"""

#print("notas_acs: ",notas_acs)
#print("notas_rit: ",notas_rit)


"""


pos=nx.multipartite_layout(G, scale=10) #regresa un dicc de la forma {nodo: array([x,y])}, donde [x,y] indica la posición del nodo
print('\nDiccionario de posiciones:\n',pos)
#array_op=lambda x: np.array([x[0],x[1]*100]) #OJO: al parecer, reescalar todas las posiciones en una coordenada no funciona, pues al dibuajar la gráfica se reescala el eje (se ve igual aunque sí cambie el valor numérico de la segunda coordenada)
#pos = {p:array_op(pos[p]) for p in pos}

for n in pos: #cambiamos las segundas coordenadas, según la clase del nodo
    if type(n)==int: #pitch classes
        pos[n][1]=pos[n][1]*4
    elif len(n)>1 and n[1]=='qL': #ritmos
        pos[n][1]=pos[n][1]*10
    elif len(n)>1 and n[1]=='i': #intervalos
        pos[n][1]=pos[n][1]*7
    else: #acordes / n-adas de intervalos (serán el mismo número)
        pos[n][1]=pos[n][1]*2
print('\nDiccionario de posiciones modificado:\n',pos)

colores_nodos=[]

for n in G.nodes():#crea lista de colores, según la clave que ya se puso antes
    colores_nodos.append(G.nodes()[n]["node_color"])
nx.draw_networkx(G,pos,node_color=colores_nodos)
plt.title("p-c-r graph")
plt.xlabel("{}".format(titulo))
plt.autoscale(False)
plt.tight_layout()
plt.show()

#quit()

#nx.draw_networkx_nodes(G,pos,nodelist=[item[0] for item in notas],node_color='springgreen',node_size=[50*item[1] for item in notas],alpha=0.5)#esta instrucción dibuja los nodos de la lista "notas" (pitch classes), asignando un tamaño según su duración total, y con una transparencia (alpha) constante
A=0#suma del total de ocurrencias de notas individuales (puede ser más que el número total de eventos, pues pueden aparecer repetidas en un mismo "evento" (acorde)). Esto lo calculamos para obtener transparencias entre 0 y 1 (único rango aceptable para el parámetro alpha (transparencia)) al dividir entre A el número de ocurrencias de cada nota
for i in range(len(notas)):
    A+=notas[i][2]
#print("A= ", A)
for i in range(len(notas)):
    nx.draw_networkx_nodes(G,pos,nodelist=[notas[i][0]],node_color='springgreen',node_size=[50*notas[i][1]],alpha=notas[i][2]/A)
for i in range(len(acordes)):
    #if len(acordes[i][0]) > 1:
        nx.draw_networkx_nodes(G,pos,nodelist=[acordes[i][0]],node_color='red',node_size=[1000*acordes[i][1]],alpha=acordes[i][2]/len(eventos))
for i in intervalos:
    nx.draw_networkx_nodes(G,pos,nodelist=[(i,'i')],node_color='purple',node_size=[100*intervalos[i][0]],alpha=intervalos[i][1]/len(eventos)) #OJO: intervalos es un diccionario cuyas claves tienen un valor que es una lista con dos entradas: dur total y ocurrencias
for i in range(len(ritmos)):#para asignar distintos grados de transparencia en el color de los nodos (parámetro alpha (float)), hay que asignarlo nodo por nodo (no admite listas como node_color o node_size)
    nx.draw_networkx_nodes(G,pos,nodelist=[ritmos[i][0]],node_color='blue',node_size=[50*ritmos[i][1]],alpha=ritmos[i][1]/len(eventos))
nx.draw_networkx_labels(G,pos)
nx.draw_networkx_edges(G,pos)
plt.title("weighted p-c-r graph")
plt.xlabel("{}".format(titulo))
plt.tight_layout()
plt.show()
#asignar pesos a nodos: generar contador de alturas, acordes, intervalos y duraciones
#asignar pesos a aristas




#Construccion de las Graficas de Notas, Acordes, Intervalos y Ritmos
GNotas=nx.Graph()
GAcs=nx.DiGraph()
GInts=nx.Graph()
GRit=nx.DiGraph()


colores_nodos_notas=[]
aristas_notas=[]

aristas_acs=[]
aristas_ints=[]
aristas_rit=[]

for n in G.nodes():
    if G.nodes()[n]["subset"] == 1: #se une cada clase de altura con otra si ambas pertenecen a un mismo acorde
        GNotas.add_node(n)
        colores_nodos_notas.append(G.nodes()[n]["node_color"])
        for edge in G.edges():
            if n in edge:
                i=1-edge.index(n)
                for x in G.neighbors(edge[i]):
                    if G.nodes()[x]["subset"]==1:
                        aristas_notas.append((n,x))
                        GNotas.add_edge(n,x)

    elif G.nodes()[n]["subset"] == 3:
        GInts.add_node(n)
        for j in range(len(intervalos_acs)):
            if len(intervalos_acs[j][0])>0 and n[0] in intervalos_acs[j][0]:
                for y in intervalos_acs[j][0]:
                    if y != n[0]:
                        GInts.add_edge(n,(y,'i'))
    elif G.nodes()[n]["subset"] == 4:
        GRit.add_node(n) #FALTA agregar flechas entre ritmos sucesivos
print("\n aristas_notas: ",aristas_notas)
print("\n aristas_intervalos: ", GInts.edges())



GAcs.add_weighted_edges_from([(par[0][0],par[0][1],par[1]) for par in eventos2_cons])
#print("GAcs nodos: " , GAcs.nodes(data=True))
print("\nOrden y tamaño gráfica de acordes: ", len(GAcs.nodes()), "nodos , ", len(GAcs.edges()), " aristas")

#agregar peso a las aristas
for e in GNotas.edges():
    GNotas.edges()[e]['width']=aristas_notas.count(e)
print("\nAristas GNotas: ", GNotas.edges(data=True))
width_notas=[GNotas[u][v]['width']/10 for u,v in GNotas.edges()]
pos=nx.shell_layout(GNotas)
for i in range(len(notas)):
    nx.draw_networkx_nodes(GNotas,pos,nodelist=[notas[i][0]],node_color='red',node_size=[100*notas[i][1]],alpha=notas[i][2]/A)
nx.draw_networkx_labels(GNotas,pos)
nx.draw_networkx_edges(GNotas,pos, width=width_notas)
plt.title("Vertical pitch class graph")
plt.xlabel("{}".format(titulo))
plt.tight_layout()
plt.show()



GNotas2=nx.DiGraph()

GNotas2_edge_width=[]
for par in eventos2_cons:
    for n in par[0][0]:
        GNotas2.add_weighted_edges_from([(n,k,par[1]) for k in par[0][1]])
        GNotas2_edge_width.append(par[1])
pos=nx.shell_layout(GNotas2)
for i in range(len(notas)):
    nx.draw_networkx_nodes(GNotas2,pos,nodelist=[notas[i][0]],node_color='turquoise',node_size=[100*notas[i][1]],alpha=notas[i][2]/A)

nx.draw_networkx_labels(GNotas,pos)
nx.draw_networkx_edges(GNotas2,pos,width=GNotas2_edge_width)
plt.title("Horizontal pitch class graph")
plt.xlabel("{}".format(titulo))
plt.tight_layout()
plt.show()




pos=nx.circular_layout(GAcs)
nx.draw_networkx_labels(GAcs,pos)
nx.draw_networkx_edges(GAcs,pos, width=[2*par[1] for par in eventos2_cons])
plt.title("Chord graph")
plt.xlabel("{}".format(titulo))
plt.tight_layout()
plt.show()



pos=nx.shell_layout(GInts)
nx.draw_networkx_labels(GInts,pos)
nx.draw_networkx_edges(GInts,pos, width=[1 for i in range(len(GInts.edges()))]) #falta poner el ancho de las aristas como un contador de ocurrencias
plt.title("Interval graph")
plt.xlabel("{}".format(titulo))
plt.tight_layout()
plt.show()

"""


"""
nx.draw_networkx(GNotas,pos=nx.shell_layout(GNotas),node_color=colores_nodos_notas)#esta ya se dibujó arriba
plt.show()

nx.draw_networkx_labels(GRit,pos)
nx.draw_networkx_edges(GRit,pos)
plt.tight_layout()
plt.show()
"""
"""
print("\nDensidad de la gráfica de alturas-acordes-ritmos: ", nx.density(G))
print("\nAglomeración promedio (average clustering) de la gráfica de alturas-acordes-ritmos: " , nx.average_clustering(G)) #agregar nx.eccentricity, nx.shortest_path_length??
"""

"""
# Análisis de Comunidades.

#Comunidades de alturas-acordes-ritmos
from networkx.algorithms import community
color_dict={1:'g',2:'mediumorchid',3:'r',4:'b'}
communities=community.greedy_modularity_communities(G)
print("# comunidades:", len(communities))
#graficar cada comunidad:
for i in range(len(communities)):
    print("    comunidad:", i+1, "  radio:" , nx.radius(G.subgraph(communities[i])), "  diámetro:", nx.diameter(G.subgraph(communities[i])) ,"  # nodos:",len(communities[i]), " # aristas:", len(G.subgraph(communities[i]).edges), "  0-nodos:", [n for n in G.subgraph(communities[i]).nodes if G.nodes()[n]["subset"]==1])
for i in range(len(communities)):
    print("\nGrado total y relativo de alturas en la comunidad", i+1, ":")
    for n in G.subgraph(communities[i]).nodes:
        if G.nodes()[n]["subset"]==1:
            print("    ",n, ":   ", G.degree(n), "  ",G.subgraph(communities[i]).degree(n), "  ",G.subgraph(communities[i]).degree(n)/G.degree(n))
    color_lista=[color_dict[i[1]] for i in G.subgraph(communities[i]).nodes.data("subset")]
    nx.draw_networkx(G.subgraph(communities[i]),node_color=color_lista)
    plt.title("p-c-r community #{}".format(i+1))
    plt.xlabel("{}".format(titulo))
    plt.tight_layout()
    plt.show()



#Comunidades de alturas verticales
print("\nAglomeración promedio (average clustering) de clases de alturas verticales: " , nx.average_clustering(GNotas)) #agregar nx.eccentricity, nx.shortest_path_length??
print("Densidad de la gráfica de clases de alturas verticales: ", nx.density(GNotas))
GNotass=GNotas.to_undirected() #el algoritmo de deteccion de comunidades de Networkx parece no funcionar con graficas dirigidas. para hacer deteccion de comunidades en graficas dirigidas, ver las librerias Infomap y OSLOM
communities_vpc=community.greedy_modularity_communities(GNotass)
print("\n# comunidades_acs:")#, len(communities_acs)
#graficar cada comunidad:
for i in range(len(communities_vpc)):
    print("    comunidad_alturas_verticales:", i+1, "  radio:" , nx.radius(GNotass.subgraph(communities_vpc[i])), "  diámetro:", nx.diameter(GNotass.subgraph(communities_vpc[i])) ,"  # nodos:",len(communities_vpc[i]), " # aristas:", len(GNotass.subgraph(communities_vpc[i]).edges))
for i in range(len(communities_vpc)):
    print("\nGrado total y relativo de acordes en la comunidad", i+1, ":")
    for n in GNotass.subgraph(communities_vpc[i]).nodes:
        print("    ",n, ":   ", GNotass.degree(n), "  ",GNotass.subgraph(communities_vpc[i]).degree(n), "  ",GNotass.subgraph(communities_vpc[i]).degree(n)/GNotass.degree(n))
    nx.draw_networkx(GNotas.subgraph(communities_vpc[i]), node_color='red')
    plt.title("Vertical pitch class community #{}".format(i+1))
    plt.xlabel("{}".format(titulo))
    plt.tight_layout()
    plt.show()




#Comunidades de alturas horizontales
print("\nAglomeración promedio (average clustering) de clases de alturas horizontales: " , nx.average_clustering(GNotas2)) #agregar nx.eccentricity, nx.shortest_path_length??
print("Densidad de la gráfica de clases de alturas horizontales: ", nx.density(GNotas2))
GNotas2s=GNotas2.to_undirected() #el algoritmo de deteccion de comunidades de Networkx parece no funcionar con graficas dirigidas. para hacer deteccion de comunidades en graficas dirigidas, ver las librerias Infomap y OSLOM
communities_hpc=community.greedy_modularity_communities(GNotas2s)
print("\n# comunidades_acs:")#, len(communities_acs)
#graficar cada comunidad:
for i in range(len(communities_hpc)):
    print("    comunidad_alturas_horizontales:", i+1, "  radio:" , nx.radius(GNotas2s.subgraph(communities_hpc[i])), "  diámetro:", nx.diameter(GNotas2s.subgraph(communities_hpc[i])) ,"  # nodos:",len(communities_hpc[i]), " # aristas:", len(GNotas2s.subgraph(communities_hpc[i]).edges))
for i in range(len(communities_hpc)):
    print("\nGrado total y relativo de acordes en la comunidad", i+1, ":")
    for n in GNotas2s.subgraph(communities_hpc[i]).nodes:
        print("    ",n, ":   ", GNotas2s.degree(n), "  ",GNotas2s.subgraph(communities_hpc[i]).degree(n), "  ",GNotas2s.subgraph(communities_hpc[i]).degree(n)/GNotas2s.degree(n))
    nx.draw_networkx(GNotas2.subgraph(communities_hpc[i]), node_color='turquoise')
    plt.title("Horizontal pitch class community #{}".format(i+1))
    plt.xlabel("{}".format(titulo))
    plt.tight_layout()
    plt.show()



#Comunidades de acordes:
print("\nAglomeración promedio (average clustering) de acordes: " , nx.average_clustering(GAcs)) #agregar nx.eccentricity, nx.shortest_path_length??
print("Densidad acordes: ", nx.density(GAcs))
GAcs2=GAcs.to_undirected() #el algoritmo de deteccion de comunidades de Networkx parece no funcionar con graficas dirigidas. para hacer deteccion de comunidades en graficas dirigidas, ver las librerias Infomap y OSLOM
communities_acs=community.greedy_modularity_communities(GAcs2)
print("\n# comunidades_acs:")#, len(communities_acs)
#graficar cada comunidad:
for i in range(len(communities_acs)):
    print("    comunidad_acs:", i+1, "  radio:" , nx.radius(GAcs2.subgraph(communities_acs[i])), "  diámetro:", nx.diameter(GAcs2.subgraph(communities_acs[i])) ,"  # nodos:",len(communities_acs[i]), " # aristas:", len(GAcs2.subgraph(communities_acs[i]).edges))
for i in range(len(communities_acs)):
    print("\nGrado total y relativo de acordes en la comunidad", i+1, ":")
    for n in GAcs2.subgraph(communities_acs[i]).nodes:
        print("    ",n, ":   ", GAcs2.degree(n), "  ",GAcs2.subgraph(communities_acs[i]).degree(n), "  ",GAcs2.subgraph(communities_acs[i]).degree(n)/GAcs2.degree(n))
    nx.draw_networkx(GAcs.subgraph(communities_acs[i]), node_color='orange')
    plt.title("Chord community #{}".format(i+1))
    plt.xlabel("{}".format(titulo))
    plt.tight_layout()
    plt.show()
"""

"""
#Análisis de ciclos dirigidos de acordes
ciclos_acs=[]
for ciclo in nx.simple_cycles(GAcs):
    if len(ciclo)>1:
        ciclos_acs.append(ciclo)
print("\nCiclos dirigidos de acordes: ", len(ciclos_acs))
for i in range(50):
    print("Ciclo  ", i, " : ", ciclos_acs[i])
#for ciclo in ciclos: #esto imprime todos los ciclos (pueden ser muchos (en el caso del Graffiti 1 de Luna, hay mas de 633,000!!! (aunque en los Graffitis 2 y 3 son muchos menos!))) Hay que encontrar una manera de elegir los principales (por peso de aristas)
if len(ciclos_acs)<5:
    for x in ciclos_acs:
        nx.draw_networkx(GAcs.subgraph(x), node_color='deeppink')
        plt.tight_layout()
        plt.show()
else:
    for i in range(5):
        nx.draw_networkx(GAcs.subgraph(ciclos_acs[i]), node_color='deeppink')
        plt.tight_layout()
        plt.show()
"""
"""
#Análisis de ciclos de acordes
ciclos_acs=[]
for ciclo in nx.cycle_basis(GAcs2):
    if len(ciclo)>1:
        peso_ciclo=0
        for e in GAcs2.subgraph(ciclo).edges():
            peso_ciclo+=GAcs2.subgraph(ciclo).edges()[e]['weight']
        ciclos_acs.append((ciclo,peso_ciclo))
ciclos_acs.sort(key = lambda x: x[1])
ciclos_acs.reverse()
#print("\nNúmero de ciclos simples de acordes: ", len(list(nx.simple_cycles(GAcs)))) #imprimir list(nx.simple_cycles(GAcs))?
print("\nTamaño de una base de ciclos de acordes: ", len(ciclos_acs))
print(ciclos_acs)
peso_ciclos_acs=0
for c in ciclos_acs:
    peso_ciclos_acs+=c[1]


#for ciclo in ciclos: #esto imprime todos los ciclos (pueden ser muchos (en el caso del Graffiti 1 de Luna, hay mas de 633,000!!! (aunque en los Graffitis 2 y 3 son muchos menos!))) Hay que encontrar una manera de elegir los principales (por peso de aristas)
if len(ciclos_acs)<5:
    for x in ciclos_acs:
        nx.draw_networkx(GAcs.subgraph(x[0]), node_color='deeppink')
        plt.title("Heaviest (by edges) basic chord cycle #{}".format(i+1))
        plt.xlabel("{}".format(titulo))
        plt.xlabel("\nCycle weight (sum of its edges' weights) / Total weight of basic cycles: {} / {}".format(x[1],peso_ciclos_acs))
        plt.tight_layout()
        plt.show()
else:
    for i in range(5):
        nx.draw_networkx(GAcs.subgraph(ciclos_acs[i][0]), node_color='deeppink')
        plt.title("Heaviest (by edges) basic chord cycle #{}".format(i+1))
        plt.xlabel("{}".format(titulo))
        plt.xlabel("\nCycle weight (sum of its edges' weights) / Total weight of basic cycles: {} / {}".format(ciclos_acs[i][1],peso_ciclos_acs))
        plt.tight_layout()
        plt.show()

#Conexidad de la grafica de acordes
print("\nConexidad por aristas de la gráfica de acordes: ", nx.edge_connectivity(GAcs)) #edge_connectivity considera el sentido de las flechas en una grafica dirigida
#Propiedad de Euler de Acordes (Eulerianidad??)
if nx.edge_connectivity(GAcs)>0:
    print("\nGráfica de acordes euleriana: ", nx.is_eulerian(GAcs))
    if nx.is_eulerian(GAcs):
        c=set()
        for e in nx.eulerian_circuit(GAcs):
            c.update([e[0],e[1]])
        print("   circuito euleriano: ", c )
        nx.draw_networkx(GAcs.subgraph(c), node_color="gold")
        plt.title("Eulerian chord circuit")
        plt.xlabel("{}".format(titulo))
        plt.tight_layout()
        plt.show()


print("\n") """
