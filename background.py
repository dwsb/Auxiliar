# -*- coding: utf-8 -*-
import opVetores
from triangulos import Triangulo
import scene
from camera import Camera

def run(largura, altura, cores_randomizadas, fator_de_randomizacao, entrada_camera, entrada_objeto, entrada_iluminacao):

    cam = Camera(entrada_camera)
    cena = scene.Scene(entrada_objeto, entrada_iluminacao)
    posicao_ilumi = cam.ver_coordenadas_sistema(cena.pl)
    cena.pl = posicao_ilumi

    for p in cena.pontos:
        cena.ver_coordenadas.append(cam.ver_coordenadas_sistema(p))

    for t in cena.triangulos:
        p1, p2, p3 = cena.ver_coordenadas[t[0] - 1], cena.ver_coordenadas[t[1] - 1], cena.ver_coordenadas[t[2] - 1]

        tr_normal = cam.get_normal_triangulo(p1, p2, p3)
        tr_normal = opVetores.normalizar(tr_normal)

        cena.triangulos_v_obj.append(Triangulo(p1, p2, p3, norm=tr_normal))
        
        cena.pontos_normal[t[0] - 1] += tr_normal
        cena.pontos_normal[t[1] - 1] += tr_normal
        cena.pontos_normal[t[2] - 1] += tr_normal

    for i in range(len(cena.pontos_normal)):
        cena.pontos_normal[i] = opVetores.normalizar(cena.pontos_normal[i])

    for vp in cena.ver_coordenadas:
        cena.coordenadas_tela.append(cam.converter_coordenadas(vp))


    cena.zbuffer(largura, altura)

    cena.criar_triangulos_objeto()

    cena.rast_tela_triangulos(cores_randomizadas, fator_de_randomizacao)
    
    return cena
