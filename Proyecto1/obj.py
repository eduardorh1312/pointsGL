import struct
from lib import *

class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lineas = f.read().splitlines()

        self.verts = []
        self.tverts = []
        self.normales = []
        self.faces = []
        self.read()

    def read(self):
        maximo_y = 0
        maximo_x = 0
        maximo_z = 0

        for linea in self.lineas:
            if linea:
                try:
                    prefix, val = linea.split('', 1)
                except:
                    prefix =''
                if prefix =='v':
                    
                    vert = list(map(float, val.split('')))
                    self.verts.append(vert)

                    if vert[0]>maximo_x:
                        maximo_x = vert[0]

                    if vert[1]>maximo_y:
                        maximo_y = vert[1]

                    if vert[2]>maximo_z:
                        maximo_z = vert[2]

                elif prefix =='vt':
                    self.tverts.append(
                        list(map(float, val.split('')))
                    )
                elif prefix == 'f':
                    self.faces.append(
                        [list(map(int, face.split('/'))) for face in val.split('')]
                    )
        self.vertexN = [[self.vert[i][0]/maximo_x, self.vert[i][1]/maximo_y, self.vert[i][2]/maximo_z]for i in self.verts]

class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()
    
    def read(self):
        image = open(self.path, 'rb')
        
        image.seek(10)
        headerSize = struct.unpack('=l', image.read(4))[0]

        image.seek(18)
        self.width = struct.unpack('=l', image.read(4))[0]
        self.height = struct.unpack('=l', image.read(4))[0]
        image.seek(headerSize)
        self.pixels = []
        
        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))
                self.pixels[y].append(color(r, g, b))
        image.close()
        
    def get_color(self, tx, ty):
        x = int(tx * self.width)
        y = int(ty * self.height)
        try:
            return self.pixels[y][x]
        except:
            return color(255, 255, 255)
        

    
    
    
    
    
    