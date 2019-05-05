#!/usr/bin/env python3

from functools import reduce

with open('routes.txt') as f:
    routes = [set(l.split(',')) for l in f.read().split()]
orig_routes = [r.copy() for r in routes]
universe = reduce(set.union, routes)
forced = set()

while True:
    updated = False
    rlen, ulen = len(routes), len(universe)
    print('cur: {} routes, {} elements'.format(rlen, ulen))

    coverage = dict()
    for e in universe:
        coverage[e] = {i for i,r in enumerate(routes) if e in r}

    # Remove pointless routers
    for e1 in sorted(coverage):
        c1 = coverage[e1]
        for e2,c2 in coverage.items():
            if e1 != e2 and c1 != c2 and c1.issubset(c2):
                del coverage[e1]
                universe.remove(e1)
                break

    # Simplify routes based on removed routers
    for r in routes:
        r.intersection_update(universe)

    # Remove duplicate routes
    routes = [set(rf) for rf in set(frozenset(r) for r in routes)]

    # Detect forced routers
    for r in routes:
        if len(r) == 1:
            f = r.pop()
            forced.add(f)
            universe.remove(f)

    # Remove routes covered by forced routes
    routes = [r for r in routes if len(r) > 0 and len(r.intersection(forced)) == 0]

    if len(routes) == rlen and len(universe) == ulen:
        break

# Re-add forced routers
universe.update(forced)

print('end: {} routes, {} elements ({} forced)'.format(len(routes), len(universe), len(forced)))
for r in orig_routes:
    if len(r.intersection(universe)) == 0:
        print('universe:', universe)
        print('no:', sorted(r))
        break
else:
    print('check passed')

for e,c in coverage.items():
    print(e, len(c), c)
