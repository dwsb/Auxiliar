# -*- coding: utf-8 -*-
import op.opVetores
from op.triangulos import Triangulo
from scene import scene
from scene.camera import Camera


# if __name__ == '__main__':
def run(width, height, colors_to_randomize, random_factor, input_camera, input_objeto, input_iluminacao):

    '''passos:'''

    """1) camera
    1.1) normalizar N
    1.2) V = V - proj N (V)
    1.3) U = N x V")
    t1.4) alfa = UNV = {U, N, V}"""
    cam = Camera(input_camera)


    """2) cena"""
    sc = scene.Scene(input_objeto, input_iluminacao)

    """2.1) passar a posição da fonte de luz de coordenadas de mundo para coordenadas de vista"""
    pl_view = cam.ver_coordenadas_sistema(sc.pl)
    sc.pl = pl_view

    """2.2) para cada ponto do objeto, projete-o para coordenadas de vista"""

    for p in sc.pontos:
        sc.view_coordinates.append(cam.ver_coordenadas_sistema(p))

    """
    2.3) inicializar as normais de todos os pontos do objeto com zero
    2.4) para cada triângulo calcular a normal do triângulo e normalizá-la. somar ela à normal
     de cada um dos 3 pontos (vértices do triângulo) e cria os Triangulos com vertices em coordenada de vista
    """
    for t in sc.triangulos:
        p1, p2, p3 = sc.view_coordinates[t[0] - 1], sc.view_coordinates[t[1] - 1], sc.view_coordinates[t[2] - 1]

        tr_normal = cam.get_normal_triangulo(p1, p2, p3)
        tr_normal = op.opVetores.normalizar(tr_normal)

        sc.triangles_view_objects.append(Triangulo(p1, p2, p3, norm=tr_normal))
        
        sc.pontos_normal[t[0] - 1] += tr_normal
        sc.pontos_normal[t[1] - 1] += tr_normal
        sc.pontos_normal[t[2] - 1] += tr_normal

    for i in range(len(sc.pontos_normal)):
        sc.pontos_normal[i] = op.opVetores.normalizar(sc.pontos_normal[i])

    """2.6) para cada ponto do obj, projete-o para coord de tela 2D, sem descartar os pontos em coord 3D"""
    for vp in sc.view_coordinates:
        sc.screen_coordinates.append(cam.converter_coordenadas(vp))

    """2.7) Inicializa z-buffer."""
    sc.init_zbuffer(width, height)

    #passando os triângulos para coordenadas de tela
    sc.create_triangle_screen_objects()

    """2.8) Realiza a varredura nos triangulos em coordenada de tela."""
    sc.rasterize_screen_triangles(colors_to_randomize, random_factor)
    
    return sc
