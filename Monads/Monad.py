from abc import ABC, abstractmethod

class Monad ( ABC ) :

    @abstractmethod
    def _bind( self, f ) : pass

    @abstractmethod
    def _fmap( self, f ) : pass


    def __rshift__( self, f ) :

        def _raiseTypeError() :
            raise TypeError("Operator '>>' must return a Monad.")

        if callable( f ) : 
            result = self._bind( f ) 
            return result if isinstance( result, Monad ) else _raiseTypeError()
        
        return self._bind( lambda _ : f ) if isinstance( f, Monad ) else _raiseTypeError()


    def __rmul__( self, f ) :
        return self._fmap( f )
