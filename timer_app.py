import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
import time
import os
import sys
from datetime import datetime, timedelta
import pystray
from pystray import MenuItem as item

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TimerApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Temporizador & Cronómetro")
        self.root.geometry("500x250")
        self.root.resizable(False, False)
        
        # Variables de control
        self.timer_running = False
        self.stopwatch_running = False
        self.timer_thread = None
        self.stopwatch_thread = None
        self.timer_seconds = 0
        self.stopwatch_seconds = 0
        
        # Variables para el system tray
        self.tray_icon = None
        self.is_minimized = False
        
        # Configurar para ejecutar en segundo plano
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        self.root.bind("<Unmap>", self.on_minimize)
        
        # Crear el icono del system tray
        self.create_tray_icon()
        
        self.setup_ui()
        self.center_window()
        
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Notebook para las pestañas (sin margen blanco)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Pestaña del Temporizador
        self.timer_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.timer_frame, text="⏰ Temporizador")
        self.setup_timer_tab()
        
        # Pestaña del Cronómetro
        self.stopwatch_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.stopwatch_frame, text="⏱️ Cronómetro")
        self.setup_stopwatch_tab()
        
        # Botón para minimizar
        minimize_btn = ctk.CTkButton(
            self.root,
            text="📥 Minimizar al Tray",
            command=self.minimize_to_tray,
            fg_color="orange",
            hover_color="darkorange",
            height=22,
            width=120
        )
        minimize_btn.pack(pady=2)
    
    def setup_timer_tab(self):
        """Configura la pestaña del temporizador"""
        # Frame para entrada de tiempo
        time_input_frame = ctk.CTkFrame(self.timer_frame)
        time_input_frame.pack(fill="x", padx=5, pady=3)
        
        # Frame para horas, minutos y segundos
        time_controls_frame = ctk.CTkFrame(time_input_frame)
        time_controls_frame.pack(pady=3)
        
        # Horas
        hours_frame = ctk.CTkFrame(time_controls_frame)
        hours_frame.pack(side="left", padx=5)
        ctk.CTkLabel(hours_frame, text="Horas").pack()
        self.hours_var = tk.StringVar(value="0")
        self.hours_spinbox = ctk.CTkEntry(hours_frame, textvariable=self.hours_var, width=60)
        self.hours_spinbox.pack(pady=5)
        
        # Minutos
        minutes_frame = ctk.CTkFrame(time_controls_frame)
        minutes_frame.pack(side="left", padx=5)
        ctk.CTkLabel(minutes_frame, text="Minutos").pack()
        self.minutes_var = tk.StringVar(value="0")
        self.minutes_spinbox = ctk.CTkEntry(minutes_frame, textvariable=self.minutes_var, width=60)
        self.minutes_spinbox.pack(pady=5)
        
        # Segundos
        seconds_frame = ctk.CTkFrame(time_controls_frame)
        seconds_frame.pack(side="left", padx=5)
        ctk.CTkLabel(seconds_frame, text="Segundos").pack()
        self.seconds_var = tk.StringVar(value="0")
        self.seconds_spinbox = ctk.CTkEntry(seconds_frame, textvariable=self.seconds_var, width=60)
        self.seconds_spinbox.pack(pady=5)
        
        # Display del tiempo restante
        self.timer_display = ctk.CTkLabel(
            self.timer_frame,
            text="00:00:00",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="lime"
        )
        self.timer_display.pack(pady=3)
        
        # Botones de control
        buttons_frame = ctk.CTkFrame(self.timer_frame)
        buttons_frame.pack(pady=3)
        
        self.start_timer_btn = ctk.CTkButton(
            buttons_frame,
            text="▶️ Iniciar",
            command=self.start_timer,
            fg_color="green",
            hover_color="darkgreen",
            height=28,
            width=80
        )
        self.start_timer_btn.pack(side="left", padx=3)
        
        self.pause_timer_btn = ctk.CTkButton(
            buttons_frame,
            text="⏸️ Pausar",
            command=self.pause_timer,
            fg_color="orange",
            hover_color="darkorange",
            state="disabled",
            height=28,
            width=80
        )
        self.pause_timer_btn.pack(side="left", padx=3)
        
        self.reset_timer_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 Reiniciar",
            command=self.reset_timer,
            fg_color="red",
            hover_color="darkred",
            height=28,
            width=80
        )
        self.reset_timer_btn.pack(side="left", padx=3)
        
        # Presets rápidos
        presets_frame = ctk.CTkFrame(self.timer_frame)
        presets_frame.pack(pady=2)
        
        ctk.CTkLabel(presets_frame, text="Presets:", font=ctk.CTkFont(size=11)).pack(pady=2)
        
        presets_buttons_frame = ctk.CTkFrame(presets_frame)
        presets_buttons_frame.pack(pady=2)
        
        preset_times = [("5 min", 5), ("10 min", 10), ("15 min", 15), ("30 min", 30), ("1 hora", 60)]
        for text, minutes in preset_times:
            btn = ctk.CTkButton(
                presets_buttons_frame,
                text=text,
                command=lambda m=minutes: self.set_preset_time(m),
                width=55,
                height=24
            )
            btn.pack(side="left", padx=1)
    
    def setup_stopwatch_tab(self):
        """Configura la pestaña del cronómetro"""
        # Frame principal del cronómetro sin márgenes
        main_stopwatch_frame = ctk.CTkFrame(self.stopwatch_frame)
        main_stopwatch_frame.pack(fill="both", expand=True, padx=5, pady=3)
        
        # Display del cronómetro (más compacto)
        self.stopwatch_display = ctk.CTkLabel(
            main_stopwatch_frame,
            text="00:00:00.0",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="cyan"
        )
        self.stopwatch_display.pack(pady=3)
        
        # Botones de control (más compactos)
        buttons_frame = ctk.CTkFrame(main_stopwatch_frame)
        buttons_frame.pack(pady=2)
        
        self.start_stopwatch_btn = ctk.CTkButton(
            buttons_frame,
            text="▶️ Iniciar",
            command=self.start_stopwatch,
            fg_color="green",
            hover_color="darkgreen",
            height=28,
            width=80
        )
        self.start_stopwatch_btn.pack(side="left", padx=2)
        
        self.pause_stopwatch_btn = ctk.CTkButton(
            buttons_frame,
            text="⏸️ Pausar",
            command=self.pause_stopwatch,
            fg_color="orange",
            hover_color="darkorange",
            state="disabled",
            height=28,
            width=80
        )
        self.pause_stopwatch_btn.pack(side="left", padx=2)
        
        self.reset_stopwatch_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 Reiniciar",
            command=self.reset_stopwatch,
            fg_color="red",
            hover_color="darkred",
            height=28,
            width=80
        )
        self.reset_stopwatch_btn.pack(side="left", padx=2)
        
        # Botón para marcar vuelta (más compacto)
        self.lap_btn = ctk.CTkButton(
            main_stopwatch_frame,
            text="🏁 Marcar Vuelta",
            command=self.mark_lap,
            fg_color="purple",
            hover_color="darkpurple",
            state="disabled",
            height=22,
            width=100
        )
        self.lap_btn.pack(pady=1)
        
        # Lista de vueltas (más compacta)
        laps_frame = ctk.CTkFrame(main_stopwatch_frame)
        laps_frame.pack(fill="both", expand=True, padx=5, pady=1)
        
        ctk.CTkLabel(laps_frame, text="Vueltas:", font=ctk.CTkFont(size=11)).pack(pady=1)
        
        # Scrollable frame para las vueltas (más compacto)
        self.laps_container = ctk.CTkScrollableFrame(laps_frame, height=60)
        self.laps_container.pack(fill="both", expand=True, padx=3, pady=1)
        
        self.laps = []
    
    def set_preset_time(self, minutes):
        """Establece un tiempo predefinido"""
        self.hours_var.set("0")
        self.minutes_var.set(str(minutes))
        self.seconds_var.set("0")
    
    def start_timer(self):
        """Inicia el temporizador"""
        try:
            hours = int(self.hours_var.get() or "0")
            minutes = int(self.minutes_var.get() or "0")
            seconds = int(self.seconds_var.get() or "0")
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            
            if total_seconds <= 0:
                messagebox.showwarning("Advertencia", "Por favor ingresa un tiempo válido")
                return
            
            self.timer_seconds = total_seconds
            self.timer_running = True
            
            self.start_timer_btn.configure(state="disabled")
            self.pause_timer_btn.configure(state="normal")
            
            self.timer_thread = threading.Thread(target=self.timer_countdown, daemon=True)
            self.timer_thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos")
    
    def timer_countdown(self):
        """Cuenta regresiva del temporizador"""
        while self.timer_running and self.timer_seconds > 0:
            time.sleep(1)
            self.timer_seconds -= 1
            
            # Actualizar display en el hilo principal
            self.root.after(0, self.update_timer_display)
            
            if self.timer_seconds <= 0:
                self.root.after(0, self.timer_finished)
                break
    
    def update_timer_display(self):
        """Actualiza el display del temporizador"""
        hours = self.timer_seconds // 3600
        minutes = (self.timer_seconds % 3600) // 60
        seconds = self.timer_seconds % 60
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.timer_display.configure(text=time_str)
        
        # Cambiar color según tiempo restante
        if self.timer_seconds <= 10:
            self.timer_display.configure(text_color="red")
        elif self.timer_seconds <= 30:
            self.timer_display.configure(text_color="orange")
    
    def timer_finished(self):
        """Se ejecuta cuando el temporizador termina"""
        self.timer_running = False
        self.timer_display.configure(text="00:00:00", text_color="lime")
        self.start_timer_btn.configure(state="normal")
        self.pause_timer_btn.configure(state="disabled")
        
        # Notificación
        messagebox.showinfo("Temporizador", "¡Tiempo completado!")
        
        # Hacer parpadear la ventana
        self.root.lift()
        self.root.focus_force()
    
    def pause_timer(self):
        """Pausa el temporizador"""
        self.timer_running = False
        self.start_timer_btn.configure(state="normal", text="▶️ Continuar")
        self.pause_timer_btn.configure(state="disabled")
    
    def reset_timer(self):
        """Reinicia el temporizador"""
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_display.configure(text="00:00:00", text_color="lime")
        self.start_timer_btn.configure(state="normal", text="▶️ Iniciar")
        self.pause_timer_btn.configure(state="disabled")
    
    def start_stopwatch(self):
        """Inicia el cronómetro"""
        self.stopwatch_running = True
        self.start_stopwatch_btn.configure(state="disabled")
        self.pause_stopwatch_btn.configure(state="normal")
        self.lap_btn.configure(state="normal")
        
        self.stopwatch_thread = threading.Thread(target=self.stopwatch_count, daemon=True)
        self.stopwatch_thread.start()
    
    def stopwatch_count(self):
        """Cuenta del cronómetro"""
        start_time = time.time()
        while self.stopwatch_running:
            elapsed = time.time() - start_time
            self.stopwatch_seconds = elapsed
            
            # Actualizar display en el hilo principal
            self.root.after(0, self.update_stopwatch_display)
            time.sleep(0.1)
    
    def update_stopwatch_display(self):
        """Actualiza el display del cronómetro"""
        hours = int(self.stopwatch_seconds // 3600)
        minutes = int((self.stopwatch_seconds % 3600) // 60)
        seconds = int(self.stopwatch_seconds % 60)
        tenths = int((self.stopwatch_seconds * 10) % 10)
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{tenths}"
        self.stopwatch_display.configure(text=time_str)
    
    def pause_stopwatch(self):
        """Pausa el cronómetro"""
        self.stopwatch_running = False
        self.start_stopwatch_btn.configure(state="normal", text="▶️ Continuar")
        self.pause_stopwatch_btn.configure(state="disabled")
    
    def reset_stopwatch(self):
        """Reinicia el cronómetro"""
        self.stopwatch_running = False
        self.stopwatch_seconds = 0
        self.stopwatch_display.configure(text="00:00:00.0")
        self.start_stopwatch_btn.configure(state="normal", text="▶️ Iniciar")
        self.pause_stopwatch_btn.configure(state="disabled")
        self.lap_btn.configure(state="disabled")
        
        # Limpiar vueltas
        for widget in self.laps_container.winfo_children():
            widget.destroy()
        self.laps = []
    
    def mark_lap(self):
        """Marca una vuelta en el cronómetro"""
        if self.stopwatch_running:
            lap_time = self.stopwatch_seconds
            self.laps.append(lap_time)
            
            # Crear label para la vuelta
            lap_text = f"Vuelta {len(self.laps)}: {self.format_time(lap_time)}"
            lap_label = ctk.CTkLabel(self.laps_container, text=lap_text)
            lap_label.pack(anchor="w", pady=2)
    
    def format_time(self, seconds):
        """Formatea el tiempo para mostrar"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        tenths = int((seconds * 10) % 10)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}.{tenths}"
        else:
            return f"{minutes:02d}:{secs:02d}.{tenths}"
    
    def minimize_to_tray(self):
        """Minimiza la aplicación al system tray"""
        self.root.withdraw()
        self.is_minimized = True
        
        # Mostrar el icono en el system tray
        if self.tray_icon:
            self.tray_icon.run_detached()
    
    def on_minimize(self, event):
        """Maneja el evento de minimización"""
        if self.root.state() == 'iconic':
            self.minimize_to_tray()
    
    def show_window(self, icon=None, item=None):
        """Muestra la ventana desde el system tray"""
        self.root.after(0, self._show_window)
    
    def _show_window(self):
        """Muestra la ventana en el hilo principal"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.is_minimized = False
        
        # Ocultar el icono del system tray
        if self.tray_icon:
            self.tray_icon.stop()
    
    def quit_app(self, icon=None, item=None):
        """Cierra la aplicación completamente"""
        # Detener todos los hilos
        self.timer_running = False
        self.stopwatch_running = False
        
        # Ocultar el icono del system tray
        if self.tray_icon:
            self.tray_icon.stop()
        
        # Cerrar la aplicación
        self.root.quit()
        self.root.destroy()
        os._exit(0)
    
    def create_tray_icon(self):
        """Crea el icono del system tray"""
        # Crear un icono simple (puedes reemplazarlo con tu propio icono)
        icon_image = self.create_default_icon()
        
        # Crear el menú del system tray
        menu = pystray.Menu(
            item('Mostrar', self.show_window),
            item('Salir', self.quit_app)
        )
        
        # Crear el icono del system tray
        self.tray_icon = pystray.Icon(
            "timer_app",
            icon_image,
            "Temporizador & Cronómetro",
            menu
        )
        
    def create_default_icon(self):
        """Crea un icono por defecto para el system tray"""
        # Crear un icono simple de 16x16 píxeles
        width = 16
        height = 16
        
        # Crear una imagen con un círculo azul
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        
        # Crear un círculo azul simple
        for x in range(width):
            for y in range(height):
                # Calcular distancia desde el centro
                center_x, center_y = width // 2, height // 2
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                
                if distance <= width // 2:
                    # Color azul para el círculo
                    image.putpixel((x, y), (0, 120, 255, 255))
        
        return image
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    app = TimerApp()
    app.run()

if __name__ == "__main__":
    main()
