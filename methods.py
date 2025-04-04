import string

special_chars = "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~1234567890"

def main():
    """Get matrix generation parameters from user"""
    secret_key = input("Enter your secret key: ")
    matrix_size = 7  # Fixed for this assignment
    
    print("\nSelect matrix construction method:")
    print("1 - Plain Traditional")
    print("2 - Key-Based Traditional")
    print("3 - Spiral Completion")
    
    method = input("Method (1/2/3): ")
    
    # Generate and display the matrix
    if method == "1":
        matrix = PT(secret_key, matrix_size)
    elif method == "2":
        matrix = KBT(secret_key, matrix_size)
    elif method == "3":
        matrix = SC(secret_key, matrix_size)
    else:
        print("Invalid method. Using Plain Traditional as default.")
        matrix = PT(secret_key, matrix_size)
    
    print_matrix(matrix)
    return matrix

def sanitize_key(key):
    """Sanitize the key by converting to uppercase and removing spaces"""
    return ''.join(c.upper() for c in key if c.isalnum() or c in special_chars)

def PT(key, matrix_size):
    """
    Implement the Plain Traditional matrix construction method
    
    Args:
        key: The secret key
        matrix_size: Size of the matrix (e.g., 7 for a 7x7 matrix)
    
    Returns:
        A square matrix filled according to the Plain Traditional method
    """
    # Process the key
    key = sanitize_key(key)
    
    # Create the alphabet (including special characters)
    alphabet = string.ascii_uppercase + special_chars
    
    # Remove duplicate characters from the key
    key_chars = []
    for char in key:
        if char not in key_chars:
            key_chars.append(char)
    
    # Create the matrix fill order (key followed by remaining alphabet)
    fill_order = key_chars + [c for c in alphabet if c not in key_chars]
    
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

def KBT(key, matrix_size):
    """
    Implement the Key-Based Traditional matrix construction method
    
    Args:
        key: The secret key
        matrix_size: Size of the matrix (e.g., 7 for a 7x7 matrix)
    
    Returns:
        A square matrix filled according to the Key-Based Traditional method
    """
    # Process the key
    key = sanitize_key(key)
    
    # Create the alphabet (including special characters)
    alphabet = string.ascii_uppercase + special_chars
    
    # Calculate the length of the key, limiting to 10
    key_length = min(len(key), 10)
    key_numeric = sum(ord(key[i]) for i in range(key_length))
    
    # Determine the starting position based on key
    start_row = (key_numeric // matrix_size) % matrix_size
    start_col = key_numeric % matrix_size
    
    # Create the matrix with "." (empty cells)
    matrix = [["." for _ in range(matrix_size)] for _ in range(matrix_size)]
    
    # Remove duplicate characters from the key
    key_chars = []
    for char in key:
        if char not in key_chars:
            key_chars.append(char)
    
    # Create the fill order (key followed by remaining alphabet)
    fill_order = key_chars + [c for c in alphabet if c not in key_chars]
    
    # Fill the matrix starting from the key-determined position
    # and wrapping around as needed
    index = 0
    row, col = start_row, start_col
    
    # Fill the matrix
    while index < len(fill_order) and index < matrix_size * matrix_size:
        # Place the current character if the cell is empty
        if matrix[row][col] == ".":
            matrix[row][col] = fill_order[index]
            index += 1
        
        # Move to the next position (right to left, top to bottom)
        col = (col - 1) % matrix_size
        if col == matrix_size - 1:  # If we wrapped around, move to next row
            row = (row + 1) % matrix_size
    
    return matrix

def SC(key, matrix_size):
    """
    Implement the Spiral Completion matrix construction method
    
    Args:
        key: The secret key
        matrix_size: Size of the matrix (e.g., 7 for a 7x7 matrix)
    
    Returns:
        A square matrix filled in a spiral pattern
    """
    # Process the key
    key = sanitize_key(key)
    
    # Create the alphabet (including special characters)
    alphabet = string.ascii_uppercase + special_chars
    
    # Remove duplicate characters from the key
    key_chars = []
    for char in key:
        if char not in key_chars:
            key_chars.append(char)
    
    # Create the fill order (key followed by remaining alphabet)
    fill_order = key_chars + [c for c in alphabet if c not in key_chars]
    
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

