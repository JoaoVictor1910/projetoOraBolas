# importar funções do Sistema
import os, time, sys, random

#Verificar comando do OS para limpar o terminal Repl.it = "clear" | Windows = "cls"
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

#test

#DataParser, Objetivo: ler dinamicamente o conteudo do arquivo e adicionar em uma tabela,
#para ser usada
def DataParser(nome):

  CacheParser = [
    [], #Tempo (t/s)
    [], #X Cord (x/m)
    [], #Y Cord (y/m)
  ]

  with open("{}".format(nome), "r", encoding='UTF-8') as file:
    for line in file:

      conc_line = ""  #criar cache para string, será usado no ParserCore
      next_table = 0  #mudar tabela conforme faz o parser

      #não adicionar para parsear se a linha estiver quase vazia.
      if len(line) <= 3:
        line = ""

      #ParserCore: Irá ler caractere por caractere e se achar algo diferente do que esta
      #denominado na whitelist, vai ser mandado para a respectiva tabela (T, X ou Y)  
      for i in range(len(line)):
        v_char = line[i]

        #se o caractere for alphanumerico, "," ou "/", concatene. 
        if (v_char.isalnum() or v_char == "," or v_char == "/"):
          conc_line += v_char
        #se o caracter for "\n" ou "\x20", significa que chegou no final dos valores.
        elif (next_table <= 2 and (v_char != "\n" or v_char != "\x20")):

          #Se houver algum erro na conversão para float, não converta.
          try:
            convert_to_float = float(conc_line.replace(",", ".")) # '0,5' -> 0.5
            CacheParser[next_table].append(convert_to_float)
          except ValueError:
            convert_to_float = None

          #apos inserir o valor na tabela, delete o cache e va para proxima tabela.
          conc_line = ""
          next_table += 1
  return CacheParser

#Retorna tabela de valores parseados do arquivo .dat
StructData = DataParser("data.dat") #Nome do arquivo para parsear as informações do arquivo .dat

#StructData = {
# Tempo = [] -> i=0
# CordX = [] -> i=1
# CordY = [] -> i=2
#}
"""
time_test = 0
cache_time = -1
iterations = 0
t_start = round(time.time(), 2)
while round(time.time(), 2) < (t_start + StructData[0][-1]) + 0.01:
  time_test = round(round(time.time(), 2) - t_start, 2)
  #clear()

  if (time_test in StructData[0]) and (time_test != cache_time):
    cache_time = time_test
    iterations += 1
    print("FOUND: {0}".format(time_test))
else:
  print("TEST EQUI: ", iterations, " - ", len(StructData[0]))
"""

print("T----------------------------\n")
print(StructData[0])
print("X----------------------------\n")
print(StructData[1])
print("Y----------------------------\n")
print(StructData[2])
print("----------------------------\n")
