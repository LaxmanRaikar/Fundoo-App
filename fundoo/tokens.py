from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

# PasswordResetTokenGenerator create a token that will be used for account verification \
# that will be send by email


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


