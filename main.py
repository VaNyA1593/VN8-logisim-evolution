program = []
labels = {}
defines = {}

def register_to_bin(r):
    return format(int(r[1:]), "03b")

def to_hex(bin_inst):
    return format(int(bin_inst, 2), "04x")

with open("asm.txt") as f:
    lines = [line.strip() for line in f if line.strip()]

# -----------------------------------
# PASS 1 — collect labels and defines
# -----------------------------------

inst_counter = 0

for line in lines:
    clean_line = line.split(";")[0].strip()
    if not clean_line:
        continue

    parts = clean_line.split()
    opcode = parts[0]

    if opcode.endswith(":"):
        label = opcode[:-1]
        labels[label] = inst_counter
        continue

    if opcode.startswith("#define"):
        defines[parts[1]] = format(int(parts[2], 0), "08b")
        continue

    if opcode in ["jmp", "brh", "cal"]:
        inst_counter += 2
    else:
        inst_counter += 1


# -------------------------
# PASS 2 — assemble code
# -------------------------

for line in lines:
    clean_line = line.split(";")[0].strip()
    if not clean_line:
        continue

    parts = clean_line.split()
    opcode = parts[0]

    if opcode.endswith(":") or opcode.startswith("#define"):
        continue

    # ---- NOP ----
    if opcode == "nop":
        program.append("0000\n")

    # ---- ADD ----
    elif opcode == "add":
        r1 = register_to_bin(parts[1])
        r2 = register_to_bin(parts[2])
        r3 = register_to_bin(parts[3])
        bin_inst = f"0001{r1}{r2}000{r3}"
        program.append(to_hex(bin_inst) + "\n")

    # ---- SUB ----
    elif opcode == "sub":
        r1 = register_to_bin(parts[1])
        r2 = register_to_bin(parts[2])
        r3 = register_to_bin(parts[3])
        bin_inst = f"0010{r1}{r2}000{r3}"
        program.append(to_hex(bin_inst) + "\n")

    # ---- MUL ----
    elif opcode == "mul":
        r1 = register_to_bin(parts[1])
        r2 = register_to_bin(parts[2])
        r3 = register_to_bin(parts[3])
        bin_inst = f"0011{r1}{r2}000{r3}"
        program.append(to_hex(bin_inst) + "\n")

    # ---- LOG ----
    elif opcode == "log":
        r1 = register_to_bin(parts[1])
        r2 = register_to_bin(parts[2])
        r3 = register_to_bin(parts[3])
        op_bits = {
            'and': '000',
            'or':  '001',
            'nor': '010',
            'xor': '011',
            'rsh': '100'
        }[parts[4]]
        bin_inst = f'0100{r1}{r2}{op_bits}{r3}'
        program.append(to_hex(bin_inst) + "\n")

    # ---- LDI ----
    elif opcode == "ldi":
        r1 = register_to_bin(parts[1])
        if parts[2] in defines:
            imm = defines[parts[2]]
        else:
            imm = format(int(parts[2], 0), "08b")
        bin_inst = f"1110{imm}0{r1}"
        program.append(to_hex(bin_inst) + "\n")

    # ---- JMP ----
    elif opcode == "jmp":
        addr = format(labels[parts[1]], "016b")
        bin_inst1 = "0101000000000000"
        program.append(to_hex(bin_inst1) + "\n")
        program.append(to_hex(addr) + "\n")

    # ---- BRH ----
    elif opcode == "brh":
        addr = format(labels[parts[1]], "016b")
        cond = parts[2]
        cond_bits = {
            "z":  "0000",
            "n":  "0100",
            "c":  "1000",
            "nz": "1100"
        }[cond]
        bin_inst1 = f"011000000000{cond_bits}"
        program.append(to_hex(bin_inst1) + "\n")
        program.append(to_hex(addr) + "\n")

    # ---- LOD ----
    elif opcode == "lod":
        r1 = register_to_bin(parts[1])
        r2 = register_to_bin(parts[2])
        r3 = register_to_bin(parts[3])
        bin_inst = f"0111{r2}{r1}000{r3}"
        program.append(to_hex(bin_inst) + "\n")

    # ---- STR ----
    elif opcode == "str":
        r1 = register_to_bin(parts[1])
        r2 = register_to_bin(parts[2])
        r3 = register_to_bin(parts[3])
        bin_inst = f"1000{r2}{r1}000{r3}"
        program.append(to_hex(bin_inst) + "\n")

    # ---- CALL ----
    elif opcode == "cal":
        addr = format(labels[parts[1]], "016b")
        bin_inst1 = "1100000000000000"
        program.append(to_hex(bin_inst1) + "\n")
        program.append(to_hex(addr) + "\n")

    # ---- RET ----
    elif opcode == "ret":
        program.append("d000\n")

    # ---- HLT ----
    elif opcode == "hlt":
        program.append("b000\n")

    # ---- ADI ----
    elif opcode == "adi":
        r1 = register_to_bin(parts[1])
        if parts[2] in defines:
            imm = defines[parts[2]]
        else:
            imm = format(int(parts[2], 0), "08b")
        bin_inst = f"1001{r1}0{imm}"
        program.append(to_hex(bin_inst) + "\n")

    # ---- MOV ----
    elif opcode == "mov":
        r1 = register_to_bin(parts[1])
        r2 = register_to_bin(parts[2])
        bin_inst = f"0001{r1}000000{r2}"
        program.append(to_hex(bin_inst) + "\n")

    # ---- CMP ----
    elif opcode == "cmp":
        r1 = register_to_bin(parts[1])
        r2 = register_to_bin(parts[2])
        bin_inst = f"0010{r1}{r2}000000"
        program.append(to_hex(bin_inst) + "\n")

    else:
        raise Exception(f"Unknown instruction: {opcode}")

print("Labels:", labels)
print("Defines:", defines)

with open("hex.txt", "w") as f:
    f.writelines(program)

try:
    with open("bin.txt", "w") as f:
        for hex_inst in program:
            bin_inst = format(int(hex_inst.strip(), 16), "016b")
            f.write(bin_inst + "\n")
except Exception:
    pass
