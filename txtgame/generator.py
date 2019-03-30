# Copyright (C) 2014-2019  Juraj Fiala <jurf@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from random import choice, randint, randrange


class TileType:
    allowed_exits = []

    def __init__(self, allowed_exits):
        self.allowed_exits = allowed_exits


class ExitType:
    allowed_tiles = []
    lockable = False

    def __init__(self, allowed_tiles, lockable):
        self.allowed_tiles = allowed_tiles
        self.lockable = lockable


class MapObject:
    type = ""

    def __init__(self, _type):
        self.type = _type

    @staticmethod
    def random_type(types):
        return list(types.keys())[randrange(0, len(types))]


class Tile(MapObject):
    exits = []

    def __init__(self, _type):
        super().__init__(_type)
        self._gen_exits()

    def desc(self):
        return 'You see a {name} with {exit_count} exits: {exits}.' \
               .format(name=self.type, exit_count=len(self.exits),
                       exits=[exit.data.type for exit in self.exits])

    def exit(self, exit):
        if exit in self.exits:
            exit = self.exits[self.exits.index(exit)]
            if exit.dest is None:
                new_tile = generate_tile(_from=self, through=exit)
                self.exits[self.exits.index(exit)].dest = new_tile
                return new_tile
            return exit.dest

        raise ValueError('exit not available')

    def _gen_exits(self, max_exits=3):
        self.exits = []
        possible_exits = TILE_TYPES[self.type].allowed_exits
        for _ in range(randint(1, max_exits)):
            exit_data = ExitData(choice(possible_exits), False)
            self.exits.append(Exit(exit_data))


class Exit:
    dest = None
    data = None

    def __init__(self, data, dest=None):
        self.data = data
        self.dest = dest

    def __eq__(self, other):
        return other == self.data.type


class ExitData(MapObject):
    locked = False

    def __init__(self, _type, locked):
        self.locked = locked
        super().__init__(_type)


TILE_TYPES = {
    "forest": TileType(["road", "tunnel"]),
    "room": TileType(["door", "window", "trapdoor"])
}

EXIT_TYPES = {
    "road": ExitType(["forest"], False),
    "door": ExitType(["room", "tunnel"], True),
    "window": ExitType(["room"], True),
    "trapdoor": ExitType(["tunnel", "room"], True)
}

#_map = {"forest0": Tile("forest", {"road", "tunnel"})}


def generate_tile(_from=None, through=None):
    tile = Tile(Tile.random_type(TILE_TYPES))

    if through is not None:
        tile.exits.append(Exit(through.data, dest=_from))
    return tile


#print(generate_tile(_from="forest").desc())

#map_tiles = _map.keys()
#print(_map[map_tiles[1]].desc)
