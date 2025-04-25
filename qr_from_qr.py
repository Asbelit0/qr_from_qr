import tkinter as tk
from tkinter import filedialog, messagebox
from qrcode import QRCode
try:
    import cv2  # Para leer el QR original
except ImportError:
    messagebox.showerror("Error", "El módulo 'cv2' no está instalado. Por favor, instálalo usando 'pip install opencv-python'.")
    exit()
import os

class QRManager:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Gestor de QR")
        self.window.geometry("400x700")
        self.window.configure(bg="black")
        self.window.resizable(False, False)

        # Opciones de funcionalidad
        self.instructions_label = tk.Label(self.window, text="Escanee o genere QR basado en otro QR",
                                           font=("Arial", 10, "bold"), bg="pink", borderwidth=2, relief="ridge")
        self.instructions_label.pack(pady=15)

        # Botón para cargar el QR original
        self.load_btn = tk.Button(self.window, text="Cargar QR original", font=("Arial", 10, "bold"),
                                  command=self.load_qr, bg="yellow", fg="black", bd=6, relief="groove")
        self.load_btn.pack(pady=20)

        # Campo para ingresar el nombre del QR nuevo
        self.nombre_label = tk.Label(self.window, text="Nombre del QR nuevo:", font=("Arial", 11, "bold", "italic"),
                                     bg="pink", borderwidth=2, relief="ridge")
        self.nombre_label.pack(pady=15)
        self.nombre_entry = tk.Entry(self.window, font=("Arial", 10, "italic"), width=30, borderwidth=5, relief="ridge")
        self.nombre_entry.pack()

        # Botón para generar el QR basado en el QR cargado
        self.generate_btn = tk.Button(self.window, text="Generar nuevo QR", font=("Arial", 10, "bold"),
                                      command=self.generate_qr_from_original, bg="red", fg="white", bd=6, relief="groove")
        self.generate_btn.pack(pady=30)

        self.window.mainloop()

    def load_qr(self):
        # Abrir archivo QR
        file_path = filedialog.askopenfilename(title="Seleccionar QR", filetypes=[("Imagenes", "*.png *.jpg *.jpeg")])
        if not file_path:
            messagebox.showerror("Error", "No se seleccionó ningún archivo.")
            return

        # Escanear el QR usando OpenCV
        try:
            qr_image = cv2.imread(file_path)
            detector = cv2.QRCodeDetector()
            data, _, _ = detector.detectAndDecode(qr_image)
            if data:
                self.original_data = data
                messagebox.showinfo("QR escaneado", f"Enlace extraído: {data}")
            else:
                messagebox.showerror("Error", "No se pudo leer el QR.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema al leer el QR: {e}")
    
    def generate_qr_from_original(self):
        nombre = self.nombre_entry.get()
        if not nombre:
            messagebox.showerror("Error", "Por favor, ingrese un nombre para el QR.")
            return

        if not hasattr(self, 'original_data') or not self.original_data:
            messagebox.showerror("Error", "No se ha cargado ningún QR original.")
            return

        qr = QRCode(
            version=1,
            error_correction=1,
            box_size=10,
            border=4
        )

        qr.add_data(self.original_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        nombre_archivo = f"{nombre}.png"

        if os.path.exists(nombre_archivo):
            respuesta = messagebox.askyesno("Archivo existente",
                                            f"El archivo {nombre_archivo} ya existe. ¿Desea reemplazarlo?")
            if not respuesta:
                return
        img.save(nombre_archivo)

        messagebox.showinfo("Listo", f"Nuevo QR generado correctamente y guardado como {nombre_archivo}")


if __name__ == "__main__":
    QRManager()
