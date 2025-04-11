# webauthn_utils.py
import os
import json
import base64
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
    options_to_json,
)
from webauthn.helpers.cose import COSEAlgorithmIdentifier
from webauthn.helpers.structs import (
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialParameters,
    AuthenticatorSelectionCriteria,
    UserVerificationRequirement,
    ResidentKeyRequirement,
    AttestationConveyancePreference,
)
from django.conf import settings
from django.core.cache import cache

# Replace with your application's domain
RP_ID = 'localhost'  # For development
RP_NAME = 'University Lecturer Portal'


def get_origin(request):
    # In production, this should be properly configured
    return f"http://{RP_ID}:8000"


def generate_challenge():
    """Generate a random challenge for WebAuthn operations"""
    challenge = os.urandom(32)
    return challenge


def store_challenge_for_user(user_id, challenge):
    """Store challenge in cache for later verification"""
    cache_key = f"webauthn_challenge_{user_id}"
    cache.set(cache_key, challenge, timeout=300)  # 5 minutes expiry


def get_challenge_for_user(user_id):
    """Retrieve stored challenge for verification"""
    cache_key = f"webauthn_challenge_{user_id}"
    challenge = cache.get(cache_key)
    cache.delete(cache_key)  # Remove after retrieving
    return challenge


# Utility functions to convert between bytes and base64url
def bytes_to_base64url(bytes_value):
    """Convert bytes to base64url encoding"""
    return base64.urlsafe_b64encode(bytes_value).rstrip(b'=').decode('utf-8')


def base64url_to_bytes(base64url_value):
    """Convert base64url encoding to bytes"""
    if isinstance(base64url_value, str):
        base64url_value = base64url_value.encode('utf-8')
    # Add padding if necessary
    padding = b'=' * (4 - (len(base64url_value) % 4))
    return base64.urlsafe_b64decode(base64url_value + padding)


def prepare_registration_options(lecturer):
    """Generate registration options for the lecturer"""
    challenge = generate_challenge()

    # Store the challenge for later verification
    store_challenge_for_user(lecturer.id, challenge)

    # Get existing credentials to exclude
    existing_credentials = lecturer.credentials.all()
    exclude_credentials = []

    for cred in existing_credentials:
        exclude_credentials.append(
            PublicKeyCredentialDescriptor(id=cred.credential_id)
        )

    # Generate registration options
    options = generate_registration_options(
        rp_id=RP_ID,
        rp_name=RP_NAME,
        user_id=str(lecturer.id).encode(),
        user_name=lecturer.email,
        user_display_name=lecturer.display_name,
        challenge=challenge,
        exclude_credentials=exclude_credentials,
        authenticator_selection=AuthenticatorSelectionCriteria(
            user_verification=UserVerificationRequirement.PREFERRED,
            resident_key=ResidentKeyRequirement.PREFERRED,
        ),
        attestation=AttestationConveyancePreference.NONE,
        supported_pub_key_algs=[
            COSEAlgorithmIdentifier.ECDSA_SHA_256,
            COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
        ],
    )

    return options_to_json(options), challenge


# Update the store and retrieve functions in webauthn_utils.py
def store_credential(credential_id, public_key):
    """Convert binary credential_id to string before storing"""
    credential_id_str = bytes_to_base64url(credential_id)
    return credential_id_str, public_key

def retrieve_credential(credential_id_str):
    """Convert string back to binary credential_id"""
    credential_id = base64url_to_bytes(credential_id_str)
    return credential_id