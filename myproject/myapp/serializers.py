from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        
        token['username'] = user.username
        token['is_teamleader'] = user.is_teamleader
        token['is_teammember'] = user.is_teammember
        return token
