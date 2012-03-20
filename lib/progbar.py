#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

class progbar():
    def __init__(self,
                bar_type = 1,
                bar_char = "=",
                bar_term = ">",
                bar_len = 80        ):
        """standard initializer."""

        self.bar_type = bar_type
        self.bar_char = bar_char
        self.bar_term = bar_term
        self.bar_len = bar_len
        self.prog = 0
        self.value = 0

    def update(self, value = 0):
        """causes the bar to progress by 1 or to a specific percentage if such a percentage is specified by the value key."""
        # just tick the bar up one
        if(self.value == 0):
            self.prog += 1
            if self.prog >= (self.bar_len - 2):
                self.prog = 0

        else:
            self.prog = int(self.bar_len*value)
            self.value = value

        self._print()

    def reset(self):
        """resets the progress bar to 0%."""
        self.prog = 0
        self._print()

    def _print(self):
        sys.stdout.write("\r["+self.bar_char*self.prog+self.bar_term+" "*((self.bar_len-2)-self.prog)+"]")
        if self.bar_type == 1:
            sys.stdout.write(" "+str(self.value))
        sys.stdout.flush()
