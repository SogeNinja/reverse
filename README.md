# ⏰ Temporizador & Cronómetro

Una aplicación de escritorio moderna para Windows con temporizador, cronómetro y funcionalidad de system tray.

## ✨ Características

- **⏰ Temporizador**: Cuenta regresiva configurable con presets rápidos
- **⏱️ Cronómetro**: Cronómetro preciso con marcas de vuelta
- **📱 System Tray**: Ejecución en segundo plano con icono en la bandeja del sistema
- **🎨 Interfaz moderna**: Diseño oscuro con CustomTkinter
- **🚀 Presets rápidos**: 5 min, 10 min, 15 min, 30 min, 1 hora
- **🔄 Funcionalidad completa**: Pausar, continuar, reiniciar

## 🚀 Instalación

### Opción 1: Ejecutar desde código fuente
```bash
# Clonar o descargar el proyecto
cd reverse

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python timer_app.py
```

### Opción 2: Generar instalador
```bash
# Ejecutar el script de construcción
python build_installer.py

# El script creará automáticamente:
# - Temporizador_Installer/ (carpeta del instalador)
# - Temporizador_Installer.zip (archivo comprimido)
```

## 📦 Generar Instalador

El script `build_installer.py` automatiza todo el proceso:

1. **Verifica dependencias** e instala las faltantes
2. **Limpia builds anteriores** para evitar conflictos
3. **Crea ejecutable** usando PyInstaller
4. **Genera instalador** con scripts de instalación/desinstalación
5. **Crea archivo ZIP** listo para distribución

### Requisitos para generar el instalador:
- Python 3.7+
- pip
- Conexión a internet (para descargar dependencias)

## 🎯 Uso

### Temporizador
1. Selecciona la pestaña "⏰ Temporizador"
2. Configura horas, minutos y segundos
3. Usa presets rápidos o ingresa tiempo personalizado
4. Haz clic en "▶️ Iniciar"
5. El temporizador cambiará de color según el tiempo restante

### Cronómetro
1. Selecciona la pestaña "⏱️ Cronómetro"
2. Haz clic en "▶️ Iniciar"
3. Usa "🏁 Marcar Vuelta" para registrar tiempos
4. Pausa o reinicia según necesites

### System Tray
- **Minimizar**: Haz clic en "📥 Minimizar al Tray" o cierra la ventana
- **Mostrar**: Haz clic derecho en el icono del system tray → "Mostrar"
- **Salir**: Haz clic derecho en el icono → "Salir"

## 🛠️ Tecnologías

- **Python 3.7+**: Lenguaje principal
- **CustomTkinter**: Interfaz gráfica moderna
- **PIL/Pillow**: Manejo de imágenes
- **pystray**: Funcionalidad de system tray
- **PyInstaller**: Generación de ejecutables

## 📁 Estructura del Proyecto

```
reverse/
├── timer_app.py          # Aplicación principal
├── build_installer.py    # Script para generar instalador
├── config.py             # Configuración del proyecto
├── requirements.txt      # Dependencias
├── README.md            # Este archivo
└── venv/                # Entorno virtual (se crea automáticamente)
```

## 🔧 Configuración

Puedes personalizar la aplicación editando `config.py`:

- Colores de la interfaz
- Tamaño de la ventana
- Presets del temporizador
- Configuración del system tray

## 📋 Dependencias

### Principales:
- `customtkinter==5.2.0` - Interfaz gráfica
- `pillow==10.0.1` - Manejo de imágenes
- `pystray==0.19.4` - System tray

### Para desarrollo:
- `pyinstaller==6.1.0` - Generar ejecutables

## 🚀 Distribución

Para distribuir tu aplicación:

1. Ejecuta `python build_installer.py`
2. Envía el archivo `Temporizador_Installer.zip`
3. El usuario extrae y ejecuta `Instalar.bat`
4. El programa se instala en el escritorio

## 🐛 Solución de Problemas

### Error: "No se pudo crear el ejecutable"
- Verifica que PyInstaller esté instalado: `pip install pyinstaller`
- Asegúrate de tener permisos de escritura en el directorio

### Error: "Módulo no encontrado"
- Ejecuta `pip install -r requirements.txt`
- Verifica que estés en el entorno virtual correcto

### La aplicación no aparece en el system tray
- Verifica que pystray esté instalado correctamente
- En Windows, busca el icono en "Mostrar iconos ocultos"

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Si tienes problemas o preguntas:

1. Revisa la sección de solución de problemas
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de usar Python 3.7 o superior

---

**¡Disfruta usando tu Temporizador & Cronómetro!** ⏰✨
