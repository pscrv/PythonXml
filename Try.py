from pathlib import Path

from Xml.XmlAccess import Accessor


path = Path( __file__ ).parent / 'Data'
fileName = 'sample.txt'

accessor = Accessor( path / fileName )
count = accessor.CountIfTagContains( 'csn', 'T' )
decisions = accessor.GetIfTagContains( 'csn', 'W' )

print ( 'Decisions with W:')
for decision in decisions :
   print( decision.GetTag( 'ap' ) )

print ( f'Count of decisions with T: {count}')
