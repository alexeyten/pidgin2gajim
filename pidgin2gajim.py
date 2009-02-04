#!/usr/bin/python
# vim: set fileencoding=utf-8 :

import re
import sys
import time
from datetime import datetime, timedelta
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
    lasttimestamp = 0
    jid = None

    def __init__(self, filename):
        print u"Parsing file %s:" % filename
        self.filename = filename
        self.FilenameParse()

        f = open(filename, 'r')
        self.FirstLineParse(f.next())

        for line in f:
            res = self.LineParse(line)
            if res == None:
                print line
            else:
                print time.ctime(res[2])

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

    _re_firstline = re.compile(r"Conversation with (.+?) at", re.U)

    def FirstLineParse(self, line):
        m = self._re_firstline.search(line)
        self.jid = m.group(1)
        if re.match(r"^\d+$", self.jid):
            self.jid += "@ICQ"

    _re_log_line = re.compile(r"""
        <font\s+color="\#(?P<color>[0-9a-f]{6})">
        <font\s+size="2">\((?P<time>.+?)\)</font>
        \s+
        <b>(?P<nick>.+?):?</b>
        </font>
        \s+
        (?P<log>.+)
        <br/>
    """, re.X | re.U | re.I)

    _color2dir = {
        '16569E': constants.KIND_CHAT_MSG_SENT,
        'A82F2F': constants.KIND_CHAT_MSG_RECV,

        '062585': "GUESS",
    }

    def LineParse(self, line):
        m = self._re_log_line.match(line)
        if not m:
            return None
        t = parser.parse(m.group('time'), default = self.dt)
        t = timegm(t.utctimetuple())

        if t < self.lasttimestamp:
            self.dt = self.dt + timedelta(days = 1)
            t = parser.parse(m.group('time'), default = self.dt)
            t = timegm(t.utctimetuple())

        self.lasttimestamp = t

        res = (
            self._color2dir[m.group('color')],
            self.jid,
            t,
            m.group('nick'),
            m.group('log')
        )
        return res

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for fname in sys.argv[1:]:
            Parser = PidginLogParser(fname)
    else:
        import glob
        for fname in glob.iglob('*.html'):
            Parser = PidginLogParser(fname)
        for fname in glob.iglob('logs/*.html'):
            Parser = PidginLogParser(fname)

# vim: et ts=4 sw=4
