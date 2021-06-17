"""
====================================
Filename:         quizMaker.py 
Author:              Joseph Farah 
Description:       Takes a glossary.tex file and parses it for keys and values,
                    then, makes a multiple choice quiz!
====================================
Notes
     
"""
    
#------------- imports -------------#
import sys
import random
import datetime

#------------- functions -------------#
def extract_from_glossary(glossary):

    if type(glossary) == type({'key':'value'}):
        print("You've got a formatted dictionary.")
        return glossary 

    elif type(glossary) == type(['list']):
        print("I'll convert this list into a dictionary.")

        glossary_dict = {}

        ## iterate over every line ##
        for line in glossary:

            ## split line to get key and value ##
            split_line = line.split('{')
            key = split_line[1].strip('}')
            value = split_line[2].strip('}\n')
            print(f"Key: <{key}> and value: <{value}> found.")

            ## add key and value to dictionary ##
            glossary_dict[key] = value

        return extract_from_glossary(glossary_dict)

    elif type(glossary) == type('file/path'):
        print("I'll load in this glossary.")

        ## load in glossary ##
        with open(glossary, "r") as gl_fo:
            lines = gl_fo.readlines()

        ## look for first line with a \defineterm ##
        ## ignore everything else ##
        salient_lines = []
        for line in lines:
            if 'defineterm' in line:
                salient_lines.append(line)

        ## pass list off to be reformatted ##
        return extract_from_glossary(salient_lines)


def make_quiz(glossary, multiple_choice=True, mix_key_value=True, num_q=10):

    glossary = extract_from_glossary(glossary)

    if num_q > len(glossary.keys()): 
        print(f"Number of questions requested greater than number of keys. num_q={len(glossary.keys())}.")
        num_q = len(glossary.keys())

    quiz_dict = {}
    for q in range(num_q):

        question_number = q

        ## pick random question ##
        question = 


#------------- execution -------------#


_fpath_glossary = './glossary.tex'
glossary = extract_from_glossary(_fpath_glossary)
for key in glossary:
    print(f"{key}: {glossary[key]}")


#------------- make quiz -------------#
