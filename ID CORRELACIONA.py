import os
import shutil

# Definindo os caminhos das pastas
base_path = 'AAAA'
listas_path = os.path.join(base_path, 'Listas de Presença')
notas_path = os.path.join(base_path, 'Notas')
final_path = os.path.join(base_path, 'FINAL')

# Cria a pasta FINAL se não existir
if not os.path.exists(final_path):
    os.makedirs(final_path)

# Função para obter o ID de um arquivo
def get_id_from_filename(filename, position):
    if position == 'end':
        return filename.split('-')[-1].split('.')[0].strip()
    elif position == 'start':
        return filename.split(' ')[0].strip()
    return None

# Processa os arquivos de Listas de Presença
for lista_file in os.listdir(listas_path):
    if lista_file.endswith('.pdf'):
        lista_id = get_id_from_filename(lista_file, 'end')
        lista_dest_path = os.path.join(final_path, lista_id)
        if not os.path.exists(lista_dest_path):
            os.makedirs(lista_dest_path)
        shutil.copy(os.path.join(listas_path, lista_file), os.path.join(lista_dest_path, lista_file))

# Processa os arquivos de Notas
for nota_file in os.listdir(notas_path):
    if nota_file.endswith('.pdf'):
        nota_id = get_id_from_filename(nota_file, 'start')
        nota_dest_path = os.path.join(final_path, nota_id)
        if not os.path.exists(nota_dest_path):
            os.makedirs(nota_dest_path)
        shutil.copy(os.path.join(notas_path, nota_file), os.path.join(nota_dest_path, nota_file))

print("Arquivos copiados e organizados com sucesso.")