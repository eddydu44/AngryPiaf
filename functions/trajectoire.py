import pygame
import functions.init as init
from math import sqrt
from math import asin
from math import pi

def springLenght(x0, y0, x1, y1):
    return sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
def costheta(x0, y0, x1, y1):
    if springLenght(x0, y0, x1, y1) != 0:
        return (x1 - x0) / springLenght(x0, y0, x1, y1)
    else:
        return (x1 - x0) / 0.0001
def sintheta(x0, y0, x1, y1):
    if springLenght(x0, y0, x1, y1) != 0:
        return (y1 - y0) / springLenght(x0, y0, x1, y1)
    else:
        return (y1 - y0) / 0.0001

def run():
    ### INI
    # On enregistre les coordonnées de l'oiseau au moment du laché de la souris

    x0, y0 = init.coord[0], 349 - init.coord[1]     # On inverse les coord Y pour faire les calculs, 349 pour ne pas toucher la groundLine
    x1, y1 = 177, 177                               # emplacement de l'origine de l'élastique
    x0,y0,x1,y1 = x0/100, y0/100, x1/100, y1/100    # on applique l'échelle 1m=100px

    m           = 2        # masse en kg de l'oiseau
    k           = 200      # constante de raideur de l'élastique en N/m
    L0          = 0.1      # longueur à vide de l'élastique en m
    e           = init.e   # coefficient de restitution (5/9)
    g           = 9.81     # intensité de pensanteur
    totalTime   = 0        # on initialise le tmp à 0s
    intervalle  = init.intervalle     # pour correspondre aux 60 fps
    angle       = asin(sintheta(x0, y0, x1, y1))

    ###Calculs 
    
    ## Avant rebond -> equation de trajectoire parabolique
    # On calcule la vitesse initiale avec l'energie potentielle élastique, puis on définie une équation de trajectoire (avec comme seule force le poids)
    # On applique l'équation de trajectoire toutes les n ms pour établir une liste de points empruntés par le projectile
    # On s'arrete quand on touche le sol, soit y=0 ou t=tfinal

    C           = sqrt(k / m) * (springLenght(x0, y0, x1, y1) - L0)

    v0x         = C * costheta(x0, y0, x1, y1)
    v0y         = C * sintheta(x0, y0, x1, y1)

    def Y(t): 
        return -g * 0.5 * t ** 2 + v0y * t + y0     # equation de trajectoire selon Y

    def X(t):
        return v0x * t + x0                         # equation de trajectoire selon X

    Tf = (v0y + sqrt(v0y ** 2 + 2 * g * y0)) / g
    totalTime += Tf
    P = []
    T = 0                                           # Temp total en mouvement

    while T <= Tf:
        P += [[X(T), Y(T)]]
        T += intervalle
    
    P += [[X(Tf), Y(Tf)]] # on ajoute le dernier point

    ## Après rebond
    ## On recalcule des equations de trajectoires après application d'un coefficient de restitution
    ## On répète l'opération jusqu'à ce que le temp de rebond soit inférieur à 0.1s (minimum 2 rebonds)
    ## Le projectile est alors arreté (on pourrais rajouté des frottement au sol)

    r = 0 # nombre de rebonds

    while Tf >= 0.4 or r <= 2:
        v0x     *= e                        # coefficient de restitution
        v0y     = -1 * (v0y - g * Tf) * e   # on recalcule v0y après chute libre et on applique le coef
        lastY   = P[-1][1]                  # les derniers points sont utilisés comme condition initiale
        lastX   = P[-1][0]

        def Yr(t):
            return -g * 0.5 * t ** 2 + v0y * t + lastY

        def Xr(t):
            return v0x * t + lastX

        Tf = (v0y + sqrt(v0y ** 2)) / g     # On estime que l'on part de l'ordonnée 0 (pas +v0y...)
        totalTime += Tf
        T = 0
        while T <= Tf: 
            P += [[Xr(T), Yr(T)]]
            T += intervalle
        P += [[Xr(Tf), Yr(Tf)]]
        r += 1

    # On retransforme dans les coord pygame
    
    for i in range(len(P)):
        P[i][0]*=100                # 100 px = 1 m
        P[i][1]*=100                # 100 px = 1 m
        P[i][1] = 349 - P[i][1]

    pygame.draw.lines(init.surface, (0, 0, 0), False, P, 3)         # Affichage instanné de la courbe de trajectoire

    init.valuesTraj=f'distance (m): {round(P[-1][0]/100,2)} \n' #####
    init.valuesTraj+=f'total points: {len(P)} \n'               # Ajout des valeures calculées
    init.valuesTraj+=f'total time: {round(totalTime,2)} \n'     # pour la fenêtre d'info
    init.valuesTraj+=f'angle: {round(angle*180/(pi),2)} \n'     #####

    return P  


# Pour les fonctions rebond et collision :

def basicTraj(lastX,lastY,v0x,v0y): # fonction qui renvoie une liste de point pour une simple chute libre avec CI
    
    g           = 9.81     # intensité de pensanteur
    intervalle  = init.intervalle     # pour correspondre aux 60 fps

    def Y(t):
            return -g * 0.5 * t ** 2 + v0y * t + lastY

    def X(t):
        return v0x * t + lastX

    Tf = (v0y + sqrt(v0y ** 2 + 2 * g * lastY)) / g
    T = 0
    P = []
    while T <= Tf: 
        P += [[X(T), Y(T)]]
        T += intervalle
    P += [[X(Tf), Y(Tf)]]

    for i in range(len(P)):
        P[i][0]*=100
        P[i][1]*=100
        P[i][1] = 355 - P[i][1]

    return P