from os import  PathLike

from Xml.XmlHandler import FileReader


class Accessor :

    def __init__ ( self, filePath : PathLike ) :
        self._filePath = filePath


    def CountIfTagContains ( self, tag : str, needle : str ) :
        return self._accumulateIfTagContains( tag, needle, 0, lambda x, y : x + 1 )

    def GetIfTagContains ( self, tag : str, needle : str ) :
        return self._accumulateIfTagContains( tag, needle, [], lambda x, y : x + [y] )


    def _accumulateIfTagContains ( self, tag: str, needle: str, accumulator, action ) :
        acc = accumulator
        with FileReader( self._filePath ) as reader :
            for decision in reader.IterateFromTo( '<Decision>', '</Decision>') :
                tagText = decision.GetTag( tag )
                if needle in tagText :
                    acc = action( acc, decision )
        return acc