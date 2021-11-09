from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


from .models import Guild

User = get_user_model()


# =============================================================================


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


# =============================================================================


class GuildChangeForm(forms.ModelForm):
    class Meta:
        model = Guild

        fields = ["name", "avatar"]

    def clean_field(self):
        data = self.cleaned_data["avatar"]

        if not data:
            data = self.instance.avatar

        return data


# =============================================================================


class GuildMembersForm(forms.ModelForm):
    action = forms.ChoiceField(
        choices=(("kick", _("Kick")), ("ban", _("Ban")))
    )

    class Meta:
        model = Guild

        fields = ["members"]

    def clean(self):
        cleaned_data = super().clean()

        members = cleaned_data.get("members", [])

        if self.instance.owner in members:
            self.add_error(
                "members", _("The guild owner cannot kick nor ban.")
            )
