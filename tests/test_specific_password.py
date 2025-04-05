import sys
import os

# Add the parent directory to the Python path so we can import modules from there
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import methods
import playfair_encrypt
import playfair_decrypt

def test_specific_password(password, key, method_num):
    """Test a specific password with a specific key and method"""
    method_names = {
        1: "Plain Traditional",
        2: "Key-Based Traditional",
        3: "Spiral Completion"
    }
    
    print(f"Testing password: '{password}'")
    print(f"Key: '{key}', Method: {method_num} - {method_names[method_num]}")
    
    # Generate matrix
    if method_num == 1:
        matrix = methods.PT(key, 7)
    elif method_num == 2:
        matrix = methods.KBT(key, 7)
    else:
        matrix = methods.SC(key, 7)
    
    # Print matrix
    print("\nMatrix:")
    for row in matrix:
        print(" ".join(row))
    
    # Check if '9' is in the matrix
    nine_present = False
    for row in matrix:
        if '9' in row:
            nine_present = True
            break
    print(f"Digit '9' is {'present' if nine_present else 'MISSING'} in the matrix")
    
    try:
        # Encrypt
        encrypted, case_info = playfair_encrypt.encrypt_playfair(password, matrix)
        print(f"\nEncrypted: '{encrypted}'")
        print(f"Case info: '{case_info}'")
        
        # Decrypt
        decrypted = playfair_decrypt.decrypt_playfair(encrypted, case_info, matrix)
        print(f"Decrypted: '{decrypted}'")
        
        # Check if matches
        if password == decrypted:
            print("✓ SUCCESS: Password matches\n")
            return True
        else:
            print("✗ FAILURE: Password doesn't match")
            # Show character comparison
            for i, (orig, dec) in enumerate(zip(password, decrypted)):
                match = "✓" if orig == dec else "✗"
                print(f"Position {i}: '{orig}' vs '{dec}' {match}")
            
            # Check for length mismatch
            if len(password) != len(decrypted):
                print(f"Length mismatch: original={len(password)}, decrypted={len(decrypted)}")
            
            return False
    
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    # Test the previously failing password with all methods
    problem_password = "WiFi-Security!"
    problem_key = "P@55W0RD!"
    
    print("=== TESTING PREVIOUSLY FAILING PASSWORD ===\n")
    
    results = []
    for method in [1, 2, 3]:
        success = test_specific_password(problem_password, problem_key, method)
        results.append((method, success))
    
    # Summary
    print("\n=== TEST SUMMARY ===")
    all_passed = all(success for _, success in results)
    print(f"Overall result: {'✓ ALL PASSED' if all_passed else '✗ SOME FAILED'}")
    
    for method, success in results:
        method_name = {1: "Plain Traditional", 2: "Key-Based Traditional", 3: "Spiral Completion"}[method]
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"Method {method} - {method_name}: {status}") 