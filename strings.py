frase = "     VINICius é NooB no RUblOx    "

#MÉTODO .STRIP(), exclui os espaços iniciais e os finais
print(frase.strip())

#TÉCNICA DE ENCADEAMENTO DE MÉTODOS
frase3 = '   bem-vindo ao PYTHON!' 
frase3_formatada = frase3.strip().capitalize().replace('python!', 'Onishi')
print(frase3_formatada)