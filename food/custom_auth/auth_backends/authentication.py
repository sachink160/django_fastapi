from rest_framework.authentication import TokenAuthentication

from food.custom_auth.models import MultiToken


class MultiTokenAuthentication(TokenAuthentication):
    model = MultiToken
