from direct.showbase.ShowBase import ShowBase
import pickle


class Mapmanager():
    """ Управление картой """

    def __init__(self):
        self.model = 'model/block.egg'  # модель кубика лежит в файле block.egg
        # # используются следующие текстуры:
        self.texture = 'model/stone.png'
        self.colors = [(0.2, 0.5, 0.35, 1),
                       (0.7, 0.5, 0.35, 1),
                       (0.6, 0.1, 0.35, 1),
                       (0.2, 0.75, 0.75, 1), ]  # rgba
        # self.color2 = (0.2, 0.2, 0.9, 1)

        # создаём основной узел карты:
        self.startNew()
        # создаём строительные блоки
        # self.addBlock1((0, 10, 0))
        # self.addBlock2((0, 10, 1))

    def delBlock(self, position):
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()

    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)

    def delBlockFrom(self, pos):
        x, y, z = self.findHighestEmpty(pos)
        pos = x, y, z - 1
        blocks = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()

    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        return True

    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos))

    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def loadlend(self, filename):
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z) + 1):
                        block = self.addBlock((x, y, z0))
                    x += 1
                y += 1

    def startNew(self):
        """создаёт основу для новой карты"""
        self.land = render.attachNewNode("Land")  # узел, к которому привязаны все блоки карты

    def addBlock(self, position):
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.block.setColor(self.getColor(position[2]))
        self.block.setTag("at", str(position))
        self.block.reparentTo(self.land)

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]


    def saveMap(self):
        blocks = self.land.getChildren()
        with open("mapp.dat", "wb") as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x,y,z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)

    def loadMap(self):
        self.clear()
        with open("mapp.dat", "rb") as fout:
            length = pickle.load(fout)
            for i in range(length):
                pos = pickle.load(fout)
                self.addBlock(pos)

