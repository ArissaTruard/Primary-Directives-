import hashlib

def hash_data(data):
    try:
        data_bytes = data.encode('utf-8')
        hash_object = hashlib.sha256(data_bytes)
        return hash_object.hexdigest()
    except Exception as e:
        print(f"Hashing error: {e}")
        return None
