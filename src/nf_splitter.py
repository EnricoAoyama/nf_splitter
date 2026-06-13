# Bibliotecas utilizadas
import logging
import re
from pathlib import Path

from pypdf import PdfReader, PdfWriter

# Configuração do logger para acompanhamento da execução.
# As mensagens são exibidas apenas no terminal.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def limpar_numero_nf(valor):
    """Remove caracteres de formatação do número da NF."""
    return valor.replace(".", "")


def eh_cnpj(numero):
    """Verifica se a sequência possui o tamanho de um CNPJ."""
    return len(numero) == 14


def eh_chave_acesso(numero):
    """Verifica se a sequência possui o tamanho de uma chave de acesso da NF-e."""
    return len(numero) == 44


def eh_nf_valida(numero):
    """
    Considera válido um número de NF com 1 a 9 dígitos,
    ignorando a formatação com pontos.
    """
    n = limpar_numero_nf(numero)
    return 1 <= len(n) <= 9 and n.isdigit()


def localizar_numero_nf(texto):
    """
    Localiza o número da NF-e em um trecho de texto extraído do PDF.

    A busca prioriza valores próximos ao marcador 'Nº'.
    Caso não encontre, utiliza uma busca mais ampla no texto.
    """

    # Normaliza espaços e quebras de linha para facilitar a busca.
    texto = re.sub(r"\s+", " ", texto)

    # Procura números que apareçam próximos ao marcador "Nº".
    candidatos = re.findall(
        r"N[ºo]\.?\s*[:\-]?\s*([\d\.]+)",
        texto,
        flags=re.IGNORECASE
    )

    # Retorna o primeiro candidato que passar pelas validações.
    for c in candidatos:
        n = limpar_numero_nf(c)

        if eh_chave_acesso(n):
            continue

        if eh_cnpj(n):
            continue

        if eh_nf_valida(c):
            return c

    # Busca alternativa para documentos que não seguem o padrão esperado.
    proximos = re.findall(r"([\d\.]{3,})", texto)

    for c in proximos:
        n = limpar_numero_nf(c)

        if eh_chave_acesso(n):
            continue

        if eh_cnpj(n):
            continue

        if eh_nf_valida(c):
            return c

    return None


def pg_count(arquivos):
    """
    Conta o total de páginas contidas nos PDFs informados.
    """
    pg = 0

    for arq in arquivos:
        doc = PdfReader(arq)
        pg += len(doc.pages)

    return pg


def doc_splitter(dir_entrada, dir_saida):
    """
    Divide PDFs multipágina em arquivos individuais.

    Cada página é analisada para identificar o número da NF.
    O PDF gerado é salvo utilizando o número da nota como nome.
    """

    # Obtém todos os PDFs disponíveis para processamento.
    pdfs = [
        f for f in dir_entrada.iterdir()
        if f.is_file() and f.suffix.lower() == ".pdf"
    ]

    logging.info(f"{len(pdfs)} PDF(s) encontrado(s) para processamento.")
    logging.info(f"{pg_count(pdfs)} página(s) nos PDFs de entrada.")

    # Obtém os PDFs já gerados anteriormente.
    nfs = [
        f for f in dir_saida.iterdir()
        if f.is_file() and f.suffix.lower() == ".pdf"
    ]

    logging.info(f"{len(nfs)} NF(s) anteriormente processadas.")
    logging.info("Iniciando processamento dos PDFs.")

    # Processa cada PDF encontrado na pasta de entrada.
    for f in pdfs:
        pdf = PdfReader(f)

        # Cada página é tratada como uma NF independente.
        for pagina in pdf.pages:

            conteudo = pagina.extract_text()

            # Ignora páginas cujo texto não pôde ser extraído.
            if not conteudo:
                logging.warning(f"Página sem texto em {f.name}.")
                continue

            nf = localizar_numero_nf(conteudo)

            # Ignora páginas em que o número da NF não foi identificado.
            if nf is None:
                logging.warning(
                    f"NF não encontrada em {f.name}. Página ignorada."
                )
                continue

            # Substitui pontos para evitar problemas no nome do arquivo.
            nf = nf.replace(".", "_")

            arquivo_saida = dir_saida / f"{nf}.pdf"

            # Evita recriar arquivos já processados anteriormente.
            if arquivo_saida.exists():
                logging.warning(
                    f"{arquivo_saida.name} já existe."
                )

            else:
                writer = PdfWriter()
                writer.add_page(pagina)

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

    doc_splitter(entrada, saida)