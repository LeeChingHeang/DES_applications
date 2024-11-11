import random
plaintext = "Ineedyou"
Key="LoveLong"


# make the output of array into maxtrix formated 
def print_array(array):


# Convert the plaintext and key to binary
def str2bin(text):
    binary = ''.join(format(ord(i), '08b') for i in text)
    return binary

bin_plaintext = str2bin(plaintext)
bin_key = str2bin(Key)

# convert binary to 1 demensional array
def bin2arr(binary):
    arr = []
    for i in binary:
        arr.append(int(i))
    return arr

arr_plaintext = bin2arr(bin_plaintext)
arr_key = bin2arr(bin_key)
# print(arr_plaintext)
# print(arr_key)

# initiate the permutation table
IP_Table = random.sample(range(1, 65), 64)
# IP_Table = generate_matrix()

# Generate the permutation table

IP_permutation=[]
def implement_IP(IP_Table, arr_plaintext):
    for i in IP_Table:
        IP_permutation.append(arr_plaintext[i-1])
    return IP_permutation

IP_permutation = implement_IP(IP_Table, arr_plaintext)

print("Plaintext_bin_arra = ", arr_plaintext)
print("\nIP_Table = ", IP_Table)
print("\nIP_permutation = ", IP_permutation)

# Split the IP_permutation into two halves


def split_array(array):
    # Calculate the midpoint
    midpoint = len(array) // 2
    
    # Split the array into two halves
    first_half = array[:midpoint]
    second_half = array[midpoint:]
    
    return first_half, second_half

left, right = split_array(IP_permutation)
print("\nLeft: ", left)
print("\nRight: ", right)


# expansion permutation
EP_Table = random.choices(range(1, 33), k=32)
# copy the EP_Table to EP and extend it to 48 bits
EP = EP_Table[:]
# extract the first 2 rows of EP_Table
extract_first_2row = EP_Table[:16]

EP.extend(extract_first_2row)

# print("\nEP_Table: ",EP_Table)
print("\nEP: ",EP)

def implement_EP(EP, right):
    EP_permutation = []
    for i in EP:
        EP_permutation.append(right[i-1])
    return EP_permutation

def xor(EP, key):
    xor_result = []
    for i in range(len(EP)):
        xor_result.append(EP[i] ^ key[i])
    return xor_result
# S-boxes substitution
# divide the 48 bits into 8 groups of 6 bits
def split_6bits(EP_permutation):
    split_6bits = []
    for i in range(0, len(EP_permutation), 6):
        split_6bits.append(EP_permutation[i:i+6])
    return split_6bits

# create the S-boxes table random which is 4x16 which range from 0 to 15
S_box = random.choices(range(0, 16), k=15)
print("\nS-box: ", print_array(S_box))


EP_permutation = implement_EP(EP, right)
print("\nEP_permutation: ", print_array(EP_permutation))