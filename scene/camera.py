# -*- coding: utf-8 -*-
import op.opVetores
import numpy as np

class Camera(object):
    def __init__(self, camera_input, width=800, height=600):
        super(Camera, self).__init__()

        with open(camera_input, 'r') as camera_config:
            configs = camera_config.readlines()

            position_config_splited = configs[0].split()
            self.camera_position = np.array([float(position_config_splited[0]),
                                        float(position_config_splited[1]),
                                        float(position_config_splited[2])
                                        ])

            n_config_splited = configs[1].split()
            self.camera_n = np.array([float(n_config_splited[0]),
                                 float(n_config_splited[1]),
                                 float(n_config_splited[2])
                                 ])

            v_config_splited = configs[2].split()
            self.camera_v = np.array([float(v_config_splited[0]),
                                 float(v_config_splited[1]),
                                 float(v_config_splited[2])
                                 ])

            params_config_splited = configs[3].split()
            self.d = float(params_config_splited[0])
            self.hx = float(params_config_splited[1])
            self.hy = float(params_config_splited[2])

        self.N = op.opVetores.normalizar(self.camera_n)
        self.V = op.opVetores.normalizar(
            self.camera_v - op.opVetores.grand_schimidt(self.camera_v, self.N))
        self.U = np.cross(self.N, self.V)
        self.UVN_matrice = np.array([self.U, self.V, self.N])

        self.width = width
        self.height = height


    '''retorna o ponto p no sistema de coordenadas da camera (camera_coordinate_system)'''
    def to_view_coordinate_system(self, p):
        point = np.array([0.0,0.0,0.0])
        point[0] = p[0] - self.camera_position[0]
        point[1] = p[1] - self.camera_position[1]
        point[2] = p[2] - self.camera_position[2]

        result = np.array([self.UVN_matrice[0][0] * point[0] + self.UVN_matrice[0][1] * point[1] + self.UVN_matrice[0][2] * point[2],
                            self.UVN_matrice[1][0] * point[0] + self.UVN_matrice[1][1] * point[1] + self.UVN_matrice[1][2] * point[2],
                            self.UVN_matrice[2][0] * point[0] + self.UVN_matrice[2][1] * point[1] + self.UVN_matrice[2][2] * point[2]])

        return result

    def to_screen_coordinate_system(self, p):
        '''calculate projection coordinates'''
        x = float(self.d / self.hx) * (p[0] / p[2])
        y = float(self.d / self.hy) * (p[1] / p[2])
        '''convert to screen'''
        screen_coord = np.array(
            [(int)(((x + 1)  * (self.width/ 2))),
             (int)(((1 - y) * (self.height/ 2)))]
        )

        return screen_coord

    def get_triangle_normal(self, p1, p2, p3):
        v1 = p2 - p1
        v2 = p3 - p1

        return np.cross(v1, v2)



