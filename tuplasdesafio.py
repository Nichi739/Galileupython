estoque = (
   ("Mouse LG Tech", 10),
   ("Mic Hyper X", 5),
   ("Acer Nitro 5", 3),
   ("Webcam HD", 0)
)

#sempre debugar o código
print('PRODUTOS COM MENOS DE 5 UNIDADES')

for i in estoque:
    if i[1] < 5:
        print(f'-{i[0]}')

        

