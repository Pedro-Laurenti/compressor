import os
import subprocess
import fitz  # PyMuPDF
from tqdm import tqdm
import shutil

def convert_pdf_to_images(input_pdf, output_folder):
    pdf_document = fitz.open(input_pdf)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(dpi=150)  # Ajuste o DPI conforme necessário
        output_image_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        pix.save(output_image_path)
    return len(pdf_document)

def create_pdf_from_images(image_folder, output_pdf):
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

def process_directory(directory):
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    
    total_files = len(pdf_files)
    
    with tqdm(total=total_files, desc='Processando PDF(s)', bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} {percentage:3.0f}%') as pbar:
        for pdf_file in pdf_files:
            input_file_path = pdf_file
            output_folder = os.path.join(os.path.dirname(pdf_file), 'temp_images')
            os.makedirs(output_folder, exist_ok=True)

            # Converter PDF em imagens
            convert_pdf_to_images(input_file_path, output_folder)

            # Criar um novo PDF a partir das imagens
            temp_pdf_path = os.path.join(os.path.dirname(pdf_file), f'temp_{os.path.basename(pdf_file)}')
            create_pdf_from_images(output_folder, temp_pdf_path)

            # Comprimir o novo PDF
            output_file_path = os.path.join(os.path.dirname(pdf_file), f'comp_{os.path.basename(pdf_file)}')
            compress_pdf(temp_pdf_path, output_file_path)

            # Copiar o PDF original para uma nova pasta
            destination_folder = os.path.join(directory, 'COMPRIMIDO', os.path.relpath(os.path.dirname(pdf_file), directory))
            os.makedirs(destination_folder, exist_ok=True)
            shutil.move(output_file_path, destination_folder)

            # Limpar arquivos temporários
            os.remove(temp_pdf_path)
            for img_file in os.listdir(output_folder):
                os.remove(os.path.join(output_folder, img_file))
            os.rmdir(output_folder)

            pbar.set_postfix({'current_file': os.path.basename(pdf_file)})
            pbar.update(1)

def clear_terminal():
    print("\033[H\033[J", end="")

if __name__ == '__main__':
    directory_to_process = 'INSIRA OS ARQUIVOS AQUI'
    clear_terminal()
    process_directory(directory_to_process)


