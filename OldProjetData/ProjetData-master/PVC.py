# programme de resolution du probleme du voyaguer de commerce
# par l'algorithme du recuit simule
# Dominique Lefebvre pour TangenteX.com
# 14 mars 2017

# importation des librairies
from scipy import *
from numpy import *
from matplotlib.pyplot import *
from math import *

# parametres du probleme
N = 20    # nombre de villes

# parametres de l'algorithme de recuit simule
T0 = 10.0
Tmin = 1e-2
tau = 1e4

# fonction de calcul de l'energie du systeme, egale a la distance totale
# du trajet selon le chemin courant
def EnergieTotale():
    global trajet
    energie = 0.0
    print("Content of X")
    for row in x:
        print (row)

    coord = c_[x[trajet],y[trajet]]
    print("\nContent of coord")
    print(coord)

    print("\nRoll result")
    print(roll(coord,-1,axis=0))

    print("\nCoord - Roll")
    print(coord - roll(coord,-1,axis=0))

    print("\nSum n°1")
    print(sum((coord - roll(coord,-1,axis=0)), axis=1))
    
    print("\nSum n°2 (squared)")
    print(sum((coord - roll(coord,-1,axis=0))**2, axis=1))

    print("\nSum n°3 (sqrt(squared()))")
    print(np.sqrt(sum((coord - roll(coord,-1,axis=0))**2, axis=1)))

    energie = sum(np.sqrt(sum((coord - roll(coord,-1,axis=0))**2,axis=1)))
    return energie

# fonction de fluctuation autour de l'etat "thermique" du systeme
def Fluctuation(i,j):
    global trajet
    Min = min(i,j)
    Max = max(i,j)
    trajet[Min:Max] = trajet[Min:Max].copy()[::-1]
    return

# fonction d'implementation de l'algorithme de Metropolis
def Metropolis(E1,E2):
    global T
    if E1 <= E2:
        E2 = E1  # energie du nouvel etat = energie systeme
    else:
        dE = E1-E2
        if random.uniform() > exp(-dE/T): # la fluctuation est retenue avec  
            Fluctuation(i,j)              # la proba p. sinon retour trajet anterieur
        else:
            E2 = E1 # la fluctuation est retenue 
    return E2
    
# initialisation des listes d'historique
Henergie = []     # energie
Htemps = []       # temps
HT = []           # temperature

# repartition aleatoire des N villes sur le plan [0..1,0..1]
# Génération aléatoire des listes de position X et Y
x = random.uniform(size=N)
y = random.uniform(size=N)

# definition du trajet initial : ordre croissant des villes
trajet = arange(N)
trajet_init = trajet.copy()

# calcul de l'energie initiale du systeme (la distance initiale e minimiser)
Ec = EnergieTotale()

# boucle principale de l'algorithme de recuit simule
t = 0
T = T0
while T > Tmin:
    # choix de deux villes differentes au hasard
    i = random.random_integers(0,N-1)
    j = random.random_integers(0,N-1)
    if i == j: continue
        
    # creation de la fluctuation et mesure de l'energie
    Fluctuation(i,j) 
    Ef = EnergieTotale()   
    Ec = Metropolis(Ef,Ec)
    
    # application de la loi de refroidissement    
    t += 1
    T = T0*exp(-t/tau)  

    # historisation des donnees
    if t % 10 == 0:
        Henergie.append(Ec)
        Htemps.append(t)
        HT.append(T)

# fin de boucle - affichage des etats finaux
# affichage du reseau
fig1 = figure(1)
subplot(1,2,1)
xticks([])
yticks([])
plot(x[trajet_init],y[trajet_init],'k')
plot([x[trajet_init[-1]], x[trajet_init[0]]],[y[trajet_init[-1]], \
      y[trajet_init[0]]],'k')
plot(x,y,'ro')
title('Trajet initial')

subplot(1,2,2)
xticks([])
yticks([])
plot(x[trajet],y[trajet],'k')
plot([x[trajet[-1]], x[trajet[0]]],[y[trajet[-1]], y[trajet[0]]],'k')
plot(x,y,'ro')
title('Trajet optimise')
show()

# affichage des courbes d'evolution
fig2 = figure(2)
subplot(1,2,1)
semilogy(Htemps, Henergie)
title("Evolution de l'energie totale du systeme")
xlabel('Temps')
ylabel('Energie')
subplot(1,2,2)
semilogy(Htemps, HT)
title('Evolution de la temperature du systeme')
xlabel('Temps')
ylabel('Temperature')
    
