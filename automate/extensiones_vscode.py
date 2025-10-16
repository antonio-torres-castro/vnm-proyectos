#!/usr/bin/env python3
"""
Script simplificado para instalar extensiones recomendadas de VS Code
"""

import subprocess
import shutil

# Lista de extensiones esenciales para el proyecto
EXTENSIONES_ESENCIALES = [
    # Python
    "ms-python.python",
    "ms-python.debugpy",
    # JavaScript/TypeScript/React
    "dsznajder.es7-react-js-snippets",
    "ms-vscode.vscode-typescript-next",
    "bradlc.vscode-tailwindcss",
    # Docker
    "ms-azuretools.vscode-docker",
    # Base de datos
    "cweijan.vscode-database-client2",
    # Utilidades generales
    "redhat.vscode-yaml",
    "ms-vscode.hexeditor",
    # Git
    "eamodio.gitlens",
    # Formateo y linting
    "esbenp.prettier-vscode",
    "ms-python.flake8",
    "ms-python.black-formatter",
]


def instalar_extension(extension_id: str) -> bool:
    """Instala una extensión específica de VS Code"""
    print(f"Instalando: {extension_id}")

    # Verificar que el comando `code` exista en PATH
    code_path = shutil.which("code")
    if not code_path:
        print(" No se encontró el comando 'code' en el PATH.")
        print(" Abre VS Code, presiona Ctrl+Shift+P y ejecuta:")
        print("   Shell Command: Install 'code' command in PATH")
        return False

    try:
        resultado = subprocess.run(
            [code_path, "--install-extension", extension_id, "--force"],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f" {extension_id} instalada correctamente")
        if resultado.stdout.strip():
            print(resultado.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f" Error instalando {extension_id}")
        print(e.stderr.strip() if e.stderr else str(e))
        return False


def main():
    print("Instalador de Extensiones VS Code para vnm-proyectos")
    print("=" * 55)

    print(f"\nInstalando {len(EXTENSIONES_ESENCIALES)} extensiones esenciales...")
    print("-" * 50)

    exitosas = 0
    fallidas = 0

    for extension in EXTENSIONES_ESENCIALES:
        if instalar_extension(extension):
            exitosas += 1
        else:
            fallidas += 1

    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN DE INSTALACIÓN")
    print("=" * 50)
    print(f" Exitosas: {exitosas}")
    print(f" Fallidas: {fallidas}")
    print(f" Total: {len(EXTENSIONES_ESENCIALES)}")

    if fallidas == 0:
        print(" Todas las extensiones se instalaron correctamente.")
        print(" Reinicia VS Code para activarlas.")
    else:
        print(f" {fallidas} extensiones fallaron. Revisa los mensajes arriba.")

    print("\nExtensiones instaladas/revisadas:")
    for extension in EXTENSIONES_ESENCIALES:
        print(f"  • {extension}")


if __name__ == "__main__":
    main()
