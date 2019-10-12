#!/usr/bin/env python3
import json
import queue

class Face:
    def __init__(self, name = 'tools/toolsnodraw', offset = (0, 0)):
        self.name = name.lower()
        self.offset = offset
    def isNodraw(self):
        return self.name == 'tools/toolsnodraw'
    def isTools(self):
        return self.name[0:6] == 'tools/'
    def __eq__(self, other):
        return (isinstance(other, Face) and
                ((self.name == other.name and self.offset == other.offset) or
                 (self.isNodraw() and other.isNodraw())))
    def __repr__(self):
        if self.isNodraw():return 'Face()'
        else:return 'Face({}, {})'.format(repr(self.name), repr(self.offset))
    def asPrimitive(self):
        return {'material': self.name, 'offset': self.offset}

mx = 0
my = 1
mz = 2

class Brush:
    def __init__(self, x=0, y=0, z=0,
                 dx=1, dy=1, dz=1,
                 faces = [[Face() for i in range(2)] for j in range(3)]):
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.faces = faces
    def copy(self):
        return Brush(self.x, self.y, self.z,
                     self.dx, self.dy, self.dz, 
                     self.faces)
    def expand(self, direction, high):
        if direction == mx:
            self.dx += 1
            if not high:
                self.x -= 1
        elif direction == my:
            self.dy += 1
            if not high:
                self.y -= 1
        elif direction == mz:
            self.dz += 1
            if not high:
                self.z -= 1
    def valid(self, p2cX):
        for x in range(self.x, self.x + self.dx):
            for y in range(self.y, self.y + self.dy):
                for z in range(self.z, self.z + self.dz):
                    if self.x < 0 or self.y < 0 or self.z < 0:return False
                    if self.x + self.dx > len(p2cX.array):return False
                    if self.y + self.dy > len(p2cX.array[0]):return False
                    if self.z + self.dz > len(p2cX.array[0][0]):return False
                    voxel = p2cX.voxel(x, y, z)
                    if not voxel:return False
                    if x == self.x:
                        if voxel.textures[x][0] != self.textures[x][0]:return False
                        if self.textures[x][0] == Face():self.textures[x][0] = voxel.textures[x][0]
                    if x == self.x + self.dx:
                        if voxel.textures[x][1] != self.textures[x][1]:return False
                        if self.textures[x][1] == Face():self.textures[x][1] = voxel.textures[x][1]
                    if y == self.y:
                        if voxel.textures[y][0] != self.textures[y][0]:return False
                        if self.textures[y][0] == Face():self.textures[y][0] = voxel.textures[y][0]
                    if y == self.y + self.dy:
                        if voxel.textures[y][1] != self.textures[y][1]:return False
                        if self.textures[y][1] == Face():self.textures[y][1] = voxel.textures[y][1]
                    if z == self.z:
                        if voxel.textures[z][0] != self.textures[z][0]:return False
                        if self.textures[z][0] == Face():self.textures[z][0] = voxel.textures[z][0]
                    if z == self.z + self.dz:
                        if voxel.textures[z][1] != self.textures[z][1]:return False
                        if self.textures[z][1] == Face():self.textures[z][1] = voxel.textures[z][1]
        return True
    def all_expands(self):
        copies =  [self.copy() for i in range(6)]
        copies[0].expand(mx, False)
        copies[1].expand(mx, True)
        copies[2].expand(my, False)
        copies[3].expand(my, True)
        copies[4].expand(mz, False)
        copies[5].expand(mz, True)
        return copies
    def asPrimitive(self):
        primitive = self.__dict__.copy()
        for i in range(3):
            for j in range(2):
                primitive['faces'][i][j] = primitive['faces'][i][j].asPrimitive()
    def size(self): # not quite sure what I'm supposed to be measuring, I am measuring volume.
        return dx * dy * dz
    def __repr__(self):
        return 'Brush({}, {}, {},\n      {}, {}, {},\n      {})'.format(repr(self.x), repr(self.y), repr(self.z), repr(self.dx), repr(self.dy), repr(self.dz), repr(self.faces))
class Voxel(Brush):
    def __init__(self, x=0, y=0, z=0,
                 faces = [[Face() for i in range(2)] for j in range(3)]):
        self.x = x
        self.y = y
        self.z = z
        self.dx = 1
        self.dy = 1
        self.dz = 1
        self.faces = faces
    def __repr__(self):
        return 'Voxel({}, {}, {},\n      {})'.format(repr(self.x), repr(self.y), repr(self.z), repr(self.faces))

class p2cX:
    def __init__(self, primitive):
        self.array = primitive.copy()
        for x in range(len(self.array)):
            for y in range(len(self.array[x])):
                for z in range(len(self.array[x][y])):
                    faces = self.array[x][y][z]
                    if faces:
                        for i in range(3):
                            for j in range(2):
                                faceprim = faces[i][j]
                                faces[i][j] = Face(faceprim['material'], faceprim['offset'])
                        self.array[x][y][z] = Voxel(x, y, z, faces)
    def voxel(self, x, y, z):
        return self.array[x][y][z]
    def brushes(self):
        finished = [[[False
                      for i in range(len(self.array[0][0]))]
                     for j in range(len(self.array[0]))]
                    for k in range(len(self.array))]
        brushes = []
        for x in range(len(self.array)):
            for y in range(len(self.array[x])):
                for z in range(len(self.array[x][y])):
                    if not finished[x][y][z]:
                        size = 0
                        containing = queue.Queue
                        containing.put(Brush(x, y, z))
                        possible = []
                        while containing != []:
                            value = containing.get()
                            expands = all_expands(value)
                            if any(x.valid() for x in expands):
                                for brush in expands:
                                    if brush.valid():containing.put(brush)
                            else:possible.append(value)
                        current = None
                        for brush in containing:
                            if brush.size() > size:
                                current = brush
                                size = brush.size()
                        brushes.append(current)
                        for xx in range(current.x):
                            for yy in range(current.y):
                                for zz in range(current.z):
                                    finished[xx][yy][zz] = True

if __name__ == '__main__': # Run some tests
    inname = sys.argv[0] # A json created by the editor
    outname = sys.argv[1] # A json for export by the vmf generator
    f = open(inname, 'r')
    inprim = json.load(f)
    f.close()
    outprim = [x.asPrimitive() for x in p2cX(inprim)]
    f = open(outname, 'w')
    json.dump(outprim, f)
    f.close()
