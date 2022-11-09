from bottleneckDistTDA_scores import bottleneckDistTDA_scores
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
#import numpy as np

path='/Users/alberto/Documents/doc/partituras_doc/'
#titles=['ALP-Graffiti1_JSB.mxl','JSB-ArtOfFugue-I.mid','ALP-Graffiti2_BB.mxl','Bartok-ConcOrch-I.mxl','ALP-Graffiti3_DB.mxl','DB-MyFavoriteThings.mxl','ALP-Graffiti8_FJH.mxl','Haydn-Symph88_1.mid']
titles=['JSB-Brandenburg1-I_BWV1046.mid','JSB-Brandenburg2-I_BWV1047.mid','DB-MyFavoriteThings.mxl','Webern-Concerto_Op.24.mxl','RagaAsawariJaunaPuri.mxl','Haydn-Symph88_1.mid']
files=[path+titles[i] for i in range(len(titles))]
lst_inicios=[1,1,22,1,48,17]
lst_fines=[4,4,25,4,51,20]
print(files)
l=len(files)
#OJO: probablemente despues haya que actualizar el siguiente diccionario de categorías de datos sobre las cuales correr el TDA
dic_TDAcats={"dataeventosTDA": '$(ac(\overline {12} , \, ... \, , \overline {23}), dur , pos)$', "dataeventosB": '$(vectInt(ac), dur , pos)$', "dataeventosB_VectInt": '$vectInt(ac)$', "dataeventos_I12": "Acordes en $I^{12}$", "dataeventos_R12_Tam_Alt": 'Acordes en $\mathbb{R} ^{12} , c.a. \overline {12} - \overline {23}$', "dataeventos_R12_Int_Alt": r'$\beta (acs.(alt,int))$'}
dic_bottleneck={}

for i in range(l):
    for j in range(i+1,l):
        dic=bottleneckDistTDA_scores(files[i],files[j],inicios=[lst_inicios[i],lst_inicios[j]],fines=[lst_fines[i],lst_fines[j]],showTDAplots=[False,False],showScore=False,showChords=False,showBottleMatchPlots=False)#esto da un diccionario de diccionarios
        dic_bottleneck['{},{}'.format(str(i),str(j))]={}
        for x in dic:#x es la categoria en dic_bottleneck y en dic (OJO: deben coincidir con las dadas en dic_TDAcats, que también se define explícitamente en el módulo bottleneckDistTDA_scores)
            lst=[]
            for k in dic[x]:#k es la dimensión (0-11)
                lst.append(dic[x][k][0]) #lista con las distancias entre diagramas de la cat. x, en cada dimensión k hasta la máxima que sea común a ambos conjuntos de datos. Los valores de dic[x][k] son parejas de la forma (bottleneck dist, matching), por eso se invoca la coord. [0]
                print('lst{}: '.format(str(k)),lst)
            dic_bottleneck['{},{}'.format(str(i),str(j))][x]=lst
print('\nBottleneck distances by pair of files and then TDA category and dimension (dic_bottleneck):\n')
print(dic_bottleneck)

dic0_bottleneck={}
dic1_bottleneck={}
for x in dic_TDAcats:
    dic0_bottleneck[x]=[]
    dic1_bottleneck[x]=[]
    for i in range(l):
        for j in range(i+1,l):
            lst=dic_bottleneck['{},{}'.format(str(i),str(j))][x]
            dic0_bottleneck[x].append(lst[0])
            if len(lst)>1:
                dic1_bottleneck[x].append(lst[1]) #OJO: esto funciona bien sólo si existen los diagramas de dim. 1 entre todos los objetos de la categoria correspondiente; si no, hay que ver cómo "guardar espacios" para que la dist. almacenada corresponda a los archivos correctos


print('\nBottleneck distances for $H_0$ diagrams by TDA category:\n')
print(dic0_bottleneck)
for x in dic0_bottleneck:
    print("Distance matrix for category {}".format(x))
    A=squareform(dic0_bottleneck[x])
    print(A)
    dists=dic0_bottleneck[x]
    linkage_matrix = linkage(dists, "single")
    dendrogram(linkage_matrix, labels=["{}".format(str(i))+"\n{}".format(titles[i][:-4])+"\ncc.{}-{}".format(lst_inicios[i],lst_fines[i]) for i in range(len(A))])
    plt.title('{} bottleneck matching for $H_0$'.format(str(dic_TDAcats[x])))
    plt.show()


print('\nBottleneck distances for $H_1$ diagrams by TDA category:\n')
print(dic1_bottleneck)
for x in dic1_bottleneck:#OJO: esto funciona bien sólo si existen los diagramas de dim. 1 entre todos los objetos de la categoria correspondiente; si no, hay que ver cómo "guardar espacios" para que la dist. almacenada corresponda a los archivos correctos
    if len(dic1_bottleneck[x])>0:
        print("Distance matrix for category {}".format(x))
        A=squareform(dic1_bottleneck[x])
        print(A)
        dists=dic1_bottleneck[x]
        linkage_matrix = linkage(dists, "single")
        dendrogram(linkage_matrix, labels=["{}".format(str(i))+"\n{}".format(titles[i][:-4])+"\ncc.{}-{}".format(lst_inicios[i],lst_fines[i]) for i in range(len(A))])
        plt.title('{} bottleneck matching for $H_1$'.format(str(dic_TDAcats[x])))
        plt.show()
