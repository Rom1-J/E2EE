from django import forms

from django.utils.translation import gettext as _

from .models import Guild


class GuildChangeForm(forms.Form):
    class Meta:
        model = Guild


class GuildCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["avatar"].label = _("Upload guild avatar")

    class Meta:
        model = Guild

        fields = ["name", "avatar"]
