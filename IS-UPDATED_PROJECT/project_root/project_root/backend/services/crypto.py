# professional_file_security.py
import os
import logging
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes, hmac

# ----------------------- CONFIG -----------------------
KEY_FOLDER = "keys"
LOG_FILE = "file_security.log"
os.makedirs(KEY_FOLDER, exist_ok=True)

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ------------------- KEY GENERATION -------------------
def generate_keys(password: bytes = None):
    """Generate RSA public/private keys, optionally encrypt private key with password."""
    priv_key_path = os.path.join(KEY_FOLDER, "private.pem")
    pub_key_path = os.path.join(KEY_FOLDER, "public.pem")
    
    if os.path.exists(priv_key_path) and os.path.exists(pub_key_path):
        logging.info("Keys already exist.")
        return
    
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    
    # Private key serialization
    enc_algo = (serialization.BestAvailableEncryption(password) if password 
                else serialization.NoEncryption())
    
    with open(priv_key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=enc_algo
        ))
    
    # Public key serialization
    with open(pub_key_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    
    logging.info("RSA key pair generated.")

# ------------------- FILE ENCRYPTION -------------------
def encrypt_file(file_path: str) -> str:
    """Encrypt a file using AES-GCM + RSA key encapsulation + HMAC."""
    # Read original file
    with open(file_path, "rb") as f:
        data = f.read()
    
    # Generate AES session key
    aes_key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(aes_key)
    nonce = os.urandom(12)
    
    # Encrypt file data
    encrypted_data = aesgcm.encrypt(nonce, data, None)
    
    # HMAC for integrity
    h = hmac.HMAC(aes_key, hashes.SHA256())
    h.update(encrypted_data)
    h_tag = h.finalize()
    
    # Encrypt AES key with RSA public key
    with open(os.path.join(KEY_FOLDER, "public.pem"), "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    enc_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # Combine everything: nonce + encrypted AES key + HMAC + encrypted file
    out_path = file_path + ".enc"
    with open(out_path, "wb") as f:
        f.write(nonce + enc_key + h_tag + encrypted_data)
    
    logging.info(f"File encrypted: {file_path} -> {out_path}")
    return out_path

# ------------------- FILE DECRYPTION -------------------
def decrypt_file(enc_path: str, password: bytes = None) -> str:
    """Decrypt a file encrypted by encrypt_file."""
    with open(enc_path, "rb") as f:
        content = f.read()
    
    nonce = content[:12]
    enc_key = content[12:12+256]  # RSA 2048 bits = 256 bytes
    h_tag = content[12+256:12+256+32]  # SHA256 HMAC size
    encrypted_data = content[12+256+32:]
    
    # Load private key
    with open(os.path.join(KEY_FOLDER, "private.pem"), "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=password)
    
    # Decrypt AES key
    aes_key = private_key.decrypt(
        enc_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # Verify HMAC
    h = hmac.HMAC(aes_key, hashes.SHA256())
    h.update(encrypted_data)
    h.verify(h_tag)  # Will raise InvalidSignature if tampered
    
    # Decrypt file
    aesgcm = AESGCM(aes_key)
    decrypted = aesgcm.decrypt(nonce, encrypted_data, None)
    
    out_path = enc_path.replace(".enc", ".dec")
    with open(out_path, "wb") as f:
        f.write(decrypted)
    
    logging.info(f"File decrypted: {enc_path} -> {out_path}")
    return out_path

# ------------------- EXAMPLE USAGE -------------------
if __name__ == "__main__":
    # Optional password for private key
    password = b"supersecret"  # None if you don't want encryption
    
    # Generate keys (only once)
    generate_keys(password)
    
    # Encrypt a file
    encrypted_file = encrypt_file("example.txt")
    
    # Decrypt the file
    decrypted_file = decrypt_file(encrypted_file, password)
