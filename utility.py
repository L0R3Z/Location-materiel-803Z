import hashlib

salt = "803z" # Salt value is used to make the hash more secure

# Encrypt a password
def encrypt_password(passwd):
    combined = passwd + salt
    hashed_passwd = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    return hashed_passwd

# Check if the provided password matches the hashed password contained in the database
def check_password(passwd, hashed_passwd):
    correct_hash = encrypt_password(passwd)
    if(correct_hash == hashed_passwd):
        print("The password is correct!")
        return 1
    else:
        print("The password is invalid...")
        return 0