# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 17:18:09 2026

@author: Windows
"""
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

ruta_imagen_global = None

def cargar_imagen_interfaz():
    global r_imagen_ajustada, ruta_imagen_global
    
    ruta_archivo = filedialog.askopenfilename(
        title="ingrese imagen",
        filetypes=[("archivo", "*.jpg *.jpeg *.png")]
    )
    
    if ruta_archivo:
        ruta_imagen_global = ruta_archivo
        
        imagen = cv2.imread(ruta_archivo)
        if imagen is not None:
            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            
            alto, ancho, _ = imagen_rgb.shape
            max_dim = 340
            if ancho > alto:
                proporcion = max_dim / float(ancho)
                alto = int(float(alto) * proporcion)
                ancho = max_dim
            else:
                proporcion = max_dim / float(alto)
                ancho = int(float(ancho) * proporcion)
                alto = max_dim
                
            r_imagen_ajustada = cv2.resize(imagen_rgb, (ancho, alto))
            
            img_pil = Image.fromarray(r_imagen_ajustada)
            img_tk = ImageTk.PhotoImage(img_pil)
            lbl_img_origen.config(image=img_tk)
            lbl_img_origen.image = img_tk
            
            lbl_panel_izq.config(text="imagen 1", fg="#FFFFFF")
            lbl_estado.config(text="imagen cargada.\nempezar filtro'", fg="#00FF00")
        else:
            messagebox.showerror("error")

def procesar_suavizado_interfaz():
    global r_imagen_ajustada
    if r_imagen_ajustada is None or ruta_imagen_global is None:
        messagebox.showwarning("carga una imagen.")
        return

    lbl_estado.config(text="cargando", fg="#FFCC00")
    ventana.update()
    
    alto, ancho, canales = r_imagen_ajustada.shape
    
    imagen_suavizada_float = np.zeros((alto, ancho, 3), dtype=np.float32)

    pesos = np.array([[1, 2, 1],
                      [2, 4, 2],
                      [1, 2, 1]], dtype=np.float32)
    suma_pesos = pesos.sum()

    for y in range(1, alto - 1):
        for x in range(1, ancho - 1):
            for c in range(3):
                ventana_local = r_imagen_ajustada[y-1:y+2, x-1:x+2, c].astype(np.float32)
                valor_suavizado = (ventana_local * pesos).sum() / suma_pesos
                imagen_suavizada_float[y, x, c] = valor_suavizado

    imagen_suavizada = np.clip(imagen_suavizada_float, 0, 255).astype(np.uint8)

    imagen_suavizada[0, :] = r_imagen_ajustada[0, :]
    imagen_suavizada[alto - 1, :] = r_imagen_ajustada[alto - 1, :]
    imagen_suavizada[:, 0] = r_imagen_ajustada[:, 0]
    imagen_suavizada[:, ancho - 1] = r_imagen_ajustada[:, ancho - 1]

    resultado_bgr = cv2.cvtColor(imagen_suavizada, cv2.COLOR_RGB2BGR)
    cv2.imwrite('resultado_reduccion_ruido.jpg', resultado_bgr)

    img_pil_suavizada = Image.fromarray(imagen_suavizada)
    img_tk_suavizada = ImageTk.PhotoImage(img_pil_suavizada)
    lbl_img_resultado.config(image=img_tk_suavizada)
    lbl_img_resultado.image = img_tk_suavizada

    lbl_panel_der.config(text="ventana(3x3)", fg="#00FF00")
    lbl_estado.config(text="ejecucion finalizada", fg="#00FF00")
    messagebox.showinfo( "se reducio ruido.\nSe suavizo trancissiones de color.")

def salir_aplicacion():
    ventana.quit()
    ventana.destroy()






ventana = tk.Tk()
ventana.title("Implementacion Filtro Suavizado")
ventana.geometry("1050x540")
ventana.configure(bg="#1A1A1A")

frame_control = tk.Frame(ventana, bg="#252526", width=240)
frame_control.pack(side=tk.LEFT, fill=tk.Y)
frame_control.pack_propagate(False)

lbl_titulo = tk.Label(frame_control, text="Filtro de promedio 3x3", font=("Segoe UI", 12, "bold"), bg="#252526", fg="#FFFFFF")
lbl_titulo.pack(pady=20)

btn_cargar = tk.Button(frame_control, text="subir imagen", font=("Segoe UI", 10, "bold"), bg="#007ACC", fg="#FFFFFF", bd=0, height=2, command=cargar_imagen_interfaz)
btn_cargar.pack(pady=15, padx=20, fill=tk.X)

btn_convertir = tk.Button(frame_control, text="diseñar", font=("Segoe UI", 10, "bold"), bg="#2D8A4E", fg="#FFFFFF", bd=0, height=2, command=procesar_suavizado_interfaz)
btn_convertir.pack(pady=15, padx=20, fill=tk.X)

btn_salir = tk.Button(frame_control, text="salir", font=("Segoe UI", 10, "bold"), bg="#C0392B", fg="#FFFFFF", bd=0, height=2, command=salir_aplicacion)
btn_salir.pack(side=tk.BOTTOM, pady=25, padx=20, fill=tk.X)

lbl_estado = tk.Label(frame_control, text="espere", font=("Segoe UI", 9, "italic"), bg="#252526", fg="#A0A0A0", wraplength=200)
lbl_estado.pack(side=tk.BOTTOM, pady=10)

frame_imagenes = tk.Frame(ventana, bg="#1A1A1A")
frame_imagenes.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=20, pady=20)

frame_izq = tk.Frame(frame_imagenes, bg="#2D2D2D", bd=1, relief=tk.SOLID, width=380, height=380)
frame_izq.pack(side=tk.LEFT, padx=15, expand=True)
frame_izq.pack_propagate(False)

lbl_panel_izq = tk.Label(frame_izq, text="carge una imagen", font=("Segoe UI", 10, "bold"), bg="#2D2D2D", fg="#666666")
lbl_panel_izq.pack(pady=10)

lbl_img_origen = tk.Label(frame_izq, bg="#2D2D2D")
lbl_img_origen.pack(expand=True)

frame_der = tk.Frame(frame_imagenes, bg="#2D2D2D", bd=1, relief=tk.SOLID, width=380, height=380)
frame_der.pack(side=tk.RIGHT, padx=15, expand=True)
frame_der.pack_propagate(False)

lbl_panel_der = tk.Label(frame_der, text="resulyado", font=("Segoe UI", 10, "bold"), bg="#2D2D2D", fg="#666666")
lbl_panel_der.pack(pady=10)

lbl_img_resultado = tk.Label(frame_der, bg="#2D2D2D")
lbl_img_resultado.pack(expand=True)

ventana.mainloop()