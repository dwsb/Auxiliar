import op.opVetores
from op.triangulos import Triangulo
from scene import scene
from scene.camera import Camera

def run(largura, altura, cores_randomizadas, fator_de_randomizacao, entrada_camera, entrada_objeto, entrada_iluminacao):

    cam = Camera(entrada_camera)
    cena = scene.Scene(entrada_objeto, entrada_iluminacao)
    posicao_ilumi = cam.ver_coordenadas_sistema(cena.pl)
    cena.pl = posicao_ilumi

    for p in cena.pontos:
        cena.view_coordinates.append(cam.ver_coordenadas_sistema(p))

    for t in cena.triangulos:
        p1, p2, p3 = cena.view_coordinates[t[0] - 1], cena.view_coordinates[t[1] - 1], cena.view_coordinates[t[2] - 1]

        tr_normal = cam.get_normal_triangulo(p1, p2, p3)
        tr_normal = op.opVetores.normalizar(tr_normal)

        cena.triangles_view_objects.append(Triangulo(p1, p2, p3, norm=tr_normal))
        
        cena.pontos_normal[t[0] - 1] += tr_normal
        cena.pontos_normal[t[1] - 1] += tr_normal
        cena.pontos_normal[t[2] - 1] += tr_normal

    for i in range(len(cena.pontos_normal)):
        cena.pontos_normal[i] = op.opVetores.normalizar(cena.pontos_normal[i])

    for vp in cena.view_coordinates:
        cena.screen_coordinates.append(cam.converter_coordenadas(vp))


    cena.zbuffer(largura, altura)

    cena.create_triangle_screen_objects()

    cena.rasterize_screen_triangles(cores_randomizadas, fator_de_randomizacao)
    
    return cena
