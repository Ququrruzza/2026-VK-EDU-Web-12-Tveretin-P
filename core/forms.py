from django import forms
from django.contrib import auth
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

from .models import Profile

AVATAR_EXTENSIONS = (".jpg", ".jpeg", ".png")
AVATAR_MAX_SIZE = 2 * 1024 * 1024


def validate_avatar(avatar):
    # проверяем только новый загруженный файл, а не уже сохранённый
    if not isinstance(avatar, UploadedFile):
        return avatar
    if not avatar.name.lower().endswith(AVATAR_EXTENSIONS):
        raise ValidationError("Можно загрузить только JPG или PNG.")
    if avatar.size > AVATAR_MAX_SIZE:
        raise ValidationError("Файл слишком большой, максимум 2 МБ.")
    return avatar


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class LoginForm(BootstrapFormMixin, forms.Form):
    username = forms.CharField(label="Login", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        self.user = auth.authenticate(username=cleaned_data.get("username"), password=cleaned_data.get("password"))
        if self.user is None:
            raise ValidationError("Неверный логин или пароль.")
        return cleaned_data


class SignupForm(BootstrapFormMixin, forms.ModelForm):
    email = forms.EmailField(label="Email")
    nickname = forms.CharField(label="Nickname", max_length=30, help_text="This name will be shown to other users.")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Repeat password", widget=forms.PasswordInput)
    avatar = forms.ImageField(label="Avatar", required=False, help_text="JPG or PNG, up to 2 MB. Optional.")

    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {"username": "Login"}
        help_texts = {"username": "Latin letters, digits and @/./+/-/_ only."}

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

    def clean_avatar(self):
        return validate_avatar(self.cleaned_data.get("avatar"))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        if password and password != cleaned_data.get("password_repeat"):
            self.add_error("password_repeat", "Пароли не совпадают.")
        if password:
            user = User(username=cleaned_data.get("username"), email=cleaned_data.get("email"))
            try:
                password_validation.validate_password(password, user)
            except ValidationError as error:
                self.add_error("password", error)
        return cleaned_data

    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.save()
        Profile.objects.create(
            user=user,
            nickname=self.cleaned_data["nickname"],
            avatar=self.cleaned_data.get("avatar"),
        )
        return user


class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = Profile
        fields = ["nickname", "avatar"]
        labels = {"nickname": "Nickname", "avatar": "Avatar"}
        help_texts = {"nickname": "Up to 30 characters.", "avatar": "JPG or PNG, up to 2 MB."}
        widgets = {"avatar": forms.FileInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].initial = self.instance.user.email

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exclude(id=self.instance.user_id).exists():
            raise ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

    def clean_avatar(self):
        return validate_avatar(self.cleaned_data.get("avatar"))

    def save(self):
        profile = super().save()
        profile.user.email = self.cleaned_data["email"]
        profile.user.save(update_fields=["email"])
        return profile
