# custom_config.py

RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
BOLD    = "\033[1m"
RESET   = "\033[0m"


def read_positive_int(prompt, min_value=None):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print(RED + "Value must be > 0." + RESET)
                continue
            if min_value and value < min_value:
                print(RED + f"Value must be at least {min_value}." + RESET)
                continue
            return value
        except ValueError:
            print(RED + "Please enter a valid integer." + RESET)


def get_custom_configuration():
    print(f"\n{BOLD}=== Custom Configuration ==={RESET}")

    # ----------------------------------------
    # MEMORY SIZE
    # ----------------------------------------
    mem_size = read_positive_int("Enter memory size (bytes): ", min_value=256)

    # ----------------------------------------
    # CACHE SIZE
    # ----------------------------------------
    cache_size = read_positive_int("Enter cache size (bytes): ", min_value=16)

    # ----------------------------------------
    # BLOCK SIZE with dependent validation
    # ----------------------------------------
    while True:
        block_size = read_positive_int("Enter block size (bytes): ", min_value=4)

        if block_size > cache_size:
            print(RED + "ERROR: Block size must be <= cache size." + RESET)
            continue

        if cache_size % block_size != 0:
            print(RED + "ERROR: Cache size must be divisible by block size." + RESET)
            continue

        break  # block_size valid

    num_lines = cache_size // block_size

    # ----------------------------------------
    # MAPPING POLICY
    # ----------------------------------------
    while True:
        mapping = input("Enter mapping policy (direct, full, set:N): ").strip().lower()

        if mapping in ("direct", "full"):
            break

        if mapping.startswith("set:"):
            try:
                n = int(mapping.split(":")[1])
                if n <= 0:
                    print(RED + "Associativity N must be > 0." + RESET)
                    continue
                if num_lines % n != 0:
                    print(
                        RED +
                        f"Associativity N must divide total cache lines ({num_lines})." +
                        RESET
                    )
                    continue
                break
            except ValueError:
                print(RED + "Format must be: set:N (example: set:4)" + RESET)
                continue

        print(RED + "Invalid mapping. Must be direct, full, or set:N." + RESET)

    # ----------------------------------------
    # REPLACEMENT POLICY
    # ----------------------------------------
    valid_repl = {"RAND", "LRU", "FIFO", "LFU"}

    while True:
        replacement = input("Enter replacement policy (RAND, LRU, FIFO, LFU): ").strip().upper()
        if replacement in valid_repl:
            break
        print(RED + "Invalid replacement policy." + RESET)

    # ----------------------------------------
    # WRITE POLICY
    # ----------------------------------------
    valid_write = {"WT", "WB", "WA"}

    while True:
        write = input("Enter write policy (WT, WB, WA): ").strip().upper()
        if write in valid_write:
            break
        print(RED + "Invalid write policy." + RESET)

    def get_custom_sequence():
        print(f"\n{BOLD}=== Enter Custom Access Sequence ==={RESET}")
        print("Enter operations one per line.")
        print("Examples:")
        print("  read 10")
        print("  write 20 5")
        print("Type 'done' when finished.\n")

        sequence = []

        while True:
            line = input("> ").strip().lower()

            if line == "done":
                break

            parts = line.split()

            if len(parts) == 0:
                continue

            op = parts[0]

            if op == "read":
                if len(parts) != 2 or not parts[1].isdigit():
                    print(RED + "Format: read <address>" + RESET)
                    continue
                sequence.append(("read", int(parts[1])))

            elif op == "write":
                if len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit():
                    print(RED + "Format: write <address> <value>" + RESET)
                    continue
                sequence.append(("write", int(parts[1]), int(parts[2])))

            else:
                print(RED + "Unknown command. Use read or write." + RESET)

        return sequence

    # ----------------------------------------
    # Return validated configuration
    # ----------------------------------------
    return {
        "mem_size": mem_size,
        "cache_size": cache_size,
        "block_size": block_size,
        "mapping": mapping,
        "replacement": replacement,
        "write": write,
        "sequence": get_custom_sequence()
    }
