import math
"""
CRYPTOGRAPHY FUNCTIONS
======================

This file contains all the mathematical logic for our cryptographic algorithms.
Each function is heavily commented to help you understand both the math
and the programming concepts.

We'll start with the Caesar Cipher (fully implemented) and then provide
detailed comments for implementing the other ciphers.
"""

# =============================================================================
# CAESAR CIPHER - FULLY IMPLEMENTED
# =============================================================================

def caesar_encrypt(plain_text, shift_key):
    """
    CAESAR CIPHER ENCRYPTION
    ========================
    
    The Caesar cipher is one of the simplest encryption techniques.
    It works by shifting each letter in the alphabet by a fixed number of positions.
    
    For example, with a shift of 3:
    A -> D, B -> E, C -> F, ..., X -> A, Y -> B, Z -> C
    
    Mathematical formula: new_position = (old_position + shift) mod 26
    
    Parameters:
    - plain_text (str): The text we want to encrypt
    - shift_key (int): How many positions to shift each letter
    
    Returns:
    - str: The encrypted text
    """
    
    # Convert the input to uppercase for consistency
    # This makes our cipher case-insensitive
    plain_text = plain_text.upper()
    
    # This will store our encrypted result
    encrypted_text = ""
    
    # Process each character in the input text
    for char in plain_text:
        
        # Check if the character is a letter (A-Z)
        if char.isalpha():
            
            # Convert letter to number (A=0, B=1, C=2, ..., Z=25)
            # ord() gives us the ASCII value, ord('A') = 65
            # So ord(char) - ord('A') gives us 0-25
            char_position = ord(char) - ord('A')
            
            # Apply the Caesar cipher formula
            # The % 26 ensures we wrap around (Z+1 becomes A)
            new_position = (char_position + shift_key) % 26
            
            # Convert back to a letter
            # chr() converts a number back to its ASCII character
            encrypted_char = chr(new_position + ord('A'))
            
            # Add the encrypted character to our result
            encrypted_text += encrypted_char
            
        else:
            # If it's not a letter (space, punctuation, number),
            # keep it unchanged
            encrypted_text += char
    
    return encrypted_text

def caesar_decrypt(cipher_text, shift_key):
    """
    CAESAR CIPHER DECRYPTION
    ========================
    
    To decrypt a Caesar cipher, we simply shift in the opposite direction.
    If we encrypted with +3, we decrypt with -3.
    
    Mathematical formula: old_position = (new_position - shift) mod 26
    
    Parameters:
    - cipher_text (str): The encrypted text we want to decrypt
    - shift_key (int): The same shift key used for encryption
    
    Returns:
    - str: The decrypted (original) text
    """
    
    # Decryption is just encryption with a negative shift!
    # If we encrypted with +3, we decrypt with -3
    return caesar_encrypt(cipher_text, -shift_key)

# =============================================================================
# HELPER FUNCTIONS FOR FUTURE CIPHERS
# =============================================================================

def gcd(a, b):
    """
    GREATEST COMMON DIVISOR (Euclidean Algorithm)
    =============================================
    
    This function finds the greatest common divisor of two numbers.
    It's needed for the Affine cipher and RSA.
    
    The Euclidean algorithm works by repeatedly applying:
    gcd(a, b) = gcd(b, a mod b) until b = 0
    
    TODO: This is already implemented for you to use in other ciphers!
    """
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    """
    EXTENDED EUCLIDEAN ALGORITHM
    =============================
    
    Helper function for finding modular inverses.
    Returns (gcd, x, y) where ax + by = gcd(a, b)
    """
    if b == 0:
        return (a, 1, 0)
    g, x, y = extended_gcd(b, a % b)
    return (g, y, x - (a // b) * y)
    
def mod_inverse(a, m):
    """
    MODULAR MULTIPLICATIVE INVERSE
    ==============================
    
    This finds a number 'x' such that (a * x) mod m = 1
    It's essential for decrypting Affine ciphers and RSA.
    
    TODO: Implement this using the Extended Euclidean Algorithm
    This is needed for affine_decrypt() and rsa_decrypt()
    
    Example: mod_inverse(3, 26) = 9 because (3 * 9) mod 26 = 1
    """
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m

# =============================================================================
# VIGENÈRE CIPHER - TO BE IMPLEMENTED
# =============================================================================

def vigenere_encrypt(plain_text, keyword):
    """
    VIGENÈRE CIPHER ENCRYPTION - TO BE IMPLEMENTED
    ==============================================
    
    The Vigenère cipher uses a keyword to create multiple Caesar ciphers.
    Each letter of the keyword determines the shift for that position.
    
    Algorithm:
    1. Repeat the keyword to match the length of the plain text
    2. For each letter, use the corresponding keyword letter as the shift
    3. Apply Caesar cipher with that shift
    
    Example:
    Plain text: "HELLO"
    Keyword:    "KEY"
    Repeated:   "KEYKE"
    
    H + K = H(7) + K(10) = R(17)
    E + E = E(4) + E(4) = I(8)
    L + Y = L(11) + Y(24) = J(9)  [wraps around]
    L + K = L(11) + K(10) = V(21)
    O + E = O(14) + E(4) = S(18)
    
    Result: "RIJVS"
    """
    encrypted_text = "" # Initialize empty string for resul
    keyword = keyword.lower() # Convert keyword to lowercase for consistency
    keyword_index = 0 # Track position in keyword

    for letter in plain_text:
        # Only process alphabetic characters
        if letter.isalpha():
            # Calculate shift value from current keyword character
            shift_val = ord(keyword[keyword_index % len(keyword)]) - ord('a')

            # Handle uppercase letters
            if letter.isupper():
                shifted = (ord(letter) - 65 + shift_val) % 26 # A=65, mod 26
                encrypted_letter = chr(shifted + 65)
            # Handle lowercase letters
            else:
                shifted = (ord(letter) - 97 + shift_val) % 26 # a=97, mod 26
                encrypted_letter = chr(shifted + 97)

            keyword_index += 1 # Move to next keyword character
        else:
            # Keep non-alphabetic characters unchanged
            encrypted_letter = letter
        
        # Append processed character to result
        encrypted_text += encrypted_letter

    return encrypted_text

def vigenere_decrypt(cipher_text, keyword):
    """
    VIGENÈRE CIPHER DECRYPTION - TO BE IMPLEMENTED
    ==============================================
    
    To decrypt, subtract the keyword letters instead of adding them.
    """
    decrypted_text = "" # Initialize empty string for result
    keyword = keyword.lower() # Convert keyword to lowercase for consistency
    keyword_index = 0 # Track position in keyword

    for letter in cipher_text:
        if letter.isalpha():
            # Only process alphabetic characters
            shift_val = ord(keyword[keyword_index % len(keyword)]) - ord('a')

            # Calculate shift value from current keyword character
            if letter.isupper():
                # Reverse the shift (subtract instead of add) for decryption
                shifted = (ord(letter) - 65 - shift_val) % 26 # A=65, mod 26
                decrypted_letter = chr(shifted + 65)
            # Handle lowercase letters
            else:
                shifted = (ord(letter) - 97 - shift_val) % 26 # a=97, mod 26
                decrypted_letter = chr(shifted + 97)

            keyword_index += 1 # Move to next keyword character
        else:
            # Preserve non-alphabetic characters as-i
            decrypted_letter = letter
        
        # Append processed character to result
        decrypted_text += decrypted_letter

    return decrypted_text


# =============================================================================
# AFFINE CIPHER - TO BE IMPLEMENTED
# =============================================================================

def affine_encrypt(plain_text, a, b):
    """
    AFFINE CIPHER ENCRYPTION - TO BE IMPLEMENTED
    ============================================
    
    The Affine cipher uses the formula: E(x) = (ax + b) mod 26
    where:
    - x is the letter position (A=0, B=1, ..., Z=25)
    - a and b are the keys
    - a must be coprime to 26 (gcd(a, 26) = 1)
    
    Valid values for 'a': 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
    
    Example with a=5, b=8:
    A(0) -> (5*0 + 8) mod 26 = 8 -> I
    B(1) -> (5*1 + 8) mod 26 = 13 -> N
    C(2) -> (5*2 + 8) mod 26 = 18 -> S
    
    TODO: Implement this logic!
    Remember to check that gcd(a, 26) = 1!
    """
    if gcd(a, 26) != 1:
        raise ValueError( "'a' must be coprime with 26.")

    result = ""
    for char in plain_text:
        if char.isalpha(): # Only encrypt letters
            base = ord('A') if char.isupper() else ord('a') # Preserve case
            x = ord(char) - base # Convert letter to 0-25
            encrypted_char = (a * x + b) % 26 # Apply Affine formula
            result += chr(encrypted_char + base) # Convert back to character
        else:
            result += char # Keep non-alphabet characters unchanged
    return result
    

def affine_decrypt(cipher_text, a, b):
    """
    AFFINE CIPHER DECRYPTION - TO BE IMPLEMENTED
    ============================================
    
    The decryption formula is: D(y) = a^(-1) * (y - b) mod 26
    where a^(-1) is the modular multiplicative inverse of 'a' modulo 26
    
    You'll need to use the mod_inverse() function!
    
    TODO: Implement this logic!
    """
    if gcd(a, 26) != 1:
        return ValueError("'a' must be coprime with 26.")

    a_inv = mod_inverse(a, 26) # Find modular inverse of a
    if a_inv is None:
        raise ValueError("Modular inverse does not exist.")

    result = ""
    for char in cipher_text:
        if char.isalpha(): # Only decrypt letters
            base = ord('A') if char.isupper() else ord('a') # Preserve case
            y = ord(char) - base # Convert letter to 0-25
            decrypted_char = (a_inv * (y - b)) % 26 # Apply decryption formula
            result += chr(decrypted_char + base) # Convert back to character
        else:
            result += char # Keep non-alphabet characters unchanged
    return result

# =============================================================================
# RSA CIPHER - TO BE IMPLEMENTED (ADVANCED)
# =============================================================================

def is_prime(n):
    """
    PRIME NUMBER CHECKER - TO BE IMPLEMENTED
    =======================================
    
    RSA requires prime numbers. This function should check if a number is prime.
    
    A simple algorithm:
    1. If n < 2, it's not prime
    2. Check if any number from 2 to sqrt(n) divides n evenly
    3. If any divisor is found, n is not prime.
    
    """
    if n < 2:
      return False # 0 and 1 are not primes

    for i in range(2, math.isqrt(n)+1):
        if n%i==0:
            return False # Found a divisor → not prime

    return True # No divisors found → prime

def rsa_generate_keys(p, q):
    """
    RSA KEY GENERATION - TO BE IMPLEMENTED
    =====================================
    
    This generates RSA public and private keys from two prime numbers.
    
    Algorithm:
    1. Validate p and q as distinct primes.
    2. Calculate n = p * q
    3. Calculate φ(n) = (p-1) * (q-1)
    4. Choose e (commonly 65537)
    5. Ensure gcd(e, φ(n)) = 1.
    6. Calculate d = mod_inverse(e, φ(n))
    7. Public key = (e, n), Private key = (d, n)
    
    """
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("p and q must be primes") # Validate primes
    if p == q:
        raise ValueError("p and q must be distinct") # Prevent weak keys
        
    n = p * q # RSA modulus
    phi = (p - 1) * (q - 1) # Euler's totient function
    e = 65537 # Standard public exponent
    
    if gcd(e, phi) != 1:
        raise ValueError("e must be coprime with φ(n)") # Ensure inverse exists

    d = mod_inverse(e, phi) # Private exponent
    if d is None:
        raise ValueError("No inverse exists for e mod φ(n)") # Fallback

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key # Public and private keys

def rsa_encrypt(message, public_key):
    """
    RSA ENCRYPTION - TO BE IMPLEMENTED
    =================================
    
    Encrypts a message using the public key.
    Formula: c = m^e mod n
    
    Algorithm:
        1. Convert string messages to integer (bytes → big-endian int).
        2. Check if message is too large for n.
        3. Compute c = mᵉ mod n.
    
    """
    e, n = public_key
    
    if isinstance(message, str):
        message = int.from_bytes(message.encode(), 'big') # String → int
    
    if message >= n:
        raise ValueError("Message too large for key size") # Prevent overflow
    
    c = pow(message, e, n) # Modular exponentiation
    return c

def rsa_decrypt(ciphertext, private_key):
    """
    RSA DECRYPTION - TO BE IMPLEMENTED
    =================================
    
    Decrypts a message using the private key.
    Formula: m = c^d mod n
    
    """
    d, n = private_key
    m = pow(ciphertext, d, n)  # Modular exponentiation
    try:
        # Convert integer to bytes, then to string
        return m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()
    except:
        return m # Return integer if decoding fails (e.g., non-text data)

# =============================================================================
# TESTING FUNCTIONS
# =============================================================================

def test_caesar_cipher():
    """
    Test function for the Caesar cipher to make sure it works correctly.
    You can run this to verify your implementation!
    """
    print("Testing Caesar Cipher...")
    
    # Test case 1: Basic encryption
    plain = "HELLO WORLD"
    shift = 3
    encrypted = caesar_encrypt(plain, shift)
    decrypted = caesar_decrypt(encrypted, shift)
    
    print(f"Original: {plain}")
    print(f"Encrypted (shift {shift}): {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Test passed: {plain == decrypted}")
    print()
    
    # Test case 2: Wrap-around
    plain = "XYZ"
    shift = 5
    encrypted = caesar_encrypt(plain, shift)
    decrypted = caesar_decrypt(encrypted, shift)
    
    print(f"Wrap-around test:")
    print(f"Original: {plain}")
    print(f"Encrypted (shift {shift}): {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Test passed: {plain == decrypted}")
    
def test_vigenere_cipher():
    print("\nTesting Vigenère Cipher...")
    plain = "HELLO"
    keyword = "KEY"
    encrypted = vigenere_encrypt(plain, keyword)
    decrypted = vigenere_decrypt(encrypted, keyword)
    
    print(f"Original: {plain}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Test passed: {plain == decrypted}")

def test_affine_cipher():
    print("\nTesting Affine Cipher...")
    plain = "HELLO"
    a, b = 5, 8
    encrypted = affine_encrypt(plain, a, b)
    decrypted = affine_decrypt(encrypted, a, b)
    
    print(f"Original: {plain}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Test passed: {plain == decrypted}")

def test_rsa_cipher():
    print("\nTesting RSA Cipher...")
    p, q = 61, 53  # Small primes for demonstration
    public, private = rsa_generate_keys(p, q)
    
    message = 42  # Simple number for demonstration
    encrypted = rsa_encrypt(message, public)
    decrypted = rsa_decrypt(encrypted, private)
    
    print(f"Original: {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Test passed: {message == decrypted}")

def run_comprehensive_tests():
    """
    Comprehensive test suite for the Caesar cipher.
    This helps verify that our implementation works correctly.
    """
    print("🧪 RUNNING COMPREHENSIVE CAESAR CIPHER TESTS")
    print("=" * 50)
    
    test_cases = [
        # (plain_text, shift, expected_result)
        ("HELLO", 3, "KHOOR"),
        ("WORLD", 5, "BTWQI"),
        ("ABC", 1, "BCD"),
        ("XYZ", 3, "ABC"),  # Test wrap-around
        ("HELLO WORLD!", 13, "URYYB JBEYQ!"),  # Test with punctuation
        ("", 5, ""),  # Test empty string
        ("A", 25, "Z"),  # Test maximum shift
        ("programming", 7, "WYVNYHTTPUN"),  # Test lowercase (should convert to uppercase)
    ]
    
    all_tests_passed = True
    
    for i, (plain, shift, expected) in enumerate(test_cases, 1):
        print(f"\nTest {i}: Encrypting '{plain}' with shift {shift}")
        
        # Test encryption
        encrypted = caesar_encrypt(plain, shift)
        print(f"  Expected: '{expected}'")
        print(f"  Got:      '{encrypted}'")
        
        if encrypted == expected:
            print("  ✅ Encryption PASSED")
        else:
            print("  ❌ Encryption FAILED")
            all_tests_passed = False
        
        # Test decryption (should get back original, but uppercase)
        decrypted = caesar_decrypt(encrypted, shift)
        original_upper = plain.upper()
        print(f"  Decryption test: '{encrypted}' -> '{decrypted}'")
        
        if decrypted == original_upper:
            print("  ✅ Decryption PASSED")
        else:
            print("  ❌ Decryption FAILED")
            all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! Caesar cipher is working correctly.")
    else:
        print("❌ SOME TESTS FAILED! Check the implementation.")
    print("=" * 50)
    
    # Test Vigenère cipher
    test_vigenere_cipher()
    
    # Test Affine cipher
    test_affine_cipher()
    
    # Test RSA cipher
    test_rsa_cipher()
    
    print("\n" + "=" * 60)
    print("✅ ALL CIPHER TESTS COMPLETED")

# Update the existing test function call
if __name__ == "__main__":
    run_comprehensive_tests()
