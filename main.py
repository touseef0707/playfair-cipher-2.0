import os
import methods
import playfair_encrypt
import playfair_decrypt
from prettytable import PrettyTable

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_matrix_pretty(matrix):
    """Display the Playfair matrix using PrettyTable"""
    table = PrettyTable()
    table.field_names = [f"Col {j+1}" for j in range(len(matrix[0]))]
    
    for row in matrix:
        table.add_row(row)
    
    print(table)

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
    # Use PrettyTable instead of regular print
    display_matrix_pretty(matrix)
    
    try:
        # Show the digraphs with PrettyTable
        digraphs, case_map = playfair_encrypt.prepare_message(message)
        
        # Visualize the digraphs
        table = PrettyTable()
        table.field_names = ["Pair #", "Digraph", "Type"]
        for i, digraph in enumerate(digraphs):
            is_filler = False
            if digraph.endswith('X') and (i == len(digraphs) - 1 or (i < len(digraphs) - 1 and digraph[0] == digraphs[i+1][0])):
                is_filler = True
            
            table.add_row([
                i+1, 
                digraph, 
                "Filler added" if is_filler else "Regular"
            ])
        
        print("\nDigraph Formation:")
        print(table)
        
        # Encrypt the message with normal functionality
        encrypted, case_encoded = playfair_encrypt.encrypt_playfair(message, matrix, secret_key)
        
        # Visualize the final results
        table = PrettyTable()
        table.field_names = ["Original Message", "Encrypted Result", "Case Encoding"]
        table.add_row([message, encrypted, case_encoded])
        
        print("\nEncryption Results:")
        print(table)
        
        # Original output
        print("\nEncrypted message:")
        print(encrypted)
        
        print("\nCase information (needed for decryption):")
        print(case_encoded)
        
        # Display the prepared digraphs for clarity
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
    # Use PrettyTable instead of regular print
    display_matrix_pretty(matrix)
    
    try:
        # Visualize the inputs
        table = PrettyTable()
        table.field_names = ["Encrypted Message", "Case Encoding", "Secret Key"]
        table.add_row([encrypted, case_encoded, secret_key])
        
        print("\nDecryption Inputs:")
        print(table)
        
        # Decrypt the message with normal functionality
        decrypted = playfair_decrypt.decrypt_playfair(encrypted, case_encoded, matrix, secret_key)
        
        # Visualize the decryption result
        table = PrettyTable()
        table.field_names = ["Encrypted", "Decrypted"]
        table.add_row([encrypted, decrypted])
        
        print("\nDecryption Result:")
        print(table)
        
        # Original output
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