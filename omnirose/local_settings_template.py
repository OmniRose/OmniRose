# Local settings

SECRET_KEY = 'something_secure'

DEBUG=True

# https://dashboard.stripe.com/account/apikeys
STRIPE_SECRET_KEY = "sk_test_insert_real_token_here"
STRIPE_PUBLIC_KEY = "pk_test_insert_real_token_here"

GOOGLE_ANALYTICS_TRACKING_CODE = 'UA-yours'

# Create an account on postmark and then set these values. If just developing
# leave POSTMARK_TEST_MODE = True and you don't need to change values.
POSTMARK_TEST_MODE   = True
POSTMARK_API_KEY     = 'your-key-not-needed-when-in-test-mode'
