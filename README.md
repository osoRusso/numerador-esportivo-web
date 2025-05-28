# Numerador Esportivo Web

## Como usar

1. Descompacte (ou coloque) sua chave do Google Vision (ocr-desktop-460002-e6ee797c7953.json) na mesma pasta.
2. Abra o Terminal nesta pasta.
3. Instale as dependências:
   python3 -m pip install -r requirements.txt
4. Rode o app:
   streamlit run app.py

O navegador abrirá automaticamente mostrando duas abas:
- Numerador Manual (com atalhos de teclado)
- OCR Automático (com barra esportiva animada)

## Atalhos de Teclado (Numerador Manual)

- Enter: avançar para próxima imagem
- Seta para cima (↑): copiar número da imagem anterior
- Seta para a esquerda/direita (←/→): navegar entre imagens
- Ctrl + R: inverter ordem das imagens (ou use o botão "Inverter Ordem")

## Observações

- A barra esportiva no OCR muda de acordo com o esporte (corrida, ciclismo ou natação)
- O CSV gerado segue o padrão: nome_da_imagem;número

