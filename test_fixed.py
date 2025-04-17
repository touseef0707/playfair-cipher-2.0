import methods
import playfair_encrypt
import playfair_decrypt

def test_playfair():
    """Test the Playfair cipher implementation with various passwords"""
    # Test parameters
    secret_key = "SECRETKEY123"
    matrix_size = 7
    special_chars = methods.DEFAULT_SPECIAL_CHARS
    
    # Create matrix
    matrix = methods.PT(secret_key, matrix_size, special_chars)
    
    # Display the matrix
    print("Encryption/Decryption Matrix (Plain Traditional):")
    methods.print_matrix(matrix)
    
    # Test cases
    test_messages = [
        "Password123",         # Mixed case with numbers
        "Tennis",              # Simple word
        "Secret",              # Another simple word
        "MaxPassword",         # Password that previously had issues
        "Cyber$3curity"        # With special character
    ]
    
    for message in test_messages:
        print("\n" + "="*50)
        print(f"Testing with message: '{message}'")
        
        # Display the digraphs
        digraphs, _ = playfair_encrypt.prepare_message(message)
        print(f"Digraphs: {' '.join(digraphs)}")
        
        # Encrypt
        encrypted, case_encoded = playfair_encrypt.encrypt_playfair(message, matrix, secret_key)
        print(f"Encrypted: {encrypted}")
        print(f"Case info: {case_encoded}")
        
        # Decrypt
        decrypted = playfair_decrypt.decrypt_playfair(encrypted, case_encoded, matrix, secret_key)
        print(f"Decrypted: {decrypted}")
        
        # Check if original and decrypted match
        match = message == decrypted
        print(f"Original and decrypted match: {match}")
        
        if not match:
            print("Mismatch details:")
            print(f"Original length: {len(message)}, Decrypted length: {len(decrypted)}")
            for i in range(min(len(message), len(decrypted))):
                if message[i] != decrypted[i]:
                    print(f"Position {i}: Original '{message[i]}' vs Decrypted '{decrypted[i]}'")
            
            if len(message) != len(decrypted):
                if len(message) < len(decrypted):
                    print(f"Extra characters in decrypted: '{decrypted[len(message):]}'")
                else:
                    print(f"Missing characters in decrypted, original has: '{message[len(decrypted):]}'")

if __name__ == "__main__":
    test_playfair() 