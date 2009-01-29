#!/usr/bin/python
# vim: set fileencoding=utf-8 :

import re
import sys
import time
from datetime import datetime
from calendar import timegm
from dateutil import parser, tz

sys.path.append("/usr/share/gajim/src")
from common import i18n, gajim
from common.logger import Constants
constants = Constants()

class PidginLogParser():
    "Parse Pidgin (Gaim, Adium?) logs"

    filename = None
    dt = None
    timeadjust = 0

    def __init__(self, filename):
        print u"Parsing file %s:" % filename
        self.filename = filename
        self.FilenameParse()

        f = open(filename, 'r')
        for line in f:
            res = self.LineParse(line)
           # print res
            #if p.pos:
            #    print "%s: %s %s" % (p.direction, p.time, line[p.pos:]),

    _re_filename = re.compile(r"""
        (\d+)-(\d+)-(\d+)
        \.
        (\d\d)(\d\d)(\d\d)([+-]\d{4})(\w+)
    """, re.X | re.U | re.I)
    def FilenameParse(self):
        m = self._re_filename.search(self.filename).groups()
        self.dt = parser.parse("%s-%s-%s 00:00:00 %s" % (m[0:3]+m[6:7]))
        print self.dt


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

    _color2dir = {
        '16569E': constants.KIND_CHAT_MSG_SENT,
        'A82F2F': constants.KIND_CHAT_MSG_RECV,
    }

    def LineParse(self, line):
        m = self._re_log_line.match(line)
        if not m:
            return None
        t = parser.parse(m.group('time'), default = self.dt)
        t = timegm(t.utctimetuple())
        res = (
            self._color2dir[m.group('color')],
            parser.parse(m.group('time'), default = self.dt),
            t,
            m.group('nick'),
            m.group('log')
        )
        return res

if __name__ == '__main__':
    Parser = PidginLogParser("2009-01-22.143850+0300MSK.html")
    Parser = PidginLogParser("logs/2009-01-29.041110-0600CST.html")
    Parser = PidginLogParser("logs/2009-01-29.220829+0900YAKT.html")

# vim: et ts=4 sw=4
