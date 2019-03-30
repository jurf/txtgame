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

import generator


class Game:
    commands = {}
    root = None
    current = None

    def __init__(self):
        self.commands = {
            'help': self._help,
            'look': self._look,
            'exit': self._exit,
            'go': self._go,
        }

        self.root = generator.generate_tile()
        self.current = self.root

    def run(self, command):
        command.append(None)
        try:
            self.commands[command[0]](arg=command[1:])
        except KeyError:
            self._invalid_command()

    @staticmethod
    def _invalid_command():
        print('wtf dude')

    @staticmethod
    def _help(arg=None):
        print('fuck you')

    @staticmethod
    def _exit(arg=None):
        print('well you can fuck off then')
        exit()

    def _look(self, arg=None):
        if arg is not None:
            print(self.current.desc())

    def _go(self, arg=None):
        if arg[0] is not None:
            self.current = self.current.exit(arg[0])
        else:
            print('go where')


def main():
    game = Game()
    while True:
        command = input('> ').split(' ')
        game.run(command)


main()
