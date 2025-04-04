import methods

def prepare_message(message, filler='X'):
    """
    Prepares a message for Playfair encryption:
    - Preserves case information for later restoration
    - Replaces spaces with underscores
    - Splits into digraphs (pairs of letters)
    - Ensures no pair has the same letter (inserts filler if needed)
    - Adds a filler character if the message length is odd
    
    Args:
        message: The plaintext message
        filler: Character to use when splitting doubles or odd-length messages
    
    Returns:
        List of digraphs (pairs of characters) and case map
    """
    # Replace spaces with underscores but preserve case information
    message = message.replace(' ', '_')
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

def encrypt_playfair(message, matrix):
    """
    Encrypts a message using the Playfair cipher while preserving case
    
    Args:
        message: The plaintext message
        matrix: The encryption matrix
    
    Returns:
        Encrypted message and case information
    """
    # Prepare the message and get case information
    digraphs, case_map = prepare_message(message)
    
    # Encrypt each pair
    encrypted_pairs = []
    matrix_size = len(matrix)
    
    for pair in digraphs:
        # Find positions of both characters
        pos1 = find_position(matrix, pair[0])
        pos2 = find_position(matrix, pair[1])
        
        # If either character is not in the matrix, replace with a fallback character
        if pos1 is None or pos2 is None:
            # Find first available character in matrix as fallback
            fallback = matrix[0][0]
            encrypted_pairs.append(fallback + fallback)
            continue
        
        row1, col1 = pos1
        row2, col2 = pos2
        
        # Apply Playfair rules
        if row1 == row2:  # Same row
            # Move one position to the right (with wrapping)
            encrypted_pairs.append(
                matrix[row1][(col1 + 1) % matrix_size] + 
                matrix[row2][(col2 + 1) % matrix_size]
            )
        elif col1 == col2:  # Same column
            # Move one position down (with wrapping)
            encrypted_pairs.append(
                matrix[(row1 + 1) % matrix_size][col1] + 
                matrix[(row2 + 1) % matrix_size][col2]
            )
        else:  # Rectangle
            # Swap columns
            encrypted_pairs.append(
                matrix[row1][col2] + 
                matrix[row2][col1]
            )
    
    # Encrypt the case information along with the message
    # We'll use a simple encoding scheme where 1=uppercase, 0=lowercase
    case_bits = ''.join('1' if is_upper else '0' for is_upper in case_map)
    
    # Convert case bits to characters (every 4 bits become a hex digit)
    case_encoded = ''
    for i in range(0, len(case_bits), 4):
        chunk = case_bits[i:i+4].ljust(4, '0')  # Ensure 4 bits, pad with 0s
        hex_value = int(chunk, 2)
        case_encoded += hex(hex_value)[2:]  # Convert to hex character
    
    # Return the encrypted message and case information
    encrypted = ''.join(encrypted_pairs)
    
    return encrypted, case_encoded

def main():
    """Main function for Playfair encryption"""
    print("=== Playfair Cipher Encryption with Case Preservation ===")
    
    # Get encryption parameters
    secret_key = input("Enter your secret key: ")
    matrix_size = 7  # Fixed for this assignment
    
    print("\nSelect matrix construction method:")
    print("1 - Plain Traditional")
    print("2 - Key-Based Traditional")
    print("3 - Spiral Completion")
    
    method = input("Method (1/2/3): ")
    
    # Generate the matrix
    if method == "1":
        matrix = methods.PT(secret_key, matrix_size)
    elif method == "2":
        matrix = methods.KBT(secret_key, matrix_size)
    elif method == "3":
        matrix = methods.SC(secret_key, matrix_size)
    else:
        print("Invalid method. Using Plain Traditional as default.")
        matrix = methods.PT(secret_key, matrix_size)
    
    # Display the matrix
    print("\nEncryption Matrix:")
    methods.print_matrix(matrix)
    
    # Get message to encrypt
    message = input("\nEnter the message to encrypt: ")
    
    # Encrypt the message
    encrypted, case_encoded = encrypt_playfair(message, matrix)
    
    # Display the result
    print("\nEncrypted message:")
    print(encrypted)
    
    print("\nCase information (needed for decryption):")
    print(case_encoded)
    
    # Display the prepared digraphs for clarity
    digraphs, _ = prepare_message(message)
    print("\nMessage split into digraphs:")
    print(' '.join(digraphs))
    
    # Display corresponding encrypted digraphs
    encrypted_digraphs = [encrypted[i:i+2] for i in range(0, len(encrypted), 2)]
    print("\nEncrypted digraphs:")
    print(' '.join(encrypted_digraphs))
    
    # Save encryption parameters
    save = input("\nSave encryption details to file? (y/n): ").lower()
    if save == 'y':
        filename = input("Enter filename (default: playfair_encryption.txt): ") or "playfair_encryption.txt"
        with open(filename, 'w') as f:
            f.write(f"Secret Key: {secret_key}\n")
            method_name = {
                "1": "Plain Traditional",
                "2": "Key-Based Traditional",
                "3": "Spiral Completion"
            }.get(method, "Plain Traditional")
            f.write(f"Construction Method: {method_name}\n")
            f.write(f"Original Message: {message}\n")
            f.write(f"Encrypted Message: {encrypted}\n")
            f.write(f"Case Information: {case_encoded}\n")
            f.write(f"Digraphs: {' '.join(digraphs)}\n")
            f.write(f"Encrypted Digraphs: {' '.join(encrypted_digraphs)}\n")
        print(f"Encryption details saved to {filename}")

if __name__ == "__main__":
    main() 