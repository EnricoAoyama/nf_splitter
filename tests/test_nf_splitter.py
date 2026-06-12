from pathlib import Path
from pypdf import PdfReader, PdfWriter
from src.nf_splitter import doc_splitter

def criar_pdf_teste(caminho: Path, paginas: int):
    writer = PdfWriter()

    for _ in range(paginas):
        writer.add_blank_page(width=100, height=100)

    with caminho.open("wb") as f:
        writer.write(f)

def test_nf_splitter(tmp_path):
    entrada = tmp_path / "entrada"
    saida = tmp_path / "saida"

    entrada.mkdir()
    saida.mkdir()

    pdf_teste = entrada / "teste.pdf"
    criar_pdf_teste(pdf_teste, 3)

    doc_splitter(entrada, saida)

    arquivos_gerados = sorted(saida.glob("*.pdf"))

    assert len(arquivos_gerados) == 3

    assert (saida / "nf_0.pdf").exists()
    assert (saida / "nf_1.pdf").exists()
    assert (saida / "nf_2.pdf").exists()

    for arquivo in arquivos_gerados:
        pdf = PdfReader(arquivo)
        assert len(pdf.pages) == 1