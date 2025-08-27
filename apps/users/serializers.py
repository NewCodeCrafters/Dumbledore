from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate

from apps.base.choices import UserTypeChoices
from apps.base.account_utils import complete_password_reset, email_validator, get_tokens_for_user, initiate_password_reset, send_otp_email, set_user_otp

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    
    class Meta:
        model = User
        fields = (
            "id", "email", "first_name", "last_name", "is_active", "status", "user_type"
        )
        read_only_fields = ("id", "is_active", "status", "user_type")
        
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ["meta"]
        
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input": "password"})
    confirm_password = serializers.CharField(write_only=True, style={"input": "password"})
    
    class Meta:
        model = User
        fields = (
            "email", "first_name", "last_name", "password", "confirm_password"
        )
        extra_kwargs = {"user_type": {"default": UserTypeChoices.USER}}
        

    def validate_email(self, value):
        if not email_validator(value):
            raise serializers.ValidationError("Invalid email format.")
        
        return value.lower()
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        if data['password'] < 8:
            raise serializers.ValidationError("Passwords must be atleast 8 characters.")
        
        return data
        
    def create(self, validated_data):
        validated_data.pop("password_confirm", None)
        user = User.objects.create_user(
            email=validated_data.pop('email'),
            password=validated_data.pop('password'),
            **validated_data
        )
        otp = set_user_otp(user)
        send_otp_email(user.id, otp, "email verification")
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "user_type")
        read_only_fields = ("email", "user_type")
        
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, style={"input": "password"})
    new_password = serializers.CharField(write_only=True, style={"input": "password"})
    confirm_password = serializers.CharField(write_only=True, style={"input": "password"})
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        if len(data['new_password']) < 8:
            raise serializers.ValidationError("Passwords must be at least 8 characters.")
        
        return data
    
    def save(self, user):
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password'])
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input": "password"})
    
    def validate_email(self, value):
        if not email_validator(value):
            raise serializers.ValidationError("Invalid email format.")
        return value.lower()
    
    def validate(self, data):
        email = data.get('email', "")
        password = data.get('password', "")
        
        email = email.lower().strip()
        
        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            try:
                user_obj = User.objects.get(email=email)
                if not user_obj.is_active:
                    raise serializers.ValidationError({"detail": "User account is inactive."})
                raise serializers.ValidationError({"detail": "Invalid credentials."})
            except User.DoesNotExist:
                raise serializers.ValidationError({"detail": "Invalid Credentials."})

        if user.status == UserTypeChoices.PENDING:
            raise serializers.ValidationError({"detail": "User account is pending approval."})
        if user.status == UserTypeChoices.DELETED:
            raise serializers.ValidationError({"detail": "User account has been deleted."})
        if user.status == UserTypeChoices.BLOCKED or user.status == UserTypeChoices.SUSPENDED:
            raise serializers.ValidationError({"detail": "User account is blocked or suspended."})
        
        tokens = get_tokens_for_user(user)
        return {
            "user": user,
            "tokens": tokens
        }
        
class OTPVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField(write_only=True, max_length=6)
    
    def validate_otp(self, value):
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("OTP must be a 6-digit number.")
        return value
    
    def validate(self, data):
        otp = data.get('otp')
        user = self.context.get('user')
        
        if not user or not user.otp or user.otp != otp:
            raise serializers.ValidationError({"detail": "Invalid or expired OTP."})
        
        if user.otp_verified:
            raise serializers.ValidationError({"detail": "OTP already verified."})
        
        return data
    

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        if not email_validator(value):
            raise serializers.ValidationError("Invalid email format.")
        return value.lower()
    
    def save(self):
        email = self.validated_data['email']
        initiate_password_reset(email)
        return {
            "message": "If an account with this email exists, a password reset link has been sent."
        }
        

class PasswordResetCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(write_only=True, max_length=6)
    new_password = serializers.CharField(write_only=True, style={"input": "password"})
    confirm_password = serializers.CharField(write_only=True, style={"input": "password"})
    
    def validate_email(self, value):
        if not email_validator(value):
            raise serializers.ValidationError("Invalid email format.")
        return value.lower()
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        if len(data['new_password']) < 8:
            raise serializers.ValidationError("Passwords must be at least 8 characters.")
        
        return data
    
    def save(self):
        email = self.validated_data['email']
        otp = self.validated_data['otp']
        new_password = self.validated_data['new_password']
        
        sucesss = complete_password_reset(email, otp, new_password)
        
        if not sucesss:
            raise serializers.ValidationError(
                {"detail": "Password reset failed. Invalid OTP or user not found."}
                )
        
        return {
            "message": "Password reset successful. You can now log in with your new password."
        }
        