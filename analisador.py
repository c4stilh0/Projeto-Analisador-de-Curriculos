import os
import re
from docx import Document

# Palavras-chave para análise
palavras_chave = ["Node", "React", "Front End"]

# Pasta com os arquivos .docx
pasta_curriculos = "curriculos"

# Função para extrair texto de um arquivo .docx
def extrair_texto_docx(caminho_arquivo):
    doc = Document(caminho_arquivo)
    texto = "\n".join([par.text for par in doc.paragraphs])
    return texto

# Função para calcular percentual de match
def calcular_match(texto, palavras_chave):
    encontradas = [p for p in palavras_chave if re.search(rf'\b{re.escape(p)}\b', texto, re.IGNORECASE)]
    percentual = len(encontradas) / len(palavras_chave) * 100
    return encontradas, percentual

# Processar todos os arquivos na pasta
def analisar_curriculos(pasta, palavras_chave):
    resultados = []

    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.endswith(".docx"):
            caminho = os.path.join(pasta, nome_arquivo)
            texto = extrair_texto_docx(caminho)
            encontradas, percentual = calcular_match(texto, palavras_chave)
            resultados.append({
                "arquivo": nome_arquivo,
                "palavras_encontradas": encontradas,
                "percentual_match": round(percentual, 2)
            })

    return resultados

# Execução
resultado = analisar_curriculos(pasta_curriculos, palavras_chave)

# Exibição
for r in resultado:
    print(f"\nArquivo: {r['arquivo']}")
    print(f"Palavras-chave encontradas: {', '.join(r['palavras_encontradas']) if r['palavras_encontradas'] else 'Nenhuma'}")
    print(f"Match: {r['percentual_match']}%")
