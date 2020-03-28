from Monads.Mlist import Mlist


def f ( x ) : return Mlist( [ y * y for y in x ] )


def g ( x ) : return x + x


l = Mlist( [ 1, 2, 3 ] )

(lambda x : print( x, end=' ' )) * (g * l >> f)
