import email
from weakref import ref
from rest_framework_simplejwt.tokens import RefreshToken

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['username'] = user.username
    refresh['email'] = user.email
    try:
        role = user.customer
        role = 'Customer' 
    except Exception as e:
                resp = {
                    "message": str(e)
                }

    refresh['role'] = role
    return{
        'refresh' : str(refresh),
        'access' : str(refresh.access_token),

    }