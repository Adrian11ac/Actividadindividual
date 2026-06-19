import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pyodbc

ruta_imagen_global = None

def cargar_imagen_interfaz():
    global r_imagen_ajustada, ruta_imagen_global
    
    ruta_archivo = filedialog.askopenfilename(
        title="abrir imagen",
        filetypes=[("formato", "*.jpg *.jpeg *.png")]
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
            
            lbl_panel_izq.config(text="imagen1", fg="#FFFFFF")
            lbl_estado.config(text="imagen cargado.\ningrese material a encontrar.", fg="#00FF00")
        else:
            messagebox.showerror("error")

def procesar_clasificacion_interfaz():
    global r_imagen_ajustada
    if r_imagen_ajustada is None or ruta_imagen_global is None:
        messagebox.showwarning("cargar una imagen primero.")
        return
        
    superficie_objetivo = entrada_superficie.get().strip().lower()
    if not superficie_objetivo:
        messagebox.showwarning("escriba material patra detectar(cesped, tierra, asfalto, cemento).")
        return

    lbl_estado.config(text=f" detectando {superficie_objetivo}", fg="#FFCC00")
    ventana.update()
    
    alto, ancho, _ = r_imagen_ajustada.shape
    mapa_clasificado = np.zeros((alto, ancho, 3), dtype=np.uint8)

    pixeles_detectados = 0
    suma_r, suma_g, suma_b = 0, 0, 0
    brillos = []

    for y in range(alto):
        for x in range(ancho):
            r, g, b = r_imagen_ajustada[y, x]
            r_int, g_int, b_int = int(r), int(g), int(b)
            
            es_material = False
            
            if superficie_objetivo == "cesped":
                if g_int > r_int * 1.1 and g_int > b_int * 1.1:
                    mapa_clasificado[y, x] = [0, 255, 0]
                    es_material = True
                    
            elif superficie_objetivo == "tierra":
                if r_int > g_int and g_int > b_int and r_int > 80 and b_int < 100:
                    mapa_clasificado[y, x] = [139, 69, 19]
                    es_material = True
                    
            elif superficie_objetivo == "asfalto":
                if abs(r_int - g_int) < 20 and abs(g_int - b_int) < 20 and abs(r_int - b_int) < 20:
                    if r_int < 100:
                        mapa_clasificado[y, x] = [50, 50, 50]
                        es_material = True
                        
            elif superficie_objetivo == "cemento":
                if abs(r_int - g_int) < 20 and abs(g_int - b_int) < 20 and abs(r_int - b_int) < 20:
                    if r_int >= 100:
                        mapa_clasificado[y, x] = [180, 180, 180]
                        es_material = True

            
            if es_material:
                suma_r += r_int
                suma_g += g_int
                suma_b += b_int
                brillo = 0.299 * r_int + 0.587 * g_int + 0.114 * b_int
                brillos.append(brillo)
                pixeles_detectados += 1

  
    if pixeles_detectados == 0:
        lbl_estado.config(text=" no se encontro material.", fg="#FF3333")
        messagebox.showwarning( f"no se encontraron'{superficie_objetivo}' en esta imagen.")
        return

    prom_r = round(suma_r / pixeles_detectados, 3)
    prom_g = round(suma_g / pixeles_detectados, 3)
    prom_b = round(suma_b / pixeles_detectados, 3)
    
    prom_brillo = round((0.299 * prom_r) + (0.587 * prom_g) + (0.114 * prom_b), 3)
    suma_varianza = sum((b - prom_brillo) ** 2 for b in brillos)
    varianza = round(suma_varianza / pixeles_detectados, 3)

    try:
        string_conexion = (
            "Driver={SQL Server};"
            "Server=DESKTOP-FGIP20G\\SQLEXPRESS;"
            "Database=A;"
            "Trusted_Connection=yes;"
        )
        
        conn = pyodbc.connect(string_conexion)
        cursor = conn.cursor()
        
        sql = """INSERT INTO texturas (nombre_superficie, r_promedio, g_promedio, b_promedio, varianza_brillo) 
                 VALUES (?, ?, ?, ?, ?)"""
        valores = (superficie_objetivo, prom_r, prom_g, prom_b, varianza)
        
        cursor.execute(sql, valores)
        conn.commit()
        
        cursor.close()
        conn.close()
        sql_exito = True
    except Exception as e:
        sql_exito = False
        error_msg = str(e)

    resultado_bgr = cv2.cvtColor(mapa_clasificado, cv2.COLOR_RGB2BGR)
    cv2.imwrite('resultado_texturas_gui.jpg', resultado_bgr)

    img_pil_mapa = Image.fromarray(mapa_clasificado)
    img_tk_mapa = ImageTk.PhotoImage(img_pil_mapa)
    lbl_img_resultado.config(image=img_tk_mapa)
    lbl_img_resultado.image = img_tk_mapa

    lbl_panel_der.config(text=f"se detecto: {superficie_objetivo.upper()}", fg="#00FF00")
    
    if sql_exito:
        lbl_estado.config(text=f"datos de {superficie_objetivo} guardados correctamente", fg="#00FF00")
        messagebox.showinfo("deteccion aplicada", f"análisis segmentado guardados correctamente 'A'!\n\nMaterial: {superficie_objetivo}\n- R Prom: {prom_r}\n- G Prom: {prom_g}\n- B Prom: {prom_b}\n- Varianza: {varianza}")
    else:
        lbl_estado.config(text="Filtro listo pero falló SQL.", fg="#FF3333")
        messagebox.showwarning(f"La detección visual finalizado, falla de conexión a BD:\n{error_msg}")

def salir_aplicacion():
    ventana.quit()
    ventana.destroy()

ventana = tk.Tk()
ventana.title("Clasificacion de Texturas")
ventana.geometry("1050x580")
ventana.configure(bg="#1A1A1A")

frame_control = tk.Frame(ventana, bg="#252526", width=240)
frame_control.pack(side=tk.LEFT, fill=tk.Y)
frame_control.pack_propagate(False)

lbl_titulo = tk.Label(frame_control, text="Deteccion de superficies \nclasificación", font=("Segoe UI", 12, "bold"), bg="#252526", fg="#FFFFFF")
lbl_titulo.pack(pady=20)

btn_cargar = tk.Button(frame_control, text=" subir imagen", font=("Segoe UI", 10, "bold"), bg="#007ACC", fg="#FFFFFF", bd=0, height=2, command=cargar_imagen_interfaz)
btn_cargar.pack(pady=10, padx=20, fill=tk.X)

lbl_sub_datos = tk.Label(frame_control, text="ingrese una superficie(material):", font=("Segoe UI", 9, "bold"), bg="#252526", fg="#A0A0A0")
lbl_sub_datos.pack(pady=(15, 2), padx=20, anchor="w")

entrada_superficie = tk.Entry(frame_control, font=("Segoe UI", 10), bg="#3C3C3C", fg="#FFFFFF", insertbackground="white", bd=1, relief=tk.FLAT)
entrada_superficie.pack(pady=(0, 15), padx=20, fill=tk.X)
entrada_superficie.insert(0, "escribe aqui")

btn_convertir = tk.Button(frame_control, text="detectar", font=("Segoe UI", 10, "bold"), bg="#2D8A4E", fg="#FFFFFF", bd=0, height=2, command=procesar_clasificacion_interfaz)
btn_convertir.pack(pady=10, padx=20, fill=tk.X)

btn_salir = tk.Button(frame_control, text="salir", font=("Segoe UI", 10, "bold"), bg="#C0392B", fg="#FFFFFF", bd=0, height=2, command=salir_aplicacion)
btn_salir.pack(side=tk.BOTTOM, pady=25, padx=20, fill=tk.X)

lbl_estado = tk.Label(frame_control, text="espere", font=("Segoe UI", 9, "italic"), bg="#252526", fg="#A0A0A0", wraplength=200)
lbl_estado.pack(side=tk.BOTTOM, pady=10)

frame_imagenes = tk.Frame(ventana, bg="#1A1A1A")
frame_imagenes.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=20, pady=20)

frame_izq = tk.Frame(frame_imagenes, bg="#2D2D2D", bd=1, relief=tk.SOLID, width=380, height=380)
frame_izq.pack(side=tk.LEFT, padx=15, expand=True)
frame_izq.pack_propagate(False)

lbl_panel_izq = tk.Label(frame_izq, text="Imagen no seleccionada", font=("Segoe UI", 10, "bold"), bg="#2D2D2D", fg="#666666")
lbl_panel_izq.pack(pady=10)

lbl_img_origen = tk.Label(frame_izq, bg="#2D2D2D")
lbl_img_origen.pack(expand=True)

frame_der = tk.Frame(frame_imagenes, bg="#2D2D2D", bd=1, relief=tk.SOLID, width=380, height=380)
frame_der.pack(side=tk.RIGHT, padx=15, expand=True)
frame_der.pack_propagate(False)

lbl_panel_der = tk.Label(frame_der, text="resultado", font=("Segoe UI", 10, "bold"), bg="#2D2D2D", fg="#666666")
lbl_panel_der.pack(pady=10)

lbl_img_resultado = tk.Label(frame_der, bg="#2D2D2D")
lbl_img_resultado.pack(expand=True)

ventana.mainloop()