from OpenGL.raw.GLUT import glutBitmapCharacter

from OpenGL.raw.GLUT.constants import GLUT_RGB

from OpenGL.GL import *
from OpenGL.GLUT import *
from background import run
from config import Settings
import argparse, sys, os.path


width, height = 800, 600

settings = Settings()

colors_to_randomize = {
    'R': False,
    'G': False,
    'B': False
}

random_factor = 0

window = None

PROMPT = ("ESC - SAIR","C - TROCAR DE OBJETO")


def check_args():
    global colors_to_randomize, random_factor

    parser = argparse.ArgumentParser(description="Textura randomica a partir da coloracao")
    parser.add_argument('random_factor', metavar='F', help='Fator de randomizacao (escolha entre 0-1)')
    parser.add_argument('--colors', metavar='C', default='RGB', help='Cores a serem randomizadas (e.g: RGB)')

    args = parser.parse_args()

    if not (0 <= float(args.random_factor) <= 1):
        print "Entrada invalida %r (Digite um fator de randomizacao entre 0-1)" % args.random_factor
        print "Tipo python %s -h para mais informacoes." % sys.argv[0]
        sys.exit(1)

    for c in args.colors:
        if str(c).upper() not in ['R', 'G', 'B']:
            print "Entrada invalida %r (A opcao %r nao e valida, opcoes validas (RGB))" % (args.colors, c)
            print "Tipo python %s -h para mais informacoes." % sys.argv[0]
            sys.exit(1)
        colors_to_randomize[str(c).upper()] = True

    random_factor = args.random_factor


def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(2.0)
    glBegin(GL_POINTS)
    glColor3f(0.0, 1.0, 1.0)

    print '\nCarregando objeto... Aguarde um momento!'
    sc = run(width, height, colors_to_randomize, float(random_factor), settings)
    print 'Objeto carregado\n'

    glEnd()
    glFlush()
    glutSwapBuffers()


def handle_keyboard(*args):
    global settings
    ESC = '\x1b'

    if args[0] == ESC:
        glutDestroyWindow(window)
    elif args[0] == 'c':
        path = raw_input('\n - Insira o caminho com nome do novo objeto: ')
        if os.path.isfile(path):
            settings.object_input = path
        else:
            print 'Erro! Caminho errado ou o arquivo do objeto nao existe!!!\n'
            return
        camera_path = raw_input(' - Insira o caminho com nome do arquivo de camera correspondente ao objeto: ')
        if os.path.isfile(camera_path):
            settings.camera_input = camera_path
        else:
            print 'Erro! Caminho errado ou o arquivo da camera nao existe!!!\n'

        new_random_factor = raw_input(' - Insira o fator de randomizacao entre 0-1, caso deseje mudar o atual: ')
        if len(new_random_factor) > 0:
            try:
                global random_factor
                tmp = float(new_random_factor)
                random_factor = tmp
            except:
                print ' A entrada %r e um fator invalido!!! O fator antigo permanecera.'

        new_random_colors = raw_input(' - Insira os tipos de cores a serem randomizadas [RGB], caso deseje mudar as atuais: ')
        global colors_to_randomize
        if len(new_random_colors) > 0:
            for c in new_random_colors:
                if str(c).upper() in ['R', 'G', 'B']:
                    for color in ['R', 'G', 'B']:
                        colors_to_randomize[color] = False
                    for c2 in new_random_colors:
                        if str(c2).upper() in ['R', 'G', 'B']:
                            colors_to_randomize[str(c2).upper()] = True
                    break





        glutPostRedisplay()



def init():
    glClear(GL_COLOR_BUFFER_BIT)

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glOrtho(0.0, width, height, 0.0, -5.0, 5.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


if __name__ == '__main__':
    check_args()

    print "\nAperte 'c' para mudar de objeto .\nAperte ESC para sair\n"
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow('PG2 - Random Color Texture')

    glutDisplayFunc(render)
    glutKeyboardFunc(handle_keyboard)

    glClearColor(0, 0, 0, 0)
    init()
    glutMainLoop()