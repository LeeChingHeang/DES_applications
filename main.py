import random

# convert plaintext and key to binary string
def str2bin(text):
    binary = ''.join(format(ord(i), '08b') for i in text)
    return binary
# convert binary string to string
def bin2str(binary):
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
# permutation function 
def permute(arr, table):
    return [arr[i-1] for i in table]

def generate_unique_random_array(size, start, end):
    array =  random.sample(range(start, end), size)
    return array

# find the output of the Parity drop table
def PD_box(key_bin):
    # we input the key of 64-bits but we use only 56-bits so we need to generate a random array of 56 unique numbers from 1 to 64 for table for Permutation
    PD_table = generate_unique_random_array(56, 1, 65)
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
    compressed_Dbox_table = generate_unique_random_array(48, 1, 57)
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
    ip_table = generate_unique_random_array(64, 1, 65)
    ip_permute_text = permute(text_bin,ip_table)
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
def f_function(plaintext_bin_arr_right, generate_key_bin):
    # Expansion D-box
    expansion_Dbox_table = generate_random_table(1, 33, 48, 2)
    expansion_output = permute(plaintext_bin_arr_right, expansion_Dbox_table)
    # perform XOR operation EXPANSION D-box output and the key
    xor_output = xor(expansion_output, generate_key_bin)
    # create S-boxes
    s_box = divide_chunks(xor_output, 6)
    chunk = len(s_box)

    s_box_32bits = []
    # 7 it the max index of chunk that s_box contain which have 8 chunk so -1 equal to number of the max index
    for j in range(8):
        s_box_table = create_matrix(4, 16, 0, 15)
        row = int(s_box[j][0] + s_box[j][5], 2)
        col = int(s_box[j][1:5], 2)
        
        bin_sbox_value = bin(s_box_table[row][col])[2:].zfill(4)
        # s_box_32bits += bin(s_box_table[row][col])[2:].zfill(4) 
        s_box_32bits.extend(list(bin_sbox_value))

    # Straight Permutation D-box
    # Final permutation
    return s_box_32bits
# swap function
def swap(left, right):
    return right, left
## Straight Permutation D-box

def encrypt(left, right, key):
    f_function_output = f_function(right, key)
    xor_L_fR_output = xor(left, f_function_output)
    left_new, right_new = swap(left, xor_L_fR_output)
    return left_new, right_new
# decryption it just a reverse oder of the key rotation just perform the key rotation in reverse order 


def main():
    plaintext = "Ineedyou"
    Key="LoveLong"
    # convert plaintext and key to binary string
    key_bin = str2bin(Key)
    plaintext_bin = str2bin(plaintext)
    # Initial permutation
    IP_text_bin = ip_box(plaintext_bin)

    # Parity drop box
    PD_permute_key_output = PD_box(key_bin)    
    # generate keys
    generate_keys = compression_Dbox(PD_permute_key_output)
    # split the IP_permutation into two halves
    IP_left, IP_right = split_key(IP_text_bin, len(IP_text_bin)//2)
    
    for i in range(1, 17):
        # f_function_output = f_function(IP_right, generate_keys[i-1])
        # xor_L_fR_output = xor(IP_left, f_function_output)
        # IP_left, IP_right = swap(IP_left, xor_L_fR_output)
        IP_left, IP_right = encrypt(IP_left, IP_right, generate_keys[i-1])

    
    # concatenate the left and right keys
    combined_output = list(IP_left + IP_right)
    FP_box_table = generate_unique_random_array(64, 1, 65)
    FP_permute_output = permute(combined_output, FP_box_table)
    print("Cipher text array: ", FP_permute_output)
    print("Cipher text String: ", ''.join(FP_permute_output))
    print("Cipher text: ", bin2str(''.join(FP_permute_output)))
    # FP_box = permute(combined_output, FP_box_table)
    # # Final permutation
    # print("Cipher text: ", combined_output)
    # # print("Cipher text: ", bin2str(''.join(combined_output)))
    # # print("Cipher text: ", bin2str(''.join(FP_box)))



if __name__ == "__main__":
    main()
#===========+debugging+==================
# text_bin = str2bin(plaintext)
# key_bin = str2bin(Key)

# PD_permute_key_output = PD_box(key_bin)
# PD_left, PD_right = split_key(PD_permute_key_output, len(PD_permute_key_output)//2)
# generate_keys = compression_Dbox(PD_permute_key_output)
# debug = f_function(PD_right, generate_keys[0])
# print(PD_permute_key_output)
# print("PD Left key: ",PD_left)
# print("PD Right key: ", PD_right)
# keys_generation = compression_Dbox(PD_permute_key_output)
# print("key generate:",keys_generation[0])




