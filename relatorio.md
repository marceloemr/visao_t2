# Relatório Calibração de Câmera

## 1. Introdução e Objetivo
Este relatório descreve o desenvolvimento e o funcionamento de um sistema de visão computacional implementado em Python com o auxílio da biblioteca OpenCV. O objetivo principal do programa é realizar a calibração geométrica de uma câmera e permitir o mapeamento interativo de pontos do espaço tridimensional $(X, Y, Z)$ para as coordenadas de pixel $(x, y)$ correspondentes na imagem.

---

## Metodologia e Dados
Para realizar eses experimento, foi desenvolvido um script em python com o auxílio da biblioteca OpenCV, através do qual foi realizada a calibração da câmera embutida de um notebook Lenovo ThinkPad T480.
O script utiliza um conjunto de 20 imagens de um tabuleiro de xadrez impresso, capturadas com a câmera do notebook.
Depois de calibrada a câmera, o script lê da entrada padrão coordenadas 3D e calcula sua projeção na imagem 2D, lendo e exibindo uma coordenada de cada vez.

---

## Observação sobre a Correção de Distorção
Durante os testes de remoção de distorção, constatou-se que a aplicação direta das funções de correção de distorção (`cv.undistort` combinada com `cv.getOptimalNewCameraMatrix`) deixa a **imagem com um aspecto estranho**. A causa não pode ser determinada.
