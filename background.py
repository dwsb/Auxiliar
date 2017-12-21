# -*- coding: utf-8 -*-
import operations.vector
from operations.triangle import Triangle
from scene import scene
from scene.camera import Camera


# if __name__ == '__main__':
def run(width, height, colors_to_randomize, random_factor, settings):

    '''passos:'''

    """1) camera
    1.1) normalizar N
    1.2) V = V - proj N (V)
    1.3) U = N x V")
    t1.4) alfa = UNV = {U, N, V}"""
    cam = Camera(settings.camera_input)


    """2) cena"""
    sc = scene.Scene(settings.object_input, settings.iluminacao_input)

    """2.1) passar a posição da fonte de luz de coordenadas de mundo para coordenadas de vista"""
    pl_view = cam.to_view_coordinate_system(sc.pl)
    sc.pl = pl_view

    """2.2) para cada ponto do objeto, projete-o para coordenadas de vista"""
    for p in sc.points:
        sc.view_coordinates.append(cam.to_view_coordinate_system(p))

    """
    2.3) inicializar as normais de todos os pontos do objeto com zero
    2.4) para cada triângulo calcular a normal do triângulo e normalizá-la. somar ela à normal
     de cada um dos 3 pontos (vértices do triângulo) e cria os Triangulos com vertices em coordenada de vista
    """
    for t in sc.triangles:
        p1, p2, p3 = sc.view_coordinates[t[0] - 1], sc.view_coordinates[t[1] - 1], sc.view_coordinates[t[2] - 1]

        tr_normal = cam.get_triangle_normal(p1, p2, p3)
        tr_normal = operations.vector.normalize(tr_normal)

        sc.triangles_view_objects.append(Triangle(p1, p2, p3, norm=tr_normal))
        
        sc.points_normal[t[0] - 1] += tr_normal
        sc.points_normal[t[1] - 1] += tr_normal
        sc.points_normal[t[2] - 1] += tr_normal

    for i in range(len(sc.points_normal)):
        sc.points_normal[i] = operations.vector.normalize(sc.points_normal[i])

    """2.6) para cada ponto do obj, projete-o para coord de tela 2D, sem descartar os pontos em coord 3D"""
    for vp in sc.view_coordinates:
        sc.screen_coordinates.append(cam.to_screen_coordinate_system(vp))


    """2.7) Inicializa z-buffer."""
    sc.init_zbuffer(width, height)

    #passando os triângulos para coordenadas de tela
    sc.create_triangle_screen_objects()

    """2.8) Realiza a varredura nos triangulos em coordenada de tela."""
    sc.rasterize_screen_triangles(colors_to_randomize, random_factor)

    
    return sc
