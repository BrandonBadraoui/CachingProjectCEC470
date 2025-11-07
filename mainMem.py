class Memory:
    def __init__(self, size):
        # Initialize main memory with a fixed size
        # Each memory address (byte) starts with value 0
        self.data = [0] * size

    def read_block(self, block_num, block_size):
        # Reads a block (a sequence of bytes) from memory.
        # block_num: which block in memory to read
        # block_size: how many bytes make up one block
        start = block_num * block_size             # Calculate start index of the block
        end = start + block_size                   # Calculate end index (non-inclusive)
        return self.data[start:end]                # Return a slice (copy) of the data

    def write_block(self, block_num, block_data):
        # Writes an entire block of data back to memory.
        start = block_num * len(block_data)        # Find the start index of the block
        for i in range(len(block_data)):           # Copy each byte into memory
            self.data[start + i] = block_data[i]

    def read_byte(self, address):
        # Reads a single byte from a specific memory address
        return self.data[address]

    def write_byte(self, address, value):
        # Writes a single byte to a specific memory address
        self.data[address] = value
