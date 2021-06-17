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
import copy
import time
import random
import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def warning(message):
        print (bcolors.WARNING + "[" + message + "]" + bcolors.ENDC)

    @staticmethod
    def success(message):
        print (bcolors.OKGREEN + "[" + message + "]" + bcolors.ENDC)

    @staticmethod
    def failure(message):
        print (bcolors.FAIL + "[" + message + "]" + bcolors.ENDC)



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
            value = split_line[2].strip('}\n').strip(r'See \autoref')
            # print(f"Key: <{key}> and value: <{value}> found.")

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


def generate_quiz(glossary, multiple_choice=True, mix_key_value=True, num_q=10, num_options=4):

    glossary = extract_from_glossary(glossary)

    if num_q > len(glossary.keys()): 
        print(f"Number of questions requested greater than number of keys. num_q={len(glossary.keys())}.")
        num_q = len(glossary.keys())

    quiz_dict = {}
    for q in range(num_q):

        question_number = q

        ## pick random question ##
        question = random.choice(list(glossary.keys()))
        correct_answer = glossary[question]

        ## generate incorrect options ##
        incorrect_options = [glossary[key] for key in random.sample(glossary.keys(), num_options-1)]

        ## make sure correct answer isn't among them ##
        while correct_answer in incorrect_options:
            incorrect_options.remove(correct_answer)

        ## add quiz question ##
        quiz_dict[question_number] = {'question':question, 'answer':correct_answer, 'incorrect_options':incorrect_options}


    return quiz_dict


def take_quiz(quiz):

    input("Ready to begin quiz?\n")
    
    start_time = time.time()

    shuffled_question_nums = random.sample(quiz.keys(), k=len(quiz.keys()))

    correct = 0
    for question_num in shuffled_question_nums:
        print(f"{quiz[question_num]['question']}?")
        print("Options:")
        answers = copy.copy(quiz[question_num]['incorrect_options'])
        answers.append(quiz[question_num]['answer'])
        random.shuffle(answers)
        correct_answer_num = answers.index(quiz[question_num]['answer'])+1
        for a, answer in enumerate(answers):
            print(f"({a+1}). {answer}")

        guess = input("Your choice\n>>> ")

        if int(guess) == correct_answer_num: 
            bcolors.success("Correct!")
            correct+=1
        else: bcolors.failure("Wrong!")

    bcolors.success(f"You scored {100*float(correct/len(quiz.keys()))}%.")


#------------- execution -------------#


_fpath_glossary = './glossary.tex'
glossary = extract_from_glossary(_fpath_glossary)
# for key in glossary:
#     print(f"{key}: {glossary[key]}")


#------------- make quiz -------------#
quiz = generate_quiz(glossary, num_q=4)


#------------- take quiz -------------#
take_quiz(quiz)