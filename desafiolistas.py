arenas = [
    [1200, 1500, 1100, 1800, 1700], # arena 1
    [1000, 950, 1100, 1050, 980],   # arena 2
    [2000, 1900, 1950, 2100, 2200]  # arena 3
]

contador = 0
lista_medias = []


#CRIEI UM LAÇO PARA PERCORRER A LISTA ARENAS
for a in arenas: #'Para cada a(arena) dentro da lista ARENAS
    contador += 1 #estou somando 1 do antigo valor da variavel contador
    media_arenas = sum(a) / len(a) #Calculando a media de cada lista dentro da lista arenas
    lista_medias.append(media_arenas) #Adicionando a media calculada na lista_medias
    print(f'A media da arena {contador} é de: {media_arenas}')
    print(lista_medias)
    print(f'A maior pontuação entre as arenas é de: {max(lista_medias)}')

