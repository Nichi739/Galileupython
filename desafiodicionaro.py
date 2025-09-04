loja_games  = {
    "Minecraft" : {"Preco" : 59.90, "Estoque": 5},
    "Fifa23" : {"Preco" : 199.90, "Estoque": 3},
    "God of war" : {"Preco" : 149.90, "Estoque": 4},
}

carrinho = {}

for jogo, info in loja_games.items():
    print(f' Jogo: {jogo} - Preco: {info['Preco']} - Estoque: {info['Estoque']}')

#CONFIGURANDO ESCOLHA DO CLIENTE
while True:
    escolha_cliente = input("Qual jogo da loja do Nichi você deseja?").strip().capitalize()
    if escolha_cliente == 'Sair':
        break

#verificando se existe o jogo
    if escolha_cliente in loja_games:
        print("O jogo está disponivel :D")
        quantidade_solicita = int(input("Quantas unidades você quer?"))
        if quantidade_solicita > loja_games[escolha_cliente]['Estoque']:
            print("Essa quantidade não está disponível :C")
        else: #cenário onde tem estoque disponível, vamos subtrair a quantidade do dicionário loja
            print('Compra realizada com sucesso. Adicionado no carrinho!')
            loja_games[escolha_cliente]['Estoque'] -= quantidade_solicita
            carrinho[escolha_cliente] = quantidade_solicita

    else:
        print('O jogo não está disponivel, VÁ EMBORA AGORA')


    print(carrinho)
    print(f'O estoque atual do jogo escolhido é: {loja_games[escolha_cliente]['Estoque']}')

total = 0
print('RESUMO DA COMPRA'.center(40,'-'))
for jogo, qtd in carrinho.items():
    Preco = loja_games[jogo]['Preco']
    total += Preco * qtd
    print(f'{jogo}  x{qtd} unidades'.center(40))
print('-'*40)
print(f'Total: R$ {total:.2f}'.center(40))





