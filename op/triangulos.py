import numpy as np

class Triangulo(object):
    def __init__(self, v1, v2, v3, ind1=None, ind2=None, ind3=None, norm=None):
        super(Triangulo, self).__init__()
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.ind1 = ind1
        self.ind2 = ind2
        self.ind3 = ind3
        self.norm = norm
        self.min_x = min(self.v1[0], min(self.v2[0], self.v3[0]))
        self.max_x = max(self.v1[0], max(self.v2[0], self.v3[0]))
        self.min_y = min(self.v1[1], min(self.v2[1], self.v3[1]))
        self.max_y = max(self.v1[1], max(self.v2[1], self.v3[1]))


        '''verifica se pontos pertencem ao triangulo'''
    def pontos_triangulos(self, point):
        sign = lambda p1, p2, p3: (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        b1 = sign(point, self.v1, self.v2) <= 0.0
        b2 = sign(point, self.v2, self.v3) <= 0.0
        b3 = sign(point, self.v3, self.v1) <= 0.0

        return (b1 == b2) and (b2 == b3)

    def coordenadas_baricentricas(self, point):
        '''achando coordenadas baricentricas do ponto usando a regra de cramer para resolver o sistema'''
        v0 = self.v2 - self.v1
        v1 = self.v3 - self.v1
        v2 = point - self.v1
        d00 = np.dot(v0, v0)
        d01 = np.dot(v0, v1)
        d11 = np.dot(v1, v1)
        d20 = np.dot(v2, v0)
        d21 = np.dot(v2, v1)
        aux = float(d00 * d11 - d01 * d01)
        beta = 0 if aux == 0 else (d11 * d20 - d01 * d21) / aux
        gama = 0 if aux == 0 else (d00 * d21 - d01 * d20) / aux
        alfa = max(0, 1.0 - gama - beta)
        return alfa, beta, gama
