from abc import ABC
from pathlib import Path
from typing import TextIO, Mapping

from Xml.Decision import Decision


def MoveToTag ( tag: str, file: TextIO ) :
    length = len( tag )
    for line in file :
        if line[ 0 : length ] == tag :
            return line
    return None


def ReadToTag ( tag: str, file: TextIO ) :
    length = len( tag )
    output = ''
    for line in file :
        if line[ 0 : length ] == tag :
            return Decision( output )
        output += line
    decision = Decision( output )
    return decision


def WriteDecision ( decision: Decision, file: TextIO ) :
    file.write( decision.GetDecision() )


class FileHandler( ABC ) :

    def __init__ ( self, file: Path, mode: str, encoding: str ) :
        self._file = file
        self._mode = mode
        self._encoding = encoding
        self._handle = None

    def __enter__ ( self ) :
        if not self._fileIsOpen() :
            # noinspection PyTypeChecker
            self._handle = open( self._file, self._mode, encoding=self._encoding )


    def __exit__ ( self, exceptionType, exceptionValue, exceptionTraceback ) :
        if self._handle is not None :
            self._handle.close()
            self._handle = None


    def _fileIsOpen ( self ) :
        return self._handle is not None






class FileReader( FileHandler ) :

    def __init__ ( self, file, encoding='utf_8' ) :
        super().__init__( file, 'r', encoding )

    def __enter__ ( self ) :
        super().__enter__()
        return self

    def ReadFromTo ( self, startTag: str, endTag: str ) :
        if not self._fileIsOpen() : raise self.FileReaderError( 'Please use with ... as ... ' )
        if self._moveToTag( startTag ) :
            return self._readToTag( endTag )
        return ''

    def IterateFromTo ( self, startTag: str, endTag: str ) :
        if not self._fileIsOpen() : raise self.FileReaderError( 'Please use with ... as ... ' )
        while self._moveToTag( startTag ) :
            yield self._readToTag( endTag )


    def _moveToTag ( self, tag: str ) :
        return MoveToTag( tag, self._handle )

    def _readToTag ( self, tag: str ) :
        return ReadToTag( tag, self._handle )

    class FileReaderError( Exception ) : ...




class FileWriter( FileHandler ) :

    def __init__ ( self, file, encoding='utf_8' ) :
        super().__init__( file, 'a', encoding )

    def __enter__ ( self ) :
        super().__enter__()
        return self

    def WriteDecision ( self, decision: Decision ) :
        if self._fileIsOpen() :
            WriteDecision( decision, self._handle )
        else :
            with self : self.WriteDecision( decision )



class MultipleFileWriter :

    def __init__ ( self, files: Mapping[ str, Path ], encoding='utf_8' ) :
        self._files = files
        self._encoding = encoding
        # self._writers = { key : FileWriter( file, encoding ) for (key, file) in files }

    def WriteDecision ( self, key: str, decision: Decision ) :
        if key in self._files :
            with FileWriter( self._files[ key ], self._encoding ) as writer :
                writer.WriteDecision( decision )

