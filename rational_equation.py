"""
Solve:  (x^2 - 9) / (x - 3) = 3   for real x, with Z3.

Algebra:  x^2 - 9 = (x - 3)(x + 3), so for x != 3 the fraction equals x + 3,
and x + 3 = 3  gives  x = 0.  The value x = 3 is excluded because it makes the
denominator zero (the expression is undefined there), even though it also
satisfies the cross-multiplied form  x^2 - 9 = 3(x - 3).

Z3 note: in Z3's theory of reals, division by zero is *not* an error. The
term t/0 is an unspecified value, so Z3 may happily report x = 3 if we do not
add the domain constraint x != 3 ourselves. The script shows both cases.
"""
from z3 import Real, Solver, sat, unsat

x = Real("x")

# --- 1. Naive encoding: Z3 accepts the spurious root x = 3 ------------------
naive = Solver()
naive.add((x * x - 9) / (x - 3) == 3)
naive.add(x == 3)                          # force the excluded value
print("Naive encoding, forcing x = 3:", naive.check())
print("  (sat => Z3 treats 0/0 as an arbitrary value, so x = 3 'works')")
if naive.check() == sat:
    print("  model:", naive.model())

# --- 2. Correct encoding: add the domain constraint -------------------------
s = Solver()
s.add(x != 3)                              # denominator must be non-zero
s.add((x * x - 9) / (x - 3) == 3)
res = s.check()
print("\nWith domain constraint x != 3:", res)
if res == sat:
    m = s.model()
    print("  x =", m[x])

# --- 3. Uniqueness: no solution other than x = 0 ----------------------------
u = Solver()
u.add(x != 3, (x * x - 9) / (x - 3) == 3, x != 0)
print("\nAny solution other than x = 0?", u.check(), "(unsat => x = 0 is unique)")

# --- 4. Show that x = 3 fails the equation when written without division ----
# Equivalent form for x != 3:  x + 3 == 3.  At x = 3 that gives 6 == 3, false.
chk = Solver()
chk.add(x == 3, x + 3 == 3)
print("Does x = 3 satisfy the simplified form x + 3 = 3?", chk.check(), "(unsat => no)")

# Numeric sanity check, independent of Z3
print("\nNumeric check at x = 0: (0^2 - 9) / (0 - 3) =", (0**2 - 9) / (0 - 3))
