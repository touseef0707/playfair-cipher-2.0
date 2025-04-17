import methods

def prepare_message(message, filler='X'):
    """
    Prepares a message for Playfair encryption:
    - Preserves case information for later restoration
    - Splits into digraphs (pairs of letters)
    - Ensures no pair has the same letter (inserts filler if needed)
    - Adds a filler character if the message length is odd
    
    Args:
        message: The plaintext message
        filler: Character to use when splitting doubles or odd-length messages
    
    Returns:
        A tuple containing (list of digraphs, case_map)
    """
    # Create a case map (True for uppercase/non-alpha, False for lowercase)
    case_map = [c.isupper() or not c.isalpha() for c in message]
    
    # Convert to uppercase for matrix lookup
    prepared = message.upper()
    
    # Split into digraphs, ensuring no pair has the same letter
    digraphs = []
    i = 0
    
    while i < len(prepared):
        # If this is the last character, add filler
        if i == len(prepared) - 1:
            digraphs.append(prepared[i] + filler)
            case_map.append(True)  # Filler is uppercase
            break
            
        # If the pair would have the same letter, insert filler
        if prepared[i] == prepared[i + 1]:
            digraphs.append(prepared[i] + filler)
            case_map.append(True)  # Filler is uppercase
            i += 1
        else:
            digraphs.append(prepared[i] + prepared[i + 1])
            i += 2
    
    return digraphs, case_map

def find_position(matrix, char):
    """
    Finds the position of a character in the matrix
    
    Args:
        matrix: The encryption matrix
        char: The character to find
    
    Returns:
        Tuple (row, col) or None if not found
    """
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == char:
                return (i, j)
    return None

def encrypt_digraph(c1, c2, matrix, matrix_flat):
    """
    Encrypt a single digraph (pair of characters) using Playfair cipher rules
    
    Args:
        c1: First character of the pair
        c2: Second character of the pair
        matrix: The encryption matrix
        matrix_flat: Flattened version of the matrix
    
    Returns:
        Encrypted pair of characters
    """
    # Find positions of both characters
    pos1 = find_position(matrix, c1)
    pos2 = find_position(matrix, c2)
    
    # If either character is not in the matrix, use fallback
    if pos1 is None or pos2 is None:
        return matrix[0][0] + matrix[0][0]  # Fallback
    
    i1, j1 = pos1
    i2, j2 = pos2
    matrix_size = len(matrix)
    
    # Apply Playfair rules with modifications
    if i1 == i2:  # Same row rule - shift 2 steps toward bottom
        # Move two positions down (with wrapping)
        new_row1 = (i1 + 2) % matrix_size
        new_row2 = (i2 + 2) % matrix_size
        
        encrypted_pair = (
            matrix[new_row1][j1] + 
            matrix[new_row2][j2]
        )
    elif j1 == j2:  # Same column rule - shift 3 steps toward right
        # Move three positions right (with wrapping)
        new_col1 = (j1 + 3) % matrix_size
        new_col2 = (j2 + 3) % matrix_size
        
        encrypted_pair = (
            matrix[i1][new_col1] + 
            matrix[i2][new_col2]
        )
    else:  # Rectangle rule
        # Swap columns
        encrypted_pair = (
            matrix[i1][j2] + 
            matrix[i2][j1]
        )
    
    return encrypted_pair

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

def apply_ascii_transform(text, secret_key):
    """
    Apply a reversible ASCII-based transformation using the secret key
    
    Args:
        text: The text to transform
        secret_key: The secret key to use
    
    Returns:
        Transformed text
    """
    # Define allowed characters
    valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-{}"
    
    # Generate a sequence of numbers from the secret key
    key_values = generate_key_values(secret_key)
    
    # Apply the transformation
    result = []
    for i, char in enumerate(text):
        # Get ASCII value
        ascii_val = ord(char)
        # Get the key value for this position (cycling through key values)
        key_val = key_values[i % len(key_values)]
        
        # Transform character within valid character set
        valid_chars_list = list(valid_chars)
        original_index = valid_chars_list.index(char) if char in valid_chars_list else 0
        new_index = (original_index + key_val) % len(valid_chars_list)
        new_char = valid_chars_list[new_index]
        
        result.append(new_char)
    
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

def shuffle_text(text, shuffle_key):
    """
    Shuffle the text using the provided shuffle key
    
    Args:
        text: The text to shuffle
        shuffle_key: The key to use for shuffling
    
    Returns:
        Shuffled text
    """
    if not text:
        return ""
        
    # Generate shuffling indices
    indices = generate_shuffle_indices(shuffle_key, len(text))
    
    # Create a mapping from original positions to new positions
    position_map = {}
    for new_pos, old_pos in enumerate(indices):
        position_map[old_pos] = new_pos
    
    # Apply the shuffling
    shuffled = [''] * len(text)
    for old_pos, char in enumerate(text):
        new_pos = position_map[old_pos]
        shuffled[new_pos] = char
    
    return ''.join(shuffled)

def encrypt_playfair(message, matrix, secret_key):
    """
    Encrypt a message using the Playfair cipher with enhanced rules.
    
    IMPORTANT: This implementation is designed for passwords.
    - Messages should NOT contain spaces (will raise an error)
    - Uses 'X' as a filler character for repeated letters and odd-length messages
    - Case information is preserved separately
    
    Args:
        message: The plaintext message to encrypt
        matrix: The encryption matrix (7x7)
        secret_key: The secret key used for additional encryption steps
    
    Returns:
        A tuple containing (encrypted_message, case_information)
    """
    # Validate input characters (no spaces allowed)
    valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-{}"
    for char in message:
        if char not in valid_chars:
            if char == ' ':
                raise ValueError("Spaces are not allowed in passwords. Please remove all spaces.")
            else:
                raise ValueError(f"Invalid character '{char}' in text. Only letters, numbers, and these special characters are allowed: !@#$%^&*()_+-{{}}")
    
    # Prepare the message (create digraphs with fillers) and track case
    digraphs, case_map = prepare_message(message, filler='X')
    
    # Create a flattened version of the matrix for indexing
    matrix_flat = []
    for row in matrix:
        for char in row:
            matrix_flat.append(char)
    
    # Encrypt each pair
    encrypted_pairs = []
    
    for dg in digraphs:
        c1, c2 = dg[0], dg[1]
        encrypted_pair = encrypt_digraph(c1, c2, matrix, matrix_flat)
        encrypted_pairs.append(encrypted_pair)
    
    # Join the encrypted pairs
    encrypted = ''.join(encrypted_pairs)
    
    # Apply ASCII transformation
    transformed = apply_ascii_transform(encrypted, secret_key)
    
    # Encode the case information
    # Convert case map to bits where 1=uppercase, 0=lowercase
    case_bits = ''
    for is_upper in case_map:
        case_bits += '1' if is_upper else '0'
    
    # Convert case bits to hexadecimal for compact representation
    case_encoded = ''
    for i in range(0, len(case_bits), 4):
        chunk = case_bits[i:i+4].ljust(4, '0')  # Ensure 4 bits, pad with 0s
        hex_value = int(chunk, 2)
        case_encoded += hex(hex_value)[2:]  # Convert to hex character
    
    # Shuffle the transformed text using the case information as a key
    shuffled = shuffle_text(transformed, case_encoded)
    
    return shuffled, case_encoded

def main():
    """Main function for Playfair encryption"""
    print("=== Playfair Cipher Encryption for Passwords ===")
    print("Note: This implementation is designed for passwords without spaces.")
    
    # Ask if user wants to use a file for input
    use_file = input("Use a file for input? (y/n): ").lower() == 'y'
    
    if use_file:
        input_file = input("Enter input filename (default: input.txt): ") or "input.txt"
        try:
            with open(input_file, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 1:
                    secret_key = lines[0].strip()
                    message = lines[1].strip() if len(lines) > 1 else input("\nEnter the password to encrypt: ")
                else:
                    print("File does not contain enough information. Using manual input.")
                    secret_key = input("Enter your secret key: ")
                    message = input("\nEnter the password to encrypt: ")
        except FileNotFoundError:
            print(f"File {input_file} not found. Using manual input.")
            secret_key = input("Enter your secret key: ")
            message = input("\nEnter the password to encrypt: ")
    else:
        # Get encryption parameters manually
        secret_key = input("Enter your secret key: ")
        message = input("\nEnter the password to encrypt: ")
    
    matrix_size = 7  # Fixed for this assignment
    
    # Using fixed special characters
    special_chars = methods.DEFAULT_SPECIAL_CHARS
    print(f"Using fixed special characters: {special_chars}")
    
    # Generate the matrix (Plain Traditional only)
    matrix = methods.PT(secret_key, matrix_size, special_chars)
    print("\nEncryption Matrix (Plain Traditional):")
    methods.print_matrix(matrix)
    
    try:
        # Encrypt the message
        encrypted, case_encoded = encrypt_playfair(message, matrix, secret_key)
        
        # Display the result
        print("\nEncrypted message:")
        print(encrypted)
        
        print("\nCase information (needed for decryption):")
        print(case_encoded)
        
        # Display the prepared digraphs for clarity
        digraphs, _ = prepare_message(message)
        print("\nPassword split into digraphs:")
        print(' '.join(digraphs))
        
        # Always offer to save to file
        filename = "encryption.txt"
        save = input(f"\nSave encryption results to {filename}? (y/n): ").lower()
        if save == 'y':
            with open(filename, 'w') as f:
                f.write(f"{secret_key}\n")
                f.write(f"{encrypted}\n")
                f.write(f"{case_encoded}\n")
            print(f"Encryption details saved to {filename}")
    
    except ValueError as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main() 