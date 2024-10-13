import os

def print_directory_contents(path, indent=0):
  # Imprime el nombre del directorio o archivo
  print(' ' * indent + os.path.basename(path) + '/')
  
  # Si es un directorio, recorre su contenido
  if os.path.isdir(path):
      for item in os.listdir(path):
          item_path = os.path.join(path, item)
          print_directory_contents(item_path, indent + 4)  # Aumenta la indentación para los subelementos

# Cambia esta ruta al directorio que deseas imprimir
base_directory = os.path.abspath(os.path.dirname(__file__))  # Directorio actual
print_directory_contents(base_directory)