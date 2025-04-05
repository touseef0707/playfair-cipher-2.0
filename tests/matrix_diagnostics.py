import sys
import os

# Add the parent directory to the Python path so we can import modules from there
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import methods

def print_full_matrix(matrix):
    """Print the full matrix with row and column indices for better analysis"""
    print("Matrix with coordinates:")
    print("    " + " ".join(f"{j:2d}" for j in range(len(matrix[0]))))
    print("   " + "-" * (len(matrix[0]) * 3 + 2))
    
    for i, row in enumerate(matrix):
        print(f"{i:2d} |", end=" ")
        for cell in row:
            print(f"{cell:2}", end=" ")
        print()
    print()

def check_characters_in_matrix(matrix, text):
    """Check if all characters in the text are present in the matrix"""
    print(f"Checking if all characters from '{text}' are in matrix:")
    
    # Convert to uppercase for matrix lookup
    text_upper = text.upper()
    
    # Check each character
    missing_chars = []
    char_positions = {}
    
    for char in text_upper:
        position = None
        found = False
        
        # Search for character in matrix
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == char:
                    found = True
                    position = (i, j)
                    break
            if found:
                break
        
        if found:
            char_positions[char] = position
        else:
            missing_chars.append(char)
    
    # Print results
    if not missing_chars:
        print("✓ All characters are present in the matrix.")
    else:
        print(f"✗ Missing characters: {', '.join(missing_chars)}")
    
    # Print positions of found characters
    print("\nCharacter positions in matrix:")
    for char in sorted(char_positions.keys()):
        i, j = char_positions[char]
        print(f"'{char}' at position ({i}, {j})")
    
    return len(missing_chars) == 0, char_positions

def check_digraph_transformation(matrix, digraph):
    """Check how a digraph transforms during encryption"""
    print(f"\nAnalyzing digraph transformation for '{digraph}':")
    
    # Find positions
    pos1 = None
    pos2 = None
    
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == digraph[0]:
                pos1 = (i, j)
            if matrix[i][j] == digraph[1]:
                pos2 = (i, j)
    
    if pos1 is None or pos2 is None:
        print(f"✗ Cannot analyze - one or both characters not found in matrix.")
        return None
    
    row1, col1 = pos1
    row2, col2 = pos2
    matrix_size = len(matrix)
    
    # Determine encryption rule
    encrypted_digraph = None
    rule = None
    
    if row1 == row2:  # Same row
        # Encrypt with right shift
        encrypted_digraph = (
            matrix[row1][(col1 + 1) % matrix_size] + 
            matrix[row2][(col2 + 1) % matrix_size]
        )
        rule = "Same row - characters replaced with ones to the right"
    elif col1 == col2:  # Same column
        # Encrypt with down shift
        encrypted_digraph = (
            matrix[(row1 + 1) % matrix_size][col1] + 
            matrix[(row2 + 1) % matrix_size][col2]
        )
        rule = "Same column - characters replaced with ones below"
    else:  # Rectangle
        # Swap columns
        encrypted_digraph = (
            matrix[row1][col2] + 
            matrix[row2][col1]
        )
        rule = "Rectangle - characters replaced with ones at opposite corners"
    
    print(f"Character 1: '{digraph[0]}' at position ({row1}, {col1})")
    print(f"Character 2: '{digraph[1]}' at position ({row2}, {col2})")
    print(f"Encryption rule: {rule}")
    print(f"Encrypted digraph: '{encrypted_digraph}'")
    
    # For decryption analysis - reverse the rules
    if row1 == row2:  # Same row
        decrypted_digraph = (
            matrix[row1][(col1 - 1) % matrix_size] + 
            matrix[row2][(col2 - 1) % matrix_size]
        )
        decrypt_rule = "Same row - characters replaced with ones to the left"
    elif col1 == col2:  # Same column
        decrypted_digraph = (
            matrix[(row1 - 1) % matrix_size][col1] + 
            matrix[(row2 - 1) % matrix_size][col2]
        )
        decrypt_rule = "Same column - characters replaced with ones above"
    else:  # Rectangle
        decrypted_digraph = (
            matrix[row1][col2] + 
            matrix[row2][col1]
        )
        decrypt_rule = "Rectangle - characters replaced with ones at opposite corners"
        
    print(f"Decryption rule: {decrypt_rule}")
    print(f"If we receive '{encrypted_digraph}', it would decrypt to: '{decrypted_digraph}'")
    
    return encrypted_digraph

def analyze_matrix_content(matrix):
    """Analyze the content distribution in the matrix"""
    # Count character types
    letters = 0
    digits = 0
    special_chars = 0
    empty_cells = 0
    
    # Track specific characters
    all_chars = set()
    all_special_chars = set()
    all_digits = set()
    all_letters = set()
    
    # Standard character sets
    alphabet = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    digit_set = set("0123456789")
    
    for row in matrix:
        for cell in row:
            all_chars.add(cell)
            if cell.isalpha():
                letters += 1
                all_letters.add(cell)
            elif cell.isdigit():
                digits += 1
                all_digits.add(cell)
            elif cell == '.':
                empty_cells += 1
            else:
                special_chars += 1
                all_special_chars.add(cell)
    
    # Check against our fixed special chars
    fixed_special_chars = set(methods.DEFAULT_SPECIAL_CHARS)
    extra_special_chars = all_special_chars - fixed_special_chars
    missing_special_chars = fixed_special_chars - all_special_chars
    
    print("\nMatrix Content Analysis:")
    print(f"- Letters: {letters} ({len(all_letters)} unique)")
    print(f"- Digits: {digits} ({len(all_digits)} unique)")
    print(f"- Special chars: {special_chars} ({len(all_special_chars)} unique)")
    print(f"- Empty cells: {empty_cells}")
    print(f"- Total unique characters: {len(all_chars)}")
    
    # Report on special characters
    if extra_special_chars:
        print(f"- Extra special chars (not in our fixed set): {', '.join(sorted(extra_special_chars))}")
    if missing_special_chars:
        print(f"- Missing special chars (from our fixed set): {', '.join(sorted(missing_special_chars))}")
    
    # Report on digits
    missing_digits = digit_set - all_digits
    if missing_digits:
        print(f"- Missing digits: {', '.join(sorted(missing_digits))}")
    
    # Check total capacity
    total_capacity = len(matrix) * len(matrix[0])
    filled_capacity = letters + digits + special_chars
    available_capacity = total_capacity - filled_capacity
    
    print(f"- Matrix capacity: {filled_capacity}/{total_capacity} cells used ({available_capacity} available)")
    
    # Check if we exceeded special chars
    if len(all_special_chars) > 13:
        print(f"WARNING: Matrix has {len(all_special_chars)} special characters, which exceeds the limit of 13!")
        print("This is likely causing important digits or letters to be omitted.")
    
    return {
        "letters": letters,
        "digits": digits,
        "special_chars": special_chars,
        "empty_cells": empty_cells,
        "unique_chars": len(all_chars),
        "all_special_chars": all_special_chars,
        "all_digits": all_digits,
        "missing_special_chars": missing_special_chars,
        "extra_special_chars": extra_special_chars,
        "missing_digits": missing_digits
    }

def diagnose_specific_case():
    """Diagnose the specific failing case from the tests"""
    password = "User$%^789"
    key = "P@55W0RD!"
    method = 3  # Spiral Completion
    
    print(f"Diagnosing case: password='{password}', key='{key}', method={method} (SC)")
    
    # Generate the matrix
    if method == 1:
        matrix = methods.PT(key, 7)
        method_name = "Plain Traditional"
    elif method == 2:
        matrix = methods.KBT(key, 7)
        method_name = "Key-Based Traditional"
    else:
        matrix = methods.SC(key, 7)
        method_name = "Spiral Completion"
    
    print(f"\nMatrix construction method: {method_name}")
    print_full_matrix(matrix)
    
    # Analyze matrix content
    analyze_matrix_content(matrix)
    
    # Check if all characters are in the matrix
    all_present, positions = check_characters_in_matrix(matrix, password)
    
    # Check key characters
    print("\nChecking if all key characters are in the matrix:")
    check_characters_in_matrix(matrix, key)
    
    # Analyze problematic digraphs
    digraphs = []
    for i in range(0, len(password), 2):
        if i + 1 < len(password):
            digraphs.append(password[i:i+2].upper())
        else:
            digraphs.append(password[i] + "X")  # Add filler for odd length
    
    print("\nAnalyzing digraphs:")
    for digraph in digraphs:
        print(f"- '{digraph}'")
    
    # Specifically check the problematic part (78 and 89)
    check_digraph_transformation(matrix, "78")
    check_digraph_transformation(matrix, "89")
    
    # Compare across methods
    print("\n=== Comparing Matrix Construction Methods ===")
    for m in [1, 2, 3]:
        if m == 1:
            mat = methods.PT(key, 7)
            m_name = "Plain Traditional"
        elif m == 2:
            mat = methods.KBT(key, 7)
            m_name = "Key-Based Traditional"
        else:
            mat = methods.SC(key, 7)
            m_name = "Spiral Completion"
        
        print(f"\nMethod {m} - {m_name}:")
        analyze_matrix_content(mat)

if __name__ == "__main__":
    diagnose_specific_case() 