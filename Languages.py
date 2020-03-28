from typing import Set
from pathlib import Path
from io import TextIOWrapper
from bs4 import BeautifulSoup

from FileHandler import FileReader, FileWriter


def _printSometimes( text : str, count : int ):
    if count % 100 == 0:
        print ( f'{text}: {count}' )


path = Path( __file__ ).parent / 'Data'
inputfile = path / 'uncertain.txt'
englishFile = path / 'dump.txt'
frenchFile = path / 'dump.txt'
germanFile = path / 'dump.txt'
uncertainFile = path / 'dump.txt'


englishCount = 0
frenchCount = 0
germanCount = 0
uncertainCount = 0

with FileReader( inputfile ) as reader:
    with FileWriter( englishFile ) as englishWriter:
        with FileWriter( frenchFile ) as frenchWriter:
            with FileWriter( germanFile ) as germanWriter:
                with FileWriter( uncertainFile ) as uncertainWriter:

                    for decision in reader.IterateFromTo( '<Decision>', '</Decision>' ):
                        soup = BeautifulSoup( decision, 'lxml' )
                        facts = soup.find('fsu').string


                        if facts and 'facts and submissions' in facts.lower():
                            englishCount += 1
                            _printSometimes( 'English', englishCount )
                            #englishWriter.WriteTag( decision, 'Decision' )

                        elif facts and 'faits et conclusions' in facts.lower():
                            frenchCount += 1
                            _printSometimes( 'French', frenchCount )
                            #frenchWriter.WriteTag( decision, 'Decision')

                        elif facts and 'sachverhalt und' in facts.lower():
                            germanCount += 1
                            _printSometimes( 'German', germanCount )
                            #germanWriter.WriteTag( decision, 'Decision')

                        else:
                            uncertainCount += 1
                            _printSometimes ( 'Uncertain', uncertainCount )
                            #uncertainWriter.WriteTag( decision, 'Decision' )

print( f'   English: {englishCount}' )
print( f'   French: {frenchCount}' )
print( f'   German: {germanCount}' )
print( f'   Uncertain: {uncertainCount}' )


        
