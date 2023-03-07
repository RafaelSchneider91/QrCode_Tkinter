from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image, ImageDraw, ImageFont
import qrcode
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from  qrcode.image.styles.colormasks import SolidFillColorMask
from qrcode.image.styledpil import StyledPilImage


app = Tk()



# Cria um objeto de estilo ttk
estilo = ttk.Style()

# Configura as cores do tema personalizado
estilo.configure('TButton', 
                 background='#EE6611'
                #  foreground='#444242'
                 )

app.title("Cria QRCode OEE")
app.iconbitmap(default="imagens\\icone.ico")
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

img_fundo = PhotoImage(file="imagens\\background.png")
img_btn_executar = PhotoImage(file="imagens\\btn_executar.png")

label_fundo = Label(app, image=img_fundo)
label_fundo.pack()

listaestacoes = []

vnovoestacao = Entry(app, bd=2, justify=CENTER)
vnovoestacao.place(width=100
                   , height=25
                   , x=325
                   , y=15)

def addestacao():
        
    if len(vnovoestacao.get()) == 8 and vnovoestacao.get() not in listaestacoes:
        lb_estacoes.insert(END, vnovoestacao.get())
        listaestacoes.append(vnovoestacao.get())
        print(listaestacoes)
    elif len(vnovoestacao.get()) == 8 and vnovoestacao.get() in listaestacoes:
        messagebox.showerror(title="Erro", message="O centro de trabalho ja foi adicionado!")
    else:
        messagebox.showerror(title="Erro", message="Adicionar um centro de trabalho com 8 caracteres!")
 

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
im2 = Image.open('imagens/moldura.png')

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
                        embeded_image_path="imagens/oee_logo.jpg"
                            )

    mask = style_eyes(qr_img)
    
    final_img = Image.composite(qr_eyes_img, qr_img, mask)

    return final_img

def criar_moldura(estacao, mold):
    draw = ImageDraw.Draw(mold)
    draw.text((80, 343), estacao, font=font) 

    return mold


def executar():
    iteracao = 0
    if len(listaestacoes) > 0:
        for estacao in listaestacoes:
            final_img = criar_qr(estacao)
            local_arquivo_salvo = "C:/Users/Public/Downloads"
            im2 = Image.open('imagens/moldura.png')
            mold = criar_moldura(estacao, im2)

            Image.Image.paste(mold, final_img, (pos_y, pos_x))
            mold.save(f'{local_arquivo_salvo}/qr_code_{estacao}.png')
            iteracao = iteracao + 1

            percentual = int((iteracao/len(listaestacoes))*100)
            # print(percentual)
            varBarra.set(percentual)
            app.update()

        messagebox.showinfo(title="Iteração", message=f"Total de arquivos gerados: {iteracao}")
        messagebox.showinfo(title="Informação", message=f"Salvo em: {local_arquivo_salvo}")

    else:
        messagebox.showwarning(title="Atenção", message="Nenhum evento criado, adicione os centros de trabalho!")
    

img_btn_executar = PhotoImage(file="imagens\\btn_executar.png")
# btn_executar = Button(app, bd=2, image=img_btn_executar, command=lambda: valBarra(100000))
btn_executar = Button(app, bd=2, image=img_btn_executar, command=executar)

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