from cache import Cache
from mainMem import Memory
from util import parse_args, print_stats

def main():
    mem_size, cache_size, block_size, mapping, replacement, write = parse_args()
    memory = Memory(mem_size)

    # Compute associativity based on mapping policy:
    # - "direct"  -> 1-way (direct mapped)
    # - "full"    -> fully associative (all lines in one set)
    # - "set:N"   -> N-way set associative
    num_lines = cache_size // block_size

    if mapping == "direct":
        associativity = 1
    elif mapping == "full":
        associativity = num_lines
    elif mapping.startswith("set:"):
        try:
            associativity = int(mapping.split(":", 1)[1])
        except ValueError:
            raise ValueError(f"Invalid set-associative mapping '{mapping}'. Use format 'set:N', e.g., 'set:4'.")
    else:
        raise ValueError(
            f"Unknown mapping policy '{mapping}'. "
            "Use 'direct', 'full', or 'set:N' (e.g., 'set:4')."
        )

    # Basic sanity check: cache must divide cleanly into sets
    if num_lines % associativity != 0 or associativity <= 0:
        raise ValueError(
            f"Invalid associativity {associativity} for cache_size={cache_size}, block_size={block_size}. "
            f"Total lines={num_lines} must be divisible by associativity."
        )

    cache = Cache(
        cache_size,
        block_size,
        associativity=associativity,
        replacement_policy=replacement,
        write_policy=write,
    )

    # Print configuration summary
    print("=== Configuration ===")
    print(f"Memory size: {mem_size} bytes")
    print(f"Cache size:  {cache_size} bytes")
    print(f"Block size:  {block_size} bytes")
    print(f"Mapping:     {mapping}  (associativity = {associativity}-way, sets = {cache.num_sets})")
    print(f"Replacement: {replacement}")
    print(f"Write policy:{write}")
    print("=====================")

    print("CPU Cache Simulator Ready. Type 'help' for commands.")

    while True:
        try:
            cmd = input("> ").split()
        except KeyboardInterrupt:
            print("\nExiting simulator.")
            break

        if not cmd:
            continue

        if cmd[0] == "read":
            if len(cmd) != 2:
                print("Usage: read <addr>")
                continue
            try:
                addr = int(cmd[1])
            except ValueError:
                print("Address must be an integer.")
                continue
            val = cache.read(addr, memory)
            print(f"Read value: {val}")

        elif cmd[0] == "write":
            if len(cmd) != 3:
                print("Usage: write <addr> <val>")
                continue
            try:
                addr = int(cmd[1])
                value = int(cmd[2])
            except ValueError:
                print("Address and value must be integers.")
                continue
            cache.write(addr, value, memory)

        elif cmd[0] == "stats":
            print_stats(cache.hits, cache.misses)

        elif cmd[0] == "quit":
            break

        elif cmd[0] == "help":
            print("Commands: read <addr>, write <addr> <val>, stats, quit")

        else:
            print("Unknown command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    main()