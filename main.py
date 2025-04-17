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
    
    # Ask if user wants to use a file for input
    use_file = input("Use a file for input? (y/n): ").lower() == 'y'
    
    if use_file:
        input_file = input("Enter input filename (default: input.txt): ") or "input.txt"
        try:
            with open(input_file, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 1:
                    secret_key = lines[0].strip()
                    message = lines[1].strip() if len(lines) > 1 else input("\nEnter the password to encrypt: ")
                else:
                    print("File does not contain enough information. Using manual input.")
                    secret_key = input("Enter your secret key: ")
                    message = input("\nEnter the password to encrypt: ")
        except FileNotFoundError:
            print(f"File {input_file} not found. Using manual input.")
            secret_key = input("Enter your secret key: ")
            message = input("\nEnter the password to encrypt: ")
    else:
        # Get encryption parameters manually
        secret_key = input("Enter your secret key: ")
        message = input("\nEnter the password to encrypt: ")
    
    matrix_size = 7  # Fixed for this assignment
    
    # Using fixed special characters
    special_chars = methods.DEFAULT_SPECIAL_CHARS
    print(f"Using fixed special characters: {special_chars}")
    
    # Generate the matrix (Plain Traditional)
    matrix = methods.PT(secret_key, matrix_size, special_chars)
    print("\nEncryption Matrix (Plain Traditional):")
    methods.print_matrix(matrix)
    
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
        
        # Always offer to save to file
        filename = "encryption.txt"
        save = input(f"\nSave encryption results to {filename}? (y/n): ").lower()
        if save == 'y':
            with open(filename, 'w') as f:
                f.write(f"{secret_key}\n")
                f.write(f"{encrypted}\n")
                f.write(f"{case_encoded}\n")
            print(f"Encryption details saved to {filename}")
    
    except ValueError as e:
        print(f"\nError: {str(e)}")

def decrypt_mode():
    """Run the decryption mode"""
    clear_screen()
    print("=== Playfair Cipher Decryption for Passwords ===")
    print("Note: This implementation is designed for passwords without spaces.")
    
    # Ask if user wants to use a file for input
    use_file = input("Use a file for input? (y/n): ").lower() == 'y'
    
    if use_file:
        input_file = input("Enter input filename (default: encryption.txt): ") or "encryption.txt"
        try:
            with open(input_file, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 3:
                    secret_key = lines[0].strip()
                    encrypted = lines[1].strip()
                    case_encoded = lines[2].strip()
                else:
                    print("File does not contain enough information. Using manual input.")
                    secret_key = input("Enter your secret key: ")
                    encrypted = input("\nEnter the encrypted message: ")
                    case_encoded = input("Enter the case information: ")
        except FileNotFoundError:
            print(f"File {input_file} not found. Using manual input.")
            secret_key = input("Enter your secret key: ")
            encrypted = input("\nEnter the encrypted message: ")
            case_encoded = input("Enter the case information: ")
    else:
        # Get decryption parameters manually
        secret_key = input("Enter your secret key: ")
        encrypted = input("\nEnter the encrypted message: ")
        case_encoded = input("Enter the case information: ")
    
    matrix_size = 7  # Fixed for this assignment
    
    # Using fixed special characters
    special_chars = methods.DEFAULT_SPECIAL_CHARS
    print(f"Using fixed special characters: {special_chars}")
    
    # Generate the matrix (Plain Traditional)
    matrix = methods.PT(secret_key, matrix_size, special_chars)
    print("\nDecryption Matrix (Plain Traditional):")
    methods.print_matrix(matrix)
    
    try:
        # Decrypt the message
        decrypted = playfair_decrypt.decrypt_playfair(encrypted, case_encoded, matrix, secret_key)
        
        # Display the result
        print("\nDecrypted message:")
        print(decrypted)
        
        # Save decryption details
        filename = "decryption.txt"
        save = input(f"\nSave decrypted message to {filename}? (y/n): ").lower()
        if save == 'y':
            with open(filename, 'w') as f:
                f.write(f"{decrypted}\n")
            print(f"Decrypted message saved to {filename}")
    
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