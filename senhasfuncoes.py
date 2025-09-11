senha = 'alvoro213'

def validar_senha ():
    senha_tentativa = input('Digite a sua senha:')
    if senha_tentativa == senha:
        print("Acesso liberado!")
    else:
        print('Acesso negado')

validar_senha()