from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageFont
import qrcode
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from  qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styledpil import StyledPilImage
import base64
import io
import re

app = Tk()
#Titulo Janela
app.title("QRCode OEE")
# Cria um objeto de estilo ttk
estilo = ttk.Style()

img_base64_moldura = "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"

app.resizable(width=1, height=1)

largura_janela = 500
altura_janela = 400

largura_tela = app.winfo_screenwidth()
altura_tela = app.winfo_screenheight()

posicao_x = int(largura_tela/2 - largura_janela/2)
posicao_y = int(altura_tela/2 - altura_janela/2)

app.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")

app.wm_maxsize(500, 400)
app.wm_maxsize(500, 400)

img_fundo_base64 = "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"

# image_fundo.show()
img_fundo = PhotoImage(data=base64.b64decode(img_fundo_base64))
# img_btn_executar = PhotoImage(file="btn_executar.png")

label_fundo = Label(app, image=img_fundo)
label_fundo.pack()

listaestacoes = []

vnovoestacao = Entry(app, bd=2, justify=CENTER)
vnovoestacao.place(width=100
                   , height=25
                   , x=325
                   , y=15)

def addestacao():
    
    validar = vnovoestacao.get()
    padrao = re.compile(r"^\d{3}-\d{4}$")
    if padrao.match(validar):
        lb_estacoes.insert(END, vnovoestacao.get())
        listaestacoes.append(vnovoestacao.get())
        print("O número de centro trabalho é válido.")
    else:
        messagebox.showerror(title="Erro", message="O formato digitado é invalido! Exemplo:'123-1234'")
        print("O número de centro trabalho é inválido.")
 

btn_estacoes = Button(app, text="Incluir Estação", command=addestacao)
# btn_estacoes.pack()

btn_estacoes.place(width=100
                   , height=25
                   , x=325
                   , y=45)

lb_estacoes = Listbox(app, bd=2, justify=CENTER )


# scrollbar = Scrollbar(app)
# scrollbar.pack(side = RIGHT, fill = BOTH) 

for estacao in listaestacoes:
    lb_estacoes.insert(END, estacao)

# lb_estacoes.pack()

lb_estacoes.place(width=100
                   , height=170
                   , x=325
                   , y=80)



# lb_estacoes.config(yscrollcommand=scrollbar.set)
# scrollbar.config(command = lb_estacoes.yview)


def delestacao():
    try:
        indice = lb_estacoes.curselection()[0]
        lb_estacoes.delete(indice)
        listaestacoes.clear()
        
    except:
        messagebox.showerror(title="Erro", message="Selecione um centro de trabalho!")

def limparestacoes():
    lb_estacoes.delete(0, END)
    listaestacoes.clear()
    
btn_estacoes = Button(app, bd=2, text="Deletar Estação", command=delestacao)
btn_estacoes.place(width=100
                   , height=25
                   , x=325
                   , y=260)


# btn_estacoes.pack()

btn_estacoes = Button(app, text="Limpar Tudo", command=limparestacoes)
btn_estacoes.place(width=100
                   , height=25
                   , x=325
                   , y=290)

# cria o QRCode

laranja = (235, 105, 11)
verde = (0, 89, 36)

pos_x = 21
pos_y = 35

fontsize = 50  # starting font size
font = ImageFont.truetype("arial.ttf", fontsize)

# im2 = PhotoImage(data=base64.b64decode(img_base64_moldura))
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

    img_base64_oeelogo = "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"
    # decodificar a string base64
    image_data = base64.b64decode(img_base64_oeelogo)

    # criar um objeto BytesIO com os dados da imagem decodificada
    image_stream = io.BytesIO(image_data)
        
    qr_img = qr.make_image(image_factory=StyledPilImage,
                        eye_drawer=RoundedModuleDrawer(radius_ratio=1.5),
                        color_mask=SolidFillColorMask(front_color=verde),
                        embeded_image_path=image_stream
                            )

    mask = style_eyes(qr_img)
    
    final_img = Image.composite(qr_eyes_img, qr_img, mask)

    return final_img

def criar_moldura(estacao, mold):
    draw = ImageDraw.Draw(mold)
    draw.text((80, 343), estacao, font=font) 

    return mold


def executar():
    # Abre um diálogo de diretório
    diretorio = filedialog.askdirectory()

    # print(diretorio)

    iteracao = 0
    if len(listaestacoes) > 0:
        for estacao in listaestacoes:
            final_img = criar_qr(estacao)
            # local_arquivo_salvo = diretorio

            # decodificar a string base64
            image_data = base64.b64decode(img_base64_moldura)

            # criar um objeto BytesIO com os dados da imagem decodificada
            image_stream = io.BytesIO(image_data)

            # abrir a imagem com o método Image.open()
            image = Image.open(image_stream)

            # im2 = PhotoImage(data=base64.b64decode(img_base64_moldura))
            mold = criar_moldura(estacao, image)

            Image.Image.paste(mold, final_img, (pos_y, pos_x))
            mold.save(f'{diretorio}\qr_code_{estacao}.png')
            iteracao = iteracao + 1

            percentual = int((iteracao/len(listaestacoes))*100)
            # print(percentual)
            varBarra.set(percentual)
            app.update()


        messagebox.showinfo(title="Concluido", message=f"Total de arquivos gerados: {iteracao}")
        # messagebox.showinfo(title="Informação", message=f"Salvo em: {local_arquivo_salvo}")

    else:
        messagebox.showwarning(title="Atenção", message="Nenhum evento criado, adicione os centros de trabalho!")
    

# img_btn_executar = PhotoImage(file="btn_executar.png")
# btn_executar = Button(app, bd=2, image=img_btn_executar, command=lambda: valBarra(100000))
btn_executar = Button(app, bd=2, text="Executar", font=('arial', 18), command=executar)

btn_executar.place(width=150
                   , height=40
                   , x=300
                   , y=320)

varBarra=DoubleVar()
varBarra.set(0)

progress = ttk.Progressbar(app, orient="horizontal", variable=varBarra, maximum=100)
progress.place(width=150
                   , height=25
                   , x=300
                   , y=370)

app.mainloop()