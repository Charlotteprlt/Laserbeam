#!/usr/bin/env python

import string

int_letter_couples = list(zip(range(0, len(string.ascii_uppercase)),
                              string.ascii_uppercase))
int_to_letter = { int:letter for (int, letter) in int_letter_couples }
letter_to_int = { letter:int for (int, letter) in int_letter_couples }

class Particle:
    def __init__(self, x, y, dx, dy):
        assert (dx in {-1, 0, 1}) and (dy in {-1, 0, 1}), "invalid dx/dy"
        assert (dx != 0) or (dy != 0), "invalid dx/dy"
        self._x = x
        self._y = y
        self._dx = dx
        self._dy = dy
    @property
    def x(self): return self._x
    @property
    def y(self): return self._y
    @property
    def dx(self): return self._dx
    @property
    def dy(self): return self._dy
    def __str__(self):
        return "<{}, {}, {}, {}>".format(self._x, self._y, self._dx, self._dy)

class Aether:
    def __init__(self):
        pass
    @property
    def char_representation(self):
        return ' '
    def step(self, particle):
        return Particle(particle.x + particle.dx,
                        particle.y + particle.dy,
                        particle.dx,
                        particle.dy)

class ForwardSlashMirror:
    def __init__(self):
        pass
    @property
    def char_representation(self):
        return '/'
    def step(self, particle):
        dx = -particle.dy
        dy = -particle.dx
        return Particle(particle.x + dx, particle.y + dy, dx, dy)

class BackSlashMirror:
    def __init__(self):
        pass
    @property
    def char_representation(self):
        return '\\'
    def step(self, particle):
        dx = particle.dy
        dy = particle.dx
        return Particle(particle.x + dx, particle.y + dy, dx, dy)

class Box:
    def __init__(self, width, height, elements):
        assert (width >= 3) and (width <= 26), "invalid width"
        assert (height >= 3) and (height <= 26), "invalid height"
        self._width = width
        self._height = height
        self._grid = dict()
        for (x, y, element) in elements:
            self._grid[x, y] = element
    @property
    def width(self):
        return self._width
    @property
    def height(self):
        return self._height
    def __getitem__(self, key):
        x, y = key
        assert (x >= 0) and (x < self._width)
        assert (y >= 0) and (y < self._height)
        if key in self._grid:
            return self._grid[key]
        else:
            return Aether()
    def __str__(self):
        rule = " " + string.ascii_uppercase[0:self._width] + " "
        lines = []
        lines.append(rule)
        for y in range(0, self._height):
            letter = int_to_letter[y]
            elements = [self[x, y].char_representation
                        for x in range(0, self._width)]
            lines.append("".join([letter] + elements + [letter]))
        lines.append(rule)
        return "\n".join(lines)
    def _particle_of_string(self, description):
        assert (len(description) == 2)
        direction, letter = description
        assert (letter in string.ascii_uppercase)
        if direction == '>':
            return Particle(0, letter_to_int[letter], 1, 0)
        elif direction == '<':
            return Particle(self._width - 1, letter_to_int[letter], -1, 0)
        elif direction == 'v':
            return Particle(letter_to_int[letter], 0, 0, 1)
        elif direction == '^':
            return Particle(letter_to_int[letter], self._height - 1, 0, -1)
        else:
            assert False, "invalid direction"
    def _string_of_particle(self, particle):
        if particle.x < 0:
            return "<" + int_to_letter[particle.y]
        elif particle.x >= self._width:
            return ">" + int_to_letter[particle.y]
        elif particle.y < 0:
            return "^" + int_to_letter[particle.x]
        elif particle.y >= self._height:
            return "v" + int_to_letter[particle.x]
        else:
            assert False, "particle is still in the box"
    def _is_particle_in_box(self, particle):
        return (particle.x >= 0) and (particle.x < self._width) \
           and (particle.y >= 0) and (particle.y < self._height)
    def simulate(self, description):
        particle = self._particle_of_string(description)
        while self._is_particle_in_box(particle):
            particle = self[particle.x, particle.y].step(particle)
        return self._string_of_particle(particle)

def build_interactively():
    def input_dimension(text):
        res = input(text)
        assert res.isdigit(), "invalid dimension"
        return int(res)
    width = input_dimension("width? ")
    height = input_dimension("height? ")
    mirrors = []
    mirror_desc = input("mirror? ")
    while mirror_desc:
        assert len(mirror_desc) == 3, "invalid mirror description"
        x, y, kind = mirror_desc
        assert (x in string.ascii_uppercase)
        if kind == '/': mirror_obj = ForwardSlashMirror()
        elif kind == '\\': mirror_obj = BackSlashMirror()
        else: assert False, "invalid mirror kind"
        mirrors.append((letter_to_int[x], letter_to_int[y], mirror_obj))
        mirror_desc = input("mirror? ")
    return Box(width, height, mirrors)

box = build_interactively()
print(box)
print(box.simulate(input("entry point? ")))
