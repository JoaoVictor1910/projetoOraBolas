#Adicionando path dependencias#
from pathlib import Path; import sys
path_root = Path(__file__).parents[0]
sys.path.insert(0, str(path_root) + "\\Dependencias")
#---------------------------------#

#Importando dependecias
import os, sys, random
from math import *
import time; import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation
###Fim das dependecias###

#Verificar comando do OS para limpar o terminal Repl.it = "clear" | Windows = "cls"
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

#########################
#                       #
#   Projeto Ora Bolas   #
#                       #
#########################

#DataParser, Objetivo: ler dinamicamente o conteudo do arquivo e adicionar em uma tabela,para ser usada
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

#t = np.linspace(0, 100, 5)

# Create the figure and the line that we will manipulate

StartAnimFrame = 0

fig, ax = plt.subplots(facecolor='grey', num='Projeto Ora Bolas')
plt.autoscale(enable=True, axis='both', tight=True)
plt.grid(color=(0.1,0.1,0.1, 0.4), linestyle='dotted',  )
geticon = plt.get_current_fig_manager()
geticon.window.wm_iconbitmap("icone.ico")

line, = plt.plot(StructData[1][0:StartAnimFrame], StructData[2][0:StartAnimFrame], lw=2)

prediceptdist, = plt.plot([3, StructData[1][StartAnimFrame]], [3,StructData[2][StartAnimFrame]], lw=0.5, color="red")
curriceptdist, = plt.plot([3, StructData[1][StartAnimFrame]], [3,StructData[2][StartAnimFrame]], lw=0.5, color="green")
dificeptdist, = plt.plot([3, StructData[1][StartAnimFrame]], [3,StructData[2][StartAnimFrame]], lw=0.5, color="yellow")

ax.set_xlabel('Posição X/m')
ax.set_ylabel('Posição Y/m')

ax.set_ylim(bottom=0)
ax.set_ylim(top=6)

ax.set_xlim(left=0)
ax.set_xlim(right=9)  

ax.set_facecolor((0.6, 0.6, 0.6))

axslidercolor = (0.2, 0.2, 0.2)
axbuttoncolor = "#4666dd"
axhovercolor = "#e2a122"

accreq_ctx = ax.annotate(str("  [G] A REQ: N/A"), (3, 3.8), transform=fig.transFigure, fontsize=7)
timedist_ctx = ax.annotate(str("  [G] TD: N/A"), (3, 3.5), transform=fig.transFigure, fontsize=7)
interdist_ctx = ax.annotate(str("  [G]DI: N/A"), (3, 3.2), transform=fig.transFigure, fontsize=7)

diftimedist_ctx = ax.annotate(str("  ITD: N/A"), (3, 3.8), transform=fig.transFigure, fontsize=7)

aceleracao_ctx = ax.annotate(str("  D: N/A"), (3, 5.5), transform=fig.transFigure, fontsize=7)


robobola = plt.Circle((3, 3), 0.09, fc=(0.8,0.2,1), edgecolor=(0.2, 0.2, 0.2))                                                                     #robo | d = 180mm -> r = d/2 -> 0.09r

bolinha = plt.Circle((StructData[1][StartAnimFrame], StructData[2][StartAnimFrame]), 0.05, fc=(1,1,1), edgecolor=(0.2, 0.2, 0.2))                  #bolinha | d = 50mm -> r = d/2 -> 0.025r - coloquei 0.05 pq se n nem da pra ve kkkkkkk
raioIntercept = plt.Circle((StructData[1][StartAnimFrame], StructData[2][StartAnimFrame]), 0.75, edgecolor=(0.7, 0.1, 0.2, 0.4), fc=(0,0,0,0))     #bolinha | d = 1.5m -> r = d/2 -> 0.75r

raioRoboInicialPos = plt.Circle((StructData[1][StartAnimFrame], StructData[2][StartAnimFrame]), 0.50, edgecolor="#48fe1b4f", fc=(0,0,0,0)) #raio maximo da pos do robo | d = 1m -> r = d/2 -> 0.5r


ax.add_patch(robobola)
ax.add_patch(bolinha)
#ax.add_patch(raioIntercept)
ax.add_patch(raioRoboInicialPos)

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the frequency.
#axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axslidercolor)
#XSlider = Slider(
#    ax=axfreq,
#    label='Time elepsed',
#    valmin=0.1,
#    valmax=100,
#    valinit=100,
#)

# Make a vertically oriented slider to control the amplitude
#axamp = plt.axes([0.1, 0.25, 0.0225, 0.63], facecolor=axslidercolor)
#YSlider = Slider(
#    ax=axamp,
#    label="Amplitude",
#    valmin=0,
#    valmax=100,
#    valinit=50,
#    orientation="vertical"
#)
  

#fig.canvas.draw_idle()

def updateSlider(val):
  fig.canvas.draw_idle()
  #ax.set_xlim(bottom=XSlider.val)
  #ax.margins(x=3)
  #ax.margins(y=2)

# register the update function with each slider
#XSlider.on_changed(updateSlider)
#YSlider.on_changed(updateSlider)

#Variaveis "Globais" em tipo função
def Outvar():
  #Timer handler#
  Outvar.t_end = time.time() + (StructData[0][-1] - StructData[0][StartAnimFrame]) # TempoAtual +  (TempoFinal - TempoInicial[em funçao do StartFrame] )
  Outvar.t_clockwise = time.time()
  Outvar.stoptimer = False
  Outvar.pauseanim = False
  Outvar.timeinterdist = 0
  Outvar.timeframed = 0
  #Frame handler#
  Outvar.frametime = 0
  Outvar.old_frame = 0
  Outvar.max_frames = len(StructData[0]) - 1 #compensate index 0
  Outvar.predictamount = 10
  Outvar.forceclampframe = False
  Outvar.futureframes = 1
  Outvar.keyframed = 0
  Outvar.iframed = 0
  #Physics handler
  Outvar.aceleracao = 0
  Outvar.Distancia = 0
  Outvar.DistanciaTotal = 0
  #Position handler
  Outvar.predpos = (-1,-1)
  #Debug settings
  Outvar.i = StartAnimFrame
Outvar()

#Start/Stop/Restart animation buttons#
Outvar.predpoint = plt.Circle((-1,-1), 0.05, fc=(0.2, 0.4, 0.9), edgecolor=(0.2, 0.2, 0.2)) 
ax.add_patch(Outvar.predpoint)
KeyframeButton = Button(plt.axes([0.62, 0.025, 0.12, 0.04]), 'Add point', color=axbuttoncolor, hovercolor='0.7')
def keyframeanim(self):
  Outvar.predpos = (StructData[1][Outvar.futureframes], StructData[2][Outvar.futureframes])
  #ax.annotate(str(f"  FRAME: {Outvar.futureframes}"), predpos, transform=fig.transFigure, fontsize=7)
  Outvar.keyframed = Outvar.futureframes
  Outvar.timeframed = Outvar.timeinterdist
  Outvar.iframed = Outvar.i
  print(f"[KEYFRAME] ADDED POINT AT FRAME: {Outvar.futureframes} | REACH AT: {round(Outvar.timeinterdist + StructData[0][Outvar.i], 2)}s")

KeyframeButton.on_clicked(keyframeanim)
StartAnimbutton = Button(plt.axes([0.2, 0.025, 0.1, 0.04]), 'Start', color=axbuttoncolor, hovercolor='0.7')
def resumeanim(self):
  if Outvar.i >= Outvar.max_frames:
    reset(None)
  Outvar.t_end = time.time() + (StructData[0][-1] - StructData[0][Outvar.i]) #Time compensation
  Outvar.pauseanim = False
  anime.resume()
StartAnimbutton.on_clicked(resumeanim)

RestartAnimbutton = Button(plt.axes([0.8, 0.025, 0.1, 0.04]), 'Restart', color=axbuttoncolor, hovercolor='0.7')
def reset(event):
  Outvar()
  plt.figure().clear()
  anime.frame_seq = anime.new_frame_seq()
  anime.resume()
  if Outvar.keyframed > 0:
    Outvar.predpoint.remove() 
  #XSlider.reset()
  #YSlider.reset()
RestartAnimbutton.on_clicked(reset)

StopAnimbutton = Button(plt.axes([0.4, 0.025, 0.1, 0.04]), 'Stop', color=axbuttoncolor, hovercolor='0.7')
def pauseanim(self):
  Outvar.pauseanim = True
  anime.pause() 
StopAnimbutton.on_clicked(pauseanim)
#----------------------------#

def animate(ix):
  #Fix resize glitches
  if Outvar.pauseanim:
    Outvar.i -= 1
    anime.pause()
    
  main_clock = Outvar.t_end - time.time()

  #Sincronizar tempo com frames
  if main_clock - StructData[0][-Outvar.i-1] <= 0:
    Outvar.i += 1

  is_finished = ""
  if Outvar.i == Outvar.max_frames:
    Outvar.stoptimer = True
    anime.event_source.stop()
    #idealframe = (Outvar.max_frames * Outvar.frametime) * 0.001 if Outvar.frametime > 0 else 1^-8
    timeused = StructData[0][-1] - round(main_clock, 2)
    is_finished = f"""
==============DEBUG==============
- FINISHED AT {abs(round(main_clock, 2))} 
- TempoUsado: {round(timeused, 2)} de {StructData[0][-1]}
- Distancia Max: {round(Outvar.DistanciaTotal, 2)}m/s²
=================================
  """ if Outvar.stoptimer else ""

#- IdealFrame: {round(idealframe, 3)} 
#- TempoPorEficiencia: {round(timeused - idealframe, 2)}
#- EficienciaEmPorcento: {int(100 - (((timeused - idealframe) / idealframe) * 100))}%

    print("ELAPSED: {0} - {1:.2f} | D: {dist:.4f} - DT: {t_dist:.2f} {2}".format(
      Outvar.i, 
      StructData[0][Outvar.i], 
      is_finished, 
      #round(main_clock - StructData[0][-Outvar.i],2), 
      dist=Outvar.Distancia,
      t_dist=Outvar.DistanciaTotal
      )
    )

  #Desenhar tudo#
  if Outvar.i < Outvar.max_frames:
    
    Xposition = StructData[1]
    Yposition = StructData[2]
    
    line.set_data(Xposition[0:Outvar.i], Yposition[0:Outvar.i])
    
    curriceptdist.set_data([3,Xposition[Outvar.i]], [3, Yposition[Outvar.i]])
    
    Outvar.forceclampframe = Outvar.i + int(Outvar.predictamount / 2) > Outvar.max_frames
    Outvar.futureframes = Outvar.max_frames if Outvar.forceclampframe else Outvar.i + int(Outvar.predictamount / 2)
    
    prediceptdist.set_data([3,Xposition[Outvar.futureframes-1]], [3, Yposition[Outvar.futureframes-1]])
    
    dificeptdist.set_data(Xposition[Outvar.i:Outvar.futureframes], Yposition[Outvar.i:Outvar.futureframes])
    #dificeptdist.set_data([Xposition[Outvar.i],Xposition[futureframes]], [Yposition[Outvar.i], Yposition[futureframes]])
    
    diftimedist_ctx.set_position([Xposition[Outvar.futureframes], Yposition[Outvar.futureframes]])
      
    interdist = sqrt(pow(np.sum(Xposition[Outvar.i:Outvar.futureframes]) - Xposition[Outvar.futureframes] ,2) + pow(np.sum(Yposition[Outvar.i:Outvar.futureframes]) - Yposition[Outvar.i],2))
    interacc = interdist/ (Outvar.predictamount / 100)
    Outvar.timeinterdist = round(interdist/interacc, 2)
    diftimedist_ctx.set_text(f"  ITD: {Outvar.timeinterdist}s ({((Outvar.predictamount) / 2)})")
           
    aceleracao_ctx.set_position([Xposition[Outvar.i], Yposition[Outvar.i]])
    aceleracao_ctx.set_text(f"   A:{round(Outvar.aceleracao * 3.6, 2)}km/h")

    #interdist_ctx.set_position([Xposition[Outvar.i], Yposition[Outvar.i]])
    DistanceIntercept = sqrt(pow(Xposition[Outvar.i+1] - 3 ,2) + pow(Yposition[Outvar.i+1] - 3 ,2))
    interdist_ctx.set_text(f"  [G] DI: {round(DistanceIntercept, 2)}m")
    
    
    Outvar.predpoint.center = Outvar.predpos
    
    bolinha.center = ([Xposition[Outvar.i], Yposition[Outvar.i]])
    raioIntercept.center = ([Xposition[Outvar.i], Yposition[Outvar.i]]) 

    if (Outvar.old_frame != Outvar.i):
      Outvar.old_frame = Outvar.i      
      
      Outvar.Distancia = sqrt(pow(Xposition[Outvar.i+1]-Xposition[Outvar.i],2) + pow(Yposition[Outvar.i+1]-Yposition[Outvar.i],2)) #sqrt((Xb-Xa)^2 + (Yb-Ya)^2)
      Outvar.DistanciaTotal += Outvar.Distancia      
      
      Outvar.aceleracao = Outvar.Distancia / 0.02 #(StructData[0][Outvar.i+1] - StructData[0][Outvar.i])
      timedistance = round(DistanceIntercept/Outvar.aceleracao, 2)
      Outvar.predictamount = int(timedistance * 100)
      timedist_ctx.set_text(f"  [G] TD: {round(timedistance, 2)}s ({int(timedistance * 100)})")
      
      AccRequired = 2 * (DistanceIntercept - 0 * timedistance) / pow(timedistance,2)
      accreq_ctx.set_text(f"  [G] A REQ: {round(AccRequired, 2)}m/s²")      
      
      print("ELAPSED: {0} - {1:.2f} | D: {dist:.4f} - AC: {acc:.2f}m/s -> {kmacc:.2f}km/h - DT: {t_dist:.2f} {2}".format(
        Outvar.i, 
        StructData[0][Outvar.i], 
        is_finished, 
        #round(main_clock - StructData[0][-Outvar.i],2), 
        dist=Outvar.Distancia,
        t_dist=Outvar.DistanciaTotal,
        acc= Outvar.aceleracao,
        kmacc=Outvar.aceleracao * 3.6
        )
      )
    if main_clock < 0:
      #line.set_color("red")
      if not Outvar.stoptimer:
        print(f"[GLITCH] TIMEOUT REACHED: {abs(round(main_clock, 2))} --> {round(StructData[0][-1] + abs(main_clock), 2)}")
        
  if Outvar.keyframed == Outvar.i:
    currframe = StructData[0][Outvar.i]
    oldballtime = StructData[0][Outvar.iframed]
    framedkey = oldballtime + Outvar.timeframed
    print(f"""
-------------------------------------------------------          
[KEYFRAME] KEYPOINT REACHED! PREDICTED from {oldballtime}s to {round(framedkey, 2)}s 
[KEYFRAME] PRED DIF: {round(abs(currframe - framedkey), 4)} ({round(currframe, 2)} - {round(framedkey, 2)})
[KEYFRAME] ACCURACY: {round(100 - ((abs(framedkey - currframe) / currframe) * 100), 1)}% 
-------------------------------------------------------    
""")
    Outvar.keyframed = 0
    anime.pause()
    
  main_return = [line, prediceptdist, dificeptdist, bolinha, interdist_ctx, aceleracao_ctx, timedist_ctx, diftimedist_ctx, accreq_ctx, curriceptdist, Outvar.predpoint]
  main, *others = main_return
  return main, *others

anime = animation.FuncAnimation(fig, animate, interval=Outvar.frametime, frames=Outvar.max_frames, blit=True, cache_frame_data=False) #blit=True 
#plt.subplots_adjust(right=0.955,top=0.8, bottom=1)
plt.show()

"""
print("T----------------------------\n")
print(StructData[0])
print("X----------------------------\n")
print(StructData[1])
print("Y----------------------------\n")
print(Yposition)
print("----------------------------\n")
"""