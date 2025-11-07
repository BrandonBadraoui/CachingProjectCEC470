class Memory:
    def __init__(self, size):
        self.data = [0] * size

    def read_block(self, block_num, block_size):
        start = block_num * block_size
        end = start + block_size
        return self.data[start:end]

    def write_block(self, block_num, block_data):
        start = block_num * len(block_data)
        for i in range(len(block_data)):
            self.data[start + i] = block_data[i]

    def read_byte(self, address):
        return self.data[address]

    def write_byte(self, address, value):
        self.data[address] = value