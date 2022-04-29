
import numpy as np
import persim
import ripser
import matplotlib.pyplot as plt
from doc_TDA_CS1 import TDA_acs_int_rit_pos



def bottleneckDistTDA_scores(file1,file2,inicios=[1,1],fines=[4,4],todos=[False,False],showTDAplots=[True,True],showScore=False,showChords=False,showBottleMatchPlots=True):
    dic_bottleneck={}
    dic_TDAcats={"dataeventosTDA": '$(ac(\overline {12} , \, ... \, , \overline {23}), dur , pos)$', "dataeventosB": '$(vectInt(ac), dur , pos)$', "dataeventosB_VectInt": '$vectInt(ac)$', "dataeventos_I12": "Acordes en $I^{12}$", "dataeventos_R12_Tam_Alt": 'Acordes en $\mathbb{R} ^{12} , c.a. \overline {12} - \overline {23}$', "dataeventos_R12_Int_Alt": r'$\beta (acs.(alt,int))$'}
    ind_diag1=file1.rfind('/')
    ind_diag2=file2.rfind('/')
    titulo1=file1[ind_diag1+1:]
    titulo2=file2[ind_diag2+1:]
    diccTDAdgms1=TDA_acs_int_rit_pos(file1,inicio=inicios[0],fin=fines[0],todo=todos[0],showTDAplots=showTDAplots[0],showScore=showScore,showChords=showChords)
    diccTDAdgms2=TDA_acs_int_rit_pos(file2,inicio=inicios[1],fin=fines[1],todo=todos[1],showTDAplots=showTDAplots[1],showScore=showScore,showChords=showChords)
    """
    contenido de un diccionario diccTDAdgms: cada valor es una lista, del tipo generado por ripser, que contiene, para cada dimensión, un numpy array con las parejas (b,d) del correspondiente diagrama de persistencia; es decir, son listas dadas por ripser(blablaaa....)['dgms']
    #ver el módulo: doc_TDA_CS1 o el archivo original complejosSimpliciales1_notas_acordes_intervalos_ritmos_sin_octavas_sin_inversiones.py
    diccTDAdgms["dataeventosTDA"] #corr. a TDA sobre tuplas de acordes con duración y posición de inicio
    diccTDAdgms["dataeventosB"] #corr. a TDA sobre vectores de intervalos con duración y posición de inicio
    diccTDAdgms["dataeventosB_VectInt"] #corr. a TDA sobre lo anterior, pero sin duración ni posición de inicio
    diccTDAdgms["dataeventos_I12"] #corr. a TDA sobre tuplas de acordes vistos en I^12
    diccTDAdgms["dataeventos_R12_Tam_Alt"] #corr. a TDA sobre tuplas de acordes vistos en R^12, con clases de altura representadas del 12 al 23, y ceros añadidos en las dimensiones vacías.
    diccTDAdgms["dataeventos_R12_Int_Alt"] #corr. a TDA sobre tuplas de acordes vistos en R^12, según altura e intervalo sobre cada una, a partir de la forma normal.
    """
    for x in diccTDAdgms1:
        #print('dicTDAdgms1[{}]:'.format(x))
        #print(diccTDAdgms1)
        #print('dicTDAdgms2[{}]:'.format(x))
        #print(diccTDAdgms2)
        l1=len(diccTDAdgms1[x])
        l2=len(diccTDAdgms2[x])
        dic_bottleneck[x]={}
        l=0
        if l1<=l2:
            l=l1
            for i in range(l):
                dgm1=diccTDAdgms1[x][i]
                dgm2=diccTDAdgms2[x][i]
                if len(dgm1)>=1 and len(dgm2)>=1:
                    distance_bottleneck, matching = persim.bottleneck(dgm1, dgm2, matching=True)
                    dic_bottleneck[x][i]=(distance_bottleneck,matching)
                    print("{} bottleneck distance for {} cc. {}-{} and {} cc. {}-{}: ".format(str(dic_TDAcats[x]),titulo1,inicios[0],fines[0],titulo2,inicios[1],fines[1]),distance_bottleneck)
                    if showBottleMatchPlots==True:
                        persim.bottleneck_matching(dgm1, dgm2, matching, labels=[titulo1[:-4]+' '+'-'+' '+'cc. {}-{}'.format(inicios[0],fines[0]),titulo2[:-4]+' '+'-'+' '+'cc. {}-{}'.format(inicios[1],fines[1])])
                        plt.title('{} bottleneck matching for $H_{}$'.format(str(dic_TDAcats[x]),str(i))+'\nBottleneck distance: {}'.format(str(distance_bottleneck)))
                        plt.show()
                else:
                    pass
        else:
            l=l2
            for i in range(l):
                dgm1=diccTDAdgms1[x][i]
                dgm2=diccTDAdgms2[x][i]
                if len(dgm1)>=1 and len(dgm2)>=1:
                    distance_bottleneck, matching = persim.bottleneck(dgm1, dgm2, matching=True)
                    dic_bottleneck[x][i]=(distance_bottleneck,matching)
                    print("{} bottleneck distance for {} cc. {}-{} and {} cc. {}-{}: ".format(str(dic_TDAcats[x]),titulo1,inicios[0],fines[0],titulo2,inicios[1],fines[1]),distance_bottleneck)
                    if showBottleMatchPlots==True:
                        persim.bottleneck_matching(dgm1, dgm2, matching, labels=[titulo1+' '+'-'+' '+'cc. {}-{}'+'\n'.format(inicios[0],fines[0]),titulo2+' '+'-'+' '+'cc. {}-{}'.format(inicios[1],fines[1])])
                        plt.title('{} bottleneck matching for $H_{}$'.format(str(dic_TDAcats[x]),str(i))+'\nBottleneck distance: {}'.format(str(distance_bottleneck)))
                        plt.show()
                else:
                    pass
    return dic_bottleneck

if __name__ == "__main__":
    titulo1='ALP-Graffiti1_JSB-t.mxl'
    titulo2='ALP-Graffiti1_JSB-t6.mxl'
    path1='/Users/alberto/Documents/doc/partituras_doc/'
    path2='/Users/alberto/Documents/doc/partituras_doc/'
    file1=path1+titulo1
    file2=path2+titulo2
    bottleneckDistTDA_scores(file1,file2,inicios=[1,1],fines=[4,4],showTDAplots=[False,False])
