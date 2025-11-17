from cache import Cache
from mainMem import Memory
from custom_config import get_custom_configuration

# =========================================================
# ANSI COLOR CODES
# This is used to color terminal output for better readability
# =========================================================
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
BOLD    = "\033[1m"
RESET   = "\033[0m" # this makes the terminal colors normal again

# =========================================================
# Predefined Test Sequence (Used by all demos)
# =========================================================
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

# =========================================================
# Helper: Run a single demonstration with given parameters
# =========================================================
def run_demo(name, mem_size, cache_size, block_size, mapping, replacement, write):
    print(f"\n{BOLD}=== Running Demo: {name} ==={RESET}")
    print(f"{CYAN}Configuration:{RESET}")
    print(f"  Memory size:   {mem_size}")
    print(f"  Cache size:    {cache_size}")
    print(f"  Block size:    {block_size}")
    print(f"  Mapping:       {mapping}")
    print(f"  Replacement:   {replacement}")
    print(f"  Write policy:  {write}")
    print(f"{BOLD}==========================================\n")

    memory = Memory(mem_size)
    num_lines = cache_size // block_size

    # Determine associativity based on mapping
    if mapping == "direct":
        associativity = 1
    elif mapping == "full":
        associativity = num_lines
    elif mapping.startswith("set:"):
        associativity = int(mapping.split(":")[1])
    else:
        raise ValueError("Invalid mapping policy.")

    # Create cache instance
    cache = Cache(
        cache_size,
        block_size,
        associativity=associativity,
        replacement_policy=replacement,
        write_policy=write,
    )

    # Execute test sequence
    for step in TEST_SEQUENCE:
        op = step[0]

        if op == "read":
            addr = step[1]
            before_hits = cache.hits

            val = cache.read(addr, memory)

            # Determine if hit or miss occurred
            hit = (cache.hits > before_hits)

            color = GREEN if hit else RED

            print(
                f"{color}READ   addr={addr:3d} → value={val:3d}"
                f"  (hits={cache.hits}, misses={cache.misses}){RESET}"
            )

        elif op == "write":
            addr, value = step[1], step[2]

            print(f"{YELLOW}WRITE  addr={addr:3d},  value={value:3d}{RESET} "
                  f"", end="")

            before_hits = cache.hits

            cache.write(addr, value, memory)

            # Decide hit/miss color
            hit = (cache.hits > before_hits)
            color = GREEN if hit else RED

            print(
                f" {color}(hits={cache.hits}, misses={cache.misses}){RESET}"
            )

    # Final results
    print(f"\n{BOLD}=== FINAL RESULTS ==={RESET}")
    total = cache.hits + cache.misses
    ratio = cache.hits / total if total else 0

    print(f"Hits:    {GREEN}{cache.hits}{RESET}")
    print(f"Misses:  {RED}{cache.misses}{RESET}")
    print(f"Hit Ratio: {ratio:.2f}")
    print("=====================\n")


# =========================================================
# Menu-Driven Main Program
# =========================================================
def main():
    while True:
        print("\n=== Cache Simulator Demo Menu ===")
        print("1. LRU  | Direct-Mapped     | WB")
        print("2. FIFO | Fully Associative | WB")
        print("3. LRU  | 2-Way Set-Assoc   | WT")
        print("4. RAND | Direct-Mapped     | WB")
        print("5. Custom Configuration")
        print("6. Quit")

        choice = input("\nEnter choice (1–5): ").strip()

        if choice == "1":
            run_demo(
                "LRU Direct-Mapped WB",
                mem_size=1024,
                cache_size=64,
                block_size=8,
                mapping="direct",
                replacement="LRU",
                write="WB",
            )

        elif choice == "2":
            run_demo(
                "FIFO Fully Associative WB",
                mem_size=1024,
                cache_size=64,
                block_size=8,
                mapping="full",
                replacement="FIFO",
                write="WB",
            )

        elif choice == "3":
            run_demo(
                "LRU 2-Way Set Associative WT",
                mem_size=1024,
                cache_size=64,
                block_size=8,
                mapping="set:2",
                replacement="LRU",
                write="WT",
            )

        elif choice == "4":
            run_demo(
                "RAND Direct-Mapped WB",
                mem_size=1024,
                cache_size=64,
                block_size=8,
                mapping="direct",
                replacement="RAND",
                write="WB",
            )
        elif choice == "5":
            config = get_custom_configuration()
            if config is None:
                continue  # validation failed; restart menu

            run_demo(
                "Custom Configuration",
                mem_size=config["mem_size"],
                cache_size=config["cache_size"],
                block_size=config["block_size"],
                mapping=config["mapping"],
                replacement=config["replacement"],
                write=config["write"],
            )

        elif choice == "6":
            print("Exiting.")
            break

        else:
            print("Invalid choice. Please enter 1–5.")


# =========================================================
# Entry Point
# =========================================================
if __name__ == "__main__":
    main()
