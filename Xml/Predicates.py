from abc import ABC, abstractmethod
import re


from Xml.Decision import Decision


class SearchPredicate( ABC ) :

    @abstractmethod
    def Evaluate ( self, decision: Decision ) -> bool : ...


class PredicateList( SearchPredicate ) :

    def __init__ ( self ) :
        self._predicateList = set()

    def Add ( self, predicate: SearchPredicate ) :
        self._predicateList.add( predicate )
        return self

    def Evaluate ( self, decision: Decision ) -> bool :
        resultList = [ x.Evaluate( decision ) for x in self._predicateList ]
        return all( resultList )


class Combiner( SearchPredicate ) :

    @abstractmethod
    def _combine ( self, first: bool, second: bool ) -> bool : ...

    def __init__ ( self, first: SearchPredicate, second: SearchPredicate ) :
        self._first = first
        self._second = second

    def Evaluate ( self, decision: Decision ) -> bool :
        return self._combine( self._first.Evaluate( decision ), self._second.Evaluate( decision ) )


class And( Combiner ) :

    def _combine ( self, first: bool, second: bool ) -> bool :
        return first and second


class Or( Combiner ) :

    def _combine ( self, first: bool, second: bool ) -> bool :
        return first or second


class Not( SearchPredicate ) :

    def __init__ ( self, predicate: SearchPredicate ) :
        self._predicate = predicate

    def Evaluate ( self, decision: Decision ) -> bool :
        return not self._predicate.Evaluate( decision )


class TagContains( SearchPredicate ) :

    def __init__ ( self, tag: str, needle: str ) :
        self._tag = tag
        self._needle = needle

    def Evaluate ( self, decision: Decision ) -> bool :
        return self._needle in decision.GetTag( self._tag )


class TagContains_IgnoreCase( TagContains ) :

    def Evaluate ( self, decision: Decision ) -> bool :
        return self._needle.lower() in decision.GetTag( self._tag ).lower()


class TagRegex( SearchPredicate ) :

    def __init__ ( self, tag : str, pattern : str ) :
        self._tag = tag
        self._expression = re.compile( pattern )

    def Evaluate( self, decision: Decision ) -> bool :
        result = self._expression.search( decision.GetTag( self._tag ) )
        return result is not None
