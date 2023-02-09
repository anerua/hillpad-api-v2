from rest_framework import serializers

from account.models import User


class RegisterAccountSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=255, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
        )

    def create(self, validated_data):
        validated_data["role"] = User.CLIENT
        return User.objects.create_user(**validated_data)


class RegisterStaffAccountSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=255, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
        )

    def create(self, validated_data):
        validated_data["role"] = User.STAFF
        return User.objects.create_user(**validated_data)


class DetailAccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "gender",
            "date_of_birth",
            "nationality",
            "country_of_residence",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "email": {"read_only": True},
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "role": {"read_only": True},
            "gender": {"read_only": True},
            "date_of_birth": {"read_only": True},
            "nationality": {"read_only": True},
            "country_of_residence": {"read_only": True},
        }


class UpdateAccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "nationality",
            "country_of_residence",
        )
        extra_kwargs = {
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "gender": {"read_only": True},
            "date_of_birth": {"read_only": True},
            "nationality": {"read_only": True},
            "country_of_residence": {"read_only": True},
        }


class ListStaffAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name", 
            "is_active",
            "created_at",
        )
        extra_kwargs = {
            'email': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'is_active': {'write_only': True},
            'created_at': {'write_only': True},
        }


class RetrieveStaffAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'