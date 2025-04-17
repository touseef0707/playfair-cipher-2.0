import sys
import os

# Add the parent directory to the Python path so we can import modules from there
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import methods
import playfair_encrypt
import playfair_decrypt

def test_password(password, key, matrix_size, allowed_chars):
    """Test password encryption and decryption"""
    print(f"\nTesting password: '{password}'")
    print(f"Key: '{key}', Matrix Size: {matrix_size}")
    
    # Generate matrix using Plain Traditional method
    matrix = methods.PT(key, matrix_size)
    
    # Check if all characters are allowed
    invalid_chars = []
    for char in password:
        if char not in allowed_chars:
            invalid_chars.append(char)
            
    if invalid_chars:
        print(f"[FAIL] INVALID CHARACTERS in password: {', '.join(invalid_chars)}")
        return False
    
    try:
        # Encrypt
        encrypted, case_info = playfair_encrypt.encrypt_playfair(password, matrix, key)
        print(f"Encrypted: '{encrypted}'")
        print(f"Case info: '{case_info}'")
        
        # Decrypt
        decrypted = playfair_decrypt.decrypt_playfair(encrypted, case_info, matrix, key)
        print(f"Decrypted: '{decrypted}'")
        
        # Check if matches
        if password == decrypted:
            print("[PASS] Password matches")
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
    print("=== TESTING VARIOUS PASSWORDS ===")
    
    # Default special characters
    allowed_chars = methods.ALLOWED_CHARS
    
    # Test passwords
    passwords = [
        # Simple passwords
        {"password": "Password123", "key": "SECRET", "matrix_size": 7},
        {"password": "abcDEF123", "key": "KEY", "matrix_size": 7},
        {"password": "Tennis", "key": "SPORTS", "matrix_size": 7},
        {"password": "Secret", "key": "CODE", "matrix_size": 7},
        # Passwords with special characters
        {"password": "P@55w0rd", "key": "SECURE", "matrix_size": 7},
        {"password": "Cyber$3curity", "key": "HACK", "matrix_size": 7},
        {"password": "WiFi-Security!", "key": "P@55W0RD!", "matrix_size": 7},
        {"password": "Str0ng#P@ss!", "key": "COMPLEX", "matrix_size": 7}
    ]
    
    results = []
    for p in passwords:
        success = test_password(p["password"], p["key"], p["matrix_size"], allowed_chars)
        results.append((p["password"], success))
    
    # Summary
    print("\n=== TEST SUMMARY ===")
    all_passed = all(success for _, success in results)
    print(f"Overall result: {'ALL PASSED' if all_passed else 'SOME FAILED'}")
    
    for password, success in results:
        status = "PASSED" if success else "FAILED"
        print(f"Password '{password}': {status}") 