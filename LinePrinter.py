class LinePrinter:

    def __init__ ( self ):
        self._line = ''
        self._positions = { }

    def __enter__ ( self ):
        return self

    def __exit__ ( self, exceptionType, exceptionValue, exceptionTraceback ):
        print()

    def _print ( self, line : str ):
        print ( f'\r{line}', end='' )

    def Print ( self, line : str ):
        
        padLength = max ( len ( self._line ) - len ( line ), 0 )
        self._line = line
        self._print ( line + ( ' ' * padLength ) )


    def PrintAt ( self, key : str, text : str ):
        if not key in self._positions:
            raise ValueError ( f'Key = {key} has not been defined.' )

        start = self._positions[ key ]
        end = start + len ( text ) - 1
        if end > len ( self._line ):
            padLength = end - len ( self._line )
            self._line += ' ' * padLength 

        pre = self._line[ 0 : start ]
        post = self._line[ end + 1 : ]
        self.Print ( pre + text + post )


    def SetPosition ( self, key : str, index : int ):
        if index < 0: 
            raise ValueError ( f'Value index = {index} : may not be negative.' )
        
        self._positions[ key ] = index
