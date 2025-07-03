# MÉTODOS .APPEND(ELEMENTO A ADICIONAR)
lista = ['banana', 'maca', 'pêra', 'morango', 'kiwi']

lista.append('kiwi')
print(lista)

# MÉTODO .INSERT, ADICIONA UM ELEMENTO EM UMA POSIÇÃO ESPECIFICADA

lista.insert(2, 'pêra')
print(lista)

# MÉTODO .remove('banana'), ELE REMOVE UM ELEMENTO ESPECIFICADO

lista.remove('banana')
print(lista)

lista_idades = [33, 11, 13, 19, 42]
# método .sort(), ele organiza uma lista em ordem alfabetica ou numerica
lista_idades.sort()
print(lista_idades)

lista_idades.sort(reverse=True)
print(lista_idades)

# MÉTODO .reverse(), inverte a ordem da lista - pórem não organiza!

lista_idades.reverse()
print(lista_idades)

lista2 = ['banana', 'maca', 'pêra', 'morango', 'kiwi', 'banana']
# MÉTODO .count(ITEM PROCURADO) -> Conta o nujmero de vezes que o item aparece na lista

print(lista2.count('banana'))

#MÉTODO LEN (NOME DA LISTA) -> Retorna o tamanho de ua lista

print(len(lista2))
