class OSMArea:
    def __init__(self, name=None, idd=None, level=1, members=None):
        self.level = level
        self.id = idd
        self.members = members
        if members is None:
            self.members = list()
        self.name = name

    def __repr__(self):
        return 'OSMArea {} {}'.format(self.name, self.id)
