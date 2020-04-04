from pathlib import  Path
from typing import Mapping

from Xml import Predicates
from Xml.Decision import Decision
from Xml.XmlAccess import Accessor
from FileHandler import MultipleFileWriter



class _languagePredicate( Predicates.SearchPredicate ) :

    _fsuStrings = {
        'E' : 'Summary of facts',
        'F' : 'Faits et conclusion', #There is one case with "conclusion" instead of "conclusions"
        'G' : 'Sachverhalt und'
        }

    _resStrings = {
        'E' : 'Reasons for the decision',
        'F' : 'Motifs de la décision',
        'G' : 'Entscheidungsgründe'
        }

    def __init__ ( self, language: str ) :
        if language not in self._resStrings : raise ValueError( 'language must be one of E, F, and G' )
        self._languageString = self._fsuStrings[ language ]
        self._predicate = None


    def Evaluate ( self, decision: Decision ) -> bool :
        if self._predicate is None :
            self._predicate = Predicates.TagContains_IgnoreCase ( 'fsu', self._languageString )
        result = self._predicate.Evaluate( decision )
        return result


class IsEnglish ( _languagePredicate ) :
    def __init__( self ) : super().__init__( 'E' )

class IsFrench ( _languagePredicate ) :
    def __init__( self ) : super().__init__( 'F' )

class IsGerman ( _languagePredicate ) :
    def __init__( self ) : super().__init__( 'G' )


class LanguageSplitter :

    _predicates = { 'F' : IsFrench(), 'G' : IsGerman(), 'E' : IsEnglish() }

    def __init__( self, inputFile : Path, outputFiles : Mapping[ str, Path ]) :
        if not self._hasValidKey( outputFiles ) : self._raiseKeyError()
        self._inputFile = inputFile
        self._writer = MultipleFileWriter( outputFiles )


    def SplitFile ( self, predicate : Predicates.SearchPredicate = None ) :
        for result in Accessor ( self._inputFile ).MatchesDictionaryIterator( self._assemblePredicates( predicate ) ) :
            for ( language, decision ) in result.items() :
                self._writer.WriteDecision( language, decision )


    def _raiseKeyError ( self ) :
        raise ValueError( f'There must be exactly {len( self._predicates )} keys: {self._predicates.keys()}' )

    def _hasValidKey ( self, mapping : Mapping[ str, Path ]  ) :
        lengthIsValid = len ( mapping ) == len( self._predicates )
        keyValuesAreValid = all( [ x in mapping for x in self._predicates.keys() ] )
        return lengthIsValid and keyValuesAreValid

    def _assemblePredicates ( self, predicate ) :
        if predicate is None :
            return self._predicates
        else :
            return { k : Predicates.And( v, predicate ) for (k, v) in self._predicates.items() }



