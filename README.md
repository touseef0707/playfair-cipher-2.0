# Advanced Playfair Cipher Implementation for Passwords

**IMPORTANT NOTE: This implementation is designed specifically for passwords. Messages should NOT contain spaces.**

This project implements an enhanced version of the Playfair cipher with several advanced security features:
- 7×7 matrix (instead of the traditional 5×5)
- Support for numbers and special characters
- Case preservation
- ASCII transformation for additional security
- Fisher-Yates shuffling for maximum protection

## Motivation for Modification

The original Playfair cipher supports only alphabets, which is problematic for encrypting passwords that typically include numbers, symbols, and different cases. This implementation extends the cipher to handle a broader character set while maintaining the core mechanism of digraph encryption and ensuring case preservation. Additionally, ASCII transformation and Fisher-Yates shuffling provide multiple layers of security beyond the traditional Playfair approach.

## Features

- **7×7 Matrix**: Supports uppercase letters, numbers, and special characters
- **Fixed Special Characters**: Uses a set of 13 special characters including underscore: `!@#$%^&*()_-+`
- **Case Preservation**: Maintains the original case of letters during encryption and decryption
- **Traditional Playfair Behavior**: Uses 'X' as a filler character for repeated letters and odd-length messages
- **Plain Traditional Matrix**: Uses the Plain Traditional (PT) method for matrix generation
- **ASCII Transformation**: Applies modular arithmetic to further encrypt characters
- **Fisher-Yates Shuffling**: Deterministically shuffles characters based on the case encoding

## Encryption Process (Step-by-Step)

### Step 1: Case Preservation

When dealing with a modified Playfair cipher that treats all characters equally (letters, digits, and symbols), we must still preserve the original case of alphabetic characters. This is because the cipher itself works in a case-insensitive manner — it encrypts without regard for case.

To solve this:
1. Create a binary string representing the case of each character:
   - 1 for uppercase letters or any non-letter (symbols, digits)
   - 0 for lowercase letters
2. Convert the binary string to hexadecimal for compact storage
3. This hex string is saved and used during decryption to restore the original casing

**Example:**
```
Password: H$I8*kT
Length = 7 (odd), so one filler will be added later (in Step 2).

Character | Type   | Is Uppercase? | Binary
----------|--------|---------------|-------
H         | Letter | Yes           | 1
$         | Symbol | Treated as U  | 1
I         | Letter | Yes           | 1
8         | Digit  | Treated as U  | 1
*         | Symbol | Treated as U  | 1
k         | Letter | No            | 0
T         | Letter | Yes           | 1

Binary case string: 1111101
Padded to full byte: 11111011
Hexadecimal: FB

Stored Case Encoding: FB
```

### Step 2: Digraph Construction

Playfair cipher works on pairs of characters (digraphs):
1. Split the password into pairs
2. If the length is odd, add a filler character (commonly 'X') to make it even
3. If any pair has two identical characters, separate them with a filler

**Example:**
```
Initial password: H$I8*kT → Length = 7 (odd)
Add filler X → H$I8*kTX

Split into digraphs:
Index  | Digraph
-------|--------
0      | H$
1      | I8
2      | *k
3      | TX

Now we have 4 digraphs ready for encryption.
```

### Step 3: Digraph Encryption (Using 7×7 Matrix)

Using the 7×7 Playfair matrix constructed from a keyword, we encrypt each digraph using modified Playfair rules:
- Same Row: If both characters are in the same row, replace with characters two rows below, wrapping around
- Same Column: If both characters are in the same column, replace with characters three columns right, wrapping around
- Rectangle: If characters form a rectangle, replace with characters at the same row but in the column of the other character

**Example with matrix constructed using key: C@23#b**
```
C  @  2  3  #  B  A
D  E  F  G  H  I  J
K  L  M  N  O  P  Q
R  S  T  U  V  W  X
Y  Z  0  1  4  5  6
7  8  9  !  $  %  ^
&  *  (  )  _  -  +

Encrypting Each Digraph:
Digraph | Position of Chars | Rule        | Encrypted Digraph
--------|-------------------|-------------|-----------------
H$      | (1, 4) (5, 4)     | Same Column | D7
I8      | (1, 5) (5, 1)     | Rectangle   | E%
*k      | (6, 1) (2, 0)     | Rectangle   | &L
TX      | (3, 2) (3, 6)     | Same Row    | 9^

Combined encrypted output: D7E%&L9^
```

### Step 4: ASCII-based Transformation

This step converts each original character into a new character using modular arithmetic based on a key value:

1. For each character in the encrypted text:
   - Find its index in our valid character set (77 characters)
   - Add a key value (derived from the secret key)
   - Apply modulo 77 to ensure the result stays within our valid range
   - Replace with the character at the new index

**Example:**
```
Original encrypted text: D7E%&L9^
Key value (derived from secret key): 67

Character | Original Index | Calculation  | New Index | New Char
----------|----------------|--------------|-----------|----------
D         | 3              | (3+67)%77    | 70        | (
7         | 55             | (55+67)%77   | 45        | x
E         | 4              | (4+67)%77    | 71        | 6
%         | 72             | (72+67)%77   | 62        | o
&         | 74             | (74+67)%77   | 64        | S
L         | 11             | (11+67)%77   | 1         | H
9         | 57             | (57+67)%77   | 47        | !
^         | 73             | (73+67)%77   | 63        | o

Transformed result: (x6oSH!o
```

### Step 5: Shuffling using Fisher-Yates Algorithm

For additional security, the characters in the encrypted text are shuffled using a deterministic version of the Fisher-Yates algorithm. The shuffle is guided by the case information to ensure it can be reversed during decryption.

1. Convert case encoding to hex values (e.g., 'fb' → [15, 11])
2. Generate shuffle indices using these values
3. Rearrange the characters according to the shuffled indices

**Example:**
```
Starting with encrypted text: (x6oSH!o
Case encoding: 'fb' → key values [15, 11]
Initial indices: [0, 1, 2, 3, 4, 5, 6, 7]

After shuffling, indices become: [2, 6, 4, 7, 0, 5, 1, 3]
Shuffled result: 6!So(Hxo

Final encrypted text: 6!So(Hxo
```

## Decryption Process

Decryption reverses all steps of the encryption process:

### Step 1: Unshuffling

1. Using the same case encoding, regenerate the shuffle indices
2. Create a position map to determine where each character should go
3. Restore the original order of characters

**Example:**
```
Encrypted text: 6!So(Hxo
Shuffle indices: [2, 6, 4, 7, 0, 5, 1, 3]
Unshuffled result: (x6oSH!o
```

### Step 2: Reverse ASCII Transformation

1. For each character in the unshuffled text:
   - Find its index in our valid character set
   - Subtract the key value (derived from the secret key)
   - Apply modulo 77 to wrap around if needed
   - Replace with the character at the new index

**Example:**
```
Unshuffled text: (x6oSH!o
Key value: 67

Calculation for first character:
Index of '(' = 70
(70 - 67) % 77 = 3
Character at index 3 = D

After complete reverse transformation: D7E%&L9^
```

### Step 3: Decrypt Digraphs

1. Split the text into digraphs (pairs of characters)
2. Decrypt each digraph using the reverse Playfair rules:
   - Same Row → Replace with characters two rows up
   - Same Column → Replace with characters three columns left
   - Rectangle → Same rectangle rule (it's its own inverse)

**Example:**
```
Digraphs: D7 E% &L 9^
Matrix is the same as used in encryption (key: C@23#b)

Decrypted digraphs:
D7 → H$
E% → I8
&L → *k
9^ → TX

Combined: H$I8*kTX
```

### Step 4: Remove Fillers and Restore Case

1. Remove the 'X' filler characters:
   - Remove trailing 'X' (if present)
   - Remove 'X' between repeated letters
2. Apply the case information to restore the original case of letters

**Example:**
```
After removing fillers: H$I8*kT
Applying case information (fb = 11111011):
Final decrypted result: H$I8*kT
```

## Multi-layered Security

Beyond the traditional Playfair cipher, our implementation adds multiple security layers:
- **Matrix-based encryption**: The foundational Playfair digraph encryption
- **ASCII transformation**: A modular arithmetic layer that further obfuscates the encrypted text
- **Fisher-Yates shuffling**: Deterministic rearrangement of characters based on case information
- Each layer would require separate cryptanalysis, significantly increasing security

## Files

- `methods.py`: Contains the matrix construction method (Plain Traditional) and input validation
- `playfair_encrypt.py`: Implements the Playfair encryption algorithm with case preservation, ASCII transformation, and shuffling
- `playfair_decrypt.py`: Implements the Playfair decryption algorithm with case restoration, reverse ASCII transformation, and unshuffling
- `main.py`: Provides a user-friendly interface with options for encryption and decryption

## Usage

### Encryption

```
python playfair_encrypt.py
```

Follow the prompts to:
1. Enter your secret key
2. Enter the password to encrypt

The program will display:
- The encryption matrix
- The encrypted password (after all transformation steps)
- Case information (needed for decryption)
- The password split into digraphs
- The corresponding encrypted digraphs

### Decryption

```
python playfair_decrypt.py
```

Follow the prompts to:
1. Enter the secret key (must match the one used for encryption)
2. Enter the encrypted password
3. Enter the case information

The program will display the decrypted password.

### User Interface

```
python main.py
```

Provides a menu-based interface with options for:
- Encrypting passwords
- Decrypting passwords
- Visualizing the encryption/decryption process
- Saving results to files
