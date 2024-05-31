import os
from PyPDF2 import PdfMerger

def merge_pdfs(folder_path, output_path):
    # Cria um objeto PdfMerger
    merger = PdfMerger()
    
    # Percorre todos os arquivos na pasta
    for filename in sorted(os.listdir(folder_path)):
        # Verifica se o arquivo tem extensão .pdf
        if filename.endswith('.pdf'):
            filepath = os.path.join(folder_path, filename)
            # Adiciona o PDF ao objeto PdfMerger
            merger.append(filepath)
            print(f'Adicionado: {filename}')
    
    # Escreve o PDF combinado no caminho de saída
    with open(output_path, 'wb') as f_out:
        merger.write(f_out)
    print(f'PDF combinado salvo como: {output_path}')

# Especifique o caminho da pasta contendo os PDFs e o caminho de saída para o PDF combinado
folder_path = './INSIRA OS ARQUIVOS AQUI'
output_path = './output/setembro-novembro.pdf'

merge_pdfs(folder_path, output_path)