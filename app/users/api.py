from typing import Optional
import jwt
import os
from jwt import PyJWKClient
from fastapi import APIRouter, Header
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users")


@router.get("/me")
async def get_current_user(x_pomerium_jwt_assertion: Optional[str] = Header(None)):
    url = os.environ["JWK_ENDPOINT"]
    jwks_client = PyJWKClient(url)
    signing_key = jwks_client.get_signing_key_from_jwt(x_pomerium_jwt_assertion)
    decoded = jwt.decode(
        x_pomerium_jwt_assertion,
        signing_key.key,
        algorithms=["ES256"],
        options={
            "verify_aud": False,
        },
    )
    return decoded
