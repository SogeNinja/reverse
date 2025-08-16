"""
Configuración del proyecto Temporizador & Cronómetro
"""

# Configuración de la aplicación
APP_NAME = "Temporizador & Cronómetro"
APP_VERSION = "0.1.0"
APP_AUTHOR = "SogeNinja"
APP_DESCRIPTION = "Aplicación de temporizador y cronómetro con system tray"

# Configuración de la ventana
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 250
WINDOW_RESIZABLE = False

# Configuración de colores
COLORS = {
    'primary': '#1f538d',
    'secondary': '#14375e',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

# Configuración de temporizador
TIMER_PRESETS = [
    ("5 min", 5),
    ("10 min", 10),
    ("15 min", 15),
    ("30 min", 30),
    ("1 hora", 60)
]

# Configuración del system tray
TRAY_ICON_SIZE = 16
TRAY_ICON_COLOR = (0, 120, 255, 255)  # Azul con transparencia
