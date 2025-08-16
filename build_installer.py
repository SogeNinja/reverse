#!/usr/bin/env python3
"""
Script para generar un instalador de la aplicación Temporizador & Cronómetro
Autor: Tu Nombre
Fecha: 2024
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Muestra el banner del script"""
    print("=" * 60)
    print("🔧 GENERADOR DE INSTALADOR - TEMPORIZADOR & CRONÓMETRO")
    print("=" * 60)
    print()

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("📋 Verificando dependencias...")
    
    required_packages = [
        'customtkinter',
        'pillow', 
        'pystray',
        'pyinstaller'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - NO INSTALADO")
    
    if missing_packages:
        print(f"\n⚠️  Paquetes faltantes: {', '.join(missing_packages)}")
        print("Instalando paquetes faltantes...")
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ {package} instalado correctamente")
            except subprocess.CalledProcessError:
                print(f"❌ Error al instalar {package}")
                return False
    
    print("✅ Todas las dependencias están instaladas\n")
    return True

def clean_build_dirs():
    """Limpia directorios de build anteriores"""
    print("🧹 Limpiando directorios de build anteriores...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ {dir_name} eliminado")
    
    # Limpiar archivos .spec
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"✅ {spec_file} eliminado")
    
    print()

def create_executable():
    """Crea el ejecutable usando PyInstaller"""
    print("🔨 Creando ejecutable...")
    
    # Configuración de PyInstaller
    pyinstaller_cmd = [
        'pyinstaller',
        '--onefile',                    # Archivo único
        '--windowed',                   # Sin consola
        '--name=Temporizador',          # Nombre del ejecutable
        '--icon=icon.ico',              # Icono (si existe)
        '--add-data=venv/Lib/site-packages/customtkinter;customtkinter',  # Incluir CustomTkinter
        '--hidden-import=PIL._tkinter_finder',  # Import oculto necesario
        '--hidden-import=pystray._util.win32',   # Import para Windows
        '--clean',                      # Limpiar cache
        'timer_app.py'                  # Archivo principal
    ]
    
    # Si no existe icon.ico, remover esa opción
    if not os.path.exists('icon.ico'):
        pyinstaller_cmd.remove('--icon=icon.ico')
        print("⚠️  No se encontró icon.ico, usando icono por defecto")
    
    try:
        subprocess.check_call(pyinstaller_cmd)
        print("✅ Ejecutable creado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al crear el ejecutable: {e}")
        return False

def create_installer():
    """Crea un instalador simple"""
    print("📦 Creando instalador...")
    
    # Crear directorio de instalación
    install_dir = "Temporizador_Installer"
    if os.path.exists(install_dir):
        shutil.rmtree(install_dir)
    
    os.makedirs(install_dir)
    
    # Copiar ejecutable
    exe_source = "dist/Temporizador.exe"
    if os.path.exists(exe_source):
        shutil.copy2(exe_source, install_dir)
        print("✅ Ejecutable copiado al instalador")
    else:
        print("❌ No se encontró el ejecutable")
        return False
    
    # Crear archivo de instalación batch
    install_bat = os.path.join(install_dir, "Instalar.bat")
    with open(install_bat, 'w', encoding='utf-8') as f:
        f.write('@echo off\n')
        f.write('echo Instalando Temporizador & Cronometro...\n')
        f.write('echo.\n')
        f.write('if not exist "%USERPROFILE%\\Desktop" mkdir "%USERPROFILE%\\Desktop"\n')
        f.write('copy "Temporizador.exe" "%USERPROFILE%\\Desktop\\"\n')
        f.write('echo.\n')
        f.write('echo Instalacion completada!\n')
        f.write('echo El programa se encuentra en tu escritorio.\n')
        f.write('pause\n')
    
    print("✅ Archivo de instalación batch creado")
    
    # Crear archivo README
    readme_file = os.path.join(install_dir, "README.txt")
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write("TEMPORIZADOR & CRONÓMETRO\n")
        f.write("=" * 30 + "\n\n")
        f.write("INSTRUCCIONES DE INSTALACIÓN:\n")
        f.write("1. Ejecuta 'Instalar.bat' como administrador\n")
        f.write("2. El programa se instalará en tu escritorio\n")
        f.write("3. Haz doble clic en 'Temporizador.exe' para ejecutar\n\n")
        f.write("CARACTERÍSTICAS:\n")
        f.write("- Temporizador con cuenta regresiva\n")
        f.write("- Cronómetro con marcas de vuelta\n")
        f.write("- Ejecución en segundo plano\n")
        f.write("- Icono en la bandeja del sistema\n\n")
        f.write("NOTAS:\n")
        f.write("- El programa se ejecuta en segundo plano\n")
        f.write("- Para cerrar completamente, haz clic derecho en el icono del system tray\n")
        f.write("- Selecciona 'Salir' para cerrar la aplicación\n")
    
    print("✅ Archivo README creado")
    
    # Crear archivo de desinstalación
    uninstall_bat = os.path.join(install_dir, "Desinstalar.bat")
    with open(uninstall_bat, 'w', encoding='utf-8') as f:
        f.write('@echo off\n')
        f.write('echo Desinstalando Temporizador & Cronometro...\n')
        f.write('echo.\n')
        f.write('if exist "%USERPROFILE%\\Desktop\\Temporizador.exe" (\n')
        f.write('    del "%USERPROFILE%\\Desktop\\Temporizador.exe"\n')
        f.write('    echo Programa desinstalado del escritorio.\n')
        f.write(') else (\n')
        f.write('    echo El programa no estaba instalado.\n')
        f.write(')\n')
        f.write('echo.\n')
        f.write('pause\n')
    
    print("✅ Archivo de desinstalación creado")
    
    return True

def create_zip_installer():
    """Crea un archivo ZIP del instalador"""
    print("🗜️  Creando archivo ZIP del instalador...")
    
    try:
        shutil.make_archive("Temporizador_Installer", 'zip', "Temporizador_Installer")
        print("✅ Archivo ZIP creado: Temporizador_Installer.zip")
        return True
    except Exception as e:
        print(f"❌ Error al crear el ZIP: {e}")
        return False

def main():
    """Función principal"""
    print_banner()
    
    # Verificar dependencias
    if not check_dependencies():
        print("❌ No se pudieron instalar todas las dependencias")
        input("Presiona Enter para salir...")
        return
    
    # Limpiar directorios anteriores
    clean_build_dirs()
    
    # Crear ejecutable
    if not create_executable():
        print("❌ No se pudo crear el ejecutable")
        input("Presiona Enter para salir...")
        return
    
    print()
    
    # Crear instalador
    if not create_installer():
        print("❌ No se pudo crear el instalador")
        input("Presiona Enter para salir...")
        return
    
    # Crear ZIP
    create_zip_installer()
    
    print("\n" + "=" * 60)
    print("🎉 ¡INSTALADOR CREADO EXITOSAMENTE!")
    print("=" * 60)
    print()
    print("📁 Archivos creados:")
    print("   - Temporizador_Installer/ (carpeta del instalador)")
    print("   - Temporizador_Installer.zip (archivo comprimido)")
    print()
    print("📋 Contenido del instalador:")
    print("   - Temporizador.exe (programa principal)")
    print("   - Instalar.bat (script de instalación)")
    print("   - Desinstalar.bat (script de desinstalación)")
    print("   - README.txt (instrucciones)")
    print()
    print("🚀 Para distribuir:")
    print("   1. Envía el archivo 'Temporizador_Installer.zip'")
    print("   2. El usuario debe extraer y ejecutar 'Instalar.bat'")
    print()
    
    input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
