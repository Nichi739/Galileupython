pedidos = [
    ("Camisa", "Vestuário", 59.90, "Entregue"),
    ("Tênis", "Calçados", 199.90, "Cancelado"),
    ("Calça", "Vestuário", 89.90, "Entregue"),
    ("Fone de Ouvido", "Eletrônicos", 129.90, "Pendente"),
    ("Meia", "Vestuário", 19.90, "Entregue"),
    ("Notebook", "Eletrônicos", 3299.90, "Entregue"),
    ("Jaqueta", "Vestuário", 139.90, "Cancelado"),
]

somacanceladovestuario = 0

pedidos_entregues = []
print('PRODUTOS ENTREGUES'.center(40, '-'))
for i in pedidos:
    if i[3] == 'Entregue':
        print(f' - {i[0]}')
        pedidos_entregues.append(i[2])
print(pedidos_entregues)
soma = sum(pedidos_entregues)
print (soma)

print('Ultimos 3 pedidos:')


print(pedidos[-1])

for i in pedidos:
    if i[3] == 'Cancelado' and i[1] == 'Vestuário':
        somacanceladovestuario += 1
print(f'cancelados da categoria vestuario: {somacanceladovestuario}')

filtro = input('Digite uma categoria para filtrar: ')

for i in pedidos:
    if filtro == i[1]:
        print(f'- {i[0]}')


