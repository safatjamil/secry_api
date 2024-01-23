from rest_framework_simplejwt.tokens import RefreshToken

# create tokens manually
def create_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    data = {"tokens":{"refresh": str(refresh),
                      "access": str(refresh.access_token)}}
    return data