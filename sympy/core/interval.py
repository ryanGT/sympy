
from basic import Basic, sympify

class Interval(Basic):

    def __new__(cls, start, end, **assumptions):
        start = sympify(start)
        end = sympify(end)
        return Basic.__new__(cls, start, end, **assumptions)

    @property
    def start(self):
        return self._args[0]

    @property
    def end(self):
        return self._args[1]

    def tostr(self, level=0):
        r = '[%s, %s]' % (self.start, self.end)
        if self.precedence <= level:
            r = '(%s)' % (r)
        return r

    
