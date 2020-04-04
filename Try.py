from Xml.Languages import *


path = Path( __file__ ).parent / 'Data'
inputFileName = 'sample.txt'
inputFile = path / inputFileName
TEFileName = 'EDump.txt'
TFFileName = 'FDump.txt'
TGFileName = 'GDump.txt'
outputFiles = { 'E': path / TEFileName, 'F' : path / TFFileName, 'G' : path / TGFileName }
predicate = Predicates.TagRegex( 'csn', 'W\d{4}/\d{2}')


splitter = LanguageSplitter ( inputFile, outputFiles )
splitter.SplitFile( predicate )
