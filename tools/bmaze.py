"""Build the ぼうけん mazes for app.html from a short spec, and check each one can be finished from anywhere.

Run `python3 tools/bmaze.py`: it checks every maze, then prints BMAPS (two screens side by side, 40 x 13) and
BMAPS4 (four screens in a 2 x 2 grid, 40 x 26) to paste into app.html.

A screen is 20 x 13 cells. Screens side by side are split by a double wall (columns 19 and 20); screens one above
the other by a double floor (rows 12 and 13). Each screen has four storeys, two cells high. Storey s counts from the
top: 0-3 on the top screens, 4-7 on the bottom ones.

Spec operations (s = storey, x = column):
  ('door', s)      an opening in the middle wall on storey s, between the left and right screens
  ('kelp', s, x)   kelp from storey s up through the floor above into storey s-1 (s = 4 crosses between screens)
  ('hole', s, x[, w]) a hole w cells wide (default 2) in the floor under storey s (s = 3 crosses between screens)
  ('trap', s, x)   a two-cell trap door in the floor under storey s (not s = 3)
  ('wall', s, x)   stone the full height of the storey;  ('lock', s, x) a locked door the full height
  ('roof', s, x)   a sea snake in the roof
  (ch, s, x)       one cell on the storey's lower row: X jellyfish, # step, S start, K key,
                   W wall snake (beside stone), a-f chests (a capital letter is the chest behind the locked door)
"""
import sys
from collections import deque


def UP(s): return 1 + 3 * s + (1 if s >= 4 else 0)
def LOW(s): return UP(s) + 1


def build(spec, tall):
    W, H = 40, 26 if tall else 13
    g = [['#'] * W for _ in range(H)]
    for s in range(8 if tall else 4):
        for r in (UP(s), LOW(s)):
            for x in range(1, W - 1):
                if x not in (19, 20):
                    g[r][x] = '.'
    for op, *a in spec:
        if op == 'door':
            s, = a
            for r in (UP(s), LOW(s)):
                g[r][19] = g[r][20] = '.'
        elif op == 'kelp':
            s, x = a
            for r in range(LOW(s - 1) + 1, LOW(s) + 1):
                g[r][x] = 'H'
        elif op == 'hole':
            s, x, *w = a
            for r in range(LOW(s) + 1, UP(s + 1)):
                for i in range(w[0] if w else 2):
                    g[r][x + i] = '.'
        elif op == 'trap':
            s, x = a
            assert s != 3, 'no trap doors in the double floor'
            g[LOW(s) + 1][x] = g[LOW(s) + 1][x + 1] = 'T'
        elif op == 'wall':
            s, x = a
            g[UP(s)][x] = g[LOW(s)][x] = '#'
        elif op == 'lock':
            s, x = a
            g[UP(s)][x] = g[LOW(s)][x] = '|'
        elif op == 'roof':
            s, x = a
            g[UP(s)][x] = 'R'
        else:
            s, x = a
            g[LOW(s)][x] = op
    return [''.join(r) for r in g]


def check(g, name):
    H, W = len(g), len(g[0])
    at = lambda r, x: '.' if r < 0 or r >= H else '#' if x < 0 or x >= W else g[r][x]
    def solid(r, x, locked):
        c = at(r, x)
        return c == '#' or c == 'T' or (c == '|' and locked)
    # A position (r, x): she is in cell r with her feet on the top of cell r+1.
    def stand(r, x, locked):
        if solid(r, x, locked) or at(r, x) == 'X':
            return False
        return solid(r + 1, x, locked) or at(r + 1, x) == 'H' or at(r, x) == 'H'
    def fall(r, x, locked):
        while not stand(r, x, locked):
            if solid(r + 1, x, locked) or r >= H:
                return None
            r += 1
            if at(r, x) == 'X':
                return None
        return (r, x)
    def moves(p, locked):
        r, x = p
        out = []
        for d in (-1, 1):
            if not solid(r, x + d, locked):
                q = fall(r, x + d, locked)
                if q: out.append(q)
            elif not solid(r - 1, x + d, locked) and not solid(r - 1, x, locked) and stand(r - 1, x + d, locked):
                out.append((r - 1, x + d))  # a step one cell high
            for k in (2, 3):  # a jump or a turtle ride across
                cells = [x + d * i for i in range(1, k + 1)]
                if all(not solid(r, c, locked) and not solid(r - 1, c, locked) for c in cells):
                    q = fall(r, x + d * k, locked)
                    if q: out.append(q)
        if at(r, x) == 'H' or at(r + 1, x) == 'H':  # kelp, up or down
            top = r if at(r, x) == 'H' else r + 1
            while at(top - 1, x) == 'H': top -= 1
            bot = top
            while at(bot + 1, x) == 'H': bot += 1
            for rr in range(top - 1, bot + 1):
                if stand(rr, x, locked): out.append((rr, x))
        if at(r + 1, x) in 'HT':  # drop through a kelp top or a trap door
            q = fall(r + 2, x, locked)
            if q: out.append(q)
        return out
    def reach(src, locked):
        seen = {src}; dq = deque([src])
        while dq:
            for q in moves(dq.popleft(), locked):
                if q not in seen:
                    seen.add(q); dq.append(q)
        return seen
    find = lambda chs: [(r, x) for r in range(H) for x in range(W) if g[r][x] in chs]
    S = find('S')[0]; chests = find('abcdefABCDEF'); key = find('K'); door = find('|')
    ok = True
    def bad(*m):
        nonlocal ok; ok = False; print(name, *m, file=sys.stderr)
    if not 5 <= len(chests) <= 7: bad('has', len(chests), 'chests')
    if not door or not key or sum(g[r][x].isupper() for r, x in chests) != 1: bad('needs one locked door, one key and one capital chest')
    for locked in (True, False):
        R = reach(S, locked)
        for c in chests + (key if locked else []):
            if locked and c in chests and g[c[0]][c[1]].isupper():
                if c in R: bad('the locked chest is reachable without the key', c)
            elif c not in R: bad('cannot reach', g[c[0]][c[1]], c, 'locked' if locked else 'open')
        # Everywhere she can get to must lead back to the start: search backwards from it.
        back = {}
        for p in R:
            for q in moves(p, locked): back.setdefault(q, []).append(p)
        seen = {S}; dq = deque([S])
        while dq:
            for q in back.get(dq.popleft(), []):
                if q not in seen: seen.add(q); dq.append(q)
        stuck = sorted(R - seen)
        if stuck: bad('can get stuck at', stuck[:5], 'locked' if locked else 'open')
    return ok


S = 'S'
MAPS2 = [
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

MAPS4 = [
  ('おおきな しんでん: up from the bottom left', [
    ('S',7,2),('X',7,9),('kelp',7,15),('door',7),('a',7,36),('W',7,30),('#',7,31),('kelp',7,24),
    ('c',6,3),('kelp',6,6),('roof',6,13),('X',6,30),('hole',6,35),('kelp',6,37),
    ('door',5),('trap',5,10),('b',5,16),('kelp',5,2),('#',5,27),('d',5,23),('kelp',5,33),
    ('X',4,9),('kelp',4,14),
    ('door',3),('X',3,6),('kelp',3,4),('hole',3,25),('kelp',3,35),('roof',3,30),
    ('wall',2,10),('kelp',3,16),('X',2,28),('K',2,22),('kelp',2,24),
    ('door',1),('lock',1,4),('A',1,2),('kelp',2,7),('roof',1,30),('hole',1,34),
    ('kelp',1,12),('X',0,6),('e',0,3),('kelp',1,36),('trap',0,28),
  ]),
  ('ふかい たに: down from the top right', [
    ('S',0,37),('X',0,30),('door',0),('hole',0,24),('kelp',1,33),('a',0,2),('kelp',1,10),('trap',0,14),
    ('X',1,5),('kelp',2,8),('W',1,36),('#',1,37),('kelp',2,28),
    ('door',2),('c',2,14),('hole',2,3),('X',2,33),('roof',2,23),
    ('kelp',3,6),('X',3,12),('kelp',4,16),('kelp',3,37),('d',3,26),('hole',3,30),
    ('door',4),('K',4,3),('hole',4,10),('X',4,25),('kelp',5,35),('hole',4,22),
    ('kelp',5,5),('trap',5,12),('wall',5,28),('f',5,22),('kelp',5,26),
    ('kelp',6,4),('lock',6,15),('C',6,17),('kelp',7,30),('X',6,34),
    ('door',7),('kelp',7,8),('e',7,37),
  ]),
  ('ぐるぐる: round and round', [
    ('S',0,9),('X',0,4),('door',0),('a',0,37),('kelp',1,22),
    ('kelp',1,15),('hole',1,3),('#',1,11),('W',1,12),('X',1,28),('b',1,37),('hole',1,33),
    ('door',2),('kelp',2,6),('trap',2,26),('kelp',2,36),
    ('kelp',4,4),('X',3,10),('d',3,16),('kelp',3,13),('kelp',3,23),('hole',3,36),
    ('door',4),('K',4,16),('X',4,30),('kelp',5,25),
    ('kelp',5,9),('roof',5,14),('e',5,2),('hole',5,32),
    ('door',6),('kelp',6,12),('X',6,6),('f',6,37),('kelp',7,22),
    ('kelp',7,3),('lock',7,14),('E',7,17),('X',7,30),
  ]),
]


if __name__ == '__main__':
    allok = True
    for var, maps, tall in (('BMAPS', MAPS2, False), ('BMAPS4', MAPS4, True)):
        print(f'const {var}=[')
        for name, sp in maps:
            rows = build(sp, tall)
            allok &= check(rows, name)
            print(f'  // {name}\n  [\n' + ''.join(f"    '{r}',\n" for r in rows) + '  ],')
        print('];')
    print('ALL OK' if allok else 'PROBLEMS', file=sys.stderr)
