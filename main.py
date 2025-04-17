import os
import methods
import playfair_encrypt
import playfair_decrypt

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def encrypt_mode():
    """Run the encryption mode"""
    clear_screen()
    print("=== Playfair Cipher Encryption for Passwords ===")
    print("Note: This implementation is designed for passwords without spaces.")
    
    # Get encryption parameters
    secret_key = input("Enter your secret key: ")
    matrix_size = 7  # Fixed for this assignment
    
    # Using fixed special characters
    special_chars = methods.DEFAULT_SPECIAL_CHARS
    print(f"Using fixed special characters: {special_chars}")
    
    # Generate the matrix (Plain Traditional)
    matrix = methods.PT(secret_key, matrix_size, special_chars)
    print("\nEncryption Matrix (Plain Traditional):")
    methods.print_matrix(matrix)
    
    # Get message to encrypt
    message = input("\nEnter the password to encrypt: ")
    
    try:
        # Encrypt the message
        encrypted, case_encoded = playfair_encrypt.encrypt_playfair(message, matrix, secret_key)
        
        # Display the result
        print("\nEncrypted message:")
        print(encrypted)
        
        print("\nCase information (needed for decryption):")
        print(case_encoded)
        
        # Display the prepared digraphs for clarity
        digraphs, _ = playfair_encrypt.prepare_message(message)
        print("\nPassword split into digraphs:")
        print(' '.join(digraphs))
        
        # Option to save to file
        save = input("\nSave encryption details to file? (y/n): ").lower()
        if save == 'y':
            filename = input("Enter filename (default: playfair_encryption.txt): ") or "playfair_encryption.txt"
            with open(filename, 'w') as f:
                f.write(f"Secret Key: {secret_key}\n")
                f.write(f"Construction Method: Plain Traditional\n")
                f.write(f"Original Message: {message}\n")
                f.write(f"Encrypted Message: {encrypted}\n")
                f.write(f"Case Information: {case_encoded}\n")
                f.write(f"Digraphs: {' '.join(digraphs)}\n")
                
                # Get the core encrypted digraphs (before transformation)
                matrix_flat = [char for row in matrix for char in row]
                core_pairs = []
                for dg in digraphs:
                    c1, c2 = dg[0], dg[1]
                    encrypted_pair = playfair_encrypt.encrypt_digraph(c1, c2, matrix, matrix_flat)
                    core_pairs.append(encrypted_pair)
                core_encrypted = ''.join(core_pairs)
                enc_digraphs = [core_encrypted[i:i+2] for i in range(0, len(core_encrypted), 2)]
                f.write(f"Encrypted Digraphs: {' '.join(enc_digraphs)}\n")
                
            print(f"Encryption details saved to {filename}")
    
    except ValueError as e:
        print(f"\nError: {str(e)}")

def decrypt_mode():
    """Run the decryption mode"""
    clear_screen()
    print("=== Playfair Cipher Decryption for Passwords ===")
    print("Note: This implementation is designed for passwords without spaces.")
    
    # Get decryption parameters
    secret_key = input("Enter your secret key: ")
    matrix_size = 7  # Fixed for this assignment
    
    # Using fixed special characters
    special_chars = methods.DEFAULT_SPECIAL_CHARS
    print(f"Using fixed special characters: {special_chars}")
    
    # Generate the matrix (Plain Traditional)
    matrix = methods.PT(secret_key, matrix_size, special_chars)
    print("\nDecryption Matrix (Plain Traditional):")
    methods.print_matrix(matrix)
    
    # Get encrypted message and metadata
    encrypted = input("\nEnter the encrypted message: ")
    case_encoded = input("Enter the case information: ")
    
    try:
        # Decrypt the message
        decrypted = playfair_decrypt.decrypt_playfair(encrypted, case_encoded, matrix, secret_key)
        
        # Display the result
        print("\nDecrypted message:")
        print(decrypted)
        
        # Option to save to file
        save = input("\nSave decryption details to file? (y/n): ").lower()
        if save == 'y':
            filename = input("Enter filename (default: playfair_decryption.txt): ") or "playfair_decryption.txt"
            with open(filename, 'w') as f:
                f.write(f"Secret Key: {secret_key}\n")
                f.write(f"Construction Method: Plain Traditional\n")
                f.write(f"Encrypted Message: {encrypted}\n")
                f.write(f"Case Information: {case_encoded}\n")
                f.write(f"Decrypted Message: {decrypted}\n")
            print(f"Decryption details saved to {filename}")
    
    except ValueError as e:
        print(f"\nError: {str(e)}")

def main():
    """Main function for the Playfair cipher program"""
    while True:
        clear_screen()
        print("=== Playfair Cipher Implementation ===")
        print("1. Encrypt a password")
        print("2. Decrypt a password")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1/2/3): ")
        
        if choice == '1':
            encrypt_mode()
            input("\nPress Enter to continue...")
        elif choice == '2':
            decrypt_mode()
            input("\nPress Enter to continue...")
        elif choice == '3':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 