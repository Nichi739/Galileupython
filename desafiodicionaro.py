loja_games  = {
    "Minecraft" : {"Preço" : 59.90, "Estoque": 5},
    "Fifa23" : {"Preço" : 199.90, "Estoque": 3},
    "God of war" : {"Preço" : 149.90, "Estoque": 4},
}
for jogo, info in loja_games.items():
    print(f' Jogo: {jogo} - Preço: {info['Preço']} - Estoque: {info['Estoque']}')

#CONFIGURANDO ESCOLHA DO CLIENTE
escolha_cliente = input("Qual jogo da loja do Nichi você deseja?").strip().capitalize()

#verificando se existe o jogo
if escolha_cliente in loja_games:
    print("O jogo está disponivel :D")
    quantidade_solicita = int(input("Quantas unidades você quer?"))
    if quantidade_solicita >= loja_games[escolha_cliente]['Estoque']:
        print("Essa quantidade não está disponível :C")

else:
    print('O jogo não está disponivel, VÁ EMBORA AGORA')


