import sys
import os

# Add the parent directory to the Python path so we can import modules from there
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import methods
import playfair_encrypt
import playfair_decrypt

def test_specific_password(password, key):
    """Test a specific password with a specific key using Plain Traditional method"""
    print(f"Testing password: '{password}'")
    print(f"Key: '{key}', Method: Plain Traditional")
    
    # Generate matrix using Plain Traditional method
    matrix = methods.PT(key, 7)
    
    # Print matrix
    print("\nMatrix:")
    for row in matrix:
        print(" ".join(row))
    
    # Check if problematic characters are in the matrix
    special_chars = "-!"
    for char in special_chars:
        char_present = False
        for row in matrix:
            if char in row:
                char_present = True
                break
        print(f"Character '{char}' is {'present' if char_present else 'MISSING'} in the matrix")
    
    try:
        # Encrypt
        encrypted, case_info = playfair_encrypt.encrypt_playfair(password, matrix, key)
        print(f"\nEncrypted: '{encrypted}'")
        print(f"Case info: '{case_info}'")
        
        # Decrypt
        decrypted = playfair_decrypt.decrypt_playfair(encrypted, case_info, matrix, key)
        print(f"Decrypted: '{decrypted}'")
        
        # Check if matches
        if password == decrypted:
            print("[PASS] Password matches\n")
            return True
        else:
            print("[FAIL] Password doesn't match")
            # Show character comparison
            for i, (orig, dec) in enumerate(zip(password, decrypted)):
                match = "[MATCH]" if orig == dec else "[DIFF]"
                print(f"Position {i}: '{orig}' vs '{dec}' {match}")
            
            # Check for length mismatch
            if len(password) != len(decrypted):
                print(f"Length mismatch: original={len(password)}, decrypted={len(decrypted)}")
            
            return False
    
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

if __name__ == "__main__":
    # Test the previously failing password
    problem_password = "WiFi-Security!"
    problem_key = "P@55W0RD!"
    
    print("=== TESTING PREVIOUSLY FAILING PASSWORD ===\n")
    
    success = test_specific_password(problem_password, problem_key)
    
    # Summary
    print("\n=== TEST SUMMARY ===")
    status = "PASSED" if success else "FAILED"
    print(f"Overall result: {status}") 