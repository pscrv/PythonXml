from bs4 import BeautifulSoup


Tags = [ 'AP', 'ART', 'BOA', 'CLR', 'CSN', 'CWD', 'DCI', 'DIS', 'FSU', 'HDN', 'HDW', 'IC', 'KEY', 'OFJ', 'OPP', 'ORD',
         'PA', 'PD', 'PRL', 'RDE', 'REM', 'RES', 'TI' ]


class DuplicateTagError( Exception ) : ...


class Decision :

    def __init__ ( self, raw: str ) :
        self._rawString = raw
        self._soup = None

    def _makeSoup ( self ) :
        self._soup = BeautifulSoup( self._rawString, 'html.parser' )

    def _makeSoupIfNeeded ( self ) :
        if self._soup is None : self._makeSoup()

    def HasTag ( self, tagName: str ) :
        self._makeSoupIfNeeded()
        found = self._soup.find( tagName.lower() )
        return found is not None


    def HasAllValidTags( self ) :
        hasTags = [ self.HasTag( tag ) for tag in Tags ]
        return all( hasTags )

    def HasOnlyValidTags( self ) :
        self._makeSoupIfNeeded()
        tags = self._soup.find_all()
        names = [ tag.name for tag in tags ]
        valid = [ name.upper() in Tags for name in names ]
        return all( valid )


    def GetTag ( self, tag: str ) :
        self._makeSoupIfNeeded()
        tag = self._soup.find( tag.lower() )
        return '' if tag is None else tag.text

    def AddTag ( self, tagName: str, tagContent: str ) :
        if self.HasTag( tagName ) :
            raise DuplicateTagError( tagName )

        self._soup = None
        self._rawString += f'<{tagName}>{tagContent}</{tagName}>\n'

    def GetDecision ( self ) :
        return f'<Decision>\n{self._rawString}</Decision>\n'
