from os import PathLike
from abc import ABC, abstractmethod

from Xml.Decision import Decision
from Xml.Predicates import SearchPredicate
from Xml.XmlHandler import FileReader


class _searchAccumulator( ABC ) :

    def __init__ ( self, predicate: SearchPredicate ) :
        self._predicate = predicate

    @abstractmethod
    def Add ( self, decision: Decision ) : ...

    @property
    @abstractmethod
    def Result ( self ) : ...


class _countAccumulator( _searchAccumulator ) :

    def __init__ ( self, predicate: SearchPredicate ) :
        super().__init__( predicate )
        self._result = 0

    def Add ( self, decision ) :
        if self._predicate.Evaluate( decision ) :
            self._result += 1

    @property
    def Result ( self ) :
        return self._result


class _listAccumulator( _searchAccumulator ) :

    def __init__ ( self, predicate: SearchPredicate ) :
        super().__init__( predicate )
        self._result = [ ]

    def Add ( self, decision: Decision ) :
        if self._predicate.Evaluate( decision ) :
            self._result.append( decision )

    @property
    def Result ( self ) :
        return self._result


class _matchAndMismatchCountAccumulator( _searchAccumulator ) :

    def __init__ ( self, predicate: SearchPredicate ) :
        super().__init__( predicate )
        self._matchResult = 0
        self._mismatchResult = 0

    def Add ( self, decision: Decision ) :
        if self._predicate.Evaluate( decision ) :
            self._matchResult += 1
        else :
            self._mismatchResult += 1

    @property
    def Result ( self ) :
        return { 'Match' : self._matchResult, 'Mismatch' : self._mismatchResult }


class _matchAndMismatchListAccumulator( _searchAccumulator ) :

    def __init__ ( self, predicate: SearchPredicate ) :
        super().__init__( predicate )
        self._matchResult = [ ]
        self._mismatchResult = [ ]

    def Add ( self, decision: Decision ) :
        if self._predicate.Evaluate( decision ) :
            self._matchResult.append( decision )
        else :
            self._mismatchResult.append( decision )

    @property
    def Result ( self ) :
        return { 'Match' : self._matchResult, 'Mismatch' : self._mismatchResult }



class Accessor :

    def __init__ ( self, filePath: PathLike ) :
        self._filePath = filePath

    def CountMatches ( self, predicate: SearchPredicate ) :
        return self._search( _countAccumulator( predicate ) )

    def CountMatchesAndMismatches ( self, predicate : SearchPredicate ) :
        return self._search( _matchAndMismatchCountAccumulator( predicate ))

    def ListMatches ( self, predicate: SearchPredicate ) :
        return self._search( _listAccumulator( predicate ) )

    def ListMatchesAndMismatches ( self, predicate : SearchPredicate ) :
        return self._search( _matchAndMismatchListAccumulator( predicate ) )

    def _search ( self, result: _searchAccumulator ) :
        with FileReader( self._filePath ) as reader :
            for decision in reader.IterateFromTo( '<Decision>', '</Decision>' ) :
                result.Add( decision )
            return result.Result
