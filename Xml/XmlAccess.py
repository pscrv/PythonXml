from os import PathLike
from abc import ABC, abstractmethod, abstractproperty

from Xml.Decision import Decision
from Xml.XmlHandler import FileReader



class _searchResult( ABC ) :

        @abstractmethod
        def Add ( self, decision: Decision ) : ...

        @property
        @abstractmethod
        def Result ( self ) : ...


class _countResult( _searchResult ) :

    def __init__ ( self ) :
        self._result = 0

    def Add ( self, decision ) :
        self._result += 1

    @property
    def Result ( self ) :
        return self._result


class _listResult( _searchResult ) :

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

    def CountIfTagContains ( self, tag: str, needle: str ) :
        return self._accumulateIfTagContains( tag, needle, _countResult() )

    def GetIfTagContains ( self, tag: str, needle: str ) :
        return self._accumulateIfTagContains( tag, needle, _listResult() )

    def _accumulateIfTagContains ( self, tag: str, needle: str, result : _searchResult ) :
        with FileReader( self._filePath ) as reader :
            for decision in reader.IterateFromTo( '<Decision>', '</Decision>' ) :
                tagText = decision.GetTag( tag )
                if needle in tagText :
                    result.Add( decision )
        return result.Result

