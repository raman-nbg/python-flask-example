from authlib.integrations.flask_oauth2 import ResourceProtector
from authlib.oauth2.rfc9068 import JWTBearerTokenValidator
from authlib.oauth2.rfc9068.claims import JWTAccessTokenClaims
from authlib.jose import jwt
from authlib.jose.errors import DecodeError
import requests

class AzureJWTAccessTokenClaims(JWTAccessTokenClaims):
    def validate_typ(self):
        # The resource server MUST verify that the 'typ' header value is 'at+jwt'
        # or 'application/at+jwt' and reject tokens carrying any other value.

        # But Azure AD does not follow the standard. We have to override the function and check against 'jwt'.
        if self.header['typ'].lower() != 'jwt':
            raise InvalidClaimError('typ')

class AzureJWTValidator(JWTBearerTokenValidator):
    def get_jwks(self):
        # TODO: Add caching
        return requests.get(_jwks_uri).json()

    def validate_request(self, request):
        # always valid
        pass

    def authenticate_token(self, token_string):
        claims_options = {
            'iss': {'essential': True, 'validate': self.validate_iss},
            'exp': {'essential': True},
            'aud': {'essential': True, 'value': self.resource_server},
            'sub': {'essential': False}, # Override default for client_credentials based authentication
            'client_id': {'essential': False}, # Override default as not supported by Azure AD
            'iat': {'essential': True},
            'jti': {'essential': False},
            'auth_time': {'essential': False},
            'acr': {'essential': False},
            'amr': {'essential': False},
            'scope': {'essential': False},
            'groups': {'essential': False},
            'roles': {'essential': False},
            'entitlements': {'essential': False},
        }
        jwks = self.get_jwks()

        # The resource server MUST validate the signature of all incoming JWT access
        # tokens according to [RFC7515] using the algorithm specified in the JWT 'alg'
        # Header Parameter. The resource server MUST reject any JWT in which the value
        # of 'alg' is 'none'. The resource server MUST use the keys provided by the
        # authorization server.
        try:
            return jwt.decode(
                token_string,
                key=jwks,
                claims_cls=AzureJWTAccessTokenClaims,
                claims_options=claims_options,
            )
        except DecodeError:
            raise InvalidTokenError(
                realm=self.realm, extra_attributes=self.extra_attributes
            )

_jwks_uri = "https://login.microsoftonline.com/<azure-tenant-id>/discovery/v2.0/keys"
_issuer = "https://login.microsoftonline.com/<azure-tenant-id>/v2.0"
_audience = "<application-id>"

require_oauth = ResourceProtector()
require_oauth.register_token_validator(
    AzureJWTValidator(
        issuer=_issuer,
        resource_server=_audience,
    )
)
