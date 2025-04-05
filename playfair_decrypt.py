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

def decrypt_playfair(encrypted, case_encoded, matrix):
    """
    Decrypts a message using the Playfair cipher.
    
    IMPORTANT: This implementation is designed for passwords.
    - Does not handle spaces (passwords typically don't have spaces)
    - Uses 'X' as a filler character for repeated letters and odd-length messages
    - Case information is restored from the encoding
    
    Args:
        encrypted: The encrypted message
        case_encoded: Encoded case information
        matrix: The decryption matrix
    
    Returns:
        Decrypted message with original case restored
    """
    # Validate input characters
    valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-{}"
    for char in encrypted:
        if char not in valid_chars:
            raise ValueError(f"Invalid character '{char}' in encrypted text. Only letters, numbers, and these special characters are allowed: !@#$%^&*()_+-{{}}")
    
    # Split into digraphs
    digraphs = [encrypted[i:i+2] for i in range(0, len(encrypted), 2)]
    
    # Decrypt each pair
    decrypted_pairs = []
    matrix_size = len(matrix)
    
    for pair in digraphs:
        # Find positions of both characters
        pos1 = find_position(matrix, pair[0])
        pos2 = find_position(matrix, pair[1])
        
        # If either character is not in the matrix, use placeholder
        if pos1 is None or pos2 is None:
            decrypted_pairs.append("??")
            continue
            
        row1, col1 = pos1
        row2, col2 = pos2
        
        # Apply Playfair decryption rules (reverse of encryption)
        if row1 == row2:  # Same row
            # Move one position to the left (with wrapping)
            decrypted_pairs.append(
                matrix[row1][(col1 - 1) % matrix_size] + 
                matrix[row2][(col2 - 1) % matrix_size]
            )
        elif col1 == col2:  # Same column
            # Move one position up (with wrapping)
            decrypted_pairs.append(
                matrix[(row1 - 1) % matrix_size][col1] + 
                matrix[(row2 - 1) % matrix_size][col2]
            )
        else:  # Rectangle
            # Swap columns
            decrypted_pairs.append(
                matrix[row1][col2] + 
                matrix[row2][col1]
            )
    
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
    
    print("\nSelect matrix construction method:")
    print("1 - Plain Traditional")
    print("2 - Key-Based Traditional")
    print("3 - Spiral Completion")
    method = input("Method (1/2/3): ")
    
    # Generate the matrix
    if method == "1":
        matrix = methods.PT(secret_key, matrix_size, special_chars)
    elif method == "2":
        matrix = methods.KBT(secret_key, matrix_size, special_chars)
    elif method == "3":
        matrix = methods.SC(secret_key, matrix_size, special_chars)
    else:
        print("Invalid method. Using Plain Traditional as default.")
        matrix = methods.PT(secret_key, matrix_size, special_chars)
    
    # Display the matrix
    print("\nDecryption Matrix:")
    methods.print_matrix(matrix)
    
    # Get encrypted message and metadata
    encrypted = input("\nEnter the encrypted message: ")
    case_encoded = input("Enter the case information: ")
    
    # Decrypt the message
    decrypted = decrypt_playfair(encrypted, case_encoded, matrix)
    
    # Display the result
    print("\nDecrypted message:")
    print(decrypted)
    
    # Save decryption details
    save = input("\nSave decryption details to file? (y/n): ").lower()
    if save == 'y':
        filename = input("Enter filename (default: playfair_decryption.txt): ") or "playfair_decryption.txt"
        with open(filename, 'w') as f:
            f.write(f"Secret Key: {secret_key}\n")
            method_name = {
                "1": "Plain Traditional",
                "2": "Key-Based Traditional",
                "3": "Spiral Completion"
            }.get(method, "Plain Traditional")
            f.write(f"Construction Method: {method_name}\n")
            f.write(f"Special Characters: {special_chars}\n")
            f.write(f"Encrypted Message: {encrypted}\n")
            f.write(f"Case Information: {case_encoded}\n")
            f.write(f"Decrypted Message: {decrypted}\n")
        print(f"Decryption details saved to {filename}")

if __name__ == "__main__":
    main() 