import os
import random
import struct

code = '''
#include <stdio.h>

int main(int argc, char **argv) {
        printf("Hello, world!\\r\\n");
        for (int i = 0; i < argc; i++) {
                printf("Argument %d: [%s]\\r\\n", i, argv[i]);
        }
        return 0;
}
'''

with open('./code/main.c', 'w') as file:
    file.write(code)

return_val = os.system('cd ./code && gcc main.c')

with open('./code/a.out', 'rb') as compiled:
    length = len(compiled.read())

j = 0

while not (seed := input("Please type a random seed: ")).isdigit():
    pass
seed = int(seed)%256

while return_val == 0:
    return_val = os.system('./code/a.out test > /dev/null')
    with open('./code/a.out', 'r+b') as compiled:
        data = list(bytearray(compiled.read()))
        data[random.randrange(0, length)] = seed
        compiled.seek(0)
        compiled.write(struct.pack("{}B".format(len(data)), *data)) # whatever this line does, it works
    j += 1
print(j)