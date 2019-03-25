#!/usr/bin/python

#
# filename: mapgenerator.py
#
# Copyright (c) 2014 Juraj Fiala<doctorjellyface@riseup.net>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from random import randint

max_exits = 4


class TileType:
    allowed_exits = [""]

    def __init__(self, allowed_exits=[""]):
        self.allowed_exits = allowed_exits


class ExitType:
    allowed_tiles = [""]
    lockable = False

    def __init__(self, allowed_tiles=[""], lockable=False):
        self.allowed_tiles = allowed_tiles
        self.lockable = lockable


class Tile:
    desc = ""
    type = ""
    exits = [""]

    def __init__(self, desc="", exit_to=[]):
        self.desc = desc
        self.exits = exit_to


class Exit:
    type = ""
    destination = ""
    locked = False

    def __init__(self, type="", locked=False):
        self.type = type
        self.locked = locked


tile_types = {
    "forest": TileType(["road", "tunnel"]),
    "room": TileType(["door", "window", "trapdoor"])
}

tiles = tile_types.keys()

num_of = {}

for tile_num in range(0, tiles.__len__()):
    num_of[tiles[tile_num]] = 0

exit_types = {
    "road": ExitType(["forest"], False),
    "door": ExitType(["room", "tunnel"], True),
    "window": ExitType(["room"], True),
    "trapdoor": ExitType(["tunnel", "room"], True)
}

exits = exit_types.keys()

map = {"forest0": Tile("forest", {"road", "tunnel"})}


def generate_tile(from_name="", through=""):
    type_num = randint(0, tile_types.__len__() - 1)
    tile_type_name = tiles[type_num]
    num_of[tile_type_name] += 1
    tile_type = tile_types[tile_type_name]

    num_exits = randint(1, max_exits)
    tile_exits = []

    possible_exits = []

    for i in range(0, exits.__len__()):

        for ii in range(0, tile_type.allowed_exits.__len__()):

            if exits[i] == tile_type.allowed_exits[ii]:
                possible_exits.append(exits[i])

    for iii in range(0, num_exits):
        exit_name = possible_exits[randint(0, possible_exits.__len__() - 1)]
        tile_exit = exit_types[exit_name]
        tile_exits.append(Exit(exit_name, False))

    first_exit = exit_types[through]
    tile_exits.append(Exit(through, False))

    TILE = Tile("You see a " + tile_type_name + " tile with " + str(tile_exits.__len__()) + " possible exits.",
                tile_exits)
    tile_name = tile_type_name + str(num_of[tile_type_name])

    global map
    map[tile_name] = TILE


generate_tile("forest", "door")

map_tiles = map.keys()
print(map[map_tiles[1]].desc)
