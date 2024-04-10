CFG = [
    # B0
    [
        ('i',)
    ],
    # B1
    [
        ('a',),
        ('b',)
    ],
    # B2
    [
        ('b',),
        ('c',),
        ('d',)
    ],
    # B3
    [
        ('a',),
        ('d',)
    ],
    # B4
    [
        ('d',)
    ],
    # B5
    [
        ('c',)
    ],
    # B6
    [
        ('b',)
    ],
    # B7
    [
        ('y', 'a', 'b'),
        ('z', 'c', 'd'),
        ('i', 'i'),
    ]
]

variables = set()
for B in CFG:
    for instruction in B:
        for variable in instruction:
            variables.add(variable)

Globals = set()

Blocks = {}
for variable in variables:
    Blocks[variable] = set()

for N, B in enumerate(CFG):
    def_b = set()

    for instruction in B:
        x = instruction[0]
        y = instruction[1] if len(instruction) > 1 else None
        z = instruction[2] if len(instruction) > 2 else None

        if y is not None and y not in def_b:
            Globals = Globals.union({y})
        if z is not None and z not in def_b:
            Globals = Globals.union({z})

        def_b = def_b.union(x)
        Blocks[x] = Blocks[x].union({N})

print(Globals)
print(Blocks)

DF = {
    0: set(),
    1: {1},
    2: {7},
    3: {7},
    4: {6},
    5: {6},
    6: {7},
    7: {1}
}

update_CFG = CFG.copy()

for x in Globals:
    WorkList = Blocks[x]

    while len(WorkList) > 0:
        B = list(WorkList)[0]
        for D in DF[B]:
            phi_x = 'phi(' + x + ', ' + x + ')'
            if phi_x not in update_CFG[D]:
                update_CFG[D].insert(0, phi_x)
                WorkList = WorkList.union({D})

        WorkList = WorkList - {B}

for N, B in enumerate(update_CFG):
    print(N, B)
