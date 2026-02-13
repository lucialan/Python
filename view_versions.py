#!/usr/bin/env python3
"""
Script para ver el historial de versiones de salidas de archivos Python.
"""

import os
import json
import sys
from datetime import datetime

def load_index():
    """Carga el índice de versiones."""
    versions_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'versions')
    index_file = os.path.join(versions_dir, 'index.json')
    
    if not os.path.exists(index_file):
        return []
    
    with open(index_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_version(version_file):
    """Carga un archivo de versión específico."""
    versions_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'versions')
    file_path = os.path.join(versions_dir, version_file)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_versions(file_filter=None):
    """Lista todas las versiones disponibles."""
    index = load_index()
    
    if not index:
        print("No hay versiones guardadas aún.")
        print("Ejecuta 'python3 run_all.py' primero para generar versiones.")
        return
    
    print("=" * 80)
    print("HISTORIAL DE VERSIONES")
    print("=" * 80)
    
    # Agrupar por archivo
    files_dict = {}
    for entry in index:
        file_name = entry['file']
        if file_filter and file_filter not in file_name:
            continue
        if file_name not in files_dict:
            files_dict[file_name] = []
        files_dict[file_name].append(entry)
    
    for file_name, versions in sorted(files_dict.items()):
        print(f"\n📄 {file_name}")
        print("-" * 80)
        for i, version in enumerate(reversed(versions), 1):
            timestamp = datetime.fromisoformat(version['timestamp'])
            print(f"  {i}. {timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
                  f"Commit: {version['git_commit']} | "
                  f"Archivo: {version['version_file']}")
    
    print("\n" + "=" * 80)

def show_version_output(file_name, version_number=1):
    """Muestra la salida de una versión específica."""
    index = load_index()
    
    # Filtrar versiones del archivo
    file_versions = [v for v in index if v['file'] == file_name]
    
    if not file_versions:
        print(f"No se encontraron versiones para {file_name}")
        return
    
    # Ordenar por timestamp (más reciente primero)
    file_versions.sort(key=lambda x: x['timestamp'], reverse=True)
    
    if version_number > len(file_versions):
        print(f"Solo hay {len(file_versions)} versión(es) para {file_name}")
        return
    
    version_entry = file_versions[version_number - 1]
    version_data = load_version(version_entry['version_file'])
    
    print("=" * 80)
    print(f"SALIDA DE: {file_name}")
    print(f"Versión {version_number} de {len(file_versions)}")
    print(f"Fecha: {datetime.fromisoformat(version_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Commit: {version_data['git_commit']} | Branch: {version_data['git_branch']}")
    print("=" * 80)
    
    if version_data['output']:
        print("\n--- SALIDA ---")
        print(version_data['output'])
    
    if version_data['error']:
        print("\n--- ERRORES ---")
        print(version_data['error'])
    
    if version_data['returncode'] != 0:
        print(f"\n⚠️  Código de retorno: {version_data['returncode']}")
    else:
        print("\n✓ Ejecución exitosa")
    
    print("=" * 80)

def compare_versions(file_name, version1=1, version2=2):
    """Compara dos versiones del mismo archivo."""
    index = load_index()
    
    # Filtrar versiones del archivo
    file_versions = [v for v in index if v['file'] == file_name]
    
    if not file_versions:
        print(f"No se encontraron versiones para {file_name}")
        return
    
    # Ordenar por timestamp (más reciente primero)
    file_versions.sort(key=lambda x: x['timestamp'], reverse=True)
    
    if version1 > len(file_versions) or version2 > len(file_versions):
        print(f"Solo hay {len(file_versions)} versión(es) para {file_name}")
        return
    
    v1_data = load_version(file_versions[version1 - 1]['version_file'])
    v2_data = load_version(file_versions[version2 - 1]['version_file'])
    
    print("=" * 80)
    print(f"COMPARACIÓN DE VERSIONES: {file_name}")
    print("=" * 80)
    
    print(f"\nVERSIÓN {version1}:")
    print(f"  Fecha: {datetime.fromisoformat(v1_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Commit: {v1_data['git_commit']}")
    print(f"  Salida:\n{v1_data['output']}")
    
    print(f"\nVERSIÓN {version2}:")
    print(f"  Fecha: {datetime.fromisoformat(v2_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Commit: {v2_data['git_commit']}")
    print(f"  Salida:\n{v2_data['output']}")
    
    if v1_data['output'] == v2_data['output']:
        print("\n✓ Las salidas son idénticas")
    else:
        print("\n⚠️  Las salidas son diferentes")
    
    print("=" * 80)

def show_help():
    """Muestra la ayuda del programa."""
    print("""
USO: python3 view_versions.py [comando] [argumentos]

COMANDOS:
  list [archivo]              Lista todas las versiones (opcionalmente filtrado por archivo)
  show <archivo> [version]    Muestra la salida de una versión específica (por defecto: versión 1 = más reciente)
  compare <archivo> [v1] [v2] Compara dos versiones (por defecto: v1=1, v2=2)
  help                        Muestra esta ayuda

EJEMPLOS:
  python3 view_versions.py list
  python3 view_versions.py list hola_mundo
  python3 view_versions.py show hola_mundo.py
  python3 view_versions.py show hola_mundo.py 2
  python3 view_versions.py compare leccion1.py 1 2
    """)

def main():
    if len(sys.argv) < 2:
        list_versions()
        return
    
    command = sys.argv[1]
    
    if command == 'help':
        show_help()
    elif command == 'list':
        file_filter = sys.argv[2] if len(sys.argv) > 2 else None
        list_versions(file_filter)
    elif command == 'show':
        if len(sys.argv) < 3:
            print("Error: Debes especificar un archivo")
            show_help()
            return
        file_name = sys.argv[2]
        version = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        show_version_output(file_name, version)
    elif command == 'compare':
        if len(sys.argv) < 3:
            print("Error: Debes especificar un archivo")
            show_help()
            return
        file_name = sys.argv[2]
        v1 = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        v2 = int(sys.argv[4]) if len(sys.argv) > 4 else 2
        compare_versions(file_name, v1, v2)
    else:
        print(f"Comando desconocido: {command}")
        show_help()

if __name__ == "__main__":
    main()
