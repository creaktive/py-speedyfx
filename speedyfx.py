# -*- coding: utf-8 -*-
import sys

class SpeedyFx:
    length = 256
    code_table = [0] * length

    def __init__(self, seed=1):
        fold_table = [0] * self.length
        rand_table = [seed] + [0] * (self.length - 1)

        for i in xrange(1, self.length):
            #j = unichr(i)
            j = chr(i)
            if (j.isalnum()):
                fold_table[i] = ord(j.lower())
            else:
                fold_table[i] = 0
            rand_table[i] = rand_table[i - 1]
            rand_table[i] *= 0x10a860c1
            rand_table[i] &= 0xffffffff
            rand_table[i] %= 0xfffffffb

        for i in xrange(self.length):
            if (fold_table[i]):
                self.code_table[i] = rand_table[fold_table[i]]

    def hash(self, string):
        result = {}
        wordhash = 0

        for c in string:
            code = self.code_table[ord(c) % self.length]
            if (code):
                wordhash = (wordhash >> 1) + code
            elif (wordhash):
                if (wordhash in result):
                    result[wordhash] += 1
                else:
                    result[wordhash] = 1
                wordhash = 0

        if (wordhash):
            if (wordhash in result):
                result[wordhash] += 1
            else:
                result[wordhash] = 1

        return result

    def hash_min(self, string):
        minhash = sys.maxint
        wordhash = 0

        for c in string:
            code = self.code_table[ord(c) % self.length]
            if (code):
                wordhash = (wordhash >> 1) + code
            elif (wordhash):
                minhash = min(minhash, wordhash)
                wordhash = 0

        if (wordhash):
            minhash = min(minhash, wordhash)

        return minhash

sfx = SpeedyFx()
str = 'To be or not to be?'
print sfx.hash(str)
print sfx.hash_min(str)
