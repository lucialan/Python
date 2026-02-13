#!/usr/bin/env python3
"""
Script para ejecutar todos los archivos Python en el repositorio.
Ahora con seguimiento de versiones de salida.
"""

import os
import subprocess
import sys
import json
from datetime import datetime

def get_git_info():
    """Obtiene información del commit actual de git."""
    try:
        commit = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'],
                              capture_output=True, text=True, timeout=5)
        branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                              capture_output=True, text=True, timeout=5)
        return {
            'commit': commit.stdout.strip() if commit.returncode == 0 else 'unknown',
            'branch': branch.stdout.strip() if branch.returncode == 0 else 'unknown'
        }
    except Exception:
        return {'commit': 'unknown', 'branch': 'unknown'}

def save_version_output(current_dir, py_file, output, error, returncode, git_info):
    """Guarda la salida del archivo en el historial de versiones."""
    versions_dir = os.path.join(current_dir, 'versions')
    os.makedirs(versions_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_base = py_file.replace('.py', '')
    
    # Crear entrada de versión
    version_entry = {
        'timestamp': datetime.now().isoformat(),
        'file': py_file,
        'git_commit': git_info['commit'],
        'git_branch': git_info['branch'],
        'output': output,
        'error': error,
        'returncode': returncode
    }
    
    # Guardar en archivo JSON individual
    version_file = os.path.join(versions_dir, f'{file_base}_{timestamp}.json')
    with open(version_file, 'w', encoding='utf-8') as f:
        json.dump(version_entry, f, indent=2, ensure_ascii=False)
    
    # Actualizar índice de versiones
    index_file = os.path.join(versions_dir, 'index.json')
    index = []
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            try:
                index = json.load(f)
            except json.JSONDecodeError:
                index = []
    
    index.append({
        'file': py_file,
        'timestamp': datetime.now().isoformat(),
        'version_file': f'{file_base}_{timestamp}.json',
        'git_commit': git_info['commit']
    })
    
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

def main():
    # Directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Buscar todos los archivos .py excepto este script
    python_files = [f for f in os.listdir(current_dir) 
                   if f.endswith('.py') and f != 'run_all.py' and f != 'view_versions.py']
    
    if not python_files:
        print("No se encontraron archivos Python para ejecutar.")
        return
    
    # Obtener información de git
    git_info = get_git_info()
    
    print("=" * 60)
    print("Ejecutando archivos Python en el repositorio")
    print(f"Git Branch: {git_info['branch']} | Commit: {git_info['commit']}")
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
                                  timeout=30)
            
            # Guardar la salida en el historial de versiones
            save_version_output(current_dir, py_file, result.stdout, 
                              result.stderr, result.returncode, git_info)
            
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
            save_version_output(current_dir, py_file, '', 'Timeout', -1, git_info)
        except Exception as e:
            print(f"❌ Error ejecutando {py_file}: {e}")
            save_version_output(current_dir, py_file, '', str(e), -1, git_info)
    
    print(f"\n{'='*60}")
    print("Ejecución completada")
    print(f"💾 Salidas guardadas en el directorio 'versions/'")
    print("=" * 60)

if __name__ == "__main__":
    main()
