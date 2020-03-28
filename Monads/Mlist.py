
from Monads.Monad import Monad


class Mlist( Monad ) :
    
    def __init__( self, list : list ) :
        self._list = list

    def _fmap( self, f ) :
        return Mlist( [ f( x ) for x in self._list ] )

    def _bind( self, f ) :
        result = f( self._list )
        if not isinstance( result, Mlist ):
            raise TypeError ( f'{f} does not map to Mlist ' )
        return result


