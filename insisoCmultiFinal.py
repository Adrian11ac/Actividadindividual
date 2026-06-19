# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 21:28:52 2026

@author: Windows
"""
import cv2
import tkinter as tk
from tkinter import messagebox
import pygame
import threading
import time
import os

pygame.mixer.init()

def reproducir_audio_externo():
    ruta_audio = r"C:\Users\Windows\Downloads\audiomulti.mp3"
    try:
        pygame.mixer.music.load(ruta_audio)
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showerror( f"no se pudo cargar el archivo de :\n{e}")

def reproducir_animacion_frames():
    ruta_imagenes = r"C:\Users\Windows\Documents\vaca"
    
    try:
        v1_img = cv2.imread(os.path.join(ruta_imagenes, "v1.jpg"))
        v2_img = cv2.imread(os.path.join(ruta_imagenes, "v2.jpg"))
        v3_img = cv2.imread(os.path.join(ruta_imagenes, "v3.jpg"))
        
        if any(img is None for img in [v1_img, v2_img, v3_img]): 
            raise FileNotFoundError
        
        v1_img = cv2.cvtColor(v1_img, cv2.COLOR_BGR2RGB)
        v2_img = cv2.cvtColor(v2_img, cv2.COLOR_BGR2RGB)
        v3_img = cv2.cvtColor(v3_img, cv2.COLOR_RGB2BGR)
    except FileNotFoundError:
        messagebox.showerror( f"no se encontraron las imágenes en:\n{ruta_imagenes}")
        return

    mapa_frames = {
        "v1": v1_img, 
        "v2": v2_img, 
        "v3": v3_img
    }
    
    cv2.namedWindow("Cover Vaca lola", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("monigote animado", cv2.cvtColor(v1_img, cv2.COLOR_RGB2BGR))
    cv2.waitKey(1)


    t_silaba = 110          
    t_retorno = 100         
    t_retorno_rapido = 80   
    t_largo = 450           
    t_silencio = 550        
    t_muu_inter = 950       

    t_silaba_v2 = 75    
    t_retorno_v2 = 75
    t_largo_v2 = 320        
    
    t_muu_final = 2600      
    

    bloque_1 = [
        ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_largo), ("v1", t_retorno),
        ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_largo), ("v1", t_silencio),
        ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno),
        ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_largo), ("v1", t_retorno_rapido),
        ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_largo), ("v1", t_retorno),
        ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_largo), ("v1", t_silencio),
        ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno),
        ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_largo), ("v1", t_retorno_rapido),
        ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v3", t_muu_inter)
    ]

    bloque_2 = [
        ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_largo_v2), ("v1", t_retorno_v2),
        ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_largo_v2), ("v1", 650),
        ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno),
        ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_largo), ("v1", t_retorno_rapido),
        ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_largo_v2), ("v1", t_retorno_v2),
        ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_silaba_v2), ("v1", t_retorno_v2), ("v2", t_largo_v2), ("v1", 1200),
        ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno),
        ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_largo), ("v1", t_retorno_rapido),
        ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v2", t_silaba), ("v1", t_retorno), ("v3", t_muu_final)
    ]

    secuencia_completa = bloque_1 + bloque_2

    for id_frame, duracion in secuencia_completa:
        img_actual = mapa_frames[id_frame]
        cv2.imshow("animacion de monigote", cv2.cvtColor(img_actual, cv2.COLOR_RGB2BGR))
        
        duracion_ms = int(round(duracion, 3))
        
        if cv2.waitKey(duracion_ms) & 0xFF == 27:
            pygame.mixer.music.stop()
            break
            
    cv2.destroyAllWindows()

def comenzar_show_multimedia():
    lbl_estado.config(text="comenzando", fg="#00FFCD")
    ventana.update()
    
    hilo_audio = threading.Thread(target=reproducir_audio_externo)
    hilo_audio.start()
    
    time.sleep(0.005)
    reproducir_animacion_frames()
    
    lbl_estado.config(text="cover terminado", fg="#00FF00")

def salir_aplicacion():
    pygame.mixer.music.stop()
    ventana.quit()
    ventana.destroy()
    
    
    
    
    
    

ventana = tk.Tk()
ventana.title("Vaca Lola Daddy Yankke yeeea")
ventana.geometry("450x320")
ventana.configure(bg="#1A1A1A")

frame_control = tk.Frame(ventana, bg="#252526")
frame_control.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

lbl_titulo = tk.Label(frame_control, text="EMPEZAR COVER", font=("Segoe UI", 14, "bold"), bg="#252526", fg="#FFFFFF")
lbl_titulo.pack(pady=20)

btn_multimedia = tk.Button(frame_control, text="VALA LOLA", font=("Segoe UI", 11, "bold"), bg="#2D8A4E", fg="#FFFFFF", bd=0, height=2, command=comenzar_show_multimedia)
btn_multimedia.pack(pady=20, padx=40, fill=tk.X)

btn_salir = tk.Button(frame_control, text="salir", font=("Segoe UI", 10, "bold"), bg="#C0392B", fg="#FFFFFF", bd=0, height=1, command=salir_aplicacion)
btn_salir.pack(side=tk.BOTTOM, pady=10, padx=40, fill=tk.X)

lbl_estado = tk.Label(frame_control, text="cantada por Daddy Yankee", font=("Segoe UI", 9, "italic"), bg="#252526", fg="#A0A0A0", wraplength=350)
lbl_estado.pack(side=tk.BOTTOM, pady=10)

ventana.mainloop()