import hashlib
import hmac

class InvalidSignatureError(Exception):
    pass

def validate_signature(channel_secret, signature, body):
    # Generate the expected signature using the channel secret and request body
    expected_signature = generate_signature(channel_secret, body)

    # Compare the expected signature with the received signature
    if signature != expected_signature:
        raise InvalidSignatureError('Invalid signature')

def generate_signature(channel_secret, body):
    channel_secret = channel_secret.encode('utf-8')
    body = body.encode('utf-8')

    # Use HMAC-SHA256 to generate the signature
    signature = hmac.new(channel_secret, body, hashlib.sha256).digest()
    signature = base64.b64encode(signature).decode('utf-8')

    return signature
