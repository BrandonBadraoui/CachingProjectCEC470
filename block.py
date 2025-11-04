class CacheLine:
    def __init__(self, block_size):
        self.valid = False
        self.tag = None
        self.data = [0] * block_size
        self.dirty = False
        self.last_used = 0
        self.use_count = 0

    def load_block(self, tag, block_data):
        self.valid = True
        self.tag = tag
        self.data = block_data[:]
        self.dirty = False
        self.use_count = 0

    def invalidate(self):
        self.valid = False
        self.tag = None
        self.dirty = False