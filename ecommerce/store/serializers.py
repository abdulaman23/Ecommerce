from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'phone_number')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ('username', 'email','phone_number','password')


        def create(Self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


    def validate(self, data):
        user = User.objects.filter(username=data['username']).first()

        if user and user.check_password(data['password']):
            return user
        raise serializers.ValidationError("Invalid credentials")
    

class JWTSerializer(serializers.Serializer):

    access = serializers.CharField()
    refresh = serializers.CharField()


    @staticmethod
    def get_tokens_for_user(user):

        refresh = RefreshToken.for_user(user)

        return {

            'refresh': str(refresh),
            'access':str(refresh.access_token),
        }