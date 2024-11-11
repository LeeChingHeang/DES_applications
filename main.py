import random
plaintext = "Ineedyou"
Key="LoveLong"

# convert plaintext and key to binary string
def str2bin(text):
    binary = ''.join(format(ord(i), '08b') for i in text)
    return binary

# permutation function 
def permute(arr, table):
    return [arr[i-1] for i in table]

def generate_unique_random_array(size, start, end):
    array =  random.sample(range(start, end), size)
    return array

# find the output of the Parity drop table
def PD_box(key_bin):
    # we input the key of 64-bits but we use only 56-bits so we need to generate a random array of 56 unique numbers from 1 to 64 for table for Permutation
    PD_table = generate_unique_random_array(56, 1, 64)
    # Key permutation 64-bit to 56-bit
    PD_permute_key = permute(key_bin, PD_table)
    return PD_permute_key

# Round key generation
# we need to slit the 56-bit key into two 28-bit keys
def split_key(key_bin, size):
    left = key_bin[:size]
    right = key_bin[size:]
    return left, right


# key rotation
# shift left
def shift_left(arr_bin, shift):
    arr = arr_bin[shift:] + arr_bin[:shift]
    return arr

# compression D-box 
def compression_Dbox(key_bin):
    # store the generated keys in a list
    generate_keys = []
    # generate compressed-Dbox table from 1-56 key to 48-bit key length
    # we need to use the same compressed_Dbox_table for all rounds of the key generation
    compressed_Dbox_table = generate_unique_random_array(48, 1, 56)
    # we need to split the 56-bit key into two 28-bit keys
    left, right = split_key(key_bin, 28)
    # shift our bit to the left
    for i in range(1, 17):
        # set the shift value for the key rotation 
        shift = 1 if i in [1, 2, 9, 16] else 2
        # shift the left and right keys
        left = shift_left(left, shift)
        right = shift_left(right, shift)
        # debug
        # print("\nRound: ", i)
        # print("Left key: ", left)
        # print("Right key: ", right)
        # combine the two 28-bit keys
        combined_output = left + right
        # print("Combined output: ", combined_output)

        # compresses 56-bit key to 48-bit key
        compressed_key = permute(combined_output, compressed_Dbox_table)
        generate_keys.append(compressed_key) 
    return generate_keys

# main function of the DES
def generate_random_table(start, end, size, max_occurrences):
    random_numbers = random.sample(max_occurrences* list(range(start, end)), size)
    return random_numbers
# Initial permutation
def ip_box(text_bin):
    ip_table = generate_unique_random_array(64, 1, 64)
    ip_permute_text = permute(text_bin(ip_table))
    return ip_permute_text

# Create matrix
def create_matrix(rows, cols, start, end):
    return [[random.randint(start, end) for _ in range(cols)] for _ in range(rows)]
# XOR operation of binary strings
def xor(bin1, bin2):
    # check if the binary strings are of the same length
    if len(bin1) != len(bin2):
        raise ValueError("Binary strings must have the same length.")
    return ''.join('0' if a == b else '1' for a, b in zip(bin1, bin2))
# slipt the binary string of array into chunks
def divide_chunks(input_string, chunk_size):
    return [input_string[i:i+chunk_size] for i in range(0, len(input_string), chunk_size)]

# F-function 
def f_function(permuted_text_bin, generate_key_bin):
    # Expansion D-box
    expansion_Dbox_table = generate_random_table(1, 32, 48, 2)
    expansion_output = permute(text_bin, expansion_Dbox_table)
    print("Expansion output: ", expansion_output)
    print("Key: ", generate_key_bin[0])
    print("XOR output: ", xor_output)
    for i in range(0,15):
        # perform XOR operation EXPANSION D-box output and the key
        xor_output = xor(expansion_output, generate_key_bin[i])
        # S-box
        # generate s-boxes_table
        s_box_table = create_matrix(8, 4, 0, 15)
        s_box = divide_chunks(xor_output, 6)
        
    print("S-box: ", s_box)
    # Straight Permutation D-box
    # Final permutation
    return expansion_output
## Expansion D-box
## S-box
## Straight Permutation D-box
# Final permutation
    




#===========+debugging+==================
text_bin = str2bin(plaintext)
key_bin = str2bin(Key)

PD_permute_key_output = PD_box(key_bin)
PD_left, PD_right = split_key(PD_permute_key_output, len(PD_permute_key_output)//2)
generate_keys = compression_Dbox(PD_permute_key_output)
debug = f_function(PD_right, generate_keys)
# print(PD_permute_key_output)
# print("PD Left key: ",PD_left)
# print("PD Right key: ", PD_right)
# keys_generation = compression_Dbox(PD_permute_key_output)
# print("key generate:",keys_generation[0])




