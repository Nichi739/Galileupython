
import random

pokemons = {
    'charmander': {'ataque':'bola de fogo','dano':35},
    'squirtlechatao': {'ataque':'jato de água','dano': 32},
    'bulbassauro': {'ataque':'chicote de sipó','dano': 30},
}

def selecionar_pokemon(jogador):
    print('selecione seu pokemon'.center(40,'-'))
    print(' (1) Charmander \n (2) squirtlechatao \n (3) bulbassauro')
    print('_'*40)
    escolha = int(input('Escolha seu pokemon (1,2 ou 3): '))
    if escolha ==1:
        escolha = 'Charmander'
    if escolha2 ==2:
        escolha2 = 'squirtkechatao'
    if escolha == 3: 'bulbassauro'
        
selecionar_pokemon()
def ficha_habilidades(escolha):
    print('ficha habilidades'.center(40,'-'))
