notas = [
    ["Ana", [8, 7, 9]],
    ["Carlos", [5, 6, 7]],
    ["João",[ 10, 9, 8]],
]

for aluno in notas:
    nome_aluno = aluno[0]
    media = sum(aluno[1]) / len(aluno)

print(f'a media do aluno {nome_aluno} é de {media}')