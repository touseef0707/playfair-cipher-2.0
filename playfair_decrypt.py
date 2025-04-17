import methods

def find_position(matrix, char):
    """
    Finds the position of a character in the matrix
    
    Args:
        matrix: The decryption matrix
        char: The character to find
    
    Returns:
        Tuple (row, col) or None if not found
    """
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == char:
                return (i, j)
    return None

def decrypt_digraph(e1, e2, matrix):
    """
    Decrypt a single digraph (pair of characters) using Playfair cipher rules
    
    Args:
        e1: First encrypted character
        e2: Second encrypted character
        matrix: The decryption matrix
    
    Returns:
        The decrypted character pair
    """
    # Find positions of encrypted characters
    pos1 = find_position(matrix, e1)
    pos2 = find_position(matrix, e2)
    
    # If either character is not in the matrix, return a placeholder
    if pos1 is None or pos2 is None:
        return "??"
    
    i1, j1 = pos1
    i2, j2 = pos2
    matrix_size = len(matrix)
    
    # Apply the appropriate decryption rule based on character positions
    if i1 == i2:  # Same row rule - shift 2 steps up
        # Move two positions up (with wrapping)
        decrypted_pair = (
            matrix[(i1 - 2) % matrix_size][j1] + 
            matrix[(i2 - 2) % matrix_size][j2]
        )
    elif j1 == j2:  # Same column rule - shift 3 steps left
        # Move three positions left (with wrapping)
        decrypted_pair = (
            matrix[i1][(j1 - 3) % matrix_size] + 
            matrix[i2][(j2 - 3) % matrix_size]
        )
    else:  # Rectangle rule
        # For rectangle rule, we swap columns (same for encryption and decryption)
        decrypted_pair = (
            matrix[i1][j2] + 
            matrix[i2][j1]
        )
    
    return decrypted_pair

def generate_key_values(secret_key):
    """
    Generate a sequence of numbers from the secret key without using hash functions
    
    Args:
        secret_key: The secret key
    
    Returns:
        List of integers derived from the key
    """
    # Convert each character to its ASCII value
    key_values = [ord(c) for c in secret_key]
    
    # Extend the key values to make it more complex
    extended_values = []
    sum_so_far = 0
    
    for i, val in enumerate(key_values):
        sum_so_far = (sum_so_far + val) % 256
        product = (val * (i + 1)) % 256
        extended_values.append(sum_so_far)
        extended_values.append(product)
    
    return extended_values

def reverse_ascii_transform(text, secret_key):
    """
    Reverse the ASCII-based transformation using the secret key
    
    Args:
        text: The transformed text
        secret_key: The secret key used for the transformation
    
    Returns:
        Original text
    """
    # Define allowed characters
    valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-{}"
    valid_chars_list = list(valid_chars)
    
    # Generate a sequence of numbers from the secret key
    key_values = generate_key_values(secret_key)
    
    # Apply the reverse transformation
    result = []
    for i, char in enumerate(text):
        # Get the key value for this position (cycling through key values)
        key_val = key_values[i % len(key_values)]
        
        # Reverse transform character within valid character set
        if char in valid_chars_list:
            original_index = valid_chars_list.index(char)
            new_index = (original_index - key_val) % len(valid_chars_list)
            new_char = valid_chars_list[new_index]
            result.append(new_char)
        else:
            # If the character isn't in our valid set, keep it as is (shouldn't happen)
            result.append(char)
    
    return ''.join(result)

def generate_shuffle_indices(shuffle_key, length):
    """
    Generate shuffling indices based on the shuffle key
    
    Args:
        shuffle_key: The key to use for shuffling
        length: The length of the text to shuffle
    
    Returns:
        A list of indices for shuffling
    """
    # Convert the shuffle key to a list of integers
    if len(shuffle_key) == 0:
        return list(range(length))
        
    # Convert shuffle key chars to values
    key_values = []
    for c in shuffle_key:
        # Convert to a value between 0-15
        if c.isdigit():
            key_values.append(int(c))
        elif 'A' <= c <= 'F' or 'a' <= c <= 'f':
            key_values.append(10 + ord(c.upper()) - ord('A'))
        else:
            key_values.append(ord(c) % 16)
    
    # Generate indices
    indices = list(range(length))
    
    # Shuffle the indices using Fisher-Yates algorithm with the key values
    for i in range(length - 1, 0, -1):
        # Use key_values to determine the swap index
        j = key_values[i % len(key_values)] % (i + 1)
        # Swap indices[i] and indices[j]
        indices[i], indices[j] = indices[j], indices[i]
    
    return indices

def unshuffle_text(text, shuffle_key):
    """
    Reverse the shuffling of text using the provided shuffle key
    
    Args:
        text: The shuffled text
        shuffle_key: The key used for shuffling
    
    Returns:
        Unshuffled text
    """
    if not text:
        return ""
        
    # Generate shuffling indices
    indices = generate_shuffle_indices(shuffle_key, len(text))
    
    # Create a mapping from new positions to original positions
    position_map = {}
    for new_pos, old_pos in enumerate(indices):
        position_map[new_pos] = old_pos
    
    # Apply the unshuffling
    unshuffled = [''] * len(text)
    for new_pos, char in enumerate(text):
        old_pos = position_map[new_pos]
        unshuffled[old_pos] = char
    
    return ''.join(unshuffled)

def decrypt_playfair(encrypted, case_encoded, matrix, secret_key):
    """
    Decrypts a message using the Playfair cipher with modified rules.
    
    IMPORTANT: This implementation is designed for passwords.
    - Does not handle spaces (passwords typically don't have spaces)
    - Uses 'X' as a filler character for repeated letters and odd-length messages
    - Case information is restored from the encoding
    
    Args:
        encrypted: The encrypted message
        case_encoded: Encoded case information (with shuffle method prefix)
        matrix: The decryption matrix
        secret_key: The secret key used for encryption
    
    Returns:
        Decrypted message with original case restored
    """
    # Validate input characters
    valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-{}"
    for char in encrypted:
        if char not in valid_chars:
            raise ValueError(f"Invalid character '{char}' in encrypted text. Only letters, numbers, and these special characters are allowed: !@#$%^&*()_+-{{}}")
    
    # Determine shuffle key based on case_encoded
    if case_encoded:
        # Case information is available, use it as the shuffle key
        shuffle_key = case_encoded
    else:
        # No case information, use a sequence derived from the secret key
        key_values = generate_key_values(secret_key)
        shuffle_key = ''.join([format(v % 16, 'x') for v in key_values])
    
    # Unshuffle the text
    unshuffled = unshuffle_text(encrypted, shuffle_key)
    
    # Reverse the ASCII transformation
    transformed = reverse_ascii_transform(unshuffled, secret_key)
    
    # Split into digraphs
    digraphs = [transformed[i:i+2] for i in range(0, len(transformed), 2)]
    
    # Decrypt each pair
    decrypted_pairs = []
    
    for dg in digraphs:
        e1, e2 = dg[0], dg[1]
        decrypted_pair = decrypt_digraph(e1, e2, matrix)
        decrypted_pairs.append(decrypted_pair)
    
    # Join the decrypted pairs
    decrypted = ''.join(decrypted_pairs)
    
    # Process the result to handle fillers and special cases
    processed = []
    i = 0
    
    while i < len(decrypted):
        # Current character
        curr = decrypted[i]
        
        # Handle X as a filler character
        if i + 1 < len(decrypted) and decrypted[i+1].upper() == 'X':
            # Check if X is a filler
            if i + 2 < len(decrypted) and decrypted[i].upper() == decrypted[i+2].upper():
                # X between same letters - it's a filler
                processed.append(curr)
                i += 2  # Skip the X
            elif i + 2 >= len(decrypted):
                # X at the end - it's a trailing filler
                processed.append(curr)
                break
            else:
                # X is probably not a filler
                processed.append(curr)
                i += 1
        else:
            processed.append(curr)
            i += 1
    
    # Join the processed result
    result = ''.join(processed)
    
    # Decode case information from hex to binary
    case_bits = ''
    for c in case_encoded:
        try:
            # Convert hex digit to 4 binary digits
            bits = bin(int(c, 16))[2:].zfill(4)
            case_bits += bits
        except ValueError:
            # If not a valid hex digit, skip it
            continue
    
    # Apply case information to restore original case
    result_with_case = ''
    for i, char in enumerate(result):
        if i < len(case_bits) and char.isalpha():
            # 1 = uppercase, 0 = lowercase
            if case_bits[i] == '0':
                result_with_case += char.lower()
            else:
                result_with_case += char.upper()
        else:
            # If we run out of case bits or it's not a letter, keep as is
            result_with_case += char
    
    return result_with_case

def main():
    """Main function for Playfair decryption"""
    print("=== Playfair Cipher Decryption for Passwords ===")
    print("Note: This implementation is designed for passwords without spaces.")
    
    # Get decryption parameters
    secret_key = input("Enter your secret key: ")
    matrix_size = 7  # Fixed for this assignment
    
    # Using fixed special characters
    special_chars = methods.DEFAULT_SPECIAL_CHARS
    print(f"Using fixed special characters: {special_chars}")
    
    # Generate the matrix (Plain Traditional only)
    matrix = methods.PT(secret_key, matrix_size, special_chars)
    print("\nDecryption Matrix (Plain Traditional):")
    methods.print_matrix(matrix)
    
    # Get encrypted message and metadata
    encrypted = input("\nEnter the encrypted message: ")
    case_encoded = input("Enter the case information: ")
    
    # Decrypt the message
    decrypted = decrypt_playfair(encrypted, case_encoded, matrix, secret_key)
    
    # Display the result
    print("\nDecrypted message:")
    print(decrypted)
    
    # Save decryption details
    save = input("\nSave decryption details to file? (y/n): ").lower()
    if save == 'y':
        filename = input("Enter filename (default: playfair_decryption.txt): ") or "playfair_decryption.txt"
        with open(filename, 'w') as f:
            f.write(f"Secret Key: {secret_key}\n")
            f.write(f"Construction Method: Plain Traditional\n")
            f.write(f"Encrypted Message: {encrypted}\n")
            f.write(f"Case Information: {case_encoded}\n")
            f.write(f"Decrypted Message: {decrypted}\n")
        print(f"Decryption details saved to {filename}")

if __name__ == "__main__":
    main() 