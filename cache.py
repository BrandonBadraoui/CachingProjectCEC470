from block import CacheLine
import random, time

class Cache:
    def __init__(self, cache_size, block_size, associativity, replacement_policy, write_policy):
        self.cache_size = cache_size
        self.block_size = block_size
        self.associativity = associativity
        self.replacement_policy = replacement_policy
        self.write_policy = write_policy

        self.num_lines = cache_size // block_size
        self.num_sets = self.num_lines // associativity
        self.sets = [[CacheLine(block_size) for _ in range(associativity)] for _ in range(self.num_sets)]

        self.hits = 0
        self.misses = 0

    def read(self, address, memory):
        block_num = address // self.block_size
        tag = block_num // self.num_sets
        set_index = block_num % self.num_sets
        offset = address % self.block_size

        for line in self.sets[set_index]:
            if line.valid and line.tag == tag:
                self.hits += 1
                line.last_used = time.time()
                line.use_count += 1
                return line.data[offset]

        self.misses += 1
        block_data = memory.read_block(block_num, self.block_size)
        victim = self.choose_victim(self.sets[set_index])
        if victim.dirty and self.write_policy == "WB":
            memory.write_block(victim.tag * self.num_sets + set_index, victim.data)
        victim.load_block(tag, block_data)
        victim.last_used = time.time()
        return victim.data[offset]

    def write(self, address, value, memory):
        block_num = address // self.block_size
        tag = block_num // self.num_sets
        set_index = block_num % self.num_sets
        offset = address % self.block_size

        for line in self.sets[set_index]:
            if line.valid and line.tag == tag:
                self.hits += 1
                line.data[offset] = value
                if self.write_policy == "WT":
                    memory.write_byte(address, value)
                else:
                    line.dirty = True
                line.last_used = time.time()
                line.use_count += 1
                return

        self.misses += 1
        if self.write_policy == "WT":
            memory.write_byte(address, value)
        else:
            block_data = memory.read_block(block_num, self.block_size)
            victim = self.choose_victim(self.sets[set_index])
            if victim.dirty:
                memory.write_block(victim.tag * self.num_sets + set_index, victim.data)
            victim.load_block(tag, block_data)
            victim.data[offset] = value
            victim.dirty = True
            victim.last_used = time.time()

    def choose_victim(self, cache_set):
        if self.replacement_policy == "RAND":
            return random.choice(cache_set)

        elif self.replacement_policy == "LRU":
            return min(cache_set, key=lambda l: l.last_used)
        elif self.replacement_policy == "FIFO":
            return min(cache_set, key=lambda l: l.last_used)
        elif self.replacement_policy == "LFU":
            return min(cache_set, key=lambda l: l.use_count)
        return cache_set[0]
