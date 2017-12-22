# -*- coding: utf-8 -*-
import numpy
import opVetores
from triangulos import Triangulo
from OpenGL.GL import *
import sys, random


class Scene(object):

    def __init__(self, objeto_entrada, iluminacao_entrada):
        super(Scene, self).__init__()

        self.debug = True

        self.r = 0
        self.t = 0

        self.pontos = []
        self.triangulos = []
        self.triangulos_v_obj = []
        self.triangulos__obj = []
        self.pontos_normal = []
        self.triangulos_normal = []
        self.ver_coordenadas = []
        self.coordenadas_tela = []

        self.fator_de_randomizacao = 0.0
        self.n_fator = 0.0
        self.pl = 0.0
        self.ka = 0.0
        self.ia = 0.0
        self.kd = 0.0
        self.od = 0.0
        self.ks = 0.0
        self.il = 0.0


        self.z_buffer = []
        self.carrega_vertices(objeto_entrada)
        self.carrega_iluminacao(iluminacao_entrada)

    def carrega_vertices(self, objeto_entrada):
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


    def carrega_iluminacao(self, iluminacao_entrada):
        '''Carrega os dados de illuminação'''
        with open(iluminacao_entrada, 'r') as iluminacao_config:
            linhas_iluminacao = iluminacao_config.readlines()
            self.n_fator = float(linhas_iluminacao[-1])

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
    def phong(self, ponto, N, cores_randomizadas, fator_de_randomizacao):
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
            attenuation = random.uniform(1-fator_de_randomizacao, 1)

            random_r = attenuation if cores_randomizadas['R'] is True else 1
            random_g = attenuation if cores_randomizadas['G'] is True else 1
            random_b = attenuation if cores_randomizadas['B'] is True else 1

            od = numpy.array([self.od[0]*random_r, self.od[1]*random_g, self.od[2]*random_b])

            id = (od * self.il) * self.kd * (numpy.dot(N,l))

            r = opVetores.normalizar((2*N*numpy.dot(N, l)) - l)
            if (numpy.dot(v,r) >= 0):
                ie = (self.il) * self.ks * (pow(float(numpy.dot(v,r)), self.n_fator))

        color = ia + id + ie

        for i in range(0, 3):
            color[i] = 255 if color[i] > 255 else color[i]

        color = color/255.0

        return color


    def criar_triangulos_objeto(self):
        for t in self.triangulos:
            p1, p2, p3 = self.coordenadas_tela[t[0] - 1], self.coordenadas_tela[t[1] - 1], self.coordenadas_tela[t[2] - 1]
            self.triangulos__obj.append(Triangulo(p1, p2, p3, t[0], t[1], t[2]))


    def zbuffer(self, height, width):
        self.z_buffer = numpy.full((max(height, width) + 1, max(width, height) + 1), sys.maxint, dtype=float)


    def rast_tela_triangulos(self, cores_randomizadas, fator_de_randomizacao):

        def yscan(triangulo):
            
            def bottom_flat(vertices):
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
                    desenha_linha(triangulo, curx1, curx2, scanlineY)
                    curx1 += invslope1
                    curx2 += invslope2
                    scanlineY += 1

            def top_flat(vertices):
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
                    desenha_linha(triangulo, curx1, curx2, scanlineY)
                    curx1 -= invslope1
                    curx2 -= invslope2
                    scanlineY -= 1

            ''' primeiro os vetores sao ordenados pelos seus Y'''
            v = sorted([triangulo.v1, triangulo.v2, triangulo.v3], key=lambda vx: vx[1])
            '''notação: v1 == v[0], v1.x == v[0][0], v1.y == v[0][1] etc'''

            if v[0][1] == v[1][1] == v[2][1]:
                ''' se for um triangulo "sem altura/colinear" ele é rasterizado como uma linha.'''
                curx1 = min(v[0][0], min(v[1][0], v[2][0]))
                curx2 = max(v[0][0], max(v[1][0], v[2][0]))
                desenha_linha(triangulo, curx1, curx2, v[0][1], colinear=True)
            elif v[1][1] == v[2][1]:
                ''' caso bottom_flat'''
                bottom_flat(v)
            elif v[0][1] == v[1][1]:
                '''caso top_flat'''
                top_flat(v)
            else:
                ''' caso geral '''
                '''
                Vertice v4 = new Vertice((int)(vt1.x + ((float)(vt2.y - vt1.y) / (float)(vt3.y - vt1.y)) * (vt3.x - vt1.x)), vt2.y);
                '''
                v4 = numpy.array([
                    int(v[0][0] + (float(v[1][1] - v[0][1]) / float(v[2][1] - v[0][1])) * (v[2][0] - v[0][0])),
                    v[1][1]
                ])

                bottom_flat([v[0], v[1], v4])
                top_flat([v[1], v4, v[2]])


        def desenha_linha(triangulo, curx1, curx2, y, colinear=False):
           
            t = triangulo
            x_min = min(t.min_x, min(curx1, curx2))
            x_max = max(t.max_x, max(curx1, curx2))
            for x in range(int(x_min), int(x_max)+1):
                pixel = numpy.array([x, y])
                if t.pontos_triangulos(pixel) or colinear:
                  
                    alfa, beta, gama = t.coordenadas_baricentricas(pixel)

                    _P = alfa * self.ver_coordenadas[t.ind1 - 1] + beta * self.ver_coordenadas[t.ind2 - 1] + gama * self.ver_coordenadas[t.ind3 - 1]

                    '''consulta ao Z-buffer'''
                    if _P[2] <= self.z_buffer[pixel[0]][pixel[1]]:
                        self.z_buffer[pixel[0]][pixel[1]] = _P[2]

                        N = (alfa * self.pontos_normal[t.ind1 - 1] +
                             beta * self.pontos_normal[t.ind2 - 1] +
                             gama * self.pontos_normal[t.ind3 - 1])

                        color = self.phong(_P, N, cores_randomizadas, fator_de_randomizacao)
                        glColor3f(color[0], color[1], color[2])
                        glVertex2f(pixel[0], pixel[1])


        for t in self.triangulos__obj:
            yscan(t)