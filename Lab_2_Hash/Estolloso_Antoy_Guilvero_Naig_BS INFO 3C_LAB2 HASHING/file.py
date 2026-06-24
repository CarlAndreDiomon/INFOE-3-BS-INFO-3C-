# 1st cell - Hash
# Run this one to generate the hash - you'll need it for the next cell

import hashlib

filename = 'database.csv' 

def get_file_hash(path):
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Generate and print the result
try:
    print(f"File: {filename}")
    print(f"SHA-256 Hash: {get_file_hash(filename)}") # Copy this hash!
    print("-" * 30)
except FileNotFoundError:
    print(f"Error: '{filename}' not found.")

# 2nd cell
# This will be the auditor, checking the integrity of the file

import hashlib
import os

# STEP 1: The 'Protection Profile' 
# Paste the hash string generated from Cell 1 inside the quotes below.
EXPECTED_HASH = "b5f70fd62d79dce2fb259bbd1602a7f64ef513685ffae8969d92c8178932d582"
filename = 'database.csv'

def run_integrity_audit():
    # A. THE AVAILABILITY CHECK
    if not os.path.exists(filename):
        print(f"CRITICAL ALERT: '{filename}' is missing! Availability check failed.")
        return

    # B. THE FINGERPRINTING
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
            
    current_hash = sha256_hash.hexdigest()
    
    # C. THE TECHNICAL CONTROL
    if current_hash == EXPECTED_HASH:
        print("SUCCESS: Integrity verified. The file has not been modified.")
    else:
        print("CRITICAL ALERT: Integrity check failed! Unauthorized modification detected.")
        print(f"-> Expected Hash: {EXPECTED_HASH}")
        print(f"-> Current Hash:  {current_hash}")

# Run the function
run_integrity_audit()