#! /usr/bin/env python

import os 
import codecs
import xml.etree.ElementTree as ET

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if (os.path.exists('./ParsedOutput.txt')):        
    os.remove('./ParsedOutput.txt')

fileOut = codecs.open('./ParsedOutput.txt', 'a+')

for item in os.listdir('./XibStringFiles'):

    # Ignore *.DS_Store files

    if (not item.endswith('.DS_Store')):

        filePath = './XibStringFiles/' + item

        fileIn = codecs.open(filePath, 'r', encoding='utf-16-le')

        if (os.stat('./XibStringFiles/' + item).st_size):

            if item.endswith('.strings'):

                finishedReading = False

                while (not finishedReading):

                    currLine = fileIn.readline()

                    if (not currLine):
                        finishedReading = True
                        break
                        
                    else:
                        
                        if (currLine[0] == u'/'):
                            continue
                            
                        if (currLine[0] == u'"'):
                            
                            lineLen = len(currLine)
                            beginningOfQuote = find_nth(currLine, '"', 3)
                            endOfQuote = find_nth(currLine, '"', 4)
                            stringToTranslate = currLine[beginningOfQuote + 1: -(lineLen - endOfQuote)]
                            stringLen = len(stringToTranslate)

                            # Rule of thumb says English strings translated to other languages are
                            # usually 30% longer in character length.
                            maxStringLen = int(round(stringLen + (.3 * stringLen)))
                            
                            # print a comma-separated 3-tuple of string, it's length
                            # and it's maximum translated length.
                            stringToTranslateTuple = stringToTranslate + '|' + str(stringLen) + '|'+ str(maxStringLen)
                            stringToTranslateTupleStripped = stringToTranslateTuple.lstrip(' ')
                            
                            stringToTranslateTupleStrippedOneLine = ''.join(stringToTranslateTupleStripped.splitlines()).replace('\t',' ') + '\n'
                            fileOut.write(stringToTranslateTupleStrippedOneLine.encode('utf-16-le'))
                            
            if item.endswith('.plist'):

                tree = ET.parse(filePath)
                root = tree.getroot()
                listofstrings = root.findall('array/dict/string')
                listofstringsnested = root.findall('array/dict/array/string')
                listofallstrings = listofstrings + listofstringsnested

                for stringitem in listofallstrings:
                    
                    stringitemtext = stringitem.text
                    
                    # in XCode plist files, numbers in the inner text
                    # of a <string> element can be disregarded
                    if (not is_number(stringitemtext)):
                        
                        stringLen = len(stringitemtext)
                        
                        # Rule of thumb says English strings translated to other languages are
                        # usually 30% longer in character length.
                        maxStringLen = int(round(stringLen + (.3 * stringLen)))
                        
                        # print a comma-separated 3-tuple of string, it's length
                        # and it's maximum translated length.
                        stringToTranslateTuple = stringitemtext + '|' + str(stringLen) + '|'+ str(maxStringLen)
                        stringToTranslateTupleStripped = stringToTranslateTuple.lstrip(' ')
                        stringToTranslateTupleStrippedOneLine = ''.join(stringToTranslateTupleStripped.splitlines()).replace('\t',' ') + '\n'

                        fileOut.write(stringToTranslateTupleStrippedOneLine.encode('utf-16-le'))
                        
            fileIn.close()

fileOut.close()            

