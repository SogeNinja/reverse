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

def create_default_icon():
    """Crea un icono por defecto si no existe"""
    if os.path.exists('icon.ico'):
        return True
    
    print("🎨 Creando icono por defecto...")
    
    try:
        from PIL import Image, ImageDraw
        
        # Crear una imagen 256x256 con fondo transparente
        img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Dibujar un círculo azul (representando un cronómetro)
        center = (128, 128)
        radius = 100
        draw.ellipse([center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius], 
                    fill=(70, 130, 180, 255), outline=(0, 0, 139, 255), width=3)
        
        # Dibujar manecillas del reloj
        # Manecilla de segundos (roja)
        draw.line([center, (center[0], center[1]-80)], fill=(255, 0, 0, 255), width=3)
        # Manecilla de minutos (azul)
        draw.line([center, (center[0]+40, center[1])], fill=(0, 0, 139, 255), width=4)
        # Manecilla de horas (negro)
        draw.line([center, (center[0], center[1]+30)], fill=(0, 0, 0, 255), width=5)
        
        # Punto central
        draw.ellipse([center[0]-5, center[1]-5, center[0]+5, center[1]+5], fill=(0, 0, 0, 255))
        
        # Guardar como ICO
        img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
        print("✅ Icono por defecto creado: icon.ico")
        return True
        
    except ImportError:
        print("⚠️  Pillow no disponible, no se puede crear icono personalizado")
        return False
    except Exception as e:
        print(f"⚠️  Error al crear icono: {e}")
        return False

def create_executable():
    """Crea el ejecutable usando PyInstaller"""
    print("🔨 Creando ejecutable...")
    
    # Crear icono por defecto si no existe
    create_default_icon()
    
    # Configuración de PyInstaller
    pyinstaller_cmd = [
        'pyinstaller',
        '--onefile',                    # Archivo único
        '--windowed',                   # Sin consola
        '--name=Temporizador',          # Nombre del ejecutable
        '--icon=icon.ico',              # Icono personalizado
        '--add-data=venv/Lib/site-packages/customtkinter;customtkinter',  # Incluir CustomTkinter
        '--hidden-import=PIL._tkinter_finder',  # Import oculto necesario
        '--hidden-import=pystray._util.win32',   # Import para Windows
        '--clean',                      # Limpiar cache
        'timer_app.py'                  # Archivo principal
    ]
    
    try:
        subprocess.check_call(pyinstaller_cmd)
        print("✅ Ejecutable creado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al crear el ejecutable: {e}")
        return False

def create_shortcut_script():
    """Crea un script PowerShell para crear el acceso directo con icono"""
    script_content = '''@echo off
echo Creando acceso directo con icono personalizado...
echo.

REM Crear acceso directo usando PowerShell
powershell -Command "& {
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Temporizador.lnk')
    $Shortcut.TargetPath = '%USERPROFILE%\\Desktop\\Temporizador.exe'
    $Shortcut.WorkingDirectory = '%USERPROFILE%\\Desktop'
    $Shortcut.IconLocation = '%USERPROFILE%\\Desktop\\Temporizador.exe,0'
    $Shortcut.Description = 'Temporizador y Cronómetro'
    $Shortcut.Save()
    
    Write-Host 'Acceso directo creado exitosamente con icono personalizado!'
}"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Acceso directo creado exitosamente!
    echo El programa se encuentra en tu escritorio con icono personalizado.
) else (
    echo.
    echo Se creo el programa pero hubo un problema con el acceso directo.
    echo Puedes ejecutar directamente Temporizador.exe
)
echo.
pause
'''
    return script_content

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
    
    # Copiar icono si existe
    if os.path.exists('icon.ico'):
        shutil.copy2('icon.ico', install_dir)
        print("✅ Icono copiado al instalador")
    
    # Crear archivo de instalación batch mejorado
    install_bat = os.path.join(install_dir, "Instalar.bat")
    with open(install_bat, 'w', encoding='utf-8') as f:
        f.write('@echo off\n')
        f.write('echo Instalando Temporizador y Cronometro...\n')
        f.write('echo.\n')
        f.write('if not exist "%USERPROFILE%\\Desktop" mkdir "%USERPROFILE%\\Desktop"\n')
        f.write('copy "Temporizador.exe" "%USERPROFILE%\\Desktop\\"\n')
        f.write('echo.\n')
        f.write('echo Creando acceso directo con icono personalizado...\n')
        f.write('echo.\n')
        f.write('REM Crear acceso directo usando VBScript (mas compatible)\n')
        f.write('echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs\n')
        f.write('echo sLinkFile = "%USERPROFILE%\\Desktop\\Temporizador.lnk" >> CreateShortcut.vbs\n')
        f.write('echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs\n')
        f.write('echo oLink.TargetPath = "%USERPROFILE%\\Desktop\\Temporizador.exe" >> CreateShortcut.vbs\n')
        f.write('echo oLink.WorkingDirectory = "%USERPROFILE%\\Desktop" >> CreateShortcut.vbs\n')
        f.write('echo oLink.IconLocation = "%USERPROFILE%\\Desktop\\Temporizador.exe,0" >> CreateShortcut.vbs\n')
        f.write('echo oLink.Description = "Temporizador y Cronometro" >> CreateShortcut.vbs\n')
        f.write('echo oLink.Save >> CreateShortcut.vbs\n')
        f.write('cscript //nologo CreateShortcut.vbs\n')
        f.write('if %ERRORLEVEL% EQU 0 (\n')
        f.write('    echo Acceso directo creado exitosamente!\n')
        f.write('    echo El programa se encuentra en tu escritorio con icono personalizado.\n')
        f.write(') else (\n')
        f.write('    echo Se creo el programa pero hubo un problema con el acceso directo.\n')
        f.write('    echo Puedes ejecutar directamente Temporizador.exe\n')
        f.write(')\n')
        f.write('del CreateShortcut.vbs\n')
        f.write('echo.\n')
        f.write('echo Instalacion completada!\n')
        f.write('pause\n')
    
    print("✅ Archivo de instalación batch mejorado creado")
    
    # Crear archivo README actualizado
    readme_file = os.path.join(install_dir, "README.txt")
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write("TEMPORIZADOR & CRONÓMETRO\n")
        f.write("=" * 30 + "\n\n")
        f.write("INSTRUCCIONES DE INSTALACIÓN:\n")
        f.write("1. Ejecuta 'Instalar.bat' como administrador\n")
        f.write("2. El programa se instalará en tu escritorio\n")
        f.write("3. Se creará un acceso directo con icono personalizado\n")
        f.write("4. Haz doble clic en 'Temporizador.exe' o en el acceso directo\n\n")
        f.write("CARACTERÍSTICAS:\n")
        f.write("- Temporizador con cuenta regresiva\n")
        f.write("- Cronómetro con marcas de vuelta\n")
        f.write("- Ejecución en segundo plano\n")
        f.write("- Icono en la bandeja del sistema\n")
        f.write("- Icono personalizado en el escritorio\n\n")
        f.write("NOTAS:\n")
        f.write("- El programa se ejecuta en segundo plano\n")
        f.write("- Para cerrar completamente, haz clic derecho en el icono del system tray\n")
        f.write("- Selecciona 'Salir' para cerrar la aplicación\n")
        f.write("- El acceso directo tendrá el mismo icono que el programa\n")
    
    print("✅ Archivo README actualizado creado")
    
    # Crear archivo de desinstalación mejorado
    uninstall_bat = os.path.join(install_dir, "Desinstalar.bat")
    with open(uninstall_bat, 'w', encoding='utf-8') as f:
        f.write('@echo off\n')
        f.write('echo Desinstalando Temporizador y Cronometro...\n')
        f.write('echo.\n')
        f.write('if exist "%USERPROFILE%\\Desktop\\Temporizador.exe" (\n')
        f.write('    del "%USERPROFILE%\\Desktop\\Temporizador.exe"\n')
        f.write('    echo Programa desinstalado del escritorio.\n')
        f.write(') else (\n')
        f.write('    echo El programa no estaba instalado.\n')
        f.write(')\n')
        f.write('if exist "%USERPROFILE%\\Desktop\\Temporizador.lnk" (\n')
        f.write('    del "%USERPROFILE%\\Desktop\\Temporizador.lnk"\n')
        f.write('    echo Acceso directo eliminado del escritorio.\n')
        f.write(') else (\n')
        f.write('    echo No se encontró acceso directo para eliminar.\n')
        f.write(')\n')
        f.write('echo.\n')
        f.write('echo Desinstalacion completada!\n')
        f.write('pause\n')
    
    print("✅ Archivo de desinstalación mejorado creado")
    
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
    print("   - Temporizador.exe (programa principal con icono personalizado)")
    print("   - icon.ico (icono personalizado)")
    print("   - Instalar.bat (script de instalación mejorado)")
    print("   - Desinstalar.bat (script de desinstalación mejorado)")
    print("   - README.txt (instrucciones actualizadas)")
    print()
    print("🚀 Para distribuir:")
    print("   1. Envía el archivo 'Temporizador_Installer.zip'")
    print("   2. El usuario debe extraer y ejecutar 'Instalar.bat'")
    print("   3. Se creará un acceso directo con icono personalizado")
    print()
    
    input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
