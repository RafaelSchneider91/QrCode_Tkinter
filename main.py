import qrcode
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from  qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styledpil import StyledPilImage

from PIL import Image, ImageDraw, ImageFont

estacoes = ['221-0160','221-0161','221-0700']

laranja = (235, 105, 11)
verde = (0, 89, 36)

pos_x = 21
pos_y = 35

fontsize = 50  # starting font size
font = ImageFont.truetype("arial.ttf", fontsize)
im2 = Image.open('moldura.png')

iteracao = 0



# estilo dos cantos 
def style_eyes(img):
  img_size = img.size[0]
  mask = Image.new('L', img.size, 1)
  draw = ImageDraw.Draw(mask)
  draw.rectangle((45, 45, 90, 90), fill=255)
  draw.rectangle((img_size-45, 45, img_size-90, 90), fill=255)
  draw.rectangle((45, img_size-45, 90, img_size-90), fill=255)
  return mask

# cria o QrCode
def criar_qr(estacao):
    qr = qrcode.QRCode(
        version=1,
        box_size=12,
        border=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H
        )
    qr.add_data(estacao)
    qr_eyes_img = qr.make_image(image_factory=StyledPilImage,
                                eye_drawer=RoundedModuleDrawer(radius_ratio=1.5),
                                color_mask=SolidFillColorMask(front_color=laranja))

    qr_img = qr.make_image(image_factory=StyledPilImage,
                        eye_drawer=RoundedModuleDrawer(radius_ratio=1.5),
                        color_mask=SolidFillColorMask(front_color=verde),
                        embeded_image_path="oee_logo.jpg"
                            )

    mask = style_eyes(qr_img)
    
    final_img = Image.composite(qr_eyes_img, qr_img, mask)

    return final_img

def criar_moldura(estacao, mold):
    draw = ImageDraw.Draw(mold)
    draw.text((80, 343), estacao, font=font) 

    return mold

for estacao in estacoes:
    final_img = criar_qr(estacao)
    
    im2 = Image.open('moldura.png')
    mold = criar_moldura(estacao, im2)

    Image.Image.paste(mold, final_img, (pos_y, pos_x))
    mold.save(f'oee_faltantes/qr_code_{estacao}.png')
    iteracao = iteracao + 1
    print(f"Iteracao {iteracao}")
