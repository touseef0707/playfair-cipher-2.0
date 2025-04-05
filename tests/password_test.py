import sys
import os

# Add the parent directory to the Python path so we can import modules from there
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import methods
import playfair_encrypt
import playfair_decrypt

def is_valid_password(password):
    """Check if a password contains only allowed characters"""
    allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-{}"
    for char in password:
        if char not in allowed_chars:
            return False, f"Invalid character '{char}' detected"
    return True, ""

def test_password(password, key, method_num=1, verbose=True):
    """Test password encryption and decryption"""
    if verbose:
        print(f"Testing password: '{password}'")
        print(f"Key: '{key}', Method: {method_num}")
    
    # Check if password contains only allowed characters
    is_valid, error_msg = is_valid_password(password)
    if not is_valid:
        if verbose:
            print(f"⚠️ WARNING: {error_msg}")
            print("✗ SKIPPED: Password contains invalid characters\n")
        return False, "invalid_chars"
    
    try:
        # Create matrix
        if method_num == 1:
            matrix = methods.PT(key, 7)
        elif method_num == 2:
            matrix = methods.KBT(key, 7)
        else:
            matrix = methods.SC(key, 7)
        
        # Encrypt
        encrypted, case_info = playfair_encrypt.encrypt_playfair(password, matrix)
        if verbose:
            print(f"Encrypted: '{encrypted}'")
            print(f"Case info: '{case_info}'")
        
        # Decrypt
        decrypted = playfair_decrypt.decrypt_playfair(encrypted, case_info, matrix)
        if verbose:
            print(f"Decrypted: '{decrypted}'")
        
        # Check if matches
        if password == decrypted:
            if verbose:
                print("✓ SUCCESS: Password matches\n")
            return True, "success"
        else:
            if verbose:
                print("✗ FAILURE: Password doesn't match")
                # Show character comparison
                for i, (orig, dec) in enumerate(zip(password, decrypted)):
                    match = "✓" if orig == dec else "✗"
                    print(f"Position {i}: '{orig}' vs '{dec}' {match}")
                
                # Check for length mismatch
                if len(password) != len(decrypted):
                    print(f"Length mismatch: original={len(password)}, decrypted={len(decrypted)}")
                print()
            return False, "mismatch"
    except Exception as e:
        if verbose:
            print(f"✗ ERROR: {str(e)}\n")
        return False, "error"

# Test several passwords
passwords = [
    # Basic passwords with mixed case and numbers
    "Password123",
    "Admin@123",
    "p@$$w0rd",
    "SecretKey!",
    
    # Passwords with underscore character
    "Test_Underscore",
    "user_name123",
    
    # Very short and long passwords
    "Pw1",
    "ThisIsAReallyLongPasswordWithMixedCase123!@#",
    
    # Passwords with repeated characters (to test filler handling)
    "BooksStore",  # Double 's' and double 'o'
    "PasssWord",   # Triple 's'
    "HelloWorld",  # Double 'l' twice
    
    # Passwords with common special characters 
    "Admin!@#123",
    "User$%^789",
    
    # Passwords with mixed numbers and special chars
    "123!@#456",
    "1a2b3c!@#",
    
    # Passwords with non-sequential repeated chars
    "PaPaYa123", 
    "TiTanic_2012",
    
    # Complex combinations
    "P@ssW0rd_2023!",
    "Secur3_Passw0rd#1",
    "$uper$ecure2023",
    
    # Additional test cases
    # Common patterns
    "qwerty123",
    "abc123XYZ",
    "12345abcde",
    "QWERTY!@#$%^",
    
    # Special character variations
    "Special!Chars@Here#",
    "All$pecial^&*()_+",
    "$peci@l_Ch@r@cter$",
    "!@#$%^&*()_+{}|:<>?",
    
    # Patterns with digits
    "123456789",
    "987654321",
    "1212121212",
    "9876543210ABCDEF",
    
    # Patterns with letters
    "abcdefghij",
    "ABCDEFGHIJ",
    "abcABCabcABC",
    "aAbBcCdDeEfF",
    
    # Case sensitivity checks
    "CaseSensitive",
    "cASEsENSITIVE",
    "MiXeDcAsE",
    "aLtErNaTiNgCaSe",
    
    # Sequential characters
    "abcdef123456",
    "ABCDEF123456",
    "123ABCabc",
    "XYZxyz789",
    
    # Palindromes
    "Abba",
    "Racecar",
    "Madam121Madam",
    "Able&elbA",
    
    # Repeated characters
    "aaabbbccc",
    "111222333",
    "aaa111bbb222",
    "111aaa222bbb",
    
    # Real-world scenarios
    "Summer2023!",
    "Winter2023@",
    "CompanyName123",
    "MyPassword!23",
    
    # Foreign characters - THESE WILL BE FLAGGED AS INVALID
    "España123",
    "München!@#",
    "Café_Au_Lait",
    "日本語123",
    
    # Industry-specific patterns
    "SQL_query123",
    "Python3.10Secure",
    "Java$Developer",
    "HTML_CSS_JS!",
    
    # Different lengths
    "A1",
    "A1B",
    "A1B2",
    "A1B2C",
    "A1B2C3",
    "A1B2C3D4",
    "A1B2C3D4E5",
    
    # Spaces and underscores
    "Hello_World_2023",
    "Cyber_Security_101",
    "Web_Development_2023",
    "Machine_Learning_AI",
    
    # Multiword with cases
    "ThisIsATest",
    "thisIsATest",
    "THIS_IS_A_TEST",
    "This-Is-A-Test",
    
    # Character repetition patterns
    "abababab",
    "12121212",
    "a1a1a1a1",
    "AbCdAbCd",
    
    # Security question answers
    "FirstPet2010",
    "BirthCity1990",
    "Mother$MaidenName",
    "High$chool2005",
    
    # Traditional PIN-like passwords
    "1234",
    "9876",
    "1357",
    "2468",
    
    # IT/Tech related
    "LAN_Password123",
    "WiFi-Security!",
    "Database_Admin1",
    "Cloud#Computing"
]

# Test with different methods and keys
test_configs = [
    {"key": "CIPHER", "method": 1},
    {"key": "SECURITY", "method": 2},
    {"key": "P@55W0RD!", "method": 3}
]

def main():
    success_count = 0
    invalid_chars_count = 0
    failed_count = 0
    error_count = 0
    total_tests = len(passwords) * len(test_configs)
    invalid_passwords = []
    
    print("=== COMPREHENSIVE PASSWORD ENCRYPTION/DECRYPTION TESTS ===\n")
    print("This test includes validation for character restrictions.\n")
    print(f"Allowed characters: letters (A-Z, a-z), numbers (0-9), and special characters: !@#$%^&*()_+-{{}}\n")
    
    for config in test_configs:
        key = config["key"]
        method = config["method"]
        method_name = {1: "Plain Traditional", 2: "Key-Based Traditional", 3: "Spiral Completion"}[method]
        
        print(f"\n=== Testing with Key: '{key}', Method: {method} - {method_name} ===\n")
        
        method_success = 0
        method_invalid = 0
        method_failed = 0
        method_error = 0
        
        for password in passwords:
            result, status = test_password(password, key, method)
            
            if status == "success":
                success_count += 1
                method_success += 1
            elif status == "invalid_chars":
                invalid_chars_count += 1
                method_invalid += 1
                if password not in invalid_passwords:
                    invalid_passwords.append(password)
            elif status == "mismatch":
                failed_count += 1
                method_failed += 1
            elif status == "error":
                error_count += 1
                method_error += 1
                
        # Print a method summary
        print(f"\nMethod Summary:")
        print(f"  Successful: {method_success}")
        print(f"  Invalid characters: {method_invalid}")
        print(f"  Failed matches: {method_failed}")
        print(f"  Errors: {method_error}")
        print(f"  Total valid passwords: {method_success}/{len(passwords) - method_invalid}")
        if method_invalid > 0:
            print(f"  (Skipped {method_invalid} passwords with invalid characters)")
    
    # Calculate valid tests
    valid_tests = total_tests - (invalid_chars_count)
    success_rate = (success_count / valid_tests) * 100 if valid_tests > 0 else 0
    
    # Print final summary
    print(f"\n=== FINAL TEST SUMMARY ===")
    print(f"Successful tests: {success_count}")
    print(f"Failed matches: {failed_count}")
    print(f"Errors: {error_count}")
    print(f"Passwords with invalid characters: {len(invalid_passwords)}")
    print(f"Success rate (valid passwords only): {success_rate:.2f}%")
    
    if invalid_passwords:
        print("\n=== PASSWORDS WITH INVALID CHARACTERS ===")
        print("The following passwords contain characters not in the allowed set:")
        for idx, pwd in enumerate(invalid_passwords, 1):
            invalid_chars = [c for c in pwd if c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-{}"]
            print(f"{idx}. '{pwd}' - Invalid characters: {', '.join(repr(c) for c in invalid_chars)}")
        
        print("\nINVALID CHARACTER REPORT:")
        all_invalid_chars = set()
        for pwd in invalid_passwords:
            for c in pwd:
                if c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-{}":
                    all_invalid_chars.add(c)
        
        print(f"Found {len(all_invalid_chars)} unique invalid characters: {', '.join(repr(c) for c in sorted(all_invalid_chars))}")
        print("\nREMINDER: Only the following characters are allowed:")
        print("- Letters (A-Z, a-z)")
        print("- Numbers (0-9)")
        print("- Special characters: !@#$%^&*()_+-{}")

if __name__ == "__main__":
    main() 