from abc import ABC, abstractmethod

from Monads.Monad import Monad



class Maybe ( Monad ):

    @classmethod
    def _unit( cls, value ) :
        return Just( value )




class Just ( Maybe ):

    def __init__( self, value ) :
        self._value = value


    def __str__( self ) :
        return f'Just {self._value}'
    

    def __eq__( self, other ) :
        if not isinstance(other, Just): return False
        return self._value == other._value 

    def __ne__( self, other ) :
        return not self.__eq__(other)


    def _fmap( self, f ) : 
        return Just( f ( self._value ) )

    def _bind( self, f ) :
        result = f( self._value )
        if not isinstance( result, Maybe ):
            raise TypeError ( f'{f} does not map to Maybe ' )
        return result




class Nothing ( Maybe ) :
    
    def __init__( self ) :
        pass

    def __str__( self ) :
        return 'Nothing'


    def __eq__( self, other ) :
        return isinstance ( other, Nothing )

    def __ne__( self, other ) :
        return not self.__eq__( other )



    def _fmap( self, f ) :
        return self

    def _bind( self, f ) :
        return self


