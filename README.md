# NF Splitter

Ferramenta em Python para processar PDFs contendo múltiplas DANFEs, identificar automaticamente o número da Nota Fiscal e gerar arquivos PDF individuais nomeados pela NF.

## Funcionalidades

- Leitura de PDFs multipágina
- Extração automática do número da NF
- Separação em arquivos individuais
- Renomeação automática dos PDFs gerados

## Tecnologias
- Python
  - pypdf
  - pytest
- regex

## Instalação
pip install -r requirements.txt

## Uso
python src/nf_splitter.py

## Estrutura esperada
```text
data/
├── in_PDFs/
│   └── notas.pdf
└── out_NFs/
```

### Fluxo de execução

```text
in_PDFs/notas.pdf (3 páginas)

          ↓

     nf_splitter

          ↓

out_NFs/
├── 000004726.pdf
├── 000085034.pdf
└── 000002913.pdf
```
