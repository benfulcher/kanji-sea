"""Build the two-screen ぼうけん mazes (40 x 13) for BMAPS in app.html from a short spec, and check each can be finished from anywhere.

Storey s (0 = top .. 3 = bottom) is rows 1+3s (upper) and 2+3s (lower); the floor under it is row 3+3s.
"""
import sys
from collections import deque

W, H = 40, 13
LOW = lambda s: 2 + 3 * s
UP = lambda s: 1 + 3 * s
FLOOR = lambda s: 3 + 3 * s  # floor under storey s


def build(spec):
    g = [['#'] * W for _ in range(H)]
    for s in range(4):
        for r in (UP(s), LOW(s)):
            for x in range(1, W - 1):
                if x not in (19, 20):
                    g[r][x] = '.'
    for op, *a in spec:
        if op == 'door':  # opening between the screens on storey s
            s, = a
            for r in (UP(s), LOW(s)):
                g[r][19] = g[r][20] = '.'
        elif op == 'kelp':  # from storey s up through the floor into storey s-1
            s, x = a
            for r in (FLOOR(s - 1), UP(s), LOW(s)):
                g[r][x] = 'H'
        elif op == 'hole':
            s, x, *w = a
            for i in range(w[0] if w else 2):
                g[FLOOR(s)][x + i] = '.'
        elif op == 'trap':
            s, x = a
            g[FLOOR(s)][x] = g[FLOOR(s)][x + 1] = 'T'
        elif op == 'wall':
            s, x = a
            g[UP(s)][x] = g[LOW(s)][x] = '#'
        elif op == 'lock':
            s, x = a
            g[UP(s)][x] = g[LOW(s)][x] = '|'
        elif op == 'roof':
            s, x = a
            g[UP(s)][x] = 'R'
        else:  # one cell on the lower row: X jelly, # step, S start, K key, W wall snake, a-f chests
            s, x = a
            g[LOW(s)][x] = op
    return [''.join(r) for r in g]


def solid(g, r, x, locked):
    if r < 0 or r >= H:
        return False
    if x < 0 or x >= W:
        return True
    c = g[r][x]
    return c == '#' or c == 'T' or (c == '|' and locked)


def at(g, r, x):
    return '.' if r < 0 or r >= H else '#' if x < 0 or x >= W else g[r][x]


def check(rows, name):
    g = rows
    # A position is (r, x): she stands in cell r (feet on the top of cell r+1).
    def stand(r, x, locked):
        if solid(g, r, x, locked) or at(g, r, x) == 'X':
            return False
        b = at(g, r + 1, x)
        return solid(g, r + 1, x, locked) or (b == 'H' and at(g, r, x) != 'H') or at(g, r, x) == 'H'

    def fall(r, x, locked):
        while not stand(r, x, locked):
            if solid(g, r + 1, x, locked) or r > H:
                return None
            r += 1
            if at(g, r, x) == 'X':
                return None
        return (r, x)

    def moves(p, locked):
        r, x = p
        out = []
        for d in (-1, 1):
            nx = x + d
            if not solid(g, r, nx, locked):
                q = fall(r, nx, locked)
                if q: out.append(q)
            elif not solid(g, r - 1, nx, locked) and not solid(g, r - 1, x, locked):
                if stand(r - 1, nx, locked): out.append((r - 1, nx))  # step up one
            # jump (or turtle) up to 3 across, clear of stone on rows r and r-1, landing level or lower
            for k in (2, 3):
                cells = [x + d * i for i in range(1, k + 1)]
                if all(not solid(g, r, c, locked) for c in cells) and all(not solid(g, r - 1, c, locked) for c in cells):
                    q = fall(r, x + d * k, locked)
                    if q: out.append(q)
        # kelp
        col = x
        if at(g, r, col) == 'H' or at(g, r + 1, col) == 'H':
            top = r if at(g, r, col) == 'H' else r + 1
            while at(g, top - 1, col) == 'H': top -= 1
            bot = r if at(g, r, col) == 'H' else r + 1
            while at(g, bot + 1, col) == 'H': bot += 1
            for rr in range(top - 1, bot + 1):
                if stand(rr, col, locked): out.append((rr, col))
        # drop through a kelp top or a trap door
        if at(g, r + 1, x) in 'HT':
            rr = r + 1
            while at(g, rr, x) == 'T': rr += 1
            q = fall(rr, x, locked)
            if q: out.append(q)
            if at(g, r + 1, x) == 'T':
                for d in (-1, 1):  # standing on the other half of the trap
                    if at(g, r + 1, x + d) == 'T': pass
        return out

    def reach(src, locked):
        seen = {src}; dq = deque([src])
        while dq:
            p = dq.popleft()
            for q in moves(p, locked):
                if q not in seen:
                    seen.add(q); dq.append(q)
        return seen

    find = lambda chs: [(r, x) for r in range(H) for x in range(W) if g[r][x] in chs]
    S = find('S')[0]
    chests = find('abcdefABCDEF'); key = find('K'); door = find('|')
    ok = True
    for locked in ([True, False] if door else [False]):
        R = reach(S, locked)
        need = [c for c in chests if not (locked and g[c[0]][c[1]].isupper())] + (key if locked else [])
        for c in need:
            if c not in R: print(name, 'locked' if locked else 'open', 'cannot reach', g[c[0]][c[1]], c); ok = False
        if locked and door:
            # the locked chest must be shut away
            for c in chests:
                if g[c[0]][c[1]].isupper() and c in R: print(name, 'locked chest reachable without key', c); ok = False
        # from everywhere reachable, the start must be reachable again (no dead ends)
        for p in R:
            if S not in reach(p, locked):
                print(name, 'stuck at', p, 'locked' if locked else 'open'); ok = False; break
    # unlocked with key: everything
    if door:
        R = reach(S, False)
        for c in chests:
            if c not in R: print(name, 'unlocked cannot reach', c); ok = False
    return ok


MAPS = [
  ('のぼる', [
    ('S',3,2),('X',3,8),('kelp',3,16),('door',3),('e',3,27),('W',3,33),('#',3,34),('kelp',3,37),
    ('c',2,2),('#',2,10),('kelp',2,5),('K',2,24),('trap',2,29),('roof',2,31),('kelp',2,22),
    ('door',1),('b',1,1),('X',1,9),('kelp',1,15),('d',1,36),('roof',1,27),('X',1,31),('kelp',1,34),
    ('lock',0,3),('A',0,1),('f',0,37),('X',0,28),('hole',0,24),
  ]),
  ('おりる', [
    ('S',0,1),('X',0,6),('door',0),('a',0,36),('hole',0,30),('kelp',1,2),('trap',0,13),
    ('b',1,6),('wall',1,8),('W',1,9),('kelp',2,17),('d',1,28),('roof',1,34),('hole',1,24),('kelp',1,37),
    ('door',2),('e',2,4),('X',2,10),('hole',2,6),('X',2,27),('hole',2,29),('kelp',2,22),
    ('K',3,2),('kelp',3,4),('f',3,14),('lock',3,32),('C',3,37),('kelp',3,25),('door',3),
  ]),
  ('ジグザグ', [
    ('S',3,21),('door',3),('X',3,10),('c',3,2),('kelp',3,7),('X',3,26),('W',3,33),('#',3,34),('e',3,37),
    ('kelp',3,29),('kelp',2,29),('kelp',1,29),
    ('d',2,15),('roof',2,11),('#',2,4),('trap',2,13),('kelp',2,16),('b',2,24),('X',2,34),
    ('door',1),('kelp',1,3),('X',1,10),('a',1,13),('#',1,25),('K',1,37),('roof',1,33),
    ('lock',0,15),('A',0,17),('X',0,25),('hole',0,35),('trap',0,22),
  ]),
  ('めいろ', [
    ('wall',3,6),('a',3,2),('kelp',3,4),('S',3,9),('kelp',3,11),('X',3,17),('door',3),
    ('wall',3,30),('W',3,29),('kelp',3,25),('K',3,37),('kelp',3,33),
    ('wall',2,9),('kelp',2,2),('c',2,17),('trap',2,13),('kelp',2,16),
    ('wall',2,28),('e',2,22),('kelp',2,26),('roof',2,35),('hole',2,37,1),('b',2,30),('kelp',2,36),('kelp',2,31),
    ('door',1),('X',1,8),('d',1,12),('kelp',1,10),('wall',1,33),('f',1,37),
    ('lock',0,7),('B',0,2),('door',0),('X',0,27),('hole',0,35),('roof',0,24),
  ]),
]

if __name__ == '__main__':
    # Check every maze, then print BMAPS rows to paste into app.html.
    allok = True
    for name, sp in MAPS:
        rows = build(sp)
        allok &= check(rows, name)
        print(f'  // {name}\n  [\n' + ''.join(f"    '{r}',\n" for r in rows) + '  ],')
    print('// ALL OK' if allok else '// PROBLEMS', file=sys.stderr)
