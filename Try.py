from pathlib import Path

from Xml.XmlAccess import Accessor
from Xml.Predicates import *
from Xml.Languages import *


path = Path( __file__ ).parent / 'Data'
fileName = 'sample.txt'

accessor = Accessor( path / fileName )


tCasePredicate = TagRegex( 'csn', 'T\d{4}/\d{2}' )
unknownLanguagePredicate = Not( Or( IsEnglish(), Or( IsFrench(), IsGerman() ) ) )


predicate = tCasePredicate

result = accessor.MatchesAndMismatchesCount( predicate )
print( result )

result = accessor.MatchesAndMismatchesIterator( { 'en': IsEnglish(), 'fr': IsFrench(), 'de': IsGerman(), 'T' : tCasePredicate } )
for x in result :
    for (label, decision) in x.items() :
        print( f'{label}:    {decision.GetTag( "csn" )}' )

