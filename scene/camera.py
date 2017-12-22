# -*- coding: utf-8 -*-
import op.opVetores
import numpy as numpy

class Camera(object):
    def __init__(self, camera_entrada, width=800, height=600):
        super(Camera, self).__init__()

        with open(camera_entrada, 'r') as camera_config:
            configs = camera_config.readlines()

            posicao_camera_format = configs[0].split()
            self.posicao_camera = numpy.array([float(posicao_camera_format[0]), float(posicao_camera_format[1]), float(posicao_camera_format[2])])

            n_cfg_format = configs[1].split()
            self.camera_n = numpy.array([float(n_cfg_format[0]), float(n_cfg_format[1]), float(n_cfg_format[2])])

            v_cfg_format = configs[2].split()
            self.camera_v = numpy.array([float(v_cfg_format[0]), float(v_cfg_format[1]), float(v_cfg_format[2])])

            parametros_cfg_format = configs[3].split()
            self.d = float(parametros_cfg_format[0])
            self.hx = float(parametros_cfg_format[1])
            self.hy = float(parametros_cfg_format[2])

        self.N = op.opVetores.normalizar(self.camera_n)
        self.V = op.opVetores.normalizar(self.camera_v - op.opVetores.grand_schimidt(self.camera_v, self.N))
        self.U = numpy.cross(self.N, self.V)
        self.UVN_matriz = numpy.array([self.U, self.V, self.N])
        self.width = width
        self.height = height

    def ver_coordenadas_sistema(self, p):
        '''retorna o ponto p dentro sistema de coordenadas de camera'''

        ponto = numpy.array([0.0,0.0,0.0])
        ponto[0] = p[0] - self.posicao_camera[0]
        ponto[1] = p[1] - self.posicao_camera[1]
        ponto[2] = p[2] - self.posicao_camera[2]

        result = numpy.array([self.UVN_matriz[0][0] * ponto[0] + self.UVN_matriz[0][1] * ponto[1] + self.UVN_matriz[0][2] * ponto[2],
                            self.UVN_matriz[1][0] * ponto[0] + self.UVN_matriz[1][1] * ponto[1] + self.UVN_matriz[1][2] * ponto[2],
                            self.UVN_matriz[2][0] * ponto[0] + self.UVN_matriz[2][1] * ponto[1] + self.UVN_matriz[2][2] * ponto[2]])

        return result

    def get_normal_triangulo(self, p1, p2, p3):
        '''retorna a normal do triangulo'''
        v1 = p2 - p1
        v2 = p3 - p1
        return numpy.cross(v1, v2)


    def converter_coordenadas(self, p):
        '''Calcular projecao de coordenadas'''
        x = float(self.d / self.hx) * (p[0] / p[2])
        y = float(self.d / self.hy) * (p[1] / p[2])
        '''Converter para coordenadas de tela'''
        coordenada_tela = numpy.array(
            [(int)(((x + 1)  * (self.width/ 2))),
             (int)(((1 - y) * (self.height/ 2)))]
        )
        return coordenada_tela





