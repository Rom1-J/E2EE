from django import forms

from .models import Guild


class GuildChangeForm(forms.Form):
    class Meta:
        model = Guild


class GuildCreationForm(forms.ModelForm):
    class Meta:
        model = Guild

        fields = ["name", "avatar"]

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.owner = self._user

        if commit:
            instance.save()
            self.save_m2m()

        return instance
