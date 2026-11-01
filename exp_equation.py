"""
Solve:  4^y = 2   and then evaluate  2y - 4   with Z3.

Z3's real arithmetic has no decision procedure for a variable exponent
(4 ** y with y a Real), so we rewrite the problem algebraically first:

    4^y = (2^y)^2          let a = 2^y, a > 0  ->  a^2 = 2
    4^y = 2^(2y)           so 2^(2y) = 2^1     ->  2y = 1   (2^x is injective)

We encode the second form: the exponent comparison 2y = 1 is exact and
Z3 can solve it, prove it is the unique solution, and evaluate 2y - 4.
The first form is also checked to show a = 2^y = sqrt(2) is consistent.
"""
from z3 import Real, Solver, sat, unsat, And, simplify

y = Real("y")
a = Real("a")          # a = 2^y

s = Solver()
# a = 2^y > 0 and (2^y)^2 = 4^y = 2
s.add(a > 0, a * a == 2)
# 4^y = 2^(2y) = 2^1  =>  exponents equal (2^x is injective)
s.add(2 * y == 1)

print("Constraints:", s)
res = s.check()
print("check():", res)
if res == sat:
    m = s.model()
    y_val = m[y]
    print("y        =", y_val)
    print("2^y = a  =", m[a], "  (a^2 =", simplify(m[a] * m[a]), ")")
    print("2y - 4   =", simplify(2 * y_val - 4))

# Uniqueness: no other y satisfies the exponent equation
s2 = Solver()
s2.add(2 * y == 1, 2 * y - 4 != -3)
print("Another value for 2y-4 possible?", s2.check(), "(unsat => -3 is the unique answer)")

# Sanity check numerically, independent of Z3
print("Numeric check: 4 ** 0.5 =", 4 ** 0.5, ", 2*0.5 - 4 =", 2 * 0.5 - 4)
