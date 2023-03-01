class Hero():
    def __init__(self, pos, land):

        self.mode = True
        self.land = land
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()

    def cameraBind(self):

        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()

        self.cameraOn = False

    def changeView(self):
        if self.cameraOn == True:
            self.cameraUp()
        else:
            self.cameraBind()

    def changeMode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True

    def accept_events(self):
        base.accept('c', self.changeView)
        base.accept('r', self.changeMode)
        base.accept('q', self.turn_left)
        base.accept('q' + '-repeat', self.turn_left)
        base.accept('e', self.turn_right)
        base.accept('e' + '-repeat', self.turn_right)
        base.accept('w', self.forward)
        base.accept('w' + '-repeat', self.forward)
        base.accept('s', self.back)
        base.accept('s' + '-repeat', self.back)
        base.accept('a', self.left)
        base.accept('a' + '-repeat', self.left)
        base.accept('d', self.right)
        base.accept('d' + '-repeat', self.right)
        base.accept('z', self.up)
        base.accept('z' + '-repeat', self.up)
        base.accept('x', self.down)
        base.accept('x' + '-repeat', self.down)
        base.accept('v', self.build)
        base.accept('b', self.destroy)
        base.accept('1', self.land.saveMap)
        base.accept('2', self.land.loadMap)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    def turn_left(self):
        self.hero.setH((self.hero.getH() + 10) % 360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 10) % 360)

    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)

    def forward(self):
        angle = (self.hero.getH()) % 360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)

    def up(self):
        if self.mode == True:
            self.hero.setZ(self.hero.getZ() + 1)

    def down(self):
        if self.mode == True:
            self.hero.setZ(self.hero.getZ() - 1)

    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    def move_to(self, angle):
        if self.mode == True:
            self.just_move(angle)
        else:
            self.try_move(angle)

    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def look_at(self, angle):
        from_x = round(self.hero.getX())
        from_y = round(self.hero.getY())
        from_z = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)

        return from_x + dx, from_y + dy, from_z

    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
            return 0, -1
        elif angle >= 21 and angle <= 65:
            return 1, -1
        elif angle >= 66 and angle <= 110:
            return 1, 0
        elif angle >= 111 and angle <= 155:
            return 1, 1
        elif angle >= 156 and angle <= 200:
            return 0, 1
        elif angle >= 201 and angle <= 245:
            return -1, 1
        elif angle >= 246 and angle <= 290:
            return -1, 0
        elif angle >= 291 and angle <= 335:
            return -1, -1
        else:
            return 0, -1







