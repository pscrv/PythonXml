from pathlib import Path

from FileHandler import FileReader, FileWriter


_path = Path( __file__ ).parent / 'Data'
_technicalFile = _path / 'dump.txt'
_originalFile = _path / 'goodstuff.txt'


with FileReader( _originalFile, 'ISO-8859-15' ) as reader :
    with FileWriter( _technicalFile ) as writer :
        count = 0
        total = 0

        for decision in reader.IterateFromTo( '<Decision>', '</Decision>' ) :
            total += 1
            caseNumber = decision.GetTag( 'csn' )
            if caseNumber.strip( ' ' )[ 0 ] == 'T' :
                count += 1
                if count % 100 == 0 :
                    print( f'{count} technicals out of {total}.' )
                decision.AddTag( 'STUFF', 'Nothing, really')
                writer.WriteDecision( decision )

        print( f'Total:   {count} technicals out of {total}.' )
