import base64
from io import BytesIO

import qrcode
from django import template

from chat.apps.guilds.features.invites.models import Invite

register = template.Library()


@register.filter
def generate_qr_code(invite: Invite):
    url = "https://c3e.gnous.eu" + invite.key_url()

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    return f"data:image/png;base64,{img_str.decode()}"
