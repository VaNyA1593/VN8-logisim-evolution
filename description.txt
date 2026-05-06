The VN-8 is an 8 bit processor made in logisim evolution. The specs:
  7 general purpose register (r1-r7) 
  r0 is always 0 and writes are discarded(good way to only set flags in an ALU operation for example: sub r1 r2 r0)
  256 bytes RAM
  256 instructions(16x256 ROM)
  Call stack
  Alu operations: ADD, SUB, MUL, LOG: and or nor xor rightshift
  4x input and output ports

How to use:
  1. Download logisim evolution: https://github.com/logisim-evolution/logisim-evolution/releases
  2. Download the project itself
  3. Open the project in logisim evolution
  4. Press ctrl + 1 to select the interact tool
  5. Right click the ROM (Next to the clock) and click edit, then paste in your HEX codes(make sure to clear the ROM in case there is some previous code)

How to use assembler:
  1. Download python
  2. Type the assembly code into asm.txt
  3. run the python file
  4. Go into hex.txt, press ctrl+A and ctrl+C, then use ctrl+V to paste it into the ROM.

Instruction set:
value = 8 bit value
rA/rB/rC = select register(3 bit, r0 to r7, r0 is constant zero)
con = there are 3 flags that are set after any alu operation: zero(z), carryout(c) and negative(n) !! The assembler only takes the single letter options: z, n or c
op = logic operations: and or nor xor rsh
port = 2 bit value: 0-3

nop = does nothing
add rA rB rC = rA + rB -> rC
sub rA rB rC = rA - rB -> rC
mul rA rB rC = rA * rB -> rC
log rA rB rC op = rA op rB -> rC
jmp value = value -> counter
brh value con = if con: value -> counter
lod rA rB = ram[rA] -> rB
str rA rB = rB -> ram[rA]
exr rA port = input-ports[port] -> ram[rA]
exw rA port = ram[rA] -> output-ports[port]
cal value = counter + 1 -> stack, value -> counter
ret = stack -> counter
hlt = stops the clock

labels are basically pointers in the code you can reference in jmp, brh and cal

written like this:

label:
  something

jmp label

Note that there is still some bugs especially with the call stack when using complex code however it still works.
