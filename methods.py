import string

# Fixed set of 13 special characters that will always be used
DEFAULT_SPECIAL_CHARS = "!@#$%^&*()_-+"

# Define the allowed character set
ALLOWED_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-{}"

def validate_input(text, is_key=False):
    """
    Validate that the input contains only allowed characters.
    
    Args:
        text (str): The input text to validate
        is_key (bool): Whether this is a key validation (True) or plaintext validation (False)
    
    Returns:
        tuple: (is_valid, error_message) - is_valid is True if valid, False otherwise
                                          - error_message contains the reason if invalid
    """
    if not text:
        return False, "Input cannot be empty."
    
    invalid_chars = []
    for char in text:
        if char not in ALLOWED_CHARS and char != ' ':  # Spaces handled separately
            invalid_chars.append(char)
    
    if invalid_chars:
        unique_invalid = set(invalid_chars)
        error_msg = f"Invalid character{'s' if len(unique_invalid) > 1 else ''} found: {', '.join(repr(c) for c in unique_invalid)}.\n"
        error_msg += f"Only the following characters are allowed:\n"
        error_msg += f"- Letters (A-Z, a-z)\n"
        error_msg += f"- Numbers (0-9)\n"
        error_msg += f"- Special characters: !@#$%^&*()_+-{{}}"
        return False, error_msg
    
    if ' ' in text:
        if is_key:
            return False, "Spaces are not allowed in keys. Please remove all spaces."
        else:
            return True, "Note: Spaces in the message will be removed during encryption."
    
    return True, ""

def main():
    """Get matrix generation parameters from user"""
    while True:
        secret_key = input("Enter your secret key: ")
        is_valid, error_msg = validate_input(secret_key, is_key=True)
        if is_valid:
            break
        print(f"Error: {error_msg}")
        print("Please try again.")
    
    matrix_size = 7  # Fixed for this assignment
    
    # Special characters are fixed and cannot be changed
    special_chars = DEFAULT_SPECIAL_CHARS
    
    print("\nSelect matrix construction method:")
    print("1 - Plain Traditional")
    print("2 - Key-Based Traditional")
    print("3 - Spiral Completion")
    
    method = input("Method (1/2/3): ")
    
    # Generate and display the matrix
    if method == "1":
        matrix = PT(secret_key, matrix_size, special_chars)
    elif method == "2":
        matrix = KBT(secret_key, matrix_size, special_chars)
    elif method == "3":
        matrix = SC(secret_key, matrix_size, special_chars)
    else:
        print("Invalid method. Using Plain Traditional as default.")
        matrix = PT(secret_key, matrix_size, special_chars)
    
    print_matrix(matrix)
    return matrix

def sanitize_key(key):
    """
    Sanitize the key by converting to uppercase and removing spaces.
    The key must only contain allowed characters.
    """
    # Validate the key first
    is_valid, error_msg = validate_input(key, is_key=True)
    if not is_valid:
        raise ValueError(error_msg)
    
    return ''.join(c.upper() for c in key if c.isalnum() or c in DEFAULT_SPECIAL_CHARS)

def PT(key, matrix_size, special_chars=DEFAULT_SPECIAL_CHARS):
    """
    Implement the Plain Traditional matrix construction method
    
    Args:
        key: The secret key
        matrix_size: Size of the matrix (e.g., 7 for a 7x7 matrix)
        special_chars: Special characters to include in the matrix
    
    Returns:
        A square matrix filled according to the Plain Traditional method
    """
    # Process the key
    key = sanitize_key(key)
    
    # Create the standard character set (26 letters + 10 digits + special chars)
    alphabet = string.ascii_uppercase
    digits = "0123456789"
    
    # Ensure we don't exceed 13 special characters
    if len(special_chars) > 13:
        special_chars = special_chars[:13]
    
    # Remove duplicate characters from the key
    key_chars = []
    for char in key:
        if char not in key_chars:
            key_chars.append(char)
    
    # Create the matrix fill order with priority:
    # 1. Key characters first
    # 2. Remaining alphabets
    # 3. All 10 digits (ensuring all digits are included)
    # 4. Special characters (up to 13)
    fill_order = key_chars.copy()
    
    # Add remaining letters
    for c in alphabet:
        if c not in fill_order:
            fill_order.append(c)
    
    # Add all digits (ensure digits 0-9 are included)
    for c in digits:
        if c not in fill_order:
            fill_order.append(c)
    
    # Add special characters (up to 13 total)
    special_count = 0
    for c in special_chars:
        if c not in fill_order and special_count < 13:
            fill_order.append(c)
            special_count += 1
    
    # Create the matrix
    matrix = []
    for i in range(matrix_size):
        row = []
        for j in range(matrix_size):
            index = i * matrix_size + j
            if index < len(fill_order):
                row.append(fill_order[index])
            else:
                # If we run out of characters, fill with "."
                row.append(".")
        matrix.append(row)
    
    return matrix

def KBT(key, matrix_size, special_chars=DEFAULT_SPECIAL_CHARS):
    """
    Implement the Key-Based Traditional matrix construction method
    
    Args:
        key: The secret key
        matrix_size: Size of the matrix (e.g., 7 for a 7x7 matrix)
        special_chars: Special characters to include in the matrix
    
    Returns:
        A square matrix filled according to the Key-Based Traditional method
    """
    # Process the key
    key = sanitize_key(key)
    
    # Create the standard character set (26 letters + 10 digits + special chars)
    alphabet = string.ascii_uppercase
    digits = "0123456789"
    
    # Ensure we don't exceed 13 special characters
    if len(special_chars) > 13:
        special_chars = special_chars[:13]
    
    # Remove duplicate characters from the key
    key_chars = []
    for char in key:
        if char not in key_chars:
            key_chars.append(char)
    
    # Create the fill order with priority:
    # 1. Key characters first
    # 2. Remaining alphabets
    # 3. All 10 digits (ensuring all digits are included)
    # 4. Special characters (up to 13)
    fill_order = key_chars.copy()
    
    # Add remaining alphabets
    for c in alphabet:
        if c not in fill_order:
            fill_order.append(c)
    
    # Add all digits (ensure digits 0-9 are included)
    for c in digits:
        if c not in fill_order:
            fill_order.append(c)
    
    # Add special characters (up to 13 total)
    special_count = 0
    for c in special_chars:
        if c not in fill_order and special_count < 13:
            fill_order.append(c)
            special_count += 1
    
    # Create the matrix
    matrix = []
    for i in range(matrix_size):
        row = []
        for j in range(matrix_size):
            index = i * matrix_size + j
            if index < len(fill_order):
                row.append(fill_order[index])
            else:
                # If we run out of characters, fill with "."
                row.append(".")
        matrix.append(row)
    
    return matrix

def SC(key, matrix_size, special_chars=DEFAULT_SPECIAL_CHARS):
    """
    Implement the Spiral Completion matrix construction method
    
    Args:
        key: The secret key
        matrix_size: Size of the matrix (e.g., 7 for a 7x7 matrix)
        special_chars: Special characters to include in the matrix
    
    Returns:
        A square matrix filled in a spiral pattern
    """
    # Process the key
    key = sanitize_key(key)
    
    # Create the standard character set (26 letters + 10 digits + special chars)
    alphabet = string.ascii_uppercase
    digits = "0123456789"
    
    # Remove duplicate characters from the key
    key_chars = []
    for char in key:
        if char not in key_chars:
            key_chars.append(char)
    
    # Ensure we don't exceed 13 special characters (the fixed set)
    if len(special_chars) > 13:
        special_chars = special_chars[:13]
    
    # Create the fill order with priority:
    # 1. Key characters first
    # 2. Remaining alphabets
    # 3. All 10 digits (ensuring all digits are included)
    # 4. Special characters (up to 13)
    fill_order = key_chars.copy()
    
    # Add remaining alphabets
    for c in alphabet:
        if c not in fill_order:
            fill_order.append(c)
    
    # Add all digits (ensure digits 0-9 are included)
    for c in digits:
        if c not in fill_order:
            fill_order.append(c)
    
    # Add special characters (up to 13 total)
    special_count = 0
    for c in special_chars:
        if c not in fill_order and special_count < 13:
            fill_order.append(c)
            special_count += 1
    
    # Create the matrix with "." (empty cells)
    matrix = [["." for _ in range(matrix_size)] for _ in range(matrix_size)]
    
    # Fill the matrix in a spiral pattern
    index = 0
    row_start, row_end = 0, matrix_size - 1
    col_start, col_end = 0, matrix_size - 1
    
    while row_start <= row_end and col_start <= col_end and index < len(fill_order):
        # Fill the top row from left to right
        for col in range(col_start, col_end + 1):
            if index < len(fill_order):
                matrix[row_start][col] = fill_order[index]
                index += 1
        row_start += 1
        
        # Fill the rightmost column from top to bottom
        for row in range(row_start, row_end + 1):
            if index < len(fill_order):
                matrix[row][col_end] = fill_order[index]
                index += 1
        col_end -= 1
        
        # Fill the bottom row from right to left
        if row_start <= row_end:
            for col in range(col_end, col_start - 1, -1):
                if index < len(fill_order):
                    matrix[row_end][col] = fill_order[index]
                    index += 1
            row_end -= 1
        
        # Fill the leftmost column from bottom to top
        if col_start <= col_end:
            for row in range(row_end, row_start - 1, -1):
                if index < len(fill_order):
                    matrix[row][col_start] = fill_order[index]
                    index += 1
            col_start += 1
    
    return matrix

def print_matrix(matrix):
    """Print the matrix in a readable format"""
    print("Matrix:")
    for row in matrix:
        print("".join(f"{cell:3}" for cell in row))

def validate_secret_key(key):
    """Validate the secret key (must be at least 6 characters)"""
    if len(key) < 6:
        return False, "Error: Secret key must be at least 6 characters long."
    return True, "Valid key."

if __name__ == "__main__":
    main()

# print("Plain Traditional (PT):")
# print_matrix(PT("P@55WORD!",7))
# print("\nKey-Based Traditional (KBT):")
# print_matrix(KBT("P@55WORD!",7))
# print("\nSpiral Completion (SC):")
# print_matrix(SC("P@55WORD!",7))