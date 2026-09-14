
---

# VN-8 Processor

The VN-8 is an 8-bit custom CPU I built inside Logisim Evolution. It features self-modifying instruction memory (I-RAM), memory-mapped graphics and controls, a hardware call stack, and an assembler written in Python.

---

## Specs

* **7 Registers (`r1`–`r7`):** General-purpose 8-bit registers.
* **`r0` Register:** Hardwired to `0`. Writes are ignored, which is useful for setting flags without saving the math result (e.g. `sub r1 r2 r0`).
* **64 KB RAM:** Main data memory, addressed with register pairs: `rH` (high byte) and `rL` (low byte).
* **64K Instruction RAM (I-RAM):** 16-bit wide instruction memory ($16 \times 65,536$). You can read/write to it at runtime using `lil`/`lih` and `sil`/`sih`, giving you up to ~192 KB of extra RAM space depending on program size.
* **16-Deep Call Stack:** Dedicated hardware stack for subroutines (`cal` and `ret`).
* **ALU Ops:** Supports `add`, `sub`, `mul`, and bitwise logic (`and`, `or`, `nor`, `xor`, `rsh`). Includes `adc` and `sbb` for handling multi-byte math easily.
* **Flexible Jumps:** Jumps and branches can use immediate values or register pairs (`rH rL`).

---

## Screen & Controller (Memory-Mapped I/O)

I/O addresses live from `0x00f8` to `0x00ff`. Writing to an address sends data out to hardware, while reading from it grabs input.

### Memory Map

##### **`0x00f8` — Screen X / Controller Input**

* **Write:** Sets pixel X coordinate (`0`–`127`).
* **Bit 7:** Setting this bit triggers a screen clear on the next update frame.


* **Read:** Reads controller button states (mask with `and` to test for keypresses):
* `Bit 0`: Y button
* `Bit 1`: B button
* `Bit 2`: A button
* `Bit 3`: X button
* `Bit 4`: D-pad Up
* `Bit 5`: D-pad Right
* `Bit 6`: D-pad Down
* `Bit 7`: D-pad Left



##### **`0x00f9` — Screen Y / Stdin**

* **Write:** Sets pixel Y coordinate (`0`–`127`).
* **Read:** Primary hardware input (`stdin`).

##### **`0x00fa` — Screen Color / Stdin2**

* **Write:** Sets pixel color (3-3-2 RGB format) and clocks the screen update.
* **Read:** Secondary hardware input (`stdin2`).

---

## Instruction Set

### Legend

* **`rA`, `rB`, `rC`:** Registers (`r0` to `r7`).
* **`rH rL`:** Register pair forming a 16-bit address.
* **`val`:** 8-bit number.
* **`addr`:** 16-bit address or register pair (`rH rL`).
* **`con`:** Branch flags: `z` (zero), `nz` (not zero), `c` (carry), `nc` (not carry), `n` (negative).

---

### Opcodes

* **`nop`**: Do nothing
* **`add rA rB rC`**: `rA + rB -> rC`
* **`adc rA rB rC`**: `rA + rB + Carry -> rC`
* **`sub rA rB rC`**: `rA - rB -> rC`
* **`sbb rA rB rC`**: `rA - rB - Borrow -> rC` *(Note: $C=1$ means no borrow, $C=0$ means borrow).*
* **`mul rA rB rC`**: `rA * rB -> rC`
* **`and rA rB rC`**: `rA AND rB -> rC`
* **`or  rA rB rC`**: `rA OR rB -> rC`
* **`nor rA rB rC`**: `rA NOR rB -> rC`
* **`xor rA rB rC`**: `rA XOR rB -> rC`
* **`rsh rA rC`**: `rA >> 1 -> rC`
* **`ldi rA val`**: Loads `val` into `rA`
* **`adi rA val`**: Adds `val` to `rA`
* **`lod rH rL rA`**: Loads `RAM[rH:rL]` into `rA`
* **`lil rH rL rA`**: Loads I-RAM low byte at `[rH:rL]` into `rA`
* **`lih rH rL rA`**: Loads I-RAM high byte at `[rH:rL]` into `rA`
* **`str rH rL rA`**: Stores `rA` into `RAM[rH:rL]`
* **`sil rH rL rA`**: Stores `rA` into I-RAM low byte at `[rH:rL]`
* **`sih rH rL rA`**: Stores `rA` into I-RAM high byte at `[rH:rL]`
* **`jmp addr`**: Jump to address (immediate or `rH rL`)
* **`brh addr con`**: Jump to address if condition is true
* **`cal addr`**: Call function at address
* **`ret`**: Return from function
* **`hlt`**: Halt CPU clock

---

### Assembler Syntax & Shortcuts

* **`mov rA rB`:** Copy `rA` into `rB` (turns into `add rA r0 rB`).
* **`cmp rA rB`:** Compare `rA` and `rB` to set flags without storing the result (turns into `sub rA rB r0`).
* **`lsh rA rB`:** Shift `rA` left by 1 into `rB` (turns into `add rA rA rB`).
* **Comments:** Start lines or notes with `;`.
* **Labels:** Point to code locations (e.g. `main_loop:`). Used with `jmp`, `cal`, `brh`, `ldi`, and `adi`.
* **Defines:** Constants written as `#define name value`.

---

## How to Assemble

1. Keep `main.py`, `hex.txt`, and `asm.vn` in the same folder.
2. Put your code in `asm.vn`.
3. Run the python script:
```bash
python main.py

```


4. Copy the output from `hex.txt` straight into Logisim's ROM.

---

## How to Run in Logisim

1. Open `vn8.circ` in Logisim Evolution.
2. Select the Interact tool (`Ctrl + 1`). *If wires go red, press **Reset**.*
3. Right-click the ROM module, click **Clear**, then right-click **Edit** and paste your code from `hex.txt`.
4. Press `Ctrl + K` to toggle clock ticking (each instruction takes **4 ticks**).
5. Clear ROM and hit **Reset** before flashing a new program.

---

## Included Programs

Check out `programs/` for:

* **Cursor:** Move a pixel on screen with the D-pad.
* **Screen Fill:** Fills the screen based on `0x00f9` input when holding `A`.
* **VN Kernel:** System kernel setup with I/O drivers, stack allocators (`stack_alloc`/`stack_free`), and entry points for user code (`app_layer:`).
* **VN Shell:** Terminal app running on top of the kernel. Executes 8 commands off `stdin`/`stdin2` on `A` button release. Supports RAM reading/writing, pointers, and math routines.
