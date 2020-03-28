from pathlib import Path
from bs4 import BeautifulSoup

from FileHandler import FileReader



class DecisionsAnalyser:
    
    __tags = [ 'AP', 'ART', 'BOA', 'CLR', 'CSN', 'CWD', 'DCI', 'DIS', 'FSU', 'HDN', 'HDW', 'IC', 'KEY', 'OFJ', 'OPP', 'ORD', 'PA', 'PD', 'PRL', 'RDE', 'REM', 'RES', 'TI' ]
  
    @staticmethod
    def _IsValidTag( tag : str ):
        return tag in DecisionsAnalyser.__tags
        


    def __init__ ( self, path : Path, filename : str ):
        self._path = path
        self._filename = filename



    def _findNext ( self, needle : str, tag : str, reader : FileReader ):
        if not DecisionsAnalyser._IsValidTag ( tag ):
            return None

        for decision in reader.IterateFromTo ( '<Decision>', '</Decision>'):
            soup = BeautifulSoup ( decision, 'lxml' )
            decisionTag = soup.find ( tag.lower() )
            if needle in decisionTag.text:
                return decision
        return None
        
    def _findAll ( self, needle : str, tag : str, reader : FileReader ):
        if not DecisionsAnalyser._IsValidTag ( tag ):
            return

        while True:
            result = self._findNext ( needle, tag, reader )
            if not result : 
                break
            yield result
        



    def FindNext ( self, needle : str, tag : str):
        if not DecisionsAnalyser._IsValidTag ( tag ):
            return None

        with FileReader ( self._path / self._filename ) as reader:
            return self._findNext ( needle, tag, reader )


    def FindAll ( self, needle : str, tag : str ):
        if not DecisionsAnalyser._IsValidTag ( tag ):
            return 

        with FileReader ( self._path / self._filename ) as reader:
            return self._findAll ( needle, tag, reader )
    

                











