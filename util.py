def parse_args():
    import sys
    if len(sys.argv) != 7:
        print("All EXP are 2^X, thus 10 = 2^10 Bytes")
        print("\nMap Policy: direct , full , set:N")
        print("\nReply Policy: RAND , LRU , FIFO , LFU")
        print("\nWrite Policy: WT , WB")
        print("\nUsage: simulator.py MEM_EXP CACHE_EXP BLOCK_EXP MAP_POLICY REPL_POLICY WRITE_POLICY")
        sys.exit(1)
    mem_size = 2 ** int(sys.argv[1])
    cache_size = 2 ** int(sys.argv[2])
    block_size = 2 ** int(sys.argv[3])
    mapping = sys.argv[4]
    replacement = sys.argv[5]
    write = sys.argv[6]
    return mem_size, cache_size, block_size, mapping, replacement, write

def print_stats(hits, misses):
    total = hits + misses
    ratio = hits / total if total else 0
    print(f"Hits: {hits}, Misses: {misses}, Hit Ratio: {ratio:.2f}")


def hexdump(data):
    return " ".join(f"{b:02X}" for b in data)