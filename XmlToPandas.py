from pathlib import Path
import pandas

import FileHandler


def _makeDataFrame( decisionData : str ):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup( decisionData, 'lxml' )
    tags = [ element.name for element in soup.find('body').findChildren() if element.name ]   
    frame = pandas.DataFrame( [ { key : soup.find(key).string for key in tags } ] )
    return frame


dataFolder = Path( __file__ ).parent / 'Data'
dataFileName = 'technical_english.txt'
with open( dataFolder / dataFileName, "r", encoding='ISO-8859-15' ) as file:

    count = 0
    frames = []
    while FileHandler.MoveToTag( "<Decision>", file ):
        count +=1
        if count % 100 == 0:
            print( '{0} frames so far.'.format( count ) )
        frames.append ( _makeDataFrame ( FileHandler.ReadToTag( '</Decision>', file ) ) )
    frame = pandas.concat( frames, ignore_index=True )
    print( frame[['ap', 'csn', 'boa']] )
    print( frame.columns )
    

