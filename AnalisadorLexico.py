import os
import re
from docx import Document
from collections import defaultdict
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QFileDialog, QLabel, QMessageBox
)

class AnalisadorLexico(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analisador Léxico de Currículos")
        self.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()

        self.instrucao = QLabel("Digite as palavras-chave (separadas por vírgula):")
        layout.addWidget(self.instrucao)

        self.entrada_palavras = QTextEdit()
        self.entrada_palavras.setPlaceholderText("Exemplo: Node, React, Front End")
        layout.addWidget(self.entrada_palavras)

        self.botao_pasta = QPushButton("Selecionar Pasta com Currículos")
        self.botao_pasta.clicked.connect(self.selecionar_pasta)
        layout.addWidget(self.botao_pasta)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        self.setLayout(layout)

    def selecionar_pasta(self):
        pasta = QFileDialog.getExistingDirectory(self, "Selecione a pasta com currículos")
        if pasta:
            palavras = self.entrada_palavras.toPlainText()
            if not palavras.strip():
                QMessageBox.warning(self, "Erro", "Por favor, digite pelo menos uma palavra-chave.")
                return

            palavras_chave = [p.strip().lower() for p in palavras.split(",")]
            self.analisar_curriculos(pasta, palavras_chave)

    def extrair_texto_docx(self, caminho_arquivo):
        doc = Document(caminho_arquivo)
        return "\n".join(par.text for par in doc.paragraphs)

    def tokenizar(self, texto):
        return re.findall(r'\b\w[\w\-]*\b', texto.lower())

    def classificar_token(self, token, palavras_chave):
        if token in palavras_chave:
            return "Palavra-chave"
        elif re.fullmatch(r'\d+', token):
            return "Número"
        elif "-" in token:
            return "Composto (com hífen)"
        elif re.fullmatch(r'[a-zA-Z_]\w*', token):
            return "Identificador"
        else:
            return "Outro"

    def imprimir_tokens_por_tipo(self, tokens, palavras_chave):
        classificados = defaultdict(list)
        for token in tokens:
            tipo = self.classificar_token(token, palavras_chave)
            classificados[tipo].append(token)

        texto_resultado = ""
        for tipo, lista in classificados.items():
            texto_resultado += f"\n🔸 {tipo} ({len(lista)}):\n"
            texto_resultado += ", ".join(lista[:30]) + ("..." if len(lista) > 30 else "") + "\n"
        return texto_resultado

    def analisar_curriculo(self, texto, palavras_chave):
        tokens = self.tokenizar(texto)
        encontrados = [kw for kw in palavras_chave if kw in tokens]
        percentual = len(encontrados) / len(palavras_chave) * 100 if palavras_chave else 0
        return tokens, encontrados, round(percentual, 2)

    def analisar_curriculos(self, pasta, palavras_chave):
        self.resultado.clear()
        for nome in os.listdir(pasta):
            if nome.endswith(".docx"):
                caminho = os.path.join(pasta, nome)
                texto = self.extrair_texto_docx(caminho)
                tokens, encontrados, match = self.analisar_curriculo(texto, palavras_chave)

                self.resultado.append(f"📄 {nome}")
                self.resultado.append(f"🔎 Palavras-chave encontradas: {', '.join(encontrados) if encontrados else 'Nenhuma'}")
                self.resultado.append(f"✅ Match: {match}%")
                self.resultado.append(f"🧩 Tokens extraídos ({len(tokens)}):")
                self.resultado.append(self.imprimir_tokens_por_tipo(tokens, palavras_chave))
                self.resultado.append("-" * 60)

if __name__ == "__main__":
    app = QApplication([])
    janela = AnalisadorLexico()
    janela.show()
    app.exec_()
