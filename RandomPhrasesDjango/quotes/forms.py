from django import forms
from .models import Quote
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "source", "weight"]

    def clean_text(self):
        text = self.cleaned_data["text"]
        if Quote.objects.filter(text=text).exists():
            raise forms.ValidationError("Такая цитата уже существует.")
        return text

    def clean_weight(self):
        weight = self.cleaned_data["weight"]
        if weight < 1:
            raise forms.ValidationError("Вес должен быть ≥ 1.")
        return weight

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get("source")
        if source:
            count = Quote.objects.filter(source=source).count()
            if count >= 3:
                raise forms.ValidationError("У одного источника не может быть больше 3 цитат.")
        return cleaned_data


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
