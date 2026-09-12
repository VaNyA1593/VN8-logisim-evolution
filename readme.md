
---

# VN-8 Processor

The VN-8 is an 8-bit custom CPU designed in Logisim Evolution. It features dynamic instruction RAM (I-RAM), memory-mapped graphics and controls, a hardware call stack, and an automated Python assembler.

---

## Technical Specifications

### Architecture Summary

* **7 Registers (`r1`–`r7`):** General-purpose 8-bit registers.
* **`r0` Register:** Always stays `0`. Writes to `r0` are ignored, which is useful for setting flags without changing register values (e.g., `sub r1 r2 r0`).
* **64 KB RAM:** Main data memory. Addressed using a register pair: `rH` (high byte) and `rL` (low byte).
* **64K Instruction RAM (I-RAM):** 16-bit wide instructions ($16 \times 65,536$). Can be updated while running using the `sil` and `sih` instructions.
* **16-Deep Call Stack:** Hardware stack used for subroutine calls (`cal` and `ret`).
* **ALU Operations:** Supports `add`, `sub`, `mul`, and bitwise logic (`and`, `or`, `nor`, `xor`, right shift).
* **Flexible Jumps:** Jumps and branches can use direct values or register pairs (`rH rL`).

---

## Screen & Controller (Memory-Mapped I/O)

I/O addresses range from `0x00f8` to `0x00ff`. Writing to an I/O address sends data to an output device, while reading from that same address gets data from an input device.

### Address Mapping

* **`0x00f8` — Screen X / Controller Input**
* **Write:** Sets the pixel X coordinate (0–127).
* **Read:** Reads controller button states:
* `Bit 0`: Y button
* `Bit 1`: B button
* `Bit 2`: A button
* `Bit 3`: X button
* `Bit 4`: D-pad Up
* `Bit 5`: D-pad Right
* `Bit 6`: D-pad Down
* `Bit 7`: D-pad Left




* **`0x00f9` — Screen Y / Input (stdin)**
* **Write:** Sets the pixel Y coordinate (0–127).
* **Read:** General input values (`stdin`).


* **`0x00fa` — Screen Color / Second Input (stdin2)**
* **Write:** Sets pixel color (3-3-2 RGB format) and updates the screen.
* **Read:** Secondary input values (`stdin2`).



---

## Instruction Set

### Legend

* **`rA`, `rB`, `rC`:** Registers (`r0` to `r7`).
* **`rH rL`:** Register pair forming a 16-bit address (High Byte, Low Byte).
* **`val`:** 8-bit number.
* **`addr`:** 16-bit address or register pair (`rH rL`).
* **`con`:** Flags for branching: `z` (zero), `nz` (not zero), `c` (carry), `nc` (not carry) `n` (negative).
* **`op`:** Logic operator (`and`, `or`, `nor`, `xor`, `rsh`).

---

### Instructions

* **`nop`**: Does nothing
* **`add rA rB rC`**: `rA + rB -> rC`
* **`adc rA rB rC`**: `rA + rB + Carry -> rC`
* **`sub rA rB rC`**: `rA - rB -> rC`
* **`sbb rA rB rC`**: `rA - rB - NOT Carry -> rC`
* **`mul rA rB rC`**: `rA * rB -> rC`
* **`log rA rB rC op`**: `rA op rB -> rC`
* **`ldi rA val`**: Loads `val` into `rA`
* **`adi rA val`**: Adds `val` to `rA`
* **`lod rH rL rA`**: Loads value from `RAM[rH:rL]` into `rA`
* **`lil rH rL rA`** Loads value from I-RAM low byte at `[rH:rL]`
* **`lih rH rL rA`** Loads value from I-RAM high byte at `[rH:rL]`
* **`str rH rL rA`**: Stores `rA` into `RAM[rH:rL]`
* **`sil rH rL rA`**: Stores `rA` into I-RAM low byte at `[rH:rL]`
* **`sih rH rL rA`**: Stores `rA` into I-RAM high byte at `[rH:rL]`
* **`jmp addr`**: Jumps to address (immediate or `rH rL`)
* **`brh addr con`**: Jumps to address if flag condition is true
* **`cal addr`**: Calls function at address (pushes PC to stack)
* **`ret`**: Returns from function (pops PC from stack)
* **`hlt`**: Stops the CPU clock

---

### Extra Assembler Syntax

* **`mov rA rB`:** Copies `rA` into `rB` (turns into `add rA r0 rB`).
* **`cmp rA rB`:** Compares `rA` and `rB` to set flags without saving the result (turns into `sub rA rB r0`).
* **Comments:** Start lines or comments with `;`.
* **Labels:** Point to code locations (e.g., `main_loop:`). Used directly with `jmp`, `cal`, and `brh` as well as in `ldi` and `adi` to get the address.
* **Defines:** Wrote like so: `#define name value` which defines a constant to be used in such instructions as: `ldi`, `adi`, `brh`, `jmp` and `cal`.
 

---

## How to Use the Assembler

1. Download `main.py`, `hex.txt`, and `asm.vn`.
2. Write your assembly code inside `asm.vn`.
3. Run the Python file:
`python main.py`
4. Open `hex.txt`, copy all the contents (`Ctrl+A`, `Ctrl+C`), and paste them into Logisim's ROM.

---

## How to Run in Logisim Evolution

1. Download and install [Logisim Evolution](https://github.com/logisim-evolution/logisim-evolution/releases).
2. Open `vn8.circ`.
3. Press `Ctrl + 1` to select the Interact tool.
* *If wires light up red, click the **Reset** button.*


4. Right-click the ROM module (left of the I/O block), click **Clear**, then right-click **Edit**, and paste your code from `hex.txt`.
5. Press `Ctrl + K` to toggle clock ticking, then click **Run** (or step manually). Each instruction takes **4 clock ticks**.
* Change tick speed under **Simulate -> Auto-Tick Frequency**.


6. Clear the ROM and hit **Reset** before loading a new program.

---

## Included Programs

The `programs/` folder includes:

* **Cursor:** Use the D-pad to move a pixel on screen.
* **Screen Fill:** Fills the screen with colors based on size inputs from `0x00f9` when pressing the `A` button.
* **VN-8 Kernel/Shell:** An interactive terminal program supporting 8 commands using `0x00f9` and `0x00fa` as inputs, executed by pressing and releasing `A`. Includes RAM reads/writes, pointer setups, and math operations.
