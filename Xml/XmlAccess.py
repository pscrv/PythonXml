from os import PathLike
from abc import ABC, abstractmethod

from Xml.Decision import Decision
from Xml.Predicates import SearchPredicate
from Xml.XmlHandler import FileReader



class _searchAccumulator( ABC ) :

        @abstractmethod
        def Add ( self, decision: Decision ) : ...

        @property
        @abstractmethod
        def Result ( self ) : ...


class _countAccumulator( _searchAccumulator ) :

    def __init__ ( self ) :
        self._result = 0

    def Add ( self, decision ) :
        self._result += 1

    @property
    def Result ( self ) :
        return self._result


class _listAccumulator( _searchAccumulator ) :

        def __init__ ( self ) :
            self._result = [ ]

        def Add ( self, decision: Decision ) :
            self._result.append( decision )

        @property
        def Result ( self ) :
            return self._result


class Accessor :

    def __init__ ( self, filePath: PathLike ) :
        self._filePath = filePath


    def CountSearch ( self, predicate : SearchPredicate ) :
        return self._predicateSearch( predicate, _countAccumulator() )

    def ListSearch ( self, predicate : SearchPredicate ) :
        return self._predicateSearch( predicate, _listAccumulator() )

    def _predicateSearch ( self, _predicate : SearchPredicate, result : _searchAccumulator ) :
        with FileReader( self._filePath ) as reader :
            for decision in reader.IterateFromTo( '<Decision>', '</Decision>' ) :
                if _predicate.Evaluate ( decision ) :
                    result.Add( decision )
            return result.Result



