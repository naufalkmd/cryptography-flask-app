"""
CRYPTOGRAPHY WEB APP - MAIN APPLICATION FILE (COMPLETE ROUTING)
===============================================================

This is the main Flask application file that handles all the web routes
and connects our HTML templates with the cipher logic.

Flask is a lightweight web framework for Python that makes it easy to
create web applications. Here's how it works:

1. We create a Flask app instance
2. We define routes (URLs) that users can visit
3. Each route has a function that handles what happens when someone visits that URL
4. We can render HTML templates and pass data to them
5. We can handle form submissions (POST requests)

Let's break down each part as we build it!
"""

# Import the Flask framework and specific functions we need
from flask import Flask, render_template, request, redirect, url_for, flash

# Import our custom cipher functions from the ciphers.py file
from ciphers import (
    caesar_encrypt, caesar_decrypt, 
    vigenere_encrypt, vigenere_decrypt,
    affine_encrypt, affine_decrypt,
    rsa_generate_keys, rsa_encrypt, rsa_decrypt, is_prime, gcd
    )

# Create a Flask application instance
# __name__ tells Flask where to find templates and static files
app = Flask(__name__)

# Set a secret key for session management and flash messages
# In a real application, this should be a random, secure key
# For educational purposes, we'll use a simple string
app.secret_key = 'cryptography_learning_app_secret_key_2024'

# =============================================================================
# HOME PAGE ROUTE
# =============================================================================

@app.route('/')
def index():
    """
    This is the home page route. When someone visits the root URL (/),
    this function runs and returns the home page.
    
    The @app.route('/') decorator tells Flask that this function should
    handle requests to the root URL.
    
    We could also name this function 'index' or anything else - the function
    name doesn't matter, only the route decorator matters.
    """
    print("📱 User visited the home page")  # This will show in the console
    
    # render_template() looks for HTML files in the 'templates' folder
    # and returns them to the user's browser
    return render_template("index.html")

# Alternative route for home page (some people might type /home)
@app.route('/home')
def home_alternative():
    """
    This is an alternative route to the home page.
    If someone types /home instead of just /, they'll still get to the home page.
    
    We use redirect() to send them to the main home route.
    url_for() generates the URL for the 'index' function.
    """
    return redirect(url_for('index'))

# =============================================================================
# CAESAR CIPHER ROUTE (FULLY IMPLEMENTED)
# =============================================================================

@app.route('/caesar', methods=['GET', 'POST'])
def caesar():
    """
    This route handles the Caesar Cipher page.
    
    methods=['GET', 'POST'] means this route can handle both:
    - GET requests: when someone just visits the page (shows the forms)
    - POST requests: when someone submits a form (processes the data)
    
    This is a common pattern in web development:
    - GET: "Show me the page"
    - POST: "Process this form data"
    """
    
    print("🏛️ User visited Caesar cipher page")
    
    # Initialize variables to store results
    # These will be None when the page first loads (GET request)
    encrypt_result = None
    decrypt_result = None
    error_message = None
    
    # Store the form data so we can show it back to the user
    # This improves user experience - they don't have to retype everything
    form_data = {
        'encrypt_text': '',
        'encrypt_shift': 3,
        'decrypt_text': '',
        'decrypt_shift': 3
    }
    
    # Check if this is a form submission (POST request)
    if request.method == 'POST':
        print("📝 Processing Caesar cipher form submission")
        
        try:
            # request.form contains all the data from the submitted form
            # We check which form was submitted by looking for specific button names
            
            if 'encrypt_submit' in request.form:
                # ENCRYPTION FORM WAS SUBMITTED
                print("🔒 Processing encryption request")
                
                # Get the data from the form fields
                plain_text = request.form['encrypt_text'].strip()
                shift_key = int(request.form['encrypt_shift'])
                
                # Store form data to show back to user
                form_data['encrypt_text'] = plain_text
                form_data['encrypt_shift'] = shift_key
                
                # Validate the input
                if not plain_text:
                    error_message = "Please enter some text to encrypt!"
                elif shift_key < 1 or shift_key > 25:
                    error_message = "Shift key must be between 1 and 25!"
                else:
                    # Call our encryption function from ciphers.py
                    encrypt_result = caesar_encrypt(plain_text, shift_key)
                    print(f"✅ Encryption successful: '{plain_text}' -> '{encrypt_result}'")
                    
                    # Flash a success message (optional - shows at top of page)
                    flash(f"Successfully encrypted '{plain_text}' with shift {shift_key}!", 'success')
                
            elif 'decrypt_submit' in request.form:
                # DECRYPTION FORM WAS SUBMITTED
                print("🔓 Processing decryption request")
                
                # Get the data from the form fields
                cipher_text = request.form['decrypt_text'].strip()
                shift_key = int(request.form['decrypt_shift'])
                
                # Store form data to show back to user
                form_data['decrypt_text'] = cipher_text
                form_data['decrypt_shift'] = shift_key
                
                # Validate the input
                if not cipher_text:
                    error_message = "Please enter some text to decrypt!"
                elif shift_key < 1 or shift_key > 25:
                    error_message = "Shift key must be between 1 and 25!"
                else:
                    # Call our decryption function from ciphers.py
                    decrypt_result = caesar_decrypt(cipher_text, shift_key)
                    print(f"✅ Decryption successful: '{cipher_text}' -> '{decrypt_result}'")
                    
                    # Flash a success message
                    flash(f"Successfully decrypted '{cipher_text}' with shift {shift_key}!", 'success')
                
        except ValueError as e:
            # This happens if someone enters a non-number for the shift key
            error_message = "Please enter a valid number for the shift key!"
            print(f"❌ ValueError: {e}")
            
        except Exception as e:
            # This catches any other unexpected errors
            error_message = f"An unexpected error occurred: {str(e)}"
            print(f"❌ Unexpected error: {e}")
    
    # Render the Caesar cipher template and pass our results to it
    # The template can then display these results to the user
    return render_template('caesar.html', 
                         encrypt_result=encrypt_result,
                         decrypt_result=decrypt_result,
                         error_message=error_message,
                         form_data=form_data)

# =============================================================================
# PLACEHOLDER ROUTES FOR OTHER CIPHERS (FOR YOU TO IMPLEMENT)
# =============================================================================

@app.route('/vigenere', methods=['GET', 'POST'])
def vigenere():
    """
    Vigenère Cipher route - PLACEHOLDER FOR YOUR IMPLEMENTATION
    
    The Vigenère cipher uses a keyword to encrypt text. Unlike Caesar cipher
    which shifts all letters by the same amount, Vigenère uses different
    shifts for each letter based on the keyword.
    """
    
    print("🔑 User visited Vigenère cipher page")
    
    # Initialize variables to store results and errors
    # These will be None when the page first loads (GET request)
    encrypt_result = None
    decrypt_result = None
    error_message = None
    
    # Store the form data so we can show it back to the user
    # Default form data with empty strings and default keyword "KEY"
    form_data = {
        'encrypt_text': '',
        'encrypt_keyword': 'KEY',
        'decrypt_text': '',
        'decrypt_keyword': 'KEY'
    }

    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        print("📝 Processing Vigenere cipher form submission")
        try:
            # request.form contains all the data from the submitted form
            # We check which form was submitted by looking for specific button names
            
            # Check if encryption form was submitted
            if 'vigenere_encrypt_submit' in request.form:
                # ENCRYPTION FORM WAS SUBMITTED
                print("🔒 Processing encryption request")
                
                # Get and clean input text and keyword
                plain_text = request.form['vigenere_encrypt_text'].strip()
                keyword = request.form['vigenere_keyword'].strip()
                
                # Store form data for repopulation
                form_data['encrypt_text'] = plain_text
                form_data['encrypt_keyword'] = keyword
                
                # Validate inputs
                if not plain_text or not keyword:
                    error_message = "Both text and keyword are required!"
                elif not keyword.isalpha():
                    error_message = "Keyword must contain only letters!"
                else:
                    # Call our encryption function from ciphers.py and show success message
                    encrypt_result = vigenere_encrypt(plain_text, keyword)
                    print(f"✅ Encryption successful: '{plain_text}' -> '{encrypt_result}'")
                    
                    # Flash a success message (optional - shows at top of page)
                    flash(f"Successfully encrypted '{plain_text}' with keyword '{keyword}'!", 'success')

            # Check if decryption form was submitted
            elif 'vigenere_decrypt_submit' in request.form:
                # DECRYPTION FORM WAS SUBMITTED
                print("🔓 Processing decryption request")
                
                # Get and clean input text and keyword
                cipher_text = request.form['vigenere_decrypt_text'].strip()
                keyword = request.form['vigenere_decrypt_keyword'].strip()
                
                # Store form data for repopulation
                form_data['decrypt_text'] = cipher_text
                form_data['decrypt_keyword'] = keyword
                
                # Validate inputs
                if not cipher_text or not keyword:
                    error_message = "Both text and keyword are required!"
                elif not keyword.isalpha():
                    error_message = "Keyword must contain only letters!"
                else:
                    # Call our decryption function from ciphers.py and show success message
                    decrypt_result = vigenere_decrypt(cipher_text, keyword)
                    print(f"✅ Decryption successful: '{cipher_text}' -> '{decrypt_result}'")

                    # Flash a success message
                    flash(f"Successfully decrypted '{cipher_text}' with keyword '{keyword}'!", 'success')
                    
        # Catch any unexpected errors
        except ValueError as e:
            # This happens if someone enters a non-alphabet for the keyword
            error_message = "Please enter a valid alphabet for the keyword!"
            print(f"❌ ValueError: {e}")
            
        except Exception as e:
            # This catches any other unexpected errors
            error_message = f"An unexpected error occurred: {str(e)}"
            print(f"❌ Unexpected error: {e}")
            
    # Render the template with all data
    # The template can then display these results to the user
    return render_template('vigenere.html',encrypt_result=encrypt_result,
                         decrypt_result=decrypt_result,
                         error_message=error_message,
                         form_data=form_data)

@app.route('/affine', methods=['GET', 'POST'])
def affine():
    """
    Affine Cipher route - PLACEHOLDER FOR YOUR IMPLEMENTATION
    
    The Affine cipher uses the mathematical formula: E(x) = (ax + b) mod 26
    where 'a' and 'b' are the keys, and 'x' is the letter position (A=0, B=1, etc.)
    
    Important: 'a' must be coprime to 26 (gcd(a, 26) = 1) for decryption to work!
    Valid values for 'a': 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
    
    TODO FOR YOU TO IMPLEMENT:
    1. Import affine_encrypt and affine_decrypt from ciphers.py
    2. Add form handling for both encryption and decryption
    3. Validate that 'a' is coprime to 26
    4. Handle the two-key system (a and b)
    
    FORM FIELD NAMES TO EXPECT:
    - affine_encrypt_text: The text to encrypt
    - affine_a: The 'a' key (multiplicative)
    - affine_b: The 'b' key (additive)
    - affine_encrypt_submit: The encryption form submit button
    - affine_decrypt_text: The text to decrypt
    - affine_decrypt_a: The 'a' key for decryption
    - affine_decrypt_b: The 'b' key for decryption
    - affine_decrypt_submit: The decryption form submit button
    
    VALIDATION TO ADD:
    - Check that 'a' is in the valid list: [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    - Check that 'b' is between 0 and 25
    - Check that text is not empty
    """
    
    print("📐 User visited Affine cipher page")
    
    # Initialize variables to store results and errors
    # These will be None when the page first loads (GET request)
    encrypt_result = None
    decrypt_result = None
    error_message = None
    
    # Store the form data so we can show it back to the user
    # Default form data with empty strings and default value
    form_data = {
        'affine_encrypt_text': '',
        'affine_a': 5,
        'affine_b': 8,
        'affine_decrypt_text': '',
        'affine_decrypt_a': 5,
        'affine_decrypt_b': 8
    }

    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        print("📝 Processing Affine cipher form submission")
        try:
             # request.form contains all the data from the submitted form
            # We check which form was submitted by looking for specific button names
            
            if 'affine_encrypt_submit' in request.form:
                # ENCRYPTION FORM WAS SUBMITTED
                print("🔒 Processing encryption request")
                
                # Get and clean input text, a and b
                plain_text = request.form['affine_encrypt_text'].strip()
                a = int(request.form['affine_a'])
                b = int(request.form['affine_b'])
                
                # Store form data for repopulation
                form_data['affine_encrypt_text'] = plain_text
                form_data['affine_a'] = a
                form_data['affine_b'] = b
                
                # Validate inputs
                if not plain_text:
                    error_message = "Text to encrypt is required!"
                elif gcd(a, 26) != 1:
                    error_message = "Key 'a' must be coprime with 26 (try 1,3,5,7,9,11,15,17,19,21,23,25)"
                else:
                    # Call our encryption function from ciphers.py and show success message
                    encrypt_result = affine_encrypt(plain_text, a, b)
                    print(f"✅ Encryption successful: '{plain_text}' -> '{encrypt_result}'")
                    
                    # Flash a success message (optional - shows at top of page)
                    flash(f"Successfully encrypted with a='{a}', b='{b}'!", 'success')

            # Check if decryption form was submitted
            elif 'affine_decrypt_submit' in request.form:
                # DECRYPTION FORM WAS SUBMITTED
                print("🔓 Processing decryption request")
                
                # Get and clean input text, a and b
                cipher_text = request.form['affine_decrypt_text'].strip()
                a = int(request.form['affine_decrypt_a'])
                b = int(request.form['affine_decrypt_b'])
                
                # Store form data for repopulation
                form_data['affine_decrypt_text'] = cipher_text
                form_data['affine_decrypt_a'] = a
                form_data['affine_decrypt_b'] = b
                
                # Validate inputs
                if not cipher_text:
                    error_message = "Text to decrypt is required!"
                elif gcd(a, 26) != 1:
                    error_message = "Key 'a' must be coprime with 26"
                else:
                    # Call our decryption function from ciphers.py and show success message
                    decrypt_result = affine_decrypt(cipher_text, a, b)
                    print(f"✅ Decryption successful: '{cipher_text}' -> '{decrypt_result}'")
                    
                    # Flash a success message (optional - shows at top of page)
                    flash(f"Successfully decrypted with a='{a}', b='{b}'!", 'success')
                    
        # Catch any unexpected errors
        except ValueError as e:
            # This happens if someone enters a non-integers for the a and b
            error_message = "Keys must be integers!"
            print(f"❌ ValueError: {e}")
        except Exception as e:
            # This catches any other unexpected errors
            error_message = f"An unexpected error occurred: {str(e)}"
            print(f"❌ Unexpected error: {e}")

    # Render the template with all data
    # The template can then display these results to the user
    return render_template('affine.html',
                         encrypt_result=encrypt_result,
                         decrypt_result=decrypt_result,
                         error_message=error_message,
                         form_data=form_data)

@app.route('/rsa', methods=['GET', 'POST'])
def rsa():
    """
    RSA Cipher route - PLACEHOLDER FOR YOUR IMPLEMENTATION
    
    RSA is a public-key cryptosystem that uses two large prime numbers.
    It's much more complex than the other ciphers!
    
    Basic RSA process:
    1. Choose two prime numbers p and q
    2. Calculate n = p * q
    3. Calculate φ(n) = (p-1) * (q-1)
    4. Choose e such that gcd(e, φ(n)) = 1
    5. Calculate d such that (d * e) mod φ(n) = 1
    
    TODO FOR YOU TO IMPLEMENT:
    1. Import RSA functions from ciphers.py
    2. Handle key generation form
    3. Handle encryption form
    4. Handle decryption form
    5. Add prime number validation
    
    FORM FIELD NAMES TO EXPECT:
    - prime_p: First prime number
    - prime_q: Second prime number
    - generate_keys_submit: Key generation form submit
    - rsa_encrypt_text: Text/number to encrypt
    - public_key_e: Public key e
    - public_key_n: Public key n
    - rsa_encrypt_submit: Encryption form submit
    - rsa_decrypt_text: Encrypted number to decrypt
    - private_key_d: Private key d
    - private_key_n: Private key n (same as public key n)
    - rsa_decrypt_submit: Decryption form submit
    
    ADVANCED FEATURES TO CONSIDER:
    - Store generated keys in session for reuse
    - Validate that p and q are actually prime
    - Handle the complexity of large number arithmetic
    """
    
    print("🔒 User visited RSA cipher page")
    
    # Initialize variables to store results and errors
    # These will be None when the page first loads (GET request)
    encrypt_result = None
    decrypt_result = None
    error_message = None
    public_key = None
    private_key = None
    
    # Store the form data so we can show it back to the user
    # Default form data with empty strings and default prime number
    form_data = {
        'prime_p': '',
        'prime_q': '',
        'encrypt_text': '',
        'decrypt_text': ''
    }

    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        print("📝 Processing RSA cipher form submission")
        try:
            # request.form contains all the data from the submitted form
            # We check which form was submitted by looking for specific button names
            
            # Generate Keys
            # Check if generate key form was submitted
            if 'generate_keys_submit' in request.form:
                # ENCRYPTION FORM WAS SUBMITTED
                print("🔒 Processing key generation request")
                
                # Get and clean input prime number p and q
                p = int(request.form['prime_p'])
                q = int(request.form['prime_q'])
                
                # Store form data to show back to user
                form_data['prime_p'] = p
                form_data['prime_q'] = q
                
                # Validate the input
                if not is_prime(p) or not is_prime(q):
                    error_message = "Both p and q must be primes!"
                else:
                    # Call our key generation function from ciphers.py and show success message
                    public_key, private_key = rsa_generate_keys(p, q)
                    print(f"✅ Key generation successfull with p '{p}' and q'{q}'")
                    
                    # Flash a success message (optional - shows at top of page)
                    flash(f"Successfully generated with p='{p}' and q='{q}'!", 'success')
                    
            # Check if encryption form was submitted
            elif 'rsa_encrypt_submit' in request.form:
                # ENCRYPTION FORM WAS SUBMITTED
                print("🔒 Processing encryption request")
                
                # Get and clean input msg, e and n
                msg = request.form['rsa_encrypt_text'].strip()
                e = int(request.form['public_key_e'])
                n = int(request.form['public_key_n'])
                
                # Store form data to show back to user
                form_data['rsa_encrypt_text'] = msg
                form_data['public_key_e'] = e
                form_data['public_key_n'] = n
                
                # Call our encryption function from ciphers.py show success message
                encrypt_result = rsa_encrypt(msg, (e, n))
                print(f"✅ Encryption successful: '{msg}' with Public Key:'{(e,n)}'")
                
                # Flash a success message (optional - shows at top of page)
                flash(f"Successfully encrypted '{msg}' with Public Key:'{(e,n)}'!", 'success')
                
            # Check if decryption form was submitted
            elif 'rsa_decrypt_submit' in request.form:
                # DECRYPTION FORM WAS SUBMITTED
                print("🔓 Processing decryption request")
                
                # Get and clean input cipher, d and n
                cipher = int(request.form['rsa_decrypt_text'])
                d = int(request.form['private_key_d'])
                n = int(request.form['private_key_n'])
                
                # Store form data to show back to user
                form_data['rsa_decrypt_text'] = cipher
                form_data['private_key_d'] = d
                form_data['private_key_n'] = n
                
                # Call our decryption function from ciphers.py show success message
                decrypt_result = rsa_decrypt(cipher, (d, n))
                print(f"✅ Decryption successful: '{cipher}' , Private Key:'{(d,n)}'")
                
                # Flash a success message (optional - shows at top of page)
                flash(f"Successfully decrypted '{cipher}' , Public Key:'{(d,n)}'!", 'success')

        # Catch any unexpected errors
        except ValueError as e:
            # This happens if someone enters a non-integers for the key
            error_message = "Please enter a valid integers for the key!"
            print(f"❌ ValueError: {e}")
        except Exception as e:
            # This catches any other unexpected errors
            error_message = f"An unexpected error occurred: {str(e)}"
            print(f"❌ Unexpected error: {e}")

    # Render the template with all data
    # The template can then display these results to the user
    return render_template('rsa.html',
                         encrypt_result=encrypt_result,
                         decrypt_result=decrypt_result,
                         public_key=public_key,
                         private_key=private_key,
                         error_message=error_message,
                         form_data=form_data)

# =============================================================================
# ERROR HANDLING ROUTES
# =============================================================================

@app.errorhandler(404)
def page_not_found(error):
    """
    This function handles 404 errors (page not found).
    
    When someone tries to visit a URL that doesn't exist,
    Flask will call this function instead of showing the default error page.
    
    This provides a better user experience with a custom error page.
    """
    print(f"❌ 404 Error: User tried to access non-existent page")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    """
    This function handles 500 errors (internal server errors).
    
    When something goes wrong in our code, Flask will call this function
    instead of showing the default error page.
    """
    print(f"❌ 500 Error: Internal server error occurred")
    return render_template('500.html'), 500

# =============================================================================
# UTILITY ROUTES
# =============================================================================

@app.route('/about')
def about():
    """
    About page route - provides information about the application
    and the cryptographic algorithms.
    
    This is optional but good for educational purposes.
    """
    print("ℹ️ User visited about page")
    return render_template('about.html')

@app.route('/help')
def help_page():
    """
    Help page route - provides usage instructions and examples.
    
    This could include step-by-step tutorials for each cipher.
    """
    print("❓ User visited help page")
    return render_template('help.html')

# =============================================================================
# APPLICATION STARTUP AND CONFIGURATION
# =============================================================================

def print_startup_info():
    """
    Print helpful information when the app starts up.
    This helps with debugging and provides useful information.
    """
    print("=" * 60)
    print("🔐 CRYPTOGRAPHY WEB APP STARTING UP")
    print("=" * 60)
    print("📚 Educational Flask Application for Discrete Mathematics")
    print("🎯 Purpose: Learn cryptographic algorithms through hands-on practice")
    print("")
    print("🌐 Available Routes:")
    print("   📱 Home Page:        http://127.0.0.1:5000/")
    print("   🏛️ Caesar Cipher:    http://127.0.0.1:5000/caesar")
    print("   🔑 Vigenère Cipher:  http://127.0.0.1:5000/vigenere")
    print("   📐 Affine Cipher:    http://127.0.0.1:5000/affine")
    print("   🔒 RSA Cipher:       http://127.0.0.1:5000/rsa")
    print("")
    print("✅ Caesar Cipher: FULLY IMPLEMENTED")
    print("🚧 Other Ciphers: Ready for your implementation!")
    print("")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)

if __name__ == '__main__':
    """
    This block only runs when we execute this file directly (python app.py)
    It won't run if this file is imported by another Python file.
    
    app.run() starts the Flask development server.
    
    Parameters explained:
    - debug=True: Enables debug mode
      * Server restarts automatically when code changes
      * Detailed error messages in browser
      * DON'T use debug=True in production!
    - host='127.0.0.1': Only accept connections from this computer
    - port=5000: Run on port 5000 (default Flask port)
    """
    
    # Print startup information
    print_startup_info()
    
    # Start the Flask development server
    app.run(debug=True, host='127.0.0.1', port=5000)
