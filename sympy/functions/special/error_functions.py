
from sympy.core.basic import Basic, S, C, sympify
from sympy.core.function import Function
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.core.cache import cache_it, cache_it_immutable

###############################################################################
################################ ERROR FUNCTION ###############################
###############################################################################

class erf(Function):

    nargs = 1

    def fdiff(self, argindex=1):
        if argindex == 1:
            return 2*C.exp(-self.args[0]**2)/sqrt(S.Pi)
        else:
            raise ArgumentIndexError(self, argindex)

    @classmethod
    def _eval_apply_subs(cls, *args):
        return

    @classmethod
    def canonize(cls, arg):
        arg = sympify(arg)

        if isinstance(arg, C.Number):
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Infinity:
                return S.One
            elif arg is S.NegativeInfinity:
                return S.NegativeOne
            elif arg is S.Zero:
                return S.Zero
            elif arg.is_negative:
                return -cls(-arg)
        elif isinstance(arg, C.Mul):
            coeff, terms = arg.as_coeff_terms()

            if coeff.is_negative:
                return -cls(-arg)

    @staticmethod
    @cache_it_immutable
    def taylor_term(n, x, *previous_terms):
        if n < 0 or n % 2 == 0:
            return S.Zero
        else:
            x = sympify(x)

            k = (n - 1)/2

            if len(previous_terms) > 2:
                return -previous_terms[-2] * x**2 * (n-2)/(n*k)
            else:
                return 2*(-1)**k * x**n/(n*C.Factorial(k)*sqrt(S.Pi))

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if C.Order(1,x).contains(arg):
            return arg
        else:
            return self.func(arg)

    def _eval_is_real(self):
        return self.args[0].is_real

    @classmethod
    def _eval_apply_evalf(self, arg):
        arg = arg.evalf()

        if isinstance(arg, C.Number):
            # Temporary hack
            from sympy.core.numbers import Real
            from sympy.numerics import evalf
            from sympy.numerics.functions2 import erf
            e = erf(evalf(arg))
            return Real(str(e))

