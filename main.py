import sys

from dotenv import load_dotenv

from mau_doctorgo.dashboard_v1 import run as mau1
from mau_doctorgo.dashboard_v2 import run as mau2
from mau_doctorgo.dashboard_v3 import run as mau3
from recycler.dashboard_v1 import run as recycler1


def main():
    print('Seleccione una opción:')
    print('1. MAU Dashboard 1')
    print('2. MAU Dashboard 2')
    print('3. MAU Dashboard 3')
    print('4. RECYCLER Dashboard 1')
    print('0. Salir')

    option = input()

    if option == '1':
        load_dotenv('.env.mau')
        dashboard1 = mau1()
        dashboard1.run()
    elif option == '2':
        load_dotenv('.env.mau')
        dashboard2 = mau2()
        dashboard2.run()
    elif option == '3':
        load_dotenv('.env.mau')
        dashboard2 = mau3()
        dashboard2.run()
    elif option == '4':
        load_dotenv('.env.recycler')
        dashboard3 = recycler1()
        dashboard3.run()
    elif option == '0':
        sys.exit()
    else:
        print('Opción inválida. Intente de nuevo.')

if __name__ == '__main__':
    main()