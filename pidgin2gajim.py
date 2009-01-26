#!/usr/bin/python
# vim: set fileencoding=utf-8 :

import re
import time
import sys

class PidginLogParser():
    "Parse Pidgin (Gaim, Adium?) logs"

    filename = None
    timestamp = 0
    timeadjust = 0

    def __init__(self, filename):
        print u"Parsing file %s:" % filename
        self.filename = filename

        f = open(filename, 'r')
        for line in f:
            res = self.LineParse(line)
            print res
            #if p.pos:
            #    print "%s: %s %s" % (p.direction, p.time, line[p.pos:]),

    _re_log_line = re.compile(r"""
        <font\s+color="\#(?P<color>[0-9a-f]{6})">
        <font\s+size="2">\((?P<time>.+?)\)</font>
        \s+
        <b>(?P<nick>.+?):</b>
        </font>
        \s+
        (?P<log>.+)
        <br/>
    """, re.X | re.U | re.I)

    _color2dir = { '16569E' : '>>>', 'A82F2F' : '<<<' }

    def LineParse(self, line):
        m = self._re_log_line.match(line)
        if not m:
            return None
        res = (
            self._color2dir[m.group('color')],
            m.group('time'),
            m.group('nick'),
            m.group('log')
        )
        return res

if __name__ == '__main__':
    Parser = PidginLogParser("2009-01-22.143850+0300MSK.html")
    print sys.stdout.encoding
