#!/usr/bin/python3

import json
import subprocess
import random
import time
import re
import os
import datetime
from sys import platform

USERNAME="Inès"
USERNAME_UPPERCASE_POSSESSIVE="INES'"

praises = [
    'Nice job.', 'You rock!', 'You are so smart, %s.' % USERNAME,
    'I am proud of you.', 'Wow... keep up the good work',
    'Mega cool work, %s!' % USERNAME, 'So great!',
    'You really know your spelling words.',
    'I thought for sure I could trick you with that one.',
    'You really are doing well.',
    'How are you so good at spelling?  It is amazing!', 'Whoop! Whoop!',
    'Mighty nice!', 'Super great work!', 'Most excellent',
    'You are too cool for school', 'Freaking Awesome!', 'Wonderful!',
    'Marvelous!', 'Well done!', 'Wahoooo!  Nice!'
]


def correct(answer, word):
    return answer == word


def clear_screen():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system("clear")
    elif platform == "win32":
        os.system("cls")


def say(phrase):
    phrase = phrase.replace("!", ".")
    if platform == "linux" or platform == "linux2":
        # linux
        phrase = '"' + phrase + '"'
        #print ("Saying: ", phrase)
        #subprocess.call(["spd-say", phrase])
        subprocess.call(["./say.sh", phrase])
    elif platform == "darwin":
        # OS X
        subprocess.run(["say", phrase])
    elif platform == "win32":
        # print ("Windows cannot say: " + phrase)
        # Windows...
        no_apos = re.sub("'", "", phrase)
        win_cmd = "PowerShell -Command \"Add-Type -AssemblyName System.Speech;" + \
                  "(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('%s');\"" % no_apos
        subprocess.run(win_cmd)


def print_and_say(phrase):
    print(phrase)
    say(phrase)


def wait(seconds):
    # When using say.sh, the command only returns after the sentence is finished
    # so no need to wait.
    if platform == "linux" or platform == "linux2":
        return
    time.sleep(seconds)


def all_done(missed_words, total):
    with open("stats.csv", "a") as statsfile:
        statsfile.write("%s,%s\n" % (total, len(missed_words)))
    percent = 100*len(missed_words)/total
    print()
    if len(missed_words) == 0:
        say("Excellent!  I can't believe you got them all right, %s! You did great!" % USERNAME)
        print("NICE JOB, INES!  YOU GOT THEM ALL RIGHT!")
        print()
    else:
        if percent < 10:
            print_and_say("You did very good, {}! You only missed {} words out of {}:".format(USERNAME, len(missed_words), total))
        elif percent < 50:
            print_and_say("You did quite good, {}! You only missed {} words out of {}:".format(USERNAME, len(missed_words), total))
        elif percent < 100:
            print_and_say("You need to practice these words, {}! You missed {} words out of {}:".format(USERNAME, len(missed_words), total))
        else:
            print_and_say("Oh my gosh, what happened {}? You got no correct word out of {}!".format(USERNAME, total))
        print()
        print("These are the words you spelled incorrectly:")
        print()
        print(missed_words)
        with open("mistakes_%s.json" % datetime.datetime.now().replace(microsecond=0).isoformat().replace(':', '-'), 'w') as outfile:
          outfile.write(json.dumps(missed_words, indent=2))
        print()
        print('Press Enter to close')
        print()
        input()
    exit()


def select_word_list():
    files = [
        "bee_list_words.json",
        "eason_2019_easy.json",
        "eason_2019_medium.json",
        "eason_2019_hard.json",
        "eason_2019_knockout.json",
        "short_words.json",
        "medium_words.json",
        "long_words.json",
    ]
    files.extend([x for x in os.listdir() if x not in files and x.endswith(".json")])
    if len(files) == 0:
        print("ERROR: Couldn't find a word list!")
        return
    file = files[0]
    if len(files) > 1:
        print("Choose a list of words to practice:")
        maxfile = 0
        for i, f in enumerate(files):
            fn = f.replace(".json", "").replace("_", " ")
            print(" %s - %s" % (i+1, fn))
            maxfile = i+1
        say("Choose a list of words to practice")
        idx = 0
        while idx < 1 or idx > maxfile:
            try:
                idx = int(input("Which words do you want to practice (number from 1 to %s)? " % maxfile))
            except:
                pass
        file = files[idx-1]
    return file


def do_spelling():
    global praises
    clear_screen()

    print()
    print("                                              ***   {} SPELLING BEE PROGRAM:   ***".format(USERNAME_UPPERCASE_POSSESSIVE))
    print("                                                        (enter 'q' to quit)")
    print()
    print()
    print_and_say("Hello, {}.  Welcome to your spelling bee practice program.".format(USERNAME))
    wait(4)
    print()

    file = select_word_list()

    print()
    print_and_say("Press Enter to hear a word again. Answer 'q' to quit. Let's get started!")
    wait(4)
    print()

    words = json.load(open(file))
    word_count = 1
    word_tried = 0
    missed_words = {}

    to_spell = list(words.keys())
    random.shuffle(to_spell)
    for word in to_spell:
        if words[word] and 'sentence' in words[word]:
            sentence = words[word]['sentence']
        else:
            sentence = None

        if words[word] and 'pronounced' in words[word]:
            spoken_word = words[word]['pronounced']
            spoken_sentence = sentence.replace(word, spoken_word)
        else:
            spoken_word = word
            spoken_sentence = sentence

        print("Word #" + str(word_count) + ":  ")
        if sentence:
            display_text = sentence.replace(word, " __________")
            print(display_text)
        print("Type the letters to spell the word and press Enter:  ", end='')

        say_text = "Spell... " + spoken_word
        say(say_text)
        wait(1)
        if sentence:
            say(spoken_sentence)
            time.sleep(1)
            say(spoken_word)

        answer = 'nope, not the answer'
        while answer != word:
            answer = input().lower()
            if correct(answer, word):
                word_tried += 1
                say('That is correct!')
                # Let's praise from time to time on correct answer
                if word_count % 5 == 0:
                    index = random.randint(0, len(praises) - 1)
                    praise = praises[index]
                    say(praise)
            elif answer.lower() == 'q':
                all_done(missed_words, word_tried)
            elif not answer:
                say(spoken_word)
            else:
                word_tried += 1
                say("I'm sorry, that is incorrect.  It is spelled like this.")
                print(' '.join(word))
                wait(4)
                print("Type the letters to spell it and press enter:  ", end='')
                say("Please spell: " + word)
                missed_words[word] = answer
        wait(3)
        print
        word_count += 1

    all_done(missed_words, word_tried)


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    do_spelling()

