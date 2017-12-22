from OpenGL.raw.GLUT import glutBitmapCharacter

from OpenGL.raw.GLUT.constants import GLUT_RGB

from OpenGL.GL import *
from OpenGL.GLUT import *
from background import run
import argparse, sys, os.path


largura, altura = 800, 600


input_camera = 'input/entrada/Cameras/maca.cfg'
input_objeto = 'input/entrada/Objetos/maca.byu'
input_iluminacao = 'input/iluminacao.txt'

cores = {
    'R': False,
    'G': False,
    'B': False
}

fator_randomizador = 0

window = None

PROMPT = ("ESC - SAIR","C - TROCAR DE OBJETO")


def args():
    global cores, fator_randomizador

    parser = argparse.ArgumentParser(description="Textura randomica a partir da coloracao")
    parser.add_argument('fator_randomizador', metavar='F', help='Fator de randomizacao (escolha entre 0-1)')
    parser.add_argument('--colors', metavar='C', default='RGB', help='Cores a serem randomizadas (e.g: RGB)')

    args = parser.parse_args()

    if not (0 <= float(args.fator_randomizador) <= 1):
        print "Entrada invalida %r (Digite um fator de randomizacao entre 0-1)" % args.fator_randomizador
        print "Tipo python %s -h para mais informacoes." % sys.argv[0]
        sys.exit(1)

    for c in args.colors:
        if str(c).upper() not in ['R', 'G', 'B']:
            print "Entrada invalida %r (A opcao %r nao e valida, opcoes validas (RGB))" % (args.colors, c)
            print "Tipo python %s -h para mais informacoes." % sys.argv[0]
            sys.exit(1)
        cores[str(c).upper()] = True

    fator_randomizador = args.fator_randomizador


def renderizar():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    glColor3f(0.0, 1.0, 1.0)

    print '\nCarregando objeto... Aguarde um momento!'
    sc = run(largura, altura, cores, float(fator_randomizador), input_camera, input_objeto, input_iluminacao)
    print 'Objeto carregado\n'

    glEnd()
    glFlush()
    glutSwapBuffers()


def captarEntradas(*args):
    global settings
    global input_objeto
    global input_camera
    ESC = '\x1b'

    if args[0] == ESC:
        glutDestroyWindow(window)
    elif args[0] == 'c':
        path = raw_input('\n - Insira o caminho com nome do novo objeto: ')
        if os.path.isfile("input/Objetos/"+path):
            input_objeto = "input/Objetos/"+ path
            print(input_objeto)
        else:
            print 'Erro! Caminho errado ou o arquivo do objeto nao existe!!!\n'
            return
        camera_path = raw_input(' - Insira o caminho com nome do arquivo de camera correspondente ao objeto: ')
        if os.path.isfile("input/Cameras/"+camera_path):
            input_camera = "input/Cameras/"+ camera_path
            print input_camera
        else:
            print 'Erro! Caminho errado ou o arquivo da camera nao existe!!!\n'

        new_fator_randomizador = raw_input(' - Insira o fator de randomizacao entre 0-1, caso deseje mudar o atual: ')
        if len(new_fator_randomizador) > 0:
            try:
                global fator_randomizador
                tmp = float(new_fator_randomizador)
                fator_randomizador = tmp
            except:
                print ' A entrada %r e um fator invalido!!! O fator antigo permanecera.'

        new_random_colors = raw_input(' - Insira os tipos de cores a serem randomizadas [RGB], caso deseje mudar as atuais: ')
        global cores
        if len(new_random_colors) > 0:
            for c in new_random_colors:
                if str(c).upper() in ['R', 'G', 'B']:
                    for color in ['R', 'G', 'B']:
                        cores[color] = False
                    for c2 in new_random_colors:
                        if str(c2).upper() in ['R', 'G', 'B']:
                            cores[str(c2).upper()] = True
                    break





        glutPostRedisplay()



def init():
    glClear(GL_COLOR_BUFFER_BIT)
    glViewport(0, 0, largura, altura)
    glMatrixMode(GL_PROJECTION)
    glOrtho(0.0, largura, altura, 0.0, -5.0, 5.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


if __name__ == '__main__':
    args()
    
    print "\nAperte 'c' para mudar de objeto .\nAperte ESC para sair\n"
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(largura, altura)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow('PG2 - Random Color Texture')

    glutDisplayFunc(renderizar)
    glutKeyboardFunc(captarEntradas)

    glClearColor(0, 0, 0, 0)
    init()
    glutMainLoop()