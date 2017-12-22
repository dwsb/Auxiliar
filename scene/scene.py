# -*- coding: utf-8 -*-
import numpy
from op import opVetores
from op.triangulos import Triangulo
from OpenGL.GL import *
import sys, random


class Scene(object):
    """docstring for Scene"""

    def __init__(self, calice_input, ilumination_input):
        super(Scene, self).__init__()

        self.debug = True

        self.r = 0
        self.t = 0

        self.pontos = []
        self.triangulos = []
        self.triangles_view_objects = []
        self.triangles_screen_objects = []
        self.pontos_normal = []
        self.triangles_normal = []
        self.view_coordinates = []
        self.screen_coordinates = []

        self.random_factor = 0.0
        self.n_factor = 0.0
        self.pl = 0.0
        self.ka = 0.0
        self.ia = 0.0
        self.kd = 0.0
        self.od = 0.0
        self.ks = 0.0
        self.il = 0.0


        self.z_buffer = []
        self.load_vertices(calice_input)
        self.load_ilumination(ilumination_input)

    def load_vertices(self, objeto_entrada):
        with open(objeto_entrada) as objeto_config:
            linhas = objeto_config.readlines()

        pontos_num = int(linhas[0].split(" ")[0])

        for x in range(1, pontos_num + 1):
            pontos_format = linhas[x].splitlines()[0].split()
            self.pontos.append(numpy.array([float(pontos_format[0]),float(pontos_format[1]),float(pontos_format[2])]))

            self.pontos_normal.append(numpy.array([0.0, 0.0, 0.0]))

        for x in range(pontos_num + 1, len(linhas)):
            triangulos_format = linhas[x].splitlines()[0].split()
            self.triangulos.append( numpy.array([int(triangulos_format[0]), int(triangulos_format[1]), int(triangulos_format[2])]))


    def load_ilumination(self, iluminacao_entrada):
        '''Carrega os dados de illuminação'''
        with open(iluminacao_entrada, 'r') as iluminacao_config:
            linhas_iluminacao = iluminacao_config.readlines()
            self.n_factor = float(linhas_iluminacao[-1])

            pl_format = linhas_iluminacao[0].split()

            self.pl = numpy.array([float(pl_format[0]),float(pl_format[1]),float(pl_format[2])])

            self.ka = float(linhas_iluminacao[1])

            ia_format = linhas_iluminacao[2].split()
            self.ia = numpy.array([float(ia_format[0]),float(ia_format[1]),float(ia_format[2])])
            self.kd = float(linhas_iluminacao[3])

            od_format = linhas_iluminacao[4].split()
            self.od = numpy.array([float(od_format[0]),float(od_format[1]),float(od_format[2])])
            self.ks = float(linhas_iluminacao[5])

            il_format = linhas_iluminacao[6].split()
            self.il = numpy.array([float(il_format[0]),float(il_format[1]),float(il_format[2])])

    '''a iluminação de phong é caracterizada pela junção dos vetores de iluminação
        de ambiente, difusa e especular'''
    '''
        | ; Pl - Posicao da luz em coordenadas de mundo
        | ; ka - reflexao ambiental
        | ; Ia - vetor cor ambiental
        | ; kd - constante difusa
        | ; Od - vetor difuso
        | ; ks - parte especular
        | ; Il - cor da fonte de luz
        | ; n  - constante de rugosidade
    '''
    '''
        final_color = ambient_component + diffuse_component + specular_component
    '''
    def pixel_phong_ilumination(self, ponto, N, colors_to_randomize, random_factor):
        ia = self.ia*self.ka
        l = (self.pl - ponto)
        l = opVetores.normalizar(l)
        N = opVetores.normalizar(N)

        id = numpy.array([0.0, 0.0, 0.0])
        ie = numpy.array([0.0, 0.0, 0.0])

        v = opVetores.normalizar(-ponto)
        if (numpy.dot(v,N) < 0):
            N = -N

        if (numpy.dot(N, l) >= 0):
            attenuation = random.uniform(1-random_factor, 1)

            random_r = attenuation if colors_to_randomize['R'] is True else 1
            random_g = attenuation if colors_to_randomize['G'] is True else 1
            random_b = attenuation if colors_to_randomize['B'] is True else 1

            # if d < 0.2:
            #     self.od = np.array([0.9, 0.1, 0.1])
            # elif 0.2 < d < 0.5:
            #     self.od = np.array([0.1, 0.9, 0.1])
            # elif d > 0.5:
            #     self.od = np.array([0.1, 0.1, 0.9])

            od = numpy.array([self.od[0]*random_r, self.od[1]*random_g, self.od[2]*random_b])

            id = (od * self.il) * self.kd * (numpy.dot(N,l))

            r = opVetores.normalizar((2*N*numpy.dot(N, l)) - l)
            if (numpy.dot(v,r) >= 0):
                ie = (self.il) * self.ks * (pow(float(numpy.dot(v,r)), self.n_factor))

        color = ia + id + ie

        for i in range(0, 3):
            color[i] = 255 if color[i] > 255 else color[i]

        color = color/255.0

        return color


    def create_triangle_screen_objects(self):
        for t in self.triangulos:
            p1, p2, p3 = self.screen_coordinates[t[0] - 1], self.screen_coordinates[t[1] - 1], self.screen_coordinates[t[2] - 1]
            self.triangles_screen_objects.append(Triangulo(p1, p2, p3, t[0], t[1], t[2]))


    def init_zbuffer(self, height, width):
        self.z_buffer = numpy.full((max(height, width) + 1, max(width, height) + 1), sys.maxint, dtype=float)


    def rasterize_screen_triangles(self, colors_to_randomize, random_factor):
        '''
        atentar para identação
        em python um bloco pode ter vários outros blocos dentro do seu escopo
        e no bloco-pai vc pode chamar os blocos-filhos

        :param colors_to_randomize: cores que devem ser randomizadas no Od, conforme passado na entrada
        :param random_factor: fator de aleatorização a ser aplicado nas cores
        :return: None
        '''

        def yscan(triangle):
            '''
            yscan conforme visto
            com dois casos especiais: bottom_flat e top_flat
            e o caso geral em que o triângulo é dividido em um bottom_flat e outro top_flat

            :param triangle: triangulo a ser rasterizado
            :return: None
            '''
            def fill_bottom_flat_triangle(vertices):
                '''
                :param vertices: vertices do triangulo ordenados pelo Y
                :return: None
                '''
                invslope1 = (vertices[1][0] - vertices[0][0]) / (vertices[1][1] - vertices[0][1])
                invslope2 = (vertices[2][0] - vertices[0][0]) / (vertices[2][1] - vertices[0][1])

                if invslope1 > invslope2:
                    invslope1, invslope2 = invslope2, invslope1

                curx1 = curx2 = v[0][0]

                scanlineY = v[0][1]
                while scanlineY <= v[1][1]:
                    ''' para cada linha do y scan, rasteriza a linha'''
                    draw_line(triangle, curx1, curx2, scanlineY)
                    curx1 += invslope1
                    curx2 += invslope2
                    scanlineY += 1

            def fill_top_flat_triangle(vertices):
                '''
                    :param vertices: vertices do triangulo ordenados pelo Y
                    :return: None
                '''
                invslope1 = (vertices[2][0] - vertices[0][0]) / (vertices[2][1] - vertices[0][1])
                invslope2 = (vertices[2][0] - vertices[1][0]) / float(vertices[2][1] - vertices[1][1])

                if invslope2 > invslope1:
                    invslope1, invslope2 = invslope2, invslope1

                curx1 = curx2 = v[2][0]

                scanlineY = v[2][1]
                while scanlineY > v[0][1]:
                    draw_line(triangle, curx1, curx2, scanlineY)
                    curx1 -= invslope1
                    curx2 -= invslope2
                    scanlineY -= 1

            ''' primeiro os vetores sao ordenados pelos seus Y'''
            v = sorted([triangle.v1, triangle.v2, triangle.v3], key=lambda vx: vx[1])
            '''notação: v1 == v[0], v1.x == v[0][0], v1.y == v[0][1] etc'''

            if v[0][1] == v[1][1] == v[2][1]:
                ''' se for um triangulo "sem altura/colinear" ele é rasterizado como uma linha.'''
                curx1 = min(v[0][0], min(v[1][0], v[2][0]))
                curx2 = max(v[0][0], max(v[1][0], v[2][0]))
                draw_line(triangle, curx1, curx2, v[0][1], colinear=True)
            elif v[1][1] == v[2][1]:
                ''' caso bottom_flat'''
                fill_bottom_flat_triangle(v)
            elif v[0][1] == v[1][1]:
                '''caso top_flat'''
                fill_top_flat_triangle(v)
            else:
                ''' caso geral '''
                '''
                Vertice v4 = new Vertice((int)(vt1.x + ((float)(vt2.y - vt1.y) / (float)(vt3.y - vt1.y)) * (vt3.x - vt1.x)), vt2.y);
                '''
                v4 = numpy.array([
                    int(v[0][0] + (float(v[1][1] - v[0][1]) / float(v[2][1] - v[0][1])) * (v[2][0] - v[0][0])),
                    v[1][1]
                ])

                fill_bottom_flat_triangle([v[0], v[1], v4])
                fill_top_flat_triangle([v[1], v4, v[2]])


        def draw_line(triangle, curx1, curx2, y, colinear=False):
            '''
            :param triangle: triangulo a ser rasterizado
            :param curx1: Xmin, onde começa a rasterização da linha atual
            :param curx2: Xmax, onde termina a rasterização da linha atual
            :param y: Yscan, indica qual linha (Y = y) está sendo rasterizada
            :return: None
            '''
            t = triangle
            x_min = min(t.min_x, min(curx1, curx2))
            x_max = max(t.max_x, max(curx1, curx2))
            for x in range(int(x_min), int(x_max)+1):
                pixel = numpy.array([x, y])
                if t.pontos_triangulos(pixel) or colinear:
                    '''
                    verifica se o pixel realmente pertence ao triângulo para corrigir casos de erro de precisão
                    do python
                    '''

                    ''' calcula o pixel em coordenadas baricêntricas do triângulo atual '''
                    alfa, beta, gama = t.coordenadas_baricentricas(pixel)

                    ''' passa os vertices correspondentes em coordenadas de vista (3D) para o sistema baricentrico encontrado'''
                    _P = alfa * self.view_coordinates[t.ind1 - 1] + beta * self.view_coordinates[t.ind2 - 1] + gama * self.view_coordinates[t.ind3 - 1]

                    '''consulta ao Z-buffer'''
                    if _P[2] <= self.z_buffer[pixel[0]][pixel[1]]:
                        self.z_buffer[pixel[0]][pixel[1]] = _P[2]

                        N = (alfa * self.pontos_normal[t.ind1 - 1] +
                             beta * self.pontos_normal[t.ind2 - 1] +
                             gama * self.pontos_normal[t.ind3 - 1])

                        # d = np.sqrt(pow(alfa - 1/3.0, 2) + pow(beta - 1/3.0, 2) + pow(gama - 1/3.0, 2))

                        color = self.pixel_phong_ilumination(_P, N, colors_to_randomize, random_factor)
                        glColor3f(color[0], color[1], color[2])
                        glVertex2f(pixel[0], pixel[1])


        '''para cada triângulo'''
        for t in self.triangles_screen_objects:
            '''para cada pixel P interno do triângulo'''
            yscan(t)