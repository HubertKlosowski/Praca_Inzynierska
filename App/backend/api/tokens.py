from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from rest_framework_simplejwt.tokens import RefreshToken


signer = TimestampSigner()

def generate_verification_token(email):
    return signer.sign(email)

def verify_token(token, max_age=3600):
    try:
        email = signer.unsign(token, max_age=max_age)
        return email
    except (BadSignature, SignatureExpired):
        return None

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }