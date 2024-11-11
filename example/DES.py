class DES:
    # Initial Permutation Table
    IP = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    # Final Permutation Table
    FP = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

    # Expansion D-box Table
    E = [32, 1, 2, 3, 4, 5,
         4, 5, 6, 7, 8, 9,
         8, 9, 10, 11, 12, 13,
         12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21,
         20, 21, 22, 23, 24, 25,
         24, 25, 26, 27, 28, 29,
         28, 29, 30, 31, 32, 1]

    # S-box Table
    S_BOX = [
        # S1
        [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
        # S2-S8 would go here (omitted for brevity)
    ]

    def __init__(self, key):
        self.key = self.prepare_key(key)
        self.subkeys = self.generate_subkeys()

    def prepare_key(self, key):
        # Convert key to binary
        if isinstance(key, str):
            return ''.join(format(ord(c), '08b') for c in key)[:64]
        return format(key, '064b')

    def permute(self, block, table):
        return ''.join(block[i-1] for i in table)

    def generate_subkeys(self):
        # Implementation of key schedule
        subkeys = []
        # PC-1 permutation would go here
        # For each round, generate a subkey
        left = self.key[:28]
        right = self.key[28:56]
        
        for i in range(16):
            # Perform left shifts
            left = left[1:] + left[0]
            right = right[1:] + right[0]
            # Combine and permute
            subkey = left + right
            # PC-2 permutation would go here
            subkeys.append(subkey)
        return subkeys

    def encrypt_block(self, block):
        # Initial permutation
        block = self.permute(block, self.IP)
        
        left = block[:32]
        right = block[32:]
        
        # 16 rounds of Feistel network
        for i in range(16):
            # Expansion
            expanded = self.permute(right, self.E)
            # XOR with subkey
            xored = ''.join('1' if a != b else '0' 
                          for a, b in zip(expanded, self.subkeys[i]))
            # S-box substitution
            sbox_out = ''
            for j in range(8):
                chunk = xored[j*6:(j+1)*6]
                row = int(chunk[0] + chunk[5], 2)
                col = int(chunk[1:5], 2)
                sbox_out += format(self.S_BOX[0][row][col], '04b')  # Using S1 for all boxes
            
            # P-box permutation would go here
            
            # XOR with left half
            new_right = ''.join('1' if a != b else '0' 
                              for a, b in zip(left, sbox_out))
            left = right
            right = new_right
        
        # Final permutation
        result = self.permute(right + left, self.FP)
        return result

    def encrypt(self, message):
        # Pad message to 64-bit blocks
        if isinstance(message, str):
            message = ''.join(format(ord(c), '08b') for c in message)
        message = message + '0' * (64 - len(message) % 64)
        
        # Encrypt each block
        cipher = ''
        for i in range(0, len(message), 64):
            block = message[i:i+64]
            cipher += self.encrypt_block(block)
        return cipher

# Example usage
def main():
    # Create a DES instance with a key
    key = "Lovelong"  # 8-byte key
    des = DES(key)
    
    # Encrypt a message
    message = "Ineedyou"
    cipher = des.encrypt(message)
    
    print(f"Original message: {message}")
    print(f"Encrypted (binary): {cipher}")
    print(f"Encrypted (hex): {hex(int(cipher, 2))[2:]}")

if __name__ == "__main__":
    main()