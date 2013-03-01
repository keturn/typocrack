"""typocrack: passphrase recovery by simulating typos on almost-known plaintext.
"""
from subprocess import call
import sys


def make_typos(basephrase, mutators):
    """Generate a series of strings, each of which is one typo off from the
    original string.
    """
    for mutator in mutators:
        for index in xrange(len(basephrase)):
            phrase = mutator(basephrase, index)
            yield phrase


def crack(basephrase, mutators, checker):
    """Check typos until we find the right one.

    :type basephrase: str
    :type mutators: list of f(phrase, index) -> str
    :type checker: f(str) -> bool
    :rtype: str or None
    :returns: the string that passes the checker.
    """
    for phrase in make_typos(basephrase, mutators):
        if checker(phrase):
            return phrase
    return None


## mutators

def double(phrase, index):
    return phrase[:index] + phrase[index] + phrase[index:]


def drop(phrase, index):
    return phrase[:index] + phrase[index + 1:]


def transpose(phrase, index):
    # can't transpose the last character.
    if len(phrase) - 1 == index:
        return phrase
    return (phrase[:index] + phrase[index + 1] + phrase[index] +
            phrase[index + 2:])


def caseflip(phrase, index):
    c = phrase[index]
    # shift-space is still space; the null byte is an unlikely typo
    # (and screws up our checker that spawns a subprocess.)
    if c == ' ':
        return phrase
    c = chr(ord(c) ^ 32)
    return phrase[:index] + c + phrase[index + 1:]


ALL = [drop, transpose, caseflip, double]


## checker

class ChangeKeyPassphrase(object):
    """Invokes ssh-keygen to try to change the passphrase on the keyfile.

    This has the side-effect of changing your key's passphrase when it succeeds.
    """
    keygen = '/usr/bin/ssh-keygen'

    def __init__(self, keyfile, new):
        self.keyfile = keyfile
        self.new = new

    def check(self, attempt):
        exitcode = call([self.keygen, '-p', '-P', attempt, '-N', self.new,
            '-f', self.keyfile])
        return exitcode == 0


def main():
    keyfile = sys.argv[1]
    basephrase = sys.argv[2]
    newphrase = sys.argv[3]
    checker = ChangeKeyPassphrase(keyfile, newphrase)
    cracked = crack(basephrase, ALL, checker.check)
    if cracked is not None:
        print "WIN:", cracked
        return 0
    print "exhausted :("
    return 1


if __name__ == '__main__':
    sys.exit(main())
