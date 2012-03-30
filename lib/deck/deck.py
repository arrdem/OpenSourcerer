# -*- coding: utf-8 *-*


def parse(s, verbose=False):
    import re
    deck = {}
    s = re.sub(r'\r\n', '\n', s)
    lines = re.split(r'\n', s)
    for l in lines:
        m = re.match('//', l)
        if m is None:
            l = re.sub(r'SB:  ', '', l)
            l = re.sub(r' +', ' ', l)
            l = re.sub(r'^ +', '', l)
            l = l.split(" ")
            card_name = ' '.join(l[1::])
            count = l[0]

            if(verbose): print(l,  card_name,  count)
            if l and (not False in [bool(a) for a in l]):
                try:
                    s = ' '.join(l[1::]).strip('.')
                    if s not in deck:
                        deck[s] = 0
                    deck[s] += int(l[0])

                except:
                    exit(1)

    deck['sum'] = sum(deck[i] for i in deck if isinstance(deck[i], int))
    return deck
