from block import CacheLine
import random, time

class Cache:
    def __init__(self, cache_size, block_size, associativity, replacement_policy, write_policy):
        self.cache_size = cache_size            # Total cache size (in bytes)
        self.block_size = block_size            # Size of one block (in bytes)
        self.associativity = associativity      # Number of lines per set (e.g., 1 for direct-mapped, N for N-way)
        self.replacement_policy = replacement_policy  # Policy: RAND, LRU, FIFO, or LFU
        self.write_policy = write_policy        # Policy: WT (write-through) or WB (write-back) or WA (Write Around)


        self.num_lines = cache_size // block_size       # Total number of cache lines
        self.num_sets = self.num_lines // associativity # Total number of sets in the cache

        # Create a list of sets, each containing multiple CacheLine objects
        self.sets = [
            [CacheLine(block_size) for _ in range(associativity)]
            for _ in range(self.num_sets)
        ]

        # Initialize hit/miss counters
        self.hits = 0
        self.misses = 0

    #  CACHE READ OPERATION
    def read(self, address, memory):
        # Compute block-related values
        block_num = address // self.block_size          # Block number in memory
        tag = block_num // self.num_sets                # Tag identifies which block is stored
        set_index = block_num % self.num_sets           # Which set this block maps to
        offset = address % self.block_size              # Offset inside the block

        # Search for the block in the target set
        for line in self.sets[set_index]:
            if line.valid and line.tag == tag:
                # Cache hit
                self.hits += 1
                line.last_used = time.time()            # Update last-used time (for LRU/FIFO)
                line.use_count += 1                     # Increment usage count (for LFU)
                return line.data[offset]                # Return the requested byte

        # Cache miss
        self.misses += 1

        # Read block from main memory
        block_data = memory.read_block(block_num, self.block_size)

        # Choose a line in the set to replace (victim)
        victim = self.choose_victim(self.sets[set_index])

        # If victim is dirty and write-back policy, write it back to memory
        if victim.dirty and self.write_policy == "WB":
            memory.write_block(victim.tag * self.num_sets + set_index, victim.data)

        # Load new block into victim line
        victim.load_block(tag, block_data)
        victim.last_used = time.time()
        return victim.data[offset]

    #  CACHE WRITE OPERATION
    def write(self, address, value, memory):
        # Compute block-related values
        block_num = address // self.block_size
        tag = block_num // self.num_sets
        set_index = block_num % self.num_sets
        offset = address % self.block_size

        # Search for block in target set
        for line in self.sets[set_index]:
            if line.valid and line.tag == tag:
                # Cache hit
                self.hits += 1

                if self.write_policy == "WA":
                    # Write-around (no-write-allocate) — HIT behavior:
                    # update the cache line and main memory (write-through on hits),
                    # keep the line valid so subsequent reads hit.
                    line.data[offset] = value
                    memory.write_byte(address, value)
                    line.last_used = time.time()
                    line.use_count += 1
                    return

                # For WT/WB, we keep existing behavior
                line.data[offset] = value    # Write value to cache line

                if self.write_policy == "WT":
                    # Write-through: immediately update memory
                    memory.write_byte(address, value)
                else:
                    # Write-back: mark dirty, write later on eviction
                    line.dirty = True

                line.last_used = time.time()
                line.use_count += 1
                return

        # Cache miss
        self.misses += 1

        if self.write_policy == "WA":
            # Write-around on miss: just write to memory,
            # do NOT bring the block into the cache
            memory.write_byte(address, value)
            return

        if self.write_policy == "WT":
            # For write-through, write directly to memory even on miss
            memory.write_byte(address, value)
        else:
            # For write-back, we need to load the block first
            block_data = memory.read_block(block_num, self.block_size)

            # Choose a victim to replace
            victim = self.choose_victim(self.sets[set_index])

            # If the victim line is dirty, write it back before replacement
            if victim.dirty:
                memory.write_block(victim.tag * self.num_sets + set_index, victim.data)

            # Load the new block, then update with new data
            victim.load_block(tag, block_data)
            victim.data[offset] = value
            victim.dirty = True
            victim.last_used = time.time()


    #  BLOCK REPLACEMENT (VICTIM SELECT)
    def choose_victim(self, cache_set):
        # Random Replacement: pick any line
        if self.replacement_policy == "RAND":
            return random.choice(cache_set)

        # Least Recently Used (LRU): replace line with oldest last_used timestamp
        elif self.replacement_policy == "LRU":
            return min(cache_set, key=lambda l: l.last_used)

        # First In First Out (FIFO): same as LRU here if initialized by time
        elif self.replacement_policy == "FIFO":
            return min(cache_set, key=lambda l: l.last_used)

        # Least Frequently Used (LFU): replace line with smallest use_count
        elif self.replacement_policy == "LFU":
            return min(cache_set, key=lambda l: l.use_count)

        # Default: pick first line if something goes wrong
        return cache_set[0]
