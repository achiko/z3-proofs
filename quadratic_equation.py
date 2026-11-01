"""
Solve:  t^2 - t = 12   for real t, with Z3.

Algebra:  t^2 - t - 12 = 0  factors as  (t - 4)(t + 3) = 0,
so  t = 4  or  t = -3.  Check: 16 - 4 = 12 and 9 - (-3) = 12.

Z3 is asked three things:
  1. find a solution,
  2. find a second, different solution,
  3. prove no third solution exists (unsat after excluding both),
plus a proof that the factored form is identical to the original polynomial.
"""
from z3 import Real, Solver, sat, unsat, ForAll, Not, simplify

t = Real("t")

# --- 1. First solution ------------------------------------------------------
s = Solver()
s.add(t * t - t == 12)
res = s.check()
print("t^2 - t = 12  ->", res)
m = s.model()
t1 = m[t]
print("  first solution  t =", t1)

# --- 2. Second, different solution ------------------------------------------
s.add(t != t1)
res2 = s.check()
print("Another solution besides", t1, "?", res2)
t2 = s.model()[t]
print("  second solution t =", t2)

# --- 3. Uniqueness: no solution other than those two -------------------------
s.add(t != t2)
print("A third solution besides", t1, "and", t2, "?", s.check(),
      "(unsat => exactly two real roots)")

# --- 4. Factorisation identity, proved for all real t ------------------------
p = Solver()
p.add(Not(ForAll([t], t * t - t - 12 == (t - 4) * (t + 3))))
print("\nIs (t-4)(t+3) != t^2 - t - 12 for some t?", p.check(),
      "(unsat => identity holds for all t)")

# --- 5. Direct verification of both roots -----------------------------------
from z3 import RealVal
for r in (4, -3):
    val = simplify(RealVal(r) * RealVal(r) - RealVal(r))
    print(f"  t = {r:>2}:  t^2 - t =", val)

# Numeric sanity check, independent of Z3
print("\nNumeric check:  4^2 - 4 =", 4**2 - 4, ",  (-3)^2 - (-3) =", (-3)**2 - (-3))
