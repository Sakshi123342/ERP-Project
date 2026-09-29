from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from vendor.models import AdminModel

class AdminModelRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminModel
        fields = ['email_id', 'password']

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return AdminModel.objects.create(**validated_data)

class ModulePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminModel
        fields = ['id', 'email_id', 'password']



class AdminModelLoginSerializer(serializers.Serializer):
    email_id = serializers.EmailField(required=True)  # Change to email_id
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email_id = attrs.get('email_id')
        password = attrs.get('password')

        if email_id is None or password is None:
            raise serializers.ValidationError('Both email and password are required.')

        try:
            user = AdminModel.objects.get(email_id=email_id)
            if user.password != password:  # In production, use user.check_password(password)
                raise serializers.ValidationError('Invalid email or password.')
        except AdminModel.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password.')

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
