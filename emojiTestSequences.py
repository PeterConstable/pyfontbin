# Script that reads the emoji-test.txt file and provides a list of emoji sequences

import sys
import re
import argparse
from pathlib import Path


class EmojiTestSequences(object):

    def __init__(self, fileName:str = None):
        self._fileName = fileName
        self._emojiTestPath = Path(self._fileName)
        self._getEmojiSequences()

    def _getEmojiSequences(self):
        self._emojiSequences = []
        with open(self._emojiTestPath, "r", encoding="utf-8") as emojiTestFile:
            for line in emojiTestFile:
                if line.startswith("#") or line == "\n":
                    continue
                line = line.strip()
                sequenceData = line.split("#")[0].strip()
                sequence = sequenceData.split(";")[0].strip().split()
                status = sequenceData.split(";")[1].strip()
                self._emojiSequences.append((sequence, status))

    def getEmojiSequences(self):
        return self._emojiSequences

'''
def getEmojiSequences(emojiTestPath):
    # returns list of tuples (emojiSequence, emojiName)
    emojiSequences = []
    with open(emojiTestPath, "r", encoding="utf-8") as emojiTestFile:
        for line in emojiTestFile:
            if line.startswith("#") or line == "\n":
                continue
            line = line.strip()
            sequenceData = line.split("#")[0].strip()
            sequence = sequenceData.split(";")[0].strip().split()
            status = sequenceData.split(";")[1].strip()
            emojiSequences.append((sequence, status))
    return emojiSequences
'''


def getFullyQualifiedSequences(emojiSequences):
    # returns list of sequences that are fully qualified
    return [sequence for sequence in emojiSequences if sequence[1] == "fully-qualified"]

def getMinimallyQualifiedSequences(emojiSequences):
    # returns list of sequences that are minimally qualified
    return [sequence for sequence in emojiSequences if sequence[1] == "minimally-qualified"]

def getUnqualifiedSequences(emojiSequences):
    # returns list of sequences that are unqualified
    return [sequence for sequence in emojiSequences if sequence[1] == "unqualified"]

def getComponentSequences(emojiSequences):
    # returns list of sequences that are components
    return [sequence for sequence in emojiSequences if sequence[1] == "component"]

def getZwjSequences(emojiSequences):
    # returns list of sequences that contain zwj
    return [sequence for sequence in emojiSequences if "200D" in sequence[0]]

def getNoZwjSequences(emojiSequences):
    # returns list of sequences that do not contain zwj
    return [sequence for sequence in emojiSequences if "200D" not in sequence[0]]

def getVSSequences(emojiSequences):
    # returns list of sequences that contain variation selectors
    return [sequence for sequence in emojiSequences if "FE0F" in sequence[0]]

def getNoVSSequences(emojiSequences):
    # returns list of sequences that do not contain variation selectors
    return [sequence for sequence in emojiSequences if "FE0F" not in sequence[0]]

'''
def getNoZwjNoVSSequences(emojiSequences):
    # returns list of sequences that do not contain zwj or variation selectors
    return [sequence for sequence in emojiSequences if "200D" not in sequence[0] and "FE0F" not in sequence[0]]
'''

def getSingleCharacterSequences(emojiSequences):
    # returns list of sequences that are single characters
    return [sequence for sequence in emojiSequences if len(sequence[0]) == 1]

def getRegionalIndicatorFlagSequences(emojiSequences):
    # returns list of sequences that are comprised of two regional indicator characters
    # regional indicator characters are in the range 1F1E6 - 1F1FF
    return [sequence for sequence in emojiSequences 
            if len(sequence[0]) == 2 
            and int(sequence[0][0], 16) >= int("1F1E6", 16) and int(sequence[0][0], 16) <= int("1F1FF", 16) 
            and int(sequence[0][1], 16) >= int("1F1E6", 16) and int(sequence[0][1], 16) <= int("1F1FF", 16)]

def getFlagEmojiTagSequences(emojiSequences):
    # returns list of flag emoji tag sequences -- these are sequences that begin with U+1F3F4
    # followed by one or more characters in the range U+E0061..U+E007A and ending with U+E007F
    result = []
    for sequence in emojiSequences:
        if sequence[0][0] == "1F3F4" and sequence[0][-1] == "E007F":
            if all([int(codePoint, 16) >= int("E0061", 16) and int(codePoint, 16) <= int("E007A", 16) for codePoint in sequence[0][1:-1]]):
                result.append(sequence)
    return result
            

def getEmojiSequencesWithStatus(emojiSequences, status):
    # returns list of sequences with the given status
    return [sequence for sequence in emojiSequences if sequence[1] == status]


def getStringFromSequence(characterSequence):
    # returns string from character sequence
    return "".join([chr(int(codePoint, 16)) for codePoint in characterSequence])



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get emoji sequences from emoji-test.txt")
    parser.add_argument("emojiTestPath", help="Path to emoji-test.txt")
    args = parser.parse_args()

    emojiTestPath = Path(args.emojiTestPath)
    if not emojiTestPath.exists():
        print("emoji-test.txt file not found")
        sys.exit(1)

    ets = EmojiTestSequences(args.emojiTestPath)

    emojiSequences = ets.getEmojiSequences()
    print("\n")
    print("Total emoji sequences: {}".format(len(emojiSequences)))
    print("Fully qualified emoji sequences: {}".format(len(getFullyQualifiedSequences(emojiSequences))))
    print("Minimally qualified emoji sequences: {}".format(len(getMinimallyQualifiedSequences(emojiSequences))))
    print("Unqualified emoji sequences: {}".format(len(getUnqualifiedSequences(emojiSequences))))
    print("Component emoji sequences: {}".format(len(getComponentSequences(emojiSequences))))
    print("Emoji ZWJ sequences: {}".format(len(getZwjSequences(emojiSequences))))
    print("Emoji no-ZWJ sequences: {}".format(len(getNoZwjSequences(emojiSequences))))
    print("Emoji sequences with variation selectors: {}".format(len(getVSSequences(emojiSequences))))
    print("Emoji sequences without variation selectors: {}".format(len(getNoVSSequences(emojiSequences))))

    print("Emoji sequences without ZWJ or VS: {}".format(len(getNoZwjSequences(getNoVSSequences(emojiSequences)))))
    print("Emoji single-character sequences: {}".format(len(getSingleCharacterSequences(emojiSequences))))
    print("Emoji single-character sequences not fully qualified: {}".format(len([s for s in getSingleCharacterSequences(emojiSequences) if s not in getFullyQualifiedSequences(emojiSequences)])))

    print("Emoji regional indicator flag sequences: {}".format(len(getRegionalIndicatorFlagSequences(emojiSequences))))
    print("Flag emoji tag sequences: {}".format(len(getFlagEmojiTagSequences(emojiSequences))))

    print("Sequence #2218: {}".format(getStringFromSequence(emojiSequences[2218][0])))
    print("ZWJ Sequence #734: {}".format(getStringFromSequence(getZwjSequences(emojiSequences)[734][0])))
