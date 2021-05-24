#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Başlangıç Tarihi: 06.05.2021 - 17:06
# Bitiş Tarihi: 11.05.2021 - 21:00
# instagram.com/yazilimfuryasi
# yazilimfuryasi.com

from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from cv2 import cv2
import numpy as np
import threading
import webbrowser

tk = Tk()
windowWidth = tk.winfo_reqwidth()
windowHeight = tk.winfo_reqheight()
positionRight = int(tk.winfo_screenwidth()/3 - windowWidth/3)
positionDown = int(tk.winfo_screenheight()/3 - windowHeight/1)
tk.geometry(f"800x510+{positionRight}+{positionDown}")
tk.resizable(width=False, height=False)


tk.title("Fotoğraf Maskesi Oluşturma ve Bulanıklaştırma | Yazılım Furyası")
F1 = Frame(tk)
F1.grid(row=0, column=0,pady=25, padx=25)
l1 = Label(F1, text="Orijinal Resim", font="bold")
l1.grid(row=0, column=0)
L1 = Label(F1, text="Resim Alanı",height="25",width="52",bd=0.5, relief="solid")
L1.grid(row=1, column=0, pady=10, padx=15)
l2 = Label(F1, text="Maske", font="bold")
l2.grid(row=0, column=1)
L2 = Label(F1, text="Maske",height="25",width="52",bd=0.5, relief="solid")
L2.grid(row=1, column=1)
F2 = None
F3 = None

def Resim_Ekle():
    global hsv
    global tkimage
    global orjinal
    global img_rgb
    global resimselect
    # Resim Seç
    resimselect = filedialog.askopenfilename(initialdir = "Desktop", filetypes = [('Image files', '*.png'),('Image files', '*.jpg')])
    # Resim Seçilmezse Geri Dönder
    if not resimselect:
        return
    print(resimselect)

    try:
        # Resimi Oku
        orjinal = cv2.imread(resimselect)

        # Resimi Aç
        im = Image.open(resimselect)
        im.thumbnail((360, 360))
        tkimage = ImageTk.PhotoImage(im)

        img_rgb = np.array(im)

        # RGB'den BGR'ye dönüştürürken kullanılan parametre cv2.COLOR_RGB2BGR
        hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

        # Widgetler
        L1 = Label(F1, image = None) #, image = tkimage)
        L1.config(image = tkimage)
        
        L2 = Label(F1, image = None)
        L2.config(image = tkimage)

        L1.grid(row=1, column=0)
        L2.grid(row=1, column=1)
        saveBTN.config(state="normal",cursor="hand2")
        tk.geometry("1200x510")
    except:
        return

v1 = DoubleVar()
v2 = DoubleVar()
v3 = DoubleVar()
v4 = DoubleVar()
v5 = DoubleVar()
v6 = DoubleVar()
v7 = DoubleVar()
v8 = DoubleVar()
v9 = DoubleVar()
v10 = DoubleVar()
v11 = DoubleVar()
def updateValue(event):
    global k_resim
    global orjn

    saveBTN.config(state="disabled",cursor="")

    low = np.array([l_h.get(), l_s.get(), l_v.get()])
    high = np.array([u_h.get(), u_s.get(), u_v.get()])

    k_resim = cv2.inRange(hsv, low, high)
    orjn = cv2.inRange(orjinal, low, high)

    imgtk3 = ImageTk.PhotoImage(image=Image.fromarray(k_resim))
    LabelHSV["text"] = ([l_h.get(),l_s.get(),l_v.get()],[u_h.get(),u_s.get(),u_v.get()])

    L2 = Label(F1, image = imgtk3)
    L2.image = imgtk3
    L2.grid(row=1, column=1)

    # print([l_h.get(),l_s.get(),l_v.get()],[u_h.get(),u_s.get(),u_v.get()])
    saveBTN.config(state="normal",cursor="hand2")

def yeniSayfa():
    global l_h
    global l_s
    global l_v
    global u_h
    global u_s
    global u_v
    global F2
    global LabelHSV
    if F3:
        F3.grid_forget()
        F3.destroy()
    F2 = Frame(tk)
    F2.place(x=900,y=50)
    
    l_h_lbl = Label(F2,text="Lower - H | Ton")
    l_h_lbl.grid(row=0,column=0, sticky=W, padx="100")
    l_h = Scale(F2, length=255,variable = v1, from_ = 0, to = 179, troughcolor="white", orient = HORIZONTAL)
    l_h.bind("<ButtonRelease-1>", updateValue)
    l_h.grid(row=1,column=0)
    l_s_lbl = Label(F2,text="Lower - S | Doygunluk")
    l_s_lbl.grid(row=2,column=0,sticky=W, padx="100")
    l_s = Scale(F2, length=255,variable = v2, from_ = 0, to = 255, troughcolor="white", orient = HORIZONTAL)
    l_s.bind("<ButtonRelease-1>", updateValue)
    l_s.grid(row=3,column=0)
    l_v_lbl = Label(F2,text="Lower - V | Değer")
    l_v_lbl.grid(row=4,column=0,sticky=W, padx="100")
    l_v = Scale(F2, length=255,variable = v3, from_ = 0, to = 255, troughcolor="white",orient = HORIZONTAL)
    l_v.bind("<ButtonRelease-1>", updateValue)
    l_v.grid(row=5,column=0)

    u_h_lbl = Label(F2,text="Upper - H | Ton")
    u_h_lbl.grid(row=6,column=0, sticky=W, padx="100")
    u_h = Scale(F2, length=255,variable = v4, from_ = 0, to = 179, troughcolor="red", orient = HORIZONTAL)
    u_h.bind("<ButtonRelease-1>", updateValue)
    u_h.grid(row=7,column=0)
    u_s_lbl = Label(F2,text="Upper - S | Doygunluk")
    u_s_lbl.grid(row=8,column=0,sticky=W, padx="100")
    u_s = Scale(F2, length=255,variable = v5, from_ = 0, to = 255, troughcolor="red", orient = HORIZONTAL)
    u_s.bind("<ButtonRelease-1>", updateValue)
    u_s.grid(row=9,column=0)
    u_v_lbl = Label(F2,text="Upper - V | Değer")
    u_v_lbl.grid(row=10,column=0,sticky=W, padx="100")
    u_v = Scale(F2, length=255,variable = v6, from_ = 0, to = 255, troughcolor="red", orient = HORIZONTAL)
    u_v.bind("<ButtonRelease-1>", updateValue)
    u_v.grid(row=11,column=0)
    reset = Button(F2, text ="Sıfırla",font="bold",fg="white", width = 10, command = Sıfırla, bg = "red")
    reset.config(cursor="hand2")
    reset.grid(row=13,column=0)

    def Kopyala(event):
        hsv_deger = [l_h.get(),l_s.get(),l_v.get()],[u_h.get(),u_s.get(),u_v.get()]
        tk.clipboard_append(hsv_deger)
        KayıtMesajı = Label(F2, text="Kopyalandı.", font="bold", fg="red", width = 14,height=2)
        KayıtMesajı.grid(row=13,column=0)
        KayıtMesajı.after(2000, KayıtMesajı.destroy)
    LabelHSV = Label(F2,font="bold")
    LabelHSV.grid(row=12,column=0,pady=5)
    LabelHSV.config(cursor="hand2")
    LabelHSV.bind("<Button-1>", Kopyala)

def blur_def():
    global F3
    global blur
    global blur2
    global blur3
    global blurred
    global blurred2
    if F2:
        F2.grid_forget()
        F2.destroy()
    def trgt_scale(event):
        threading.Thread(target=blrr).start()
    def trgt_scale2(event):
        threading.Thread(target=blrr2).start()
    F3 = Frame(tk)
    F3.place(x=900,y=50)

    blr_lbl = Label(F3,text="Pixel")
    blr_lbl.grid(row=0,column=0, sticky=W, padx="100")

    blur = Scale(F3, length=255,variable = v7, from_ = 1, to = 100, troughcolor="red", orient = HORIZONTAL)
    blur.bind("<ButtonRelease-1>", trgt_scale)
    blur.grid(row=1,column=0,padx=27)

    blr_lbl2 = Label(F3,text="Renk")
    blr_lbl2.grid(row=2,column=0, sticky=W, padx="100")

    blur2 = Scale(F3, length=255,variable = v8, from_ = 1, to = 100, troughcolor="white", orient = HORIZONTAL)
    blur2.bind("<ButtonRelease-1>", trgt_scale)
    blur2.grid(row=3,column=0,padx=27)
    
    blr_lbl3 = Label(F3,text="Renk Uzayı")
    blr_lbl3.grid(row=4,column=0, sticky=W, padx="100")

    blur3 = Scale(F3, length=255,variable = v9, from_ = 1, to = 100, troughcolor="red", orient = HORIZONTAL)
    blur3.bind("<ButtonRelease-1>", trgt_scale)
    blur3.grid(row=5,column=0,padx=27)

    blurred_lbl = Label(F3,text="Sigma X")
    blurred_lbl.grid(row=6,column=0, sticky=W, padx="100")

    blurred = Scale(F3, length=255,variable = v10, from_ = 1, to = 100, troughcolor="green", orient = HORIZONTAL)
    blurred.bind("<ButtonRelease-1>", trgt_scale2)
    blurred.grid(row=7,column=0,padx=27)
    
    blurred_lbl2 = Label(F3,text="sigma Y")
    blurred_lbl2.grid(row=8,column=0, sticky=W, padx="100")

    blurred2 = Scale(F3, length=255,variable = v11, from_ = 1, to = 100, troughcolor="green", orient = HORIZONTAL)
    blurred2.bind("<ButtonRelease-1>", trgt_scale2)
    blurred2.grid(row=9,column=0,padx=27)

def blrr2():
    global orjn
    saveBTN.config(state="disabled",cursor="")

    blurring = cv2.blur(img_rgb,(blurred.get(),blurred2.get()))
    orjn = cv2.blur(orjinal,(blurred.get(),blurred2.get()))
    
    imgtk3 = ImageTk.PhotoImage(image=Image.fromarray(blurring))

    L2 = Label(F1, image = imgtk3)
    L2.image = imgtk3
    L2.grid(row=1, column=1)

    saveBTN.config(state="normal",cursor="hand2")


def blrr():
    global orjn

    saveBTN.config(state="disabled",cursor="")

    bilFilter = cv2.bilateralFilter(img_rgb,blur.get(),blur2.get(),blur3.get())
    orjn = cv2.bilateralFilter(orjinal,blur.get(),blur2.get(),blur3.get())
    
    imgtk3 = ImageTk.PhotoImage(image=Image.fromarray(bilFilter))

    L2 = Label(F1, image = imgtk3)
    L2.image = imgtk3
    L2.grid(row=1, column=1)

    saveBTN.config(state="normal",cursor="hand2")

def blurring():
    global F3
    global blur
    global blur2
    global blur3
    if F2:
        F2.grid_forget()
        F2.destroy()
    def trgt_scale():
        threading.Thread(target=blrr).start()
    F4 = Frame(tk)
    F4.place(x=900,y=50)

    blr_lbl2 = Label(F4,text="Pixel")
    blr_lbl2.grid(row=0,column=0, sticky=W, padx="100")

    blur1 = Scale(F4, length=255,variable = v7, from_ = 1, to = 100, troughcolor="red", orient = HORIZONTAL)
    blur1.bind("<ButtonRelease-1>", trgt_scale)
    blur1.grid(row=1,column=0,padx=27)

    blr_lbl3 = Label(F4,text="Renk")
    blr_lbl3.grid(row=2,column=0, sticky=W, padx="100")

    blur2 = Scale(F4, length=255,variable = v8, from_ = 1, to = 100, troughcolor="white", orient = HORIZONTAL)
    blur2.bind("<ButtonRelease-1>", trgt_scale)
    blur2.grid(row=3,column=0,padx=27)

def Sıfırla():
    LabelHSV["text"] = ""
    L2 = Label(F1, image = tkimage)
    L2.image = tkimage
    L2.grid(row=1, column=1)
    l_h.set(0)
    l_s.set(0)
    l_v.set(0)
    u_h.set(0)
    u_s.set(0)
    u_v.set(0)

def Kayıt():
    # Yeni Resmi Kayıt Et
    dosyaAdi = filedialog.asksaveasfilename(initialdir ="Desktop", filetypes=[("PNG file", "*.png")])
    if not dosyaAdi:
        return
    cv2.imwrite(f"{dosyaAdi}"+".png", orjn)
    KayıtMesajı = Label(F1, text="Kayıt Edildi.", font="bold")
    KayıtMesajı.grid(row=2, column=1,pady=27)
    KayıtMesajı.after(2000, KayıtMesajı.destroy)

def maske_trgt():
    threading.Thread(target=yeniSayfa).start()
def blur_trgt():
    threading.Thread(target=blur_def).start()
def blur_trgt2():
    threading.Thread(target=blurring).start()
def trgt2():
    threading.Thread(target=Resim_Ekle).start()
def trgt3():
    threading.Thread(target=Kayıt).start()

B1 = Button(tk, text = "Resim Ekle", command=trgt2)
B1.config(cursor="hand2")
B1.place(x=180,y=450)

hsv_btn = Button(tk,text="HSV Maskeleme", width = 13, command=maske_trgt)
hsv_btn.config(cursor="hand2")
hsv_btn.place(x=800,y=56)
blur_btn = Button(tk,text="Bilateral Filter", width = 13,command=blur_trgt)
blur_btn.config(cursor="hand2")
blur_btn.place(x=800,y=90)

saveBTN = Button(tk, text = "Resmi Kayıt Et", command=trgt3)
saveBTN.config(state="disabled")
saveBTN.place(x=565,y=450)

def callback(url):
    webbrowser.open_new(url)
me = Label(tk, text="Developer: yazilimfuryasi.com | @yazilimfuryasi", fg="#6E7371",cursor="hand2",font="Verdana 7 bold")
me.place(x=280,y=485)
me.bind("<Button-1>", lambda e: callback(webbrowser.open_new("https://www.instagram.com/yazilimfuryasi/")))

tk.mainloop()
