#!/usr/bin/env python3
import sys
import json
import random
from time import sleep

presets = {
    'metal': ((1, 1), (2, 2), (2, 4), (2, 8), (4, 4), (8, 8)),
    'tile': ((1, 1), (1, 2), (1, 4), (2, 1), (2, 2), (2, 4), (4, 1), (4, 2), (4, 4)),
    'metal_tile': ((1, 1), (1, 2), (1, 4), (2, 1), (2, 2), (2, 4), (2, 8), (4, 1), (4, 2), (4, 4), (8, 8)),
    'squares': ((1, 1), (2, 2), (4, 4), (8, 8)),
}

class order_set:
    def __init__(self, iteratable = []):
        self.list = []
        self.set = set()
        for item in iteratable:self.append(item)
    def append(self, item):
        self.set.add(item)
        self.list.append(item)
    def remove_set(self, set): # must be set or other 'in' supporting type
        i = 0
        while i < len(self.list):
            if self.list[i] in set:
                self.list.pop(i)
                i -= 1
            i += 1
        for item in set:
            self.set.remove(item)
    def shuffle(self):
        random.shuffle(self.list)
    def __iter__(self):
        for item in self.list:
            yield item
    def __contains__(self, other):
        return other in self.set
    def __repr__(self):
        return repr(self.list)
    def __len__(self):
        return len(self.list)

def big_build(board, used):
    empty = order_set()
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x]:empty.append((x, y))
    while len(empty) != 0:
        tile = random.choice(used)
        empty.shuffle()
        for location in empty:
            fill = set()
            if tile[0] + location[0] > len(board[0]):continue
            if tile[1] + location[1] > len(board):continue
            for x in range(tile[0]):
                for y in range(tile[1]):
                    if (location[0] + x, location[1] + y) in empty:
                        fill.add((location[0] + x, location[1] + y))
            try:
                empty.remove_set(fill)
            except ValueError:
                continue
            offsetX = location[0] % tile[0]
            offsetY = location[1] % tile[1]
            for x in range(tile[0]):
                for y in range(tile[1]):
                    board[location[1] + y][location[0] + x] = tile + (offsetX, offsetY)
    return board
                
                        
if __name__ == '__main__':
    f = open(sys.argv[1], 'r')
    board = json.load(f)
    f.close()

    if len(sys.argv) >= 3:
        if sys.argv[2] in presets:used = presets[sys.argv[2]]
        else:used = json.loads(sys.argv[2].replace('(', '[').replace(')', ']'))
    else:
        used = presets['metal_tile']
    print(big_build(board, used))
