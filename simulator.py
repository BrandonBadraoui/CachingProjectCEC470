from cache import Cache
from mainMem import Memory
from util import print_stats

# ---------------------------------------------------------
# Predefined test cases for automated demos
# ---------------------------------------------------------
TEST_SEQUENCE = [
    ("read", 10),
    ("read", 14),
    ("read", 10),
    ("write", 18, 7),
    ("read", 18),
    ("read", 50),
    ("read", 58),
    ("write", 90, 33),
    ("read", 90),
    ("read", 10),
]

# ---------------------------------------------------------
# Helper to run a full simulation with fixed settings
# ---------------------------------------------------------
def run_demo(name, mem_size, cache_size, block_size, mapping, replacement, write):
    print(f"\n=== Running Demo: {name} ===")
    print("Configuration:")
    print(f"  Memory size:   {mem_size}")
    print(f"  Cache size:    {cache_size}")
    print(f"  Block size:    {block_size}")
    print(f"  Mapping:       {mapping}")
    print(f"  Replacement:   {replacement}")
    print(f"  Write policy:  {write}")
    print("============================\n")

    memory = Memory(mem_size)
    num_lines = cache_size // block_size

    # Determine associativity
    if mapping == "direct":
        associativity = 1
    elif mapping == "full":
        associativity = num_lines
    elif mapping.startswith("set:"):
        associativity = int(mapping.split(":")[1])
    else:
        raise ValueError("Invalid mapping.")

    cache = Cache(
        cache_size,
        block_size,
        associativity=associativity,
        replacement_policy=replacement,
        write_policy=write,
    )

    # Run test sequence
    for step in TEST_SEQUENCE:
        if step[0] == "read":
            addr = step[1]
            val = cache.read(addr, memory)
            print(f"READ  addr={addr:3d}  → value={val},   hits={cache.hits}, misses={cache.misses}")
        elif step[0] == "write":
            addr, value = step[1], step[2]
            cache.write(addr, value, memory)
            print(f"WRITE addr={addr:3d}, value={value}   hits={cache.hits}, misses={cache.misses}")

    print("\n=== FINAL RESULTS ===")
    print_stats(cache.hits, cache.misses)
    print("=====================\n")


# ---------------------------------------------------------
# Menu-driven main
# ---------------------------------------------------------
def main():
    while True:
        print("\nSelect a demo to run:\n")
        print("1. LRU  | Direct-Mapped | Write-Back")
        print("2. FIFO | Fully-Assoc   | Write-Back")
        print("3. LRU  | 2-Way Set     | Write-Through")
        print("4. Random | Direct | Write-Back")
        print("5. Quit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            run_demo(
                "LRU Direct-Mapped WB",
                mem_size=1024,
                cache_size=64,
                block_size=8,
                mapping="direct", # Direct-mapped
                replacement="LRU", # LRU replacement
                write="write-back", # Write-back policy
            )
        elif choice == "2":
            run_demo(
                "FIFO Fully Associative WB",
                mem_size=1024,
                cache_size=64,
                block_size=8,
                mapping="full", # Fully associative
                replacement="FIFO", # FIFO replacement
                write="write-back", # Write-back policy
            )
        elif choice == "3":
            run_demo(
                "LRU 2-Way Set-Assoc WT",
                mem_size=1024,
                cache_size=64,
                block_size=8,
                mapping="set:2",
                replacement="LRU", # LRU replacement
                write="write-through", # Write-through policy
            )
        elif choice == "4":
            run_demo(
                "Random Direct WB",
                mem_size=1024,
                cache_size=64,
                block_size=8,
                mapping="direct", # Direct-mapped
                replacement="Random", # Random replacement
                write="write-back", # Write-back policy
            )
        elif choice == "5":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
