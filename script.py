import cv2
import numpy as np

def calcular_clareza(pixel):
    # Calcular a clareza de um pixel
    return sum(pixel) / 3  # Soma dos valores R, G e B dividida por 3

def detectar_areas_claras(imagem, limite_clareza):
    # Detecção de áreas claras na imagem
    img_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    _, img_bin = cv2.threshold(img_gray, limite_clareza, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def calcular_quantidade_fertilizante(area, quantidade_por_area):
    # Calcular a quantidade de fertilizante por área
    return area * quantidade_por_area

# Parâmetros de entrada
caminho_imagem = (r'/Users/joao/Documents/Fiap/GS/Arnaldo/imagem_agricola.jpg')
limite_clareza = 100  # Limite de clareza para detecção de áreas claras
quantidade_por_area = 1  # Quantidade de fertilizante em quilos por área

# Carregar imagem
imagem = cv2.imread(caminho_imagem)

# Detectar áreas claras
areas_claras = detectar_areas_claras(imagem, limite_clareza)

# Calcular áreas e quantidade de fertilizante
quantidades_fertilizante = []
nomes_areas = []
posicoes_areas = []
for i, area in enumerate(areas_claras):
    x, y, w, h = cv2.boundingRect(area)
    cv2.rectangle(imagem, (x, y), (x + w, y + h), (0, 255, 0), 2)
    area_pixels = cv2.contourArea(area)
    quantidade_fertilizante = calcular_quantidade_fertilizante(area_pixels, quantidade_por_area)
    quantidades_fertilizante.append(quantidade_fertilizante)
    nomes_areas.append(f"Área {i + 1}")
    posicoes_areas.append((x, y))

# Ordenar áreas, quantidades de fertilizante, nomes e posições em ordem decrescente de quantidade
areas_quantidades_nomes_posicoes = sorted(zip(areas_claras, quantidades_fertilizante, nomes_areas, posicoes_areas), key=lambda x: x[1], reverse=True)

# Exibir informações
cv2.imshow("Imagem com áreas claras destacadas", imagem)
cv2.waitKey(0)

print("Informações sobre aplicação de fertilizante:")

for area, quantidade, nome, posicao in areas_quantidades_nomes_posicoes:
    if quantidade > 1000:
        print(f"\n{nome}:")
        print(f"Quantidade de fertilizante: {quantidade} gramas")
        print(f"Posição (x, y): {posicao}")
