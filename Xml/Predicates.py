from abc import ABC, abstractmethod

from Xml.Decision import Decision


class _searchPredicate ( ABC ) :

    @abstractmethod
    def Evaluate ( self, decision : Decision ) -> bool : ...


class TagContains ( _searchPredicate ) :

    def __init__( self, tag : str, needle : str ) :
        self._tag = tag
        self._needle = needle

    def Evaluate ( self, decision: Decision ) -> bool :
        return self._needle in decision.GetTag( self._tag )


class PredicateList ( _searchPredicate ) :

    def __init__( self ) :
        self._predicateList = set()

    def Add (self, predicate : _searchPredicate ) :
        self._predicateList.add( predicate )
        return self

    def Evaluate ( self, decision: Decision ) -> bool :
        resultList = [ x.Evaluate( decision ) for x in self._predicateList ]
        return all( resultList )


class Combiner ( _searchPredicate ) :

    @abstractmethod
    def _combine ( self, first : bool, second : bool ) -> bool : ...

    def __init__( self, first : _searchPredicate, second : _searchPredicate ) :
        self._first = first
        self._second = second

    def Evaluate ( self, decision: Decision ) -> bool :
        return self._combine( self._first.Evaluate( decision ), self._second.Evaluate( decision ) )


class And ( Combiner ) :

    def _combine ( self, first: bool, second: bool ) -> bool :
        return first and second


class Or ( Combiner ) :

    def _combine ( self, first: bool, second: bool ) -> bool :
        return first or second


class Not ( _searchPredicate ) :

    def __init__( self, predicate : _searchPredicate ):
        self._predicate = predicate

    def Evaluate( self, decision : Decision ) -> bool:
        return not self._predicate.Evaluate( decision )