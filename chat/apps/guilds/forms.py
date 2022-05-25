from typing import List, Optional, Tuple, Union

from django import forms
from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from rich import inspect

from chat.utils.patch_processor import ProcessAction

from .features.channels.models import Category, Channel
from .models import Guild


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


# =============================================================================


class GuildCategoriesForm(forms.ModelForm):
    class Meta:
        model = Category

        fields = ["name"]


# =============================================================================


class GuildChannelsForm(forms.ModelForm):
    class Meta:
        model = Channel

        fields = ["parent", "name", "topic"]


# =============================================================================
# Custom forms
# =============================================================================


def move_row(request: ASGIRequest, data: dict) -> Optional[Tuple[bool, dict]]:
    row: Union[Category, Channel] = data["values"]["row"]
    guild: Guild = data["values"]["guild"]
    direction: str = data["values"]["direction"]

    if isinstance(row, Category):
        if (direction == "up" and row.position == 1) or (
            direction == "down" and row.position == guild.categories.count()
        ):
            return True, {
                "data": {
                    "success": True,
                    "message": "Nothing to move, row already at extremum.",
                },
                "status": 200,
            }

        row.position += 1 if direction == "down" else -1
        old_row = Category.objects.filter(
            guild=guild, position=row.position
        ).first()
        old_row.position -= 1 if direction == "down" else -1  # type: ignore

        row.save()
        old_row.save()  # type: ignore

    if isinstance(row, Channel):
        if (direction == "up" and row.position == 1) or (
            direction == "down" and row.position == row.parent.channels_count()
        ):
            return True, {
                "data": {
                    "success": True,
                    "message": "Nothing to move, row already at extremum.",
                },
                "status": 200,
            }

        row.position += 1 if direction == "down" else -1
        old_row = Channel.objects.filter(
            guild=guild, position=row.position
        ).first()
        old_row.position -= 1 if direction == "down" else -1  # type: ignore

        row.save()
        old_row.save()  # type: ignore

    return True, {
        "data": {"success": True, "message": "Row moved."},
        "status": 200,
    }


# =============================================================================


def move_row_check_guild(
    request: ASGIRequest, data: dict
) -> Optional[Tuple[bool, dict]]:
    values = data.get("values", {})

    if "guild" not in values:
        return False, {
            "data": {
                "success": False,
                "message": "Missing field guild.",
            },
            "status": 400,
        }

    return True, {}


# =============================================================================


def move_row_check_row_id(
    request: ASGIRequest, data: dict
) -> Optional[Tuple[bool, dict]]:
    values = data.get("values", {})

    if "row_id" not in values:
        return False, {
            "data": {
                "success": False,
                "message": "Missing field row_id.",
            },
            "status": 400,
        }

    return True, {}


# =============================================================================


def move_row_check_direction(
    request: ASGIRequest, data: dict
) -> Optional[Tuple[bool, dict]]:
    values = data.get("values", {})

    if "direction" not in values:
        return False, {
            "data": {
                "success": False,
                "message": "Missing field direction.",
            },
            "status": 400,
        }

    return True, {}


# =============================================================================


def move_row_check_existing_row(
    request: ASGIRequest, data: dict
) -> Optional[Tuple[bool, dict]]:
    values = data.get("values", {})
    row: Optional[Union[Category, Channel]]

    if not (
        (
            row := Category.objects.filter(
                id=values.get("row_id"), guild=data["values"]["guild"]
            ).first()
        )
        or (
            row := Channel.objects.filter(
                id=values.get("row_id"), guild=data["values"]["guild"]
            ).first()
        )
    ):
        return False, {
            "data": {
                "success": False,
                "message": "Category or channel unknown.",
            },
            "status": 400,
        }

    return True, {"row": row}


# =============================================================================


move_row_actions = [move_row]
move_row_checks = [
    move_row_check_guild,
    move_row_check_row_id,
    move_row_check_direction,
    move_row_check_existing_row,
]


class GuildSettingsChannelsProcessAction:
    process = (
        ProcessAction()
        .add_actions("move_row", *move_row_actions)
        .add_checks("move_row", *move_row_checks)
    )

    def __init__(self, request: ASGIRequest, guild: Guild):
        self.process.process(request, guild=guild)

    def response(self) -> JsonResponse:
        return self.process.response()
