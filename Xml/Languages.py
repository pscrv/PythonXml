from Xml import Predicates
from Xml.Decision import Decision



class _languagePredicate( Predicates.SearchPredicate ) :

    _fsuStrings = {
        'E' : 'Summary of facts',
        'F' : 'Faits et conclusions',
        'G' : 'Sachverhalt und'
        }

    _resStrings = {
        'E' : 'Reasons for the decision',
        'F' : 'Motifs de la décision',
        'G' : 'Entscheidungsgründe'
        }

    def __init__ ( self, language: str ) :
        if language not in self._resStrings : raise ValueError( 'language must be one of E, F, and G' )
        self._languageString = self._resStrings[ language ]
        self._predicate = None


    def Evaluate ( self, decision: Decision ) -> bool :
        if self._predicate is None :
            self._predicate = Predicates.TagContains_IgnoreCase ( 'res', self._languageString )
        result = self._predicate.Evaluate( decision )
        return result


class IsEnglish ( _languagePredicate ) :
    def __init__( self ) : super().__init__( 'E' )

class IsFrench ( _languagePredicate ) :
    def __init__( self ) : super().__init__( 'F' )

class IsGerman ( _languagePredicate ) :
    def __init__( self ) : super().__init__( 'G' )