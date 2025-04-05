import sys
import methods
import playfair_encrypt
import playfair_decrypt

def print_banner():
    """Print a banner with program information"""
    print("\n" + "=" * 80)
    print("PLAYFAIR CIPHER - PASSWORD ENCRYPTION".center(80))
    print("=" * 80)
    print("\nThis program implements an enhanced Playfair cipher for password encryption.")
    print("It uses a 7×7 matrix that includes letters, numbers, and special characters.\n")
    
    print("CHARACTER RESTRICTIONS:".center(80))
    print("-" * 80)
    print("Only the following characters are allowed:")
    print("- Letters (A-Z, a-z)")
    print("- Numbers (0-9)")
    print("- Special characters: !@#$%^&*()_+-{}")
    print("\nNOTE: Spaces are not supported and will be removed during encryption.\n")
    
    print("MATRIX INFORMATION:".center(80))
    print("-" * 80)
    print("The 7×7 matrix will always include:")
    print("- All 26 uppercase letters")
    print("- All 10 digits (0-9)")
    print("- Exactly 13 special characters: !@#$%^&*()_-+")
    print("\nThe matrix prioritizes including all digits and letters.\n")
    print("=" * 80 + "\n")

def encrypt_mode():
    """Run the program in encryption mode"""
    print("\n--- ENCRYPTION MODE ---\n")
    
    # Get the key and validate it
    while True:
        key = input("Enter your secret key: ")
        is_valid, error_msg = methods.validate_input(key, is_key=True)
        if is_valid:
            break
        print(f"Error: {error_msg}")
        print("Please try again.\n")
    
    # Choose matrix construction method
    print("\nSelect matrix construction method:")
    print("1 - Plain Traditional")
    print("2 - Key-Based Traditional")
    print("3 - Spiral Completion")
    
    while True:
        method = input("Method (1/2/3): ")
        if method in ["1", "2", "3"]:
            break
        print("Invalid choice. Please enter 1, 2, or 3.")
    
    method_num = int(method)
    
    # Generate matrix
    if method_num == 1:
        matrix = methods.PT(key, 7)
        method_name = "Plain Traditional"
    elif method_num == 2:
        matrix = methods.KBT(key, 7)
        method_name = "Key-Based Traditional"
    else:
        matrix = methods.SC(key, 7)
        method_name = "Spiral Completion"
    
    # Get the message to encrypt
    while True:
        plaintext = input("\nEnter the message to encrypt: ")
        is_valid, error_msg = methods.validate_input(plaintext, is_key=False)
        if is_valid:
            if error_msg:  # This would be the space warning
                print(error_msg)
            break
        print(f"Error: {error_msg}")
        print("Please try again.\n")
    
    # Display the matrix
    print("\nUsing matrix ({}):".format(method_name))
    methods.print_matrix(matrix)
    
    # Encrypt
    try:
        encrypted, case_info = playfair_encrypt.encrypt_playfair(plaintext, matrix)
        print("\nEncrypted message: {}".format(encrypted))
        print("Case information: {}".format(case_info))
        print("\nSTORE BOTH THE ENCRYPTED MESSAGE AND CASE INFORMATION!")
        print("You will need both to decrypt the message correctly.")
    except Exception as e:
        print(f"\nError during encryption: {str(e)}")

def decrypt_mode():
    """Run the program in decryption mode"""
    print("\n--- DECRYPTION MODE ---\n")
    
    # Get the key and validate it
    while True:
        key = input("Enter your secret key: ")
        is_valid, error_msg = methods.validate_input(key, is_key=True)
        if is_valid:
            break
        print(f"Error: {error_msg}")
        print("Please try again.\n")
    
    # Choose matrix construction method
    print("\nSelect matrix construction method:")
    print("1 - Plain Traditional")
    print("2 - Key-Based Traditional")
    print("3 - Spiral Completion")
    
    while True:
        method = input("Method (1/2/3): ")
        if method in ["1", "2", "3"]:
            break
        print("Invalid choice. Please enter 1, 2, or 3.")
    
    method_num = int(method)
    
    # Generate matrix
    if method_num == 1:
        matrix = methods.PT(key, 7)
        method_name = "Plain Traditional"
    elif method_num == 2:
        matrix = methods.KBT(key, 7)
        method_name = "Key-Based Traditional"
    else:
        matrix = methods.SC(key, 7)
        method_name = "Spiral Completion"
    
    # Get the encrypted message
    while True:
        encrypted = input("\nEnter the encrypted message: ")
        is_valid, error_msg = methods.validate_input(encrypted, is_key=False)
        if is_valid:
            break
        print(f"Error: {error_msg}")
        print("Please try again.\n")
    
    # Get case information
    case_info = input("Enter the case information: ")
    
    # Display the matrix
    print("\nUsing matrix ({}):".format(method_name))
    methods.print_matrix(matrix)
    
    # Decrypt
    try:
        decrypted = playfair_decrypt.decrypt_playfair(encrypted, case_info, matrix)
        print("\nDecrypted message: {}".format(decrypted))
    except Exception as e:
        print(f"\nError during decryption: {str(e)}")

def main():
    """Main function"""
    print_banner()
    
    print("Choose operation mode:")
    print("1 - Encrypt a message")
    print("2 - Decrypt a message")
    print("3 - Exit")
    
    while True:
        choice = input("\nEnter your choice (1/2/3): ")
        
        if choice == "1":
            encrypt_mode()
        elif choice == "2":
            decrypt_mode()
        elif choice == "3":
            print("Exiting program. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
        
        # Ask if the user wants to perform another operation
        again = input("\nWould you like to perform another operation? (y/n): ")
        if again.lower() != "y":
            print("Exiting program. Goodbye!")
            break

if __name__ == "__main__":
    main() 