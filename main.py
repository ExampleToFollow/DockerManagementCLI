#!/usr/bin/env python3
"""
Docker Management CLI - Herramienta para gestionar Docker mediante menús interactivos
Autor: Sistema de gestión Docker
Versión: 1.0
"""

import subprocess
import sys
import json
import os
from typing import List, Dict, Optional


class DockerManager:
    """Clase principal para la gestión de Docker"""

    def __init__(self):
        self.check_docker_installed()

    def check_docker_installed(self):
        """Verifica si Docker está instalado y funcionando"""
        try:
            result = subprocess.run(['docker', '--version'],
                                    capture_output=True, text=True, check=True)
            print(f"✅ Docker detectado: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Docker no está instalado o no está en el PATH")
            sys.exit(1)

    def run_command(self, command: List[str]) -> Optional[str]:
        """Ejecuta un comando de Docker y retorna el resultado"""
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"❌ Error ejecutando comando: {e.stderr.strip()}")
            return None

    def run_command_interactive(self, command: List[str]) -> bool:
        """Ejecuta un comando de Docker de forma interactiva"""
        try:
            result = subprocess.run(command, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False


class ImageManager:
    """Gestión de imágenes Docker"""

    def __init__(self, docker_manager: DockerManager):
        self.dm = docker_manager

    def list_images(self):
        """Lista todas las imágenes Docker"""
        print("\n📦 IMÁGENES DOCKER DISPONIBLES:")
        print("-" * 80)

        result = self.dm.run_command(['docker', 'images', '--format',
                                      'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}\t{{.CreatedSince}}'])
        if result:
            print(result)
        else:
            print("No se pudieron listar las imágenes")

    def pull_image(self):
        """Descarga una imagen desde Docker Hub"""
        print("\n⬇️ DESCARGAR IMAGEN")
        image_name = input("Ingresa el nombre de la imagen (ej: nginx:latest): ").strip()

        if not image_name:
            print("❌ Nombre de imagen no puede estar vacío")
            return

        print(f"Descargando imagen: {image_name}...")
        if self.dm.run_command_interactive(['docker', 'pull', image_name]):
            print(f"✅ Imagen {image_name} descargada exitosamente")
        else:
            print(f"❌ Error al descargar la imagen {image_name}")

    def remove_image(self):
        """Elimina una imagen Docker"""
        self.list_images()
        print("\n🗑️ ELIMINAR IMAGEN")
        image_id = input("Ingresa el ID o nombre de la imagen a eliminar: ").strip()

        if not image_id:
            print("❌ ID de imagen no puede estar vacío")
            return

        confirm = input(f"¿Estás seguro de eliminar la imagen {image_id}? (s/N): ").strip().lower()
        if confirm == 's':
            if self.dm.run_command(['docker', 'rmi', image_id]):
                print(f"✅ Imagen {image_id} eliminada exitosamente")
            else:
                print(f"❌ Error al eliminar la imagen {image_id}")

    def build_image(self):
        """Construye una imagen desde un Dockerfile"""
        print("\n🔨 CONSTRUIR IMAGEN")
        dockerfile_path = input("Ruta del directorio con Dockerfile (. para actual): ").strip() or "."
        image_name = input("Nombre para la nueva imagen: ").strip()

        if not image_name:
            print("❌ Nombre de imagen no puede estar vacío")
            return

        if not os.path.exists(f"{dockerfile_path}/Dockerfile"):
            print(f"❌ No se encontró Dockerfile en {dockerfile_path}")
            return

        print(f"Construyendo imagen {image_name}...")
        if self.dm.run_command_interactive(['docker', 'build', '-t', image_name, dockerfile_path]):
            print(f"✅ Imagen {image_name} construida exitosamente")
        else:
            print(f"❌ Error al construir la imagen {image_name}")


class ContainerManager:
    """Gestión de contenedores Docker"""

    def __init__(self, docker_manager: DockerManager):
        self.dm = docker_manager

    def list_containers(self, all_containers=True):
        """Lista contenedores Docker"""
        status = "TODOS LOS CONTENEDORES" if all_containers else "CONTENEDORES ACTIVOS"
        print(f"\n🐳 {status}:")
        print("-" * 100)

        cmd = ['docker', 'ps', '--format',
               'table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}']
        if all_containers:
            cmd.insert(2, '-a')

        result = self.dm.run_command(cmd)
        if result:
            print(result)
        else:
            print("No se pudieron listar los contenedores")

    def run_container(self):
        """Ejecuta un nuevo contenedor"""
        print("\n🚀 EJECUTAR CONTENEDOR")
        image_name = input("Nombre de la imagen: ").strip()
        container_name = input("Nombre del contenedor (opcional): ").strip()
        port_mapping = input("Mapeo de puertos (ej: 8080:80, opcional): ").strip()

        if not image_name:
            print("❌ Nombre de imagen no puede estar vacío")
            return

        cmd = ['docker', 'run', '-d']

        if container_name:
            cmd.extend(['--name', container_name])

        if port_mapping:
            cmd.extend(['-p', port_mapping])

        cmd.append(image_name)

        result = self.dm.run_command(cmd)
        if result:
            print(f"✅ Contenedor iniciado con ID: {result[:12]}")
        else:
            print("❌ Error al iniciar el contenedor")

    def stop_container(self):
        """Detiene un contenedor"""
        self.list_containers()
        print("\n⏹️ DETENER CONTENEDOR")
        container_id = input("ID o nombre del contenedor a detener: ").strip()

        if not container_id:
            print("❌ ID de contenedor no puede estar vacío")
            return

        if self.dm.run_command(['docker', 'stop', container_id]):
            print(f"✅ Contenedor {container_id} detenido")
        else:
            print(f"❌ Error al detener el contenedor {container_id}")

    def start_container(self):
        """Inicia un contenedor detenido"""
        self.list_containers()
        print("\n▶️ INICIAR CONTENEDOR")
        container_id = input("ID o nombre del contenedor a iniciar: ").strip()

        if not container_id:
            print("❌ ID de contenedor no puede estar vacío")
            return

        if self.dm.run_command(['docker', 'start', container_id]):
            print(f"✅ Contenedor {container_id} iniciado")
        else:
            print(f"❌ Error al iniciar el contenedor {container_id}")

    def restart_container(self):
        """Reinicia un contenedor"""
        self.list_containers()
        print("\n🔄 REINICIAR CONTENEDOR")
        container_id = input("ID o nombre del contenedor a reiniciar: ").strip()

        if not container_id:
            print("❌ ID de contenedor no puede estar vacío")
            return

        if self.dm.run_command(['docker', 'restart', container_id]):
            print(f"✅ Contenedor {container_id} reiniciado")
        else:
            print(f"❌ Error al reiniciar el contenedor {container_id}")

    def remove_container(self):
        """Elimina un contenedor"""
        self.list_containers()
        print("\n🗑️ ELIMINAR CONTENEDOR")
        container_id = input("ID o nombre del contenedor a eliminar: ").strip()

        if not container_id:
            print("❌ ID de contenedor no puede estar vacío")
            return

        confirm = input(f"¿Estás seguro de eliminar el contenedor {container_id}? (s/N): ").strip().lower()
        if confirm == 's':
            # Forzar eliminación si está corriendo
            if self.dm.run_command(['docker', 'rm', '-f', container_id]):
                print(f"✅ Contenedor {container_id} eliminado")
            else:
                print(f"❌ Error al eliminar el contenedor {container_id}")

    def view_logs(self):
        """Ver logs de un contenedor"""
        self.list_containers()
        print("\n📋 VER LOGS")
        container_id = input("ID o nombre del contenedor: ").strip()

        if not container_id:
            print("❌ ID de contenedor no puede estar vacío")
            return

        print(f"\n📋 Logs del contenedor {container_id}:")
        print("-" * 60)
        self.dm.run_command_interactive(['docker', 'logs', '--tail', '50', container_id])

    def exec_container(self):
        """Ejecutar comando en contenedor"""
        self.list_containers(all_containers=False)
        print("\n💻 EJECUTAR COMANDO EN CONTENEDOR")
        container_id = input("ID o nombre del contenedor: ").strip()

        if not container_id:
            print("❌ ID de contenedor no puede estar vacío")
            return

        print("Iniciando shell interactivo en el contenedor...")
        self.dm.run_command_interactive(['docker', 'exec', '-it', container_id, '/bin/bash'])


class SystemManager:
    """Gestión del sistema Docker"""

    def __init__(self, docker_manager: DockerManager):
        self.dm = docker_manager

    def system_info(self):
        """Muestra información del sistema Docker"""
        print("\n🔧 INFORMACIÓN DEL SISTEMA DOCKER:")
        print("-" * 50)
        self.dm.run_command_interactive(['docker', 'system', 'info'])

    def system_cleanup(self):
        """Limpia recursos no utilizados"""
        print("\n🧹 LIMPIEZA DEL SISTEMA")
        print("Esto eliminará:")
        print("- Contenedores detenidos")
        print("- Redes no utilizadas")
        print("- Imágenes sin referencia")
        print("- Caché de construcción")

        confirm = input("\n¿Continuar con la limpieza? (s/N): ").strip().lower()
        if confirm == 's':
            if self.dm.run_command_interactive(['docker', 'system', 'prune', '-a', '-f']):
                print("✅ Limpieza completada")
            else:
                print("❌ Error durante la limpieza")

    def disk_usage(self):
        """Muestra uso de disco de Docker"""
        print("\n💾 USO DE DISCO DOCKER:")
        print("-" * 40)
        self.dm.run_command_interactive(['docker', 'system', 'df'])


class DockerCLI:
    """Interfaz principal de línea de comandos"""

    def __init__(self):
        self.docker_manager = DockerManager()
        self.image_manager = ImageManager(self.docker_manager)
        self.container_manager = ContainerManager(self.docker_manager)
        self.system_manager = SystemManager(self.docker_manager)

    def clear_screen(self):
        """Limpia la pantalla"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def show_header(self):
        """Muestra el encabezado de la aplicación"""
        print("=" * 60)
        print("🐳 DOCKER MANAGEMENT CLI")
        print("=" * 60)

    def show_main_menu(self):
        """Muestra el menú principal"""
        print("\n📋 MENÚ PRINCIPAL:")
        print("1. 📦 Gestión de Imágenes")
        print("2. 🐳 Gestión de Contenedores")
        print("3. 🔧 Información del Sistema")
        print("4. 🚪 Salir")
        print("-" * 30)

    def show_image_menu(self):
        """Muestra el menú de gestión de imágenes"""
        print("\n📦 GESTIÓN DE IMÁGENES:")
        print("1. 📋 Listar todas las imágenes")
        print("2. ⬇️ Descargar imagen")
        print("3. 🔨 Construir imagen")
        print("4. 🗑️ Eliminar imagen")
        print("5. ⬅️ Volver al menú principal")
        print("-" * 35)

    def show_container_menu(self):
        """Muestra el menú de gestión de contenedores"""
        print("\n🐳 GESTIÓN DE CONTENEDORES:")
        print("1. 📋 Listar contenedores activos")
        print("2. 📋 Listar todos los contenedores")
        print("3. 🚀 Ejecutar nuevo contenedor")
        print("4. ▶️ Iniciar contenedor")
        print("5. ⏹️ Detener contenedor")
        print("6. 🔄 Reiniciar contenedor")
        print("7. 🗑️ Eliminar contenedor")
        print("8. 📄 Ver logs de contenedor")
        print("9. 💻 Ejecutar comando en contenedor")
        print("10. ⬅️ Volver al menú principal")
        print("-" * 40)

    def show_system_menu(self):
        """Muestra el menú de sistema"""
        print("\n🔧 INFORMACIÓN DEL SISTEMA:")
        print("1. 📊 Información del sistema Docker")
        print("2. 💾 Uso de disco")
        print("3. 🧹 Limpiar sistema")
        print("4. ⬅️ Volver al menú principal")
        print("-" * 35)

    def handle_image_menu(self):
        """Maneja el menú de imágenes"""
        while True:
            self.show_image_menu()
            choice = input("Selecciona una opción: ").strip()

            if choice == '1':
                self.image_manager.list_images()
            elif choice == '2':
                self.image_manager.pull_image()
            elif choice == '3':
                self.image_manager.build_image()
            elif choice == '4':
                self.image_manager.remove_image()
            elif choice == '5':
                break
            else:
                print("❌ Opción inválida")

            input("\nPresiona Enter para continuar...")

    def handle_container_menu(self):
        """Maneja el menú de contenedores"""
        while True:
            self.show_container_menu()
            choice = input("Selecciona una opción: ").strip()

            if choice == '1':
                self.container_manager.list_containers(all_containers=False)
            elif choice == '2':
                self.container_manager.list_containers(all_containers=True)
            elif choice == '3':
                self.container_manager.run_container()
            elif choice == '4':
                self.container_manager.start_container()
            elif choice == '5':
                self.container_manager.stop_container()
            elif choice == '6':
                self.container_manager.restart_container()
            elif choice == '7':
                self.container_manager.remove_container()
            elif choice == '8':
                self.container_manager.view_logs()
            elif choice == '9':
                self.container_manager.exec_container()
            elif choice == '10':
                break
            else:
                print("❌ Opción inválida")

            input("\nPresiona Enter para continuar...")

    def handle_system_menu(self):
        """Maneja el menú de sistema"""
        while True:
            self.show_system_menu()
            choice = input("Selecciona una opción: ").strip()

            if choice == '1':
                self.system_manager.system_info()
            elif choice == '2':
                self.system_manager.disk_usage()
            elif choice == '3':
                self.system_manager.system_cleanup()
            elif choice == '4':
                break
            else:
                print("❌ Opción inválida")

            input("\nPresiona Enter para continuar...")

    def run(self):
        """Ejecuta la aplicación principal"""
        try:
            while True:
                self.show_header()
                self.show_main_menu()
                choice = input("Selecciona una opción: ").strip()

                if choice == '1':
                    self.handle_image_menu()
                elif choice == '2':
                    self.handle_container_menu()
                elif choice == '3':
                    self.handle_system_menu()
                elif choice == '4':
                    print("\n👋 ¡Gracias por usar Docker Management CLI!")
                    break
                else:
                    print("❌ Opción inválida")
                    input("\nPresiona Enter para continuar...")

        except KeyboardInterrupt:
            print("\n\n👋 Aplicación terminada por el usuario")
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")


def main():
    """Función principal"""
    cli = DockerCLI()
    cli.run()


if __name__ == "__main__":
    main()