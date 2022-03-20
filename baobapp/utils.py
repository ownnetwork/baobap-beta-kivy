import json
from io import BytesIO
import qrcode
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage

def get_kivy_image_from_bytes(image_bytes):
    '''Return a Kivy image set from a bytes variable
    '''

    buf = BytesIO(image_bytes)
    cim = CoreImage(buf, ext="png")
    return Image(texture=cim.texture)

def make_base64_qr_code(data: str):
    ''' Return a QRCODE bytes image set from a data variable
    '''
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=4,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()

    return img

def json_items_from_file(filename: str):
    ''' Return items json value from a content file
    '''
    return json.load(open(filename, 'r')).items()
