import methods
import playfair_encrypt
import playfair_decrypt
import time

def run_test(message, secret_key, method):
    """
    Run a full encryption and decryption test with the given parameters.
    
    Args:
        message: The plaintext message to encrypt
        secret_key: The secret key for the Playfair cipher
        method: The matrix construction method (1, 2, or 3)
    
    Returns:
        True if the test passed (decrypted message matches original), False otherwise
    """
    print(f"\n=== Testing with message: '{message}' ===")
    print(f"Secret key: '{secret_key}', Method: {method}")
    
    # Generate the matrix based on method
    if method == 1:
        matrix = methods.PT(secret_key, 7)
    elif method == 2:
        matrix = methods.KBT(secret_key, 7)
    elif method == 3:
        matrix = methods.SC(secret_key, 7)
    else:
        print("Invalid method, using Plain Traditional")
        matrix = methods.PT(secret_key, 7)
    
    # Encrypt the message
    start_time = time.time()
    encrypted, case_encoded = playfair_encrypt.encrypt_playfair(message, matrix)
    encrypt_time = time.time() - start_time
    
    print(f"Encrypted: '{encrypted}'")
    print(f"Case info: '{case_encoded}'")
    print(f"Encryption time: {encrypt_time:.4f} seconds")
    
    # Decrypt the message
    start_time = time.time()
    decrypted = playfair_decrypt.decrypt_playfair(encrypted, case_encoded, matrix)
    decrypt_time = time.time() - start_time
    
    print(f"Decrypted: '{decrypted}'")
    print(f"Decryption time: {decrypt_time:.4f} seconds")
    
    # Check if decryption was successful
    if decrypted == message:
        print("✓ TEST PASSED: Decrypted message matches original")
        return True
    else:
        print("✗ TEST FAILED: Decrypted message does not match original")
        
        # Display character-by-character comparison
        print("\nCharacter comparison:")
        for i in range(max(len(message), len(decrypted))):
            if i < len(message) and i < len(decrypted):
                match = "✓" if message[i] == decrypted[i] else "✗"
                print(f"Position {i}: '{message[i]}' vs '{decrypted[i]}' {match}")
            elif i < len(message):
                print(f"Position {i}: '{message[i]}' vs '' ✗ (missing character)")
            else:
                print(f"Position {i}: '' vs '{decrypted[i]}' ✗ (extra character)")
        
        # Show length difference
        print(f"Length difference: Original {len(message)}, Decrypted {len(decrypted)}")
        return False

def main():
    """Run a series of tests on the Playfair cipher implementation"""
    print("=== Playfair Cipher Test Suite ===\n")
    
    # Define test cases
    test_cases = [
        {
            "message": "Hello World",
            "secret_key": "SECURITY101",
            "method": 1
        },
        {
            "message": "Meet me at midnight",
            "secret_key": "CIPHER2023!",
            "method": 2
        },
        {
            "message": "Testing testing",
            "secret_key": "PLAYFAIR123",
            "method": 3
        }
    ]
    
    # Run the tests
    passed_tests = 0
    for test in test_cases:
        if run_test(test["message"], test["secret_key"], test["method"]):
            passed_tests += 1
    
    # Print summary
    print(f"\n=== Test Summary: {passed_tests}/{len(test_cases)} tests passed ===")

if __name__ == "__main__":
    main() 