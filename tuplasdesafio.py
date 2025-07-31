estoque = (
   ("Mouse LG Tech", 10),
   ("Mic Hyper X", 5),
   ("Acer Nitro 5", 3),
   ("Webcam HD", 0)
)

#sempre debugar o código
print('PRODUTOS COM MENOS DE 5 UNIDADES')
soma = 0 #estou somando cada item da tupla estoque
soma += i1

for i in estoque: #usei uma estrutura de laço para pecorrer todos os itens da loja
    if i[1] < 5: #verificando se cada tinha ou não 5 unidades
        print(f'-{i[0]}') #se a linha de cima é verdade
    if i[1] == 0:
        contador += 1
 
#PROGRAMEM A QTDADE DE ITENS ZERADOR DENTRO DA TUPLA ESTOQUE

       
print(f'produto escotados {contador}')
print(f'A soma do produtos é: {soma}')