
import random

pokemons = {
    'charmander': {'ataque':'bola de fogo','dano':35},
    'squirtlechatao': {'ataque':'jato de água','dano': 32},
    'bulbassauro': {'ataque':'chicote de sipó','dano': 30},
}


jogador1 = ''
jogador2 = ''

def selecionar_pokemon(jogador):
    print('selecione seu pokemon'.center(40,'-'))
    print(' (1) charmander \n (2) squirtlechatao \n (3) bulbassauro')
    print('_'*40)
    escolha = int(input('Escolha seu pokemon  (1,2 ou 3): '))
    if escolha ==1:
        escolha = 'charmander'
    elif escolha ==2:
        escolha = 'squirtlechatao'
    elif escolha == 3: 
        escolha = 'bulbassauro'
    else:
        print(f'não entendi,digite 1 a 3 para selecionar um pokemon')
    
    return escolha


escolha1 = selecionar_pokemon(jogador1)
escolha2 = selecionar_pokemon(jogador2)


def ficha_habilidades(escolha):
    print(f'FICHA DE HABILIDADES LEGAIS'.center(40,'-'))
    print(f'Ataque: {pokemons[escolha]['ataque']} e Dano: {pokemons[escolha]['dano']}')

ficha_habilidades(escolha1)

ficha_habilidades(escolha2)

def dano_critico (escolha):
    dano_critico = pokemons[escolha]['dano'] * random.uniform(1,2)
    print(f'o dano_critico do {escolha} é de {dano_critico:.2f}')
    return dano_critico

d1 =dano_critico(escolha1)
d2 = dano_critico(escolha2)

#CRIEM UMA FUNCAO SE CHAMADA BATALHA (DANO) (DANOCRITICO1) (DANOCRITICO2)
#CADA POKEMON TEM 100 DE VIDa
#NO FINAL DESSA BATALHA, MOSTRE O VENCEDOR

def batalha (dano1, dano2):
    vida1 = 100 - dano2
    vida2 = 100 - dano1
    if vida1 > vida2:
        print(f'o vencedor é o player1, vida restante: {vida1:.2f}')
    else:
        print(f'o vencedor é o player2, vida restante {vida2:.2f}')

batalha(d1,d2)