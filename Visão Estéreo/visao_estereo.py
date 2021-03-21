# Autores: Matheus Teixeira de Sousa (teixeira.sousa@aluno.unb.br)
#          João Luiz Machado Júnior (180137158@aluno.unb.br)
# Disciplina: Princípios de Visão Computacional - turma A

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def data_reader(file_name):
# Função para leitura de dados de calibração em arquivo .txt

	lines = []
	data = []

	with open(file_name) as f:
		lines = f.readlines()  # Armazenar linhas do arquivo em lista

	# Percorrer linhas separando termos relevantes para inserir na lista
	for i in range(len(lines)):
		clean_line = lines[i].replace('=', ' ').replace('[', '').replace(';', '').replace(']', '')
		results = clean_line.split()
		data.append(results)

	# Remover strings que identificam o nome de cada variavel
	for i in range(len(lines)):
		del data[i][0]

	return data

def disparity_calculator(left_image, right_image, disparities_num):
# Função que calcula mapa de disparidades dadas duas imagens estereo-retificadas

	window_size = 3

	left_matcher = cv.StereoSGBM_create(
	    minDisparity=16,
	    numDisparities= disparities_num,  # Numero maximo de disparidades (640 para essa imagem)
	    blockSize=window_size,
	    P1=8 * 3 * window_size,
	    P2=32 * 3 * window_size,
	    disp12MaxDiff=12,
	    uniquenessRatio=10,
	    speckleWindowSize=50,
	    speckleRange=32,
	    preFilterCap=63,
	    mode=cv.STEREO_SGBM_MODE_SGBM_3WAY
	)
	right_matcher = cv.ximgproc.createRightMatcher(left_matcher)

	# parâmetros do filtro
	lmbda = 80000
	sigma = 1.3
	visual_multiplier = 6

	wls_filter = cv.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
	wls_filter.setLambda(lmbda)

	wls_filter.setSigmaColor(sigma)
	displ = left_matcher.compute(left_image, right_image) 
	dispr = right_matcher.compute(right_image, left_image)
	displ = np.int16(displ)
	dispr = np.int16(dispr)
	filteredImg = wls_filter.filter(displ, left_image, None, dispr)

	# Normaliza o filtro
	filteredImg = cv.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv.NORM_MINMAX)
	filteredImg = np.uint8(filteredImg)

	return filteredImg

# -------------------------------------------------------------------------------

calib_jade_data = data_reader('calib_jade.txt')
calib_table_data = data_reader('calib_table.txt')

imgL = cv.imread('jadeL.png', cv.COLOR_BGR2GRAY)
imgR = cv.imread('jadeR.png', cv.COLOR_BGR2GRAY)
disparities_num = int(calib_jade_data[6][0])

filteredImg = disparity_calculator(imgL, imgR, disparities_num)

# cv.imshow('filtered', filteredImg) Corrigir o tamanho da janela de exibição
cv.imwrite('filtered.jpg', filteredImg)

# Mostra imagem de disparidades com mapa de cores, padrão "jet"
plt.imshow(filteredImg, cmap='jet')
plt.colorbar()
plt.savefig("color_filtered.jpg")
plt.show()

cv.waitKey(0)
