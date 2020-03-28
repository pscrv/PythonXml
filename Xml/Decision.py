from bs4 import BeautifulSoup


class Decision :

    def __init__ ( self, raw: str ) :
        self._rawString = raw
        self._soup = None

    def _makeSoup ( self ) :
        self._soup = BeautifulSoup( self._rawString, 'lxml' )

    def _makeSoupIfNeeded ( self ) :
        if self._soup is None : self._makeSoup()

    def GetTag ( self, tag: str ) :
        self._makeSoupIfNeeded()
        return self._soup.find( tag ).text

    def AddTag ( self, tagName : str, tagContent : str ) :
        self._soup = None
        self._rawString += f'<{tagName}> {tagContent} </{tagName}>\n'

    def GetDecision ( self ) :
        return f'<Decision>\n{self._rawString}</Decision>\n'

