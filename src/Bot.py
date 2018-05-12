class Bot(Entity):
    def __init__(self, _input, _physics, _graphics):
        super(Bot, self).__init__(_input, _physics, _graphics)
        self.shootRate = 2500
        self.totalTime = 0
        self.rect.center = 450, 0
        self.rect.w, self.rect.h = 5, 5
        self.range = 150
        self.inRange = False
        self.shot = False