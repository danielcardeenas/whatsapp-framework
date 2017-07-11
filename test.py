def char_bin(x):
    ascii_value = ord(x)
    bin_value = bin(ascii_value)
    return str(bin_value)
    
print(char_bin('A'))