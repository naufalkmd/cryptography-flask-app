# cryptography-flask-app

📚 About This Project
Learning Cryptography Through Code

What is This App?
This is an educational web application built with Flask (Python) to help students learn about cryptographic algorithms in a hands-on, interactive way. It's designed specifically for Discrete Mathematics courses.

Educational Goals:
  1. Understand how classic encryption algorithms work
  2. See the mathematical foundations behind cryptography
  3. Practice implementing algorithms in Python
  4. Learn web development with Flask
  5. Explore the evolution from simple to modern encryption

The Ciphers We Explore
🏛️ Caesar Cipher (Fully Implemented)
  The simplest substitution cipher, used by Julius Caesar. Each letter is shifted by a fixed number of positions. Security: Very weak - can be broken by trying all   25 possible shifts.

🔑 Vigenère Cipher (For You to Implement)
  Uses a keyword to create multiple Caesar ciphers. Much stronger than Caesar cipher. Security: Moderate - can be broken with frequency analysis if the key is short.

📐 Affine Cipher (For You to Implement)
  Uses mathematical functions (ax + b) mod 26. Combines multiplication and addition. Security: Weak to moderate - vulnerable to frequency analysis.

🔒 RSA Cipher (For You to Implement)
  Modern public-key cryptography using prime numbers. Used in real-world security today! Security: Very strong when implemented with large primes.

Technical Implementation
This application is built using:
 1. Backend: Python with Flask framework
 2.  Frontend: HTML5, CSS3 (no JavaScript for simplicity)
 3.  Templating: Jinja2 (built into Flask)
 4.  Styling: Custom CSS with modern design principles
  
Why Flask? 
  Flask is perfect for learning because it's simple, well-documented, and doesn't hide the underlying web concepts. You can see exactly how HTTP requests and responses work.

Learning Path
  1. Start with Caesar Cipher: Understand the basics of substitution ciphers
  2. Implement Vigenère: Learn about polyalphabetic ciphers and keywords
  3. Try Affine Cipher: Explore mathematical functions in cryptography
  4. Challenge with RSA: Dive into modern public-key cryptography
Each cipher builds on concepts from the previous ones, creating a natural learning progression from simple to complex encryption methods.
