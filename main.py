program = []
labels = {}

def register_to_bin(r):
    return format(int(r[1:]), "03b")

def to_hex(bin_inst):
    return format(int(bin_inst, 2), "04x")

with open("asm.txt") as f:
    lines = [line.strip() for line in f if line.strip()]

# -------------------------
# PASS 1 — collect labels
# -------------------------

inst_counter = 0

for line in lines:
    parts = line.split()

    if parts[0].startswith(";"):
        continue

    if parts[0].endswith(":"):
        label = parts[0][:-1]
        labels[label] = inst_counter
        continue

    inst_counter += 1


# -------------------------
# PASS 2 — assemble code
# -------------------------

for line in lines:
    parts = line.split()
    opcode = parts[0]

    if opcode.endswith(":"):
        continue

    if opcode.startswith(";"):
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
    
    elif opcode == "log":
        r1 = register_to_bin(parts[1])
        r2 = register_to_bin(parts[2])
        r3 = register_to_bin(parts[3])
        op_bits = {
            'and': '000',
            'or': '001',
            'nor': '010',
            'xor': '011',
            'rsh': '100'
        }[parts[4]]

        bin_inst = f'0100{r1}{r2}{op_bits}{r3}'
        program.append(to_hex(bin_inst) + "\n")


    # ---- LDI ----
    elif opcode == "ldi":
        r1 = register_to_bin(parts[1])
        imm = format(int(parts[2], 0), "08b")

        bin_inst = f"1110{imm}0{r1}"
        program.append(to_hex(bin_inst) + "\n")

    # ---- JMP ----
    elif opcode == "jmp":
        addr = format(labels[parts[1]], "08b")
        bin_inst = f"0101{addr}0000"
        program.append(to_hex(bin_inst) + "\n")

    # ---- BRH ----
    elif opcode == "brh":
        addr = format(labels[parts[1]], "08b")
        cond = parts[2]

        cond_bits = {
            "z": "0000",
            "n": "0100",
            "c": "1000",
            "nz": "1100"
        }[cond]

        bin_inst = f"0110{addr}{cond_bits}"
        program.append(to_hex(bin_inst) + "\n")

    # ---- LOD ----
    elif opcode == "lod":
        r1 = register_to_bin(parts[1])
        r2 = register_to_bin(parts[2])

        bin_inst = f"0111{r1}000000{r2}"
        program.append(to_hex(bin_inst) + "\n")

    # ---- STR ----
    elif opcode == "str":
        r1 = register_to_bin(parts[1])
        r2 = register_to_bin(parts[2])

        bin_inst = f"1000{r1}{r2}000000"
        program.append(to_hex(bin_inst) + "\n")

    # ---- CALL ----
    elif opcode == "cal":
        addr = format(labels[parts[1]], "08b")
        bin_inst = f"1100{addr}0000"
        program.append(to_hex(bin_inst) + "\n")

    # ---- RET ----
    elif opcode == "ret":
        program.append("d000\n")

    # ---- HLT ----
    elif opcode == "hlt":
        program.append("b000\n")

    else:
        raise Exception(f"Unknown instruction: {opcode}")

print(labels)
print(program)

with open("hex.txt", "w") as f:
    f.writelines(program)

with open("bin.txt", "w") as f:
    for hex_inst in program:
        bin_inst = format(int(hex_inst.strip(), 16), "016b")
        f.write(bin_inst + "\n")
