#bibliotecas utilizadas
import logging
from pathlib import Path
from pypdf import PdfReader, PdfWriter

# configurações do log (sem exportação)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def loc_nnf(num):  # a terminar <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    return f"nf_{num}"

def pg_count(arquivos): # contador de páginas dentro do diretório
    pg = 0
    for arq in arquivos:
        doc = PdfReader(arq)
        pg += len(doc.pages)
    return pg

def pdf_splitter(dir_entrada,dir_saida):
    """
 descrição
    """
    # lista todos os arquivos .pdf dentro do diretório de entrada
    pdfs = [
        f for f in dir_entrada.iterdir()
        if f.is_file() and f.suffix.lower() == ".pdf"
    ]
    logging.info(f"{len(pdfs)} PDF(s) encontrado(s) para processamento.")

    # idem para o diretório de saída
    nfs = [
        f for f in dir_saida.iterdir()
        if f.is_file() and f.suffix.lower() == ".pdf"
    ]
    logging.info(f"{len(nfs)} NF(s) anteriormente processadas.")

    logging.info(f"{pg_count(pdfs) - pg_count(nfs)} página(s) a serem processadas.")
    logging.info("Iniciando processamento dos PDFs.")

    # olha cada .pdf dentro do diretório de entrada
    for f in pdfs:
        pdf = PdfReader(f)

        # olha cada página dentro do documento
        for pagina in pdf.pages:
            writer = PdfWriter()
            writer.add_page(pagina)

            nf = loc_nnf(1) # a terminar <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

            arquivo_saida = dir_saida / f"{nf}.pdf"

            # verifica se a nf contida naquela página já foi processada anteriormente
            if arquivo_saida.exists():
                logging.warning(f"{arquivo_saida.name} já existe.") # se sim, avisa que tal nf já existe.

            # se não, cria um arquivo para a nf com o devido nome.
            else:
                with arquivo_saida.open("wb") as output:
                    writer.write(output)
                logging.info(f"{arquivo_saida.name} criado.")

    logging.info("Processamento concluído.")

if __name__ == '__main__':
    path = Path.cwd()

    entrada = path.parent / "data" / "in_PDFs"
    entrada.mkdir(parents=True, exist_ok=True)

    saida = path.parent / "data" / "out_NFs"
    saida.mkdir(parents=True, exist_ok=True)

    pdf_splitter(entrada,saida)