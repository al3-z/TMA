import music21 as m21

def getIntBajoFin(score):
    intPC=score.parts[-1][-1].getElementsByClass('Note')[-1].pitch.pitchClass
    int=m21.interval.Interval(-intPC)
    return int

def transpBajoFin(score,frag):
    int=getIntBajoFin(score)
    scoreT=frag.transpose(int)
    return scoreT, int

if __name__ == "__main__":
    titulo="ALP-Graffiti1_JSB"
    score=m21.converter.parse('/Users/alberto/Documents/doc/partituras_doc/{}.mxl'.format(titulo))
    acs=score.measures(1,4).chordify()
    print('\n     ===   Showing original fragment.   ===     ')
    acs.show()
    pausa=input('\n-----> Press any key to show transposed fragment...')
    transpBajoFinRes=transpBajoFin(score,acs)
    acsT=transpBajoFinRes[0]
    print('\n     ===   Showing fragment transposed by interval {}.   ===     '.format(str(transpBajoFinRes[1].directedName))+'\n')
    acsT.show()
