import os
import subprocess
import fitz  # PyMuPDF
from tqdm import tqdm
import shutil

def convert_pdf_to_images(input_pdf, output_folder):
    pdf_document = fitz.open(input_pdf)
    num_pages = len(pdf_document)
    
    # Definir o formato de numeração com zeros à esquerda
    num_digits = len(str(num_pages))
    
    with tqdm(total=num_pages, desc='Convertendo páginas', bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} {percentage:3.0f}%') as pbar:
        for page_num in range(num_pages):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap(dpi=80)
            
            # Nomear a imagem com zeros à esquerda
            output_image_path = os.path.join(output_folder, f"page_{str(page_num + 1).zfill(num_digits)}.png")
            pix.save(output_image_path)
            pbar.update(1)
    
    return num_pages

def create_pdf_from_images(image_folder, output_pdf):
    # Ordenar as imagens de forma correta
    images = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith('.png')])
    document = fitz.open()
    
    for image in images:
        img = fitz.open(image)
        rect = img[0].rect
        pdfbytes = img.convert_to_pdf()
        img_pdf = fitz.open("pdf", pdfbytes)
        page = document.new_page(width=rect.width, height=rect.height)
        page.show_pdf_page(rect, img_pdf, 0)
    
    document.save(output_pdf)

def compress_pdf(input_file_path, output_file_path):
    gs_command = [
        'gs',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        '-dPDFSETTINGS=/screen',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        f'-sOutputFile={output_file_path}',
        input_file_path
    ]
    
    try:
        subprocess.run(gs_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Failed to compress {input_file_path}: {e}')

def process_single_pdf(pdf_file):
    output_folder = os.path.join(os.path.dirname(pdf_file), 'temp_images')
    os.makedirs(output_folder, exist_ok=True)

    # Converter PDF em imagens
    num_pages = convert_pdf_to_images(pdf_file, output_folder)

    # Criar um novo PDF a partir das imagens
    temp_pdf_path = os.path.join(os.path.dirname(pdf_file), f'temp_{os.path.basename(pdf_file)}')
    create_pdf_from_images(output_folder, temp_pdf_path)

    # Comprimir o novo PDF
    output_file_path = os.path.join(os.path.dirname(pdf_file), f'comp_{os.path.basename(pdf_file)}')
    compress_pdf(temp_pdf_path, output_file_path)

    # Mover o PDF comprimido para uma nova pasta
    destination_folder = os.path.join(os.path.dirname(pdf_file), 'COMPRIMIDO')
    os.makedirs(destination_folder, exist_ok=True)
    shutil.move(output_file_path, destination_folder)

    # Limpar arquivos temporários
    os.remove(temp_pdf_path)
    for img_file in os.listdir(output_folder):
        os.remove(os.path.join(output_folder, img_file))
    os.rmdir(output_folder)

def clear_terminal():
    print("\033[H\033[J", end="")

if __name__ == '__main__':
    pdf_to_process = '/home/pedro/Desktop/myenv/03 Listas de Presença.pdf'
    clear_terminal()
    process_single_pdf(pdf_to_process)
