from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils.translation import gettext as _, gettext_lazy as __
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    default_error_messages = {
        'no_account': __('No account found with the given username'),
        'wrong_password': __('Invalid password.')
    }

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    @classmethod
    def authentication_rule(cls, user):
        return True if user is not None and user.is_active else False

    def authenticate(self, attrs):
        authenticate_kwargs = {
            'email': attrs.get('email'),
            'password': attrs.get('password'),
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        exists_account = User.objects.filter(email=authenticate_kwargs['email']).exists()
        if not exists_account:
            raise exceptions.AuthenticationFailed(
                {'username': self.error_messages['no_account']},
                'no_account'
            )

        user = authenticate(**authenticate_kwargs)

        if not self.authentication_rule(user):
            raise exceptions.AuthenticationFailed(
                {'password': self.error_messages['wrong_password']},
                'wrong_password',
            )

        return user

    def validate(self, attrs):
        user = self.authenticate(attrs)
        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(validators=[validate_password])
    password1 = serializers.CharField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise exceptions.ValidationError(_('User with this email already exists'))
        return value

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        errors = {}

        if not first_name:
            errors['first_name'] = [_('first_name is required!')]

        if not last_name:
            errors['last_name'] = [_('last_name is required!')]

        password = attrs.get('password')
        password1 = attrs.get('password1')

        if password != password1:
            errors['password'] = [_('Passwords didn\'t match')]

        if len(errors.keys()) > 0:
            raise exceptions.ValidationError(errors)
        return attrs

    def update(self, instance, validated_data):
        raise NotImplementedError(_('`UserCreateSerializer` didn\'t update instance'))

    def create(self, validated_data):
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        user = User(email=email, username=email, last_name=last_name, first_name=first_name)
        user.set_password(validated_data.get('password1'))
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'date_joined',
            'avatar',
        )
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
            'date_joined': {
                'read_only': True
            }
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField()
    password1 = serializers.CharField()

    def validate_old_password(self, value):
        if not self.instance:
            raise exceptions.ValidationError(_('`ChangePasswordSerializer` should contain instance to update'))

        if not self.instance.check_password(value):
            raise exceptions.ValidationError(_('Actual password is incorrect'))

        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password1 = attrs.get('password1')

        if not (password and password1 and password == password1):
            raise exceptions.ValidationError({
                'password': [_('Passwords didn\'t match')]
            })

        validate_password(password1)
        return attrs

    def update(self, instance: User, validated_data):
        instance.set_password(validated_data.get('password1'))
        instance.save()
        return instance

    def create(self, validated_data):
        raise NotImplementedError(_('`ChangePasswordSerializer` cannot create an instance'))


class UploadAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar',)

    def create(self, validated_data):
        raise NotImplementedError('This serializer cannot create instance')

