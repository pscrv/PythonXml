from pathlib import Path
from os import remove

import FileHandler
from Xml.Decision import Decision


class TestSet :
    path = Path( __file__ ).parent / 'Testdata'
    testFile = path / 'Test.txt'
    tag1content = 'Tag 1 content'
    tag2content = 'Tag 2 content'

    testDecisionText = '' \
                       '<Decision>' \
                       f'<tag1>{tag1content}</tag1>' \
                       f'<tag2>{tag2content}</tag2>' \
                       '</Decision>'

    testDecision = Decision( testDecisionText )

    def __enter__ ( self ) :
        return self

    def __exit__ ( self, exc_type, exc_val, exc_tb ) :
        import os
        os.remove( self.testFile )


def test_WriteRead () :
    with TestSet() as testSet :
        writer = FileHandler.FileWriter( testSet.testFile )
        writer.WriteDecision( testSet.testDecision )
        with FileHandler.FileReader( testSet.testFile ) as reader :
            read = reader.IterateFromTo( '<Decision>', '</Decision>' )
            decisions = [ x for x in read ]

        assert len( decisions ) == 1
        assert decisions[ 0 ].GetTag( 'tag1' ) == testSet.tag1content
        assert decisions[ 0 ].GetTag( 'tag2' ) == testSet.tag2content


def test_WriteRead_with () :
    with TestSet() as testSet :
        with FileHandler.FileWriter( testSet.testFile ) as writer :
            writer.WriteDecision( testSet.testDecision )
        with FileHandler.FileReader( testSet.testFile ) as reader :
            read = reader.IterateFromTo( '<Decision>', '</Decision>' )
            decisions = [ x for x in read ]

        assert len( decisions ) == 1
        assert decisions[ 0 ].GetTag( 'tag1' ) == testSet.tag1content
        assert decisions[ 0 ].GetTag( 'tag2' ) == testSet.tag2content


def test_DirDoesNotExist () :
    path = Path( __file__ ).parent / 'ThisDirectoryDoesNotExist'
    file = path / 'DoesNotMatter'

    try :
        with FileHandler.FileWriter( file ) as writer :
            writer.WriteDecision( Decision( "" ) )
            assert False, 'Expected FileNotFoundError was not thrown by FileWriter.'
    except FileNotFoundError :
        assert True
    except Exception as e :
        assert False, f'Exception {e} thrown by FileWriter, but FileNotFoundError was expected.'

    try :
        with FileHandler.FileReader( file ) as reader :
            reader.ReadFromTo( "", "" )
            assert False, 'Expected FileNotFoundError was not thrown by FileReader.'
    except FileNotFoundError :
        assert True
    except Exception as e :
        assert False, f'Exception {e} was thrown by FileReader, but FileNotFoundError was expected.'