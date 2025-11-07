from cache import Cache
from mainMem import Memory
from util import parse_args, print_stats

def main():
    mem_size, cache_size, block_size, mapping, replacement, write = parse_args()
    memory = Memory(mem_size)
    cache = Cache(cache_size, block_size, associativity=1 if mapping == "direct" else 4,
    replacement_policy=replacement, write_policy=write)

    print("CPU Cache Simulator Ready. Type 'help' for commands.")

    while True:
        cmd = input("> ").split()
        if not cmd:
            continue
        if cmd[0] == "read":
            val = cache.read(int(cmd[1]), memory)
            print(f"Read value: {val}")
        elif cmd[0] == "write":
            cache.write(int(cmd[1]), int(cmd[2]), memory)
        elif cmd[0] == "stats":
            print_stats(cache.hits, cache.misses)
        elif cmd[0] == "quit":
            break
        elif cmd[0] == "help":
            print("Commands: read <addr>, write <addr> <val>, stats, quit")

if __name__ == "__main__":
    main()