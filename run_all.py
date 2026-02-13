#!/usr/bin/env python3
"""
Script para ejecutar todos los archivos Python en el repositorio.
"""

import os
import subprocess
import sys

# Tiempo máximo de ejecución para cada script (en segundos)
TIMEOUT_SECONDS = 30

def main():
    # Directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_name = os.path.basename(__file__)
    
    # Buscar todos los archivos .py excepto este script
    python_files = [f for f in os.listdir(current_dir) 
                   if f.endswith('.py') and f != script_name]
    
    if not python_files:
        print("No se encontraron archivos Python para ejecutar.")
        return
    
    print("=" * 60)
    print("Ejecutando archivos Python en el repositorio")
    print("=" * 60)
    
    for py_file in sorted(python_files):
        print(f"\n{'='*60}")
        print(f"Ejecutando: {py_file}")
        print("=" * 60)
        
        file_path = os.path.join(current_dir, py_file)
        try:
            result = subprocess.run([sys.executable, file_path], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=TIMEOUT_SECONDS)
            
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"Errores: {result.stderr}", file=sys.stderr)
            
            if result.returncode != 0:
                print(f"⚠️  El archivo {py_file} terminó con código de error {result.returncode}")
            else:
                print(f"✓ {py_file} ejecutado exitosamente")
                
        except subprocess.TimeoutExpired:
            print(f"⚠️  Timeout ejecutando {py_file}")
        except Exception as e:
            print(f"❌ Error ejecutando {py_file}: {e}")
    
    print(f"\n{'='*60}")
    print("Ejecución completada")
    print("=" * 60)

if __name__ == "__main__":
    main()
