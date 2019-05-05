#!/usr/bin/env python3                                                                                                                                                                          
from z3 import *

routes = []
with open('routes.txt') as f:
    routes = [set(line.rstrip().split(',')) for line in f]

routers = set.union(*routes)
router_vars = {router: Bool(router) for router in routers}

opt = Optimize()
for route in routes:
    opt.add(Or([router_vars[router] for router in route]))

count = Sum([If(router_vars[router], 1, 0) for router in routers])
opt.minimize(count)

opt.check()
m = opt.model()

for router in routers:
    if m.eval(router_vars[router]):
        print(router)
