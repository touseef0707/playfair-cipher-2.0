import sys
import os

# Add the parent directory to the Python path so we can import modules from there
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import methods
import playfair_encrypt
import playfair_decrypt

def check_matrix_validity(matrix, password):
    """
    Check if all characters in the password are present in the matrix.
    
    Args:
        matrix: The encryption/decryption matrix
        password: The password to check
        
    Returns:
        Tuple (is_valid, missing_chars) where is_valid is a boolean and
        missing_chars is a list of characters not found in the matrix
    """
    # Convert password to uppercase for checking
    password_upper = password.upper()
    missing_chars = []
    
    # Check each character
    for char in password_upper:
        found = False
        for row in matrix:
            if char in row:
                found = True
                break
        
        if not found:
            missing_chars.append(char)
    
    return len(missing_chars) == 0, missing_chars

def validate_matrix_generation(key, matrix_size=7, method_num=1):
    """
    Validate that a matrix has all expected characters for the specific method.
    
    Args:
        key: The encryption key
        matrix_size: Size of the matrix (default 7)
        method_num: Matrix construction method (1=PT, 2=KBT, 3=SC)
        
    Returns:
        Tuple (matrix, is_valid, missing_expected)
    """
    # Generate the matrix
    if method_num == 1:
        matrix = methods.PT(key, matrix_size)
        method_name = "Plain Traditional"
    elif method_num == 2:
        matrix = methods.KBT(key, matrix_size)
        method_name = "Key-Based Traditional"
    else:
        matrix = methods.SC(key, matrix_size)
        method_name = "Spiral Completion"
    
    # Expected characters
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    special_chars = methods.DEFAULT_SPECIAL_CHARS
    
    # All expected characters
    expected_chars = alphabet + digits + special_chars
    
    # Check if all expected characters are in the matrix
    missing_expected = []
    for char in expected_chars:
        found = False
        for row in matrix:
            if char in row:
                found = True
                break
        
        if not found:
            missing_expected.append(char)
    
    is_valid = len(missing_expected) == 0
    
    # Print matrix if not valid
    if not is_valid:
        print(f"\nMatrix for key '{key}', method {method_name}:")
        for row in matrix:
            print(" ".join(row))
        print(f"Missing expected characters: {', '.join(missing_expected)}")
    
    return matrix, is_valid, missing_expected

def test_with_verification(password, key, method_num=1):
    """
    Test password encryption/decryption with matrix verification.
    
    Args:
        password: The password to test
        key: The encryption key
        method_num: Matrix construction method (1=PT, 2=KBT, 3=SC)
        
    Returns:
        Tuple (success, error_message)
    """
    method_names = {
        1: "Plain Traditional",
        2: "Key-Based Traditional",
        3: "Spiral Completion"
    }
    
    print(f"Testing password: '{password}'")
    print(f"Key: '{key}', Method: {method_num} - {method_names[method_num]}")
    
    # Generate matrix and validate
    matrix, is_valid_matrix, missing_expected = validate_matrix_generation(key, 7, method_num)
    
    if not is_valid_matrix:
        return False, f"Matrix is missing expected characters: {', '.join(missing_expected)}"
    
    # Check if all password characters are in the matrix
    has_all_chars, missing_chars = check_matrix_validity(matrix, password)
    
    if not has_all_chars:
        error = f"Password contains characters not in matrix: {', '.join(missing_chars)}"
        print(f"✗ FAILURE: {error}")
        return False, error
    
    # If all checks pass, attempt encryption/decryption
    try:
        # Encrypt
        encrypted, case_info = playfair_encrypt.encrypt_playfair(password, matrix)
        print(f"Encrypted: '{encrypted}'")
        print(f"Case info: '{case_info}'")
        
        # Decrypt
        decrypted = playfair_decrypt.decrypt_playfair(encrypted, case_info, matrix)
        print(f"Decrypted: '{decrypted}'")
        
        # Check if matches
        if password == decrypted:
            print("✓ SUCCESS: Password matches\n")
            return True, None
        else:
            print("✗ FAILURE: Password doesn't match")
            # Show character comparison
            for i, (orig, dec) in enumerate(zip(password, decrypted)):
                match = "✓" if orig == dec else "✗"
                print(f"Position {i}: '{orig}' vs '{dec}' {match}")
            
            # Check for length mismatch
            if len(password) != len(decrypted):
                print(f"Length mismatch: original={len(password)}, decrypted={len(decrypted)}")
            
            return False, f"Decryption result '{decrypted}' does not match original password"
            
    except Exception as e:
        error = f"Exception during encryption/decryption: {str(e)}"
        print(f"✗ FAILURE: {error}")
        return False, error

def run_verification_tests():
    """
    Run tests focusing on matrix verification for failing cases
    """
    print("=== MATRIX VERIFICATION TESTS ===\n")
    
    # Test the specific failing case
    failing_password = "User$%^789"
    failing_key = "P@55W0RD!"
    failing_method = 3  # Spiral Completion
    
    print("\n=== Testing the identified failing case ===")
    test_with_verification(failing_password, failing_key, failing_method)
    
    # Test all matrix construction methods with the same password
    print("\n=== Testing all methods with the same password ===")
    for method in [1, 2, 3]:
        test_with_verification(failing_password, failing_key, method)
    
    # Check all matrix methods for completeness
    print("\n=== Verifying matrix completeness for all methods ===")
    for method in [1, 2, 3]:
        matrix, is_valid, missing = validate_matrix_generation(failing_key, 7, method)
        method_name = {1: "Plain Traditional", 2: "Key-Based Traditional", 3: "Spiral Completion"}[method]
        if is_valid:
            print(f"✓ Method {method_name} generates a complete matrix")
        else:
            print(f"✗ Method {method_name} matrix is missing: {', '.join(missing)}")
    
    # Test with a new key that ensures full character coverage
    print("\n=== Testing with a more comprehensive key ===")
    better_key = "CIPHER123"
    for method in [1, 2, 3]:
        test_with_verification(failing_password, better_key, method)
    
    # Generate a report of characters used in matrix vs missing for each method
    print("\n=== Character Coverage Report ===")
    for method in [1, 2, 3]:
        method_name = {1: "Plain Traditional", 2: "Key-Based Traditional", 3: "Spiral Completion"}[method]
        matrix, _, missing = validate_matrix_generation(failing_key, 7, method)
        
        # Count character categories in matrix
        letters = sum(1 for row in matrix for cell in row if cell.isalpha())
        digits = sum(1 for row in matrix for cell in row if cell.isdigit())
        specials = sum(1 for row in matrix for cell in row 
                      if not cell.isalnum() and cell != '.')
        
        total_cells = 7 * 7
        filled_cells = letters + digits + specials
        empty_cells = total_cells - filled_cells
        
        print(f"\nMethod {method_name} with key '{failing_key}':")
        print(f"- Letters: {letters}")
        print(f"- Digits: {digits}")
        print(f"- Special chars: {specials}")
        print(f"- Filled cells: {filled_cells}/{total_cells}")
        print(f"- Empty cells: {empty_cells}")
        
        if missing:
            print(f"- Missing: {', '.join(missing)}")

if __name__ == "__main__":
    run_verification_tests() 