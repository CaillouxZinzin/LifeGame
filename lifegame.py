#!/usr/bin/python3.7

# --- Importation des modules ---
from tkinter import * # interface graphique
import random # génération aléatoire

# --- Objet interface graphique ---
class Interface(Frame):
    # --- Constructeur ---
    def __init__(self,fenetre):
        Frame.__init__(self,fenetre) # appel constructeur de Frame
        self.pack(fill=BOTH)

        # --- Frames ---
        self.main = Frame(self, borderwidth=2, relief=GROOVE) # création frame principale
        self.main.pack(side=LEFT, padx=5, pady=5)
        self.side = Frame(self, borderwidth=2, relief=GROOVE, height= 500) # création frame latérale
        self.side.pack(side=TOP,padx=5, pady=5)

        # --- Barre latérale ---
        self.max = 100
        self.running = False
        self.go = Button(self.side, text="Lancer", command=self.cycle) # création bouton Lancer
        self.go.pack()
        self.stop = Button(self.side, text="Arreter", command=self.stop) # création bouton Arreter
        self.stop.pack()
        self.init = Button(self.side, text="Initialiser", command=self.init) # création bouton Initialiser
        self.init.pack()
        self.taille = Scale(self.side, from_=10, to=self.max, orient=HORIZONTAL, label="Taille de grille") # création curseur Taille de grille
        self.taille.pack()
        self.taille.set(30) # valeur par défaut taille de grille
        self.vie = Scale(self.side, orient=HORIZONTAL, label="% de vie") # création curseur % de vie
        self.vie.pack()
        self.vie.set(25) # valeur par défaut % de vie
        self.vitesse = Scale(self.side, from_=1, to=100, orient=HORIZONTAL, label="Vitesse") # création curseur vitesse
        self.vitesse.pack()
        self.vitesse.set(50)  # valeur par défaut vitesse
        self.quit = Button(self.side, text="Quitter", command=self.quit) # création bouton Quitter
        self.quit.pack()

        # --- Matrice ---
        self.canDim = 250 # dimension du damier
        self.canvas = Canvas(self.main, width=self.canDim, height=self.canDim) # création du damier vide
        self.canvas.pack(padx=5, pady=5)
        self.canvas.grid()

    # --- Affichage matrice ---
    def affichage(self):
        size = self.canDim / self.taille.get() #dimension des cellules
        color = {0:"white", 1:"red"} # couleurs possibles des cellules
        for i in range(self.n):
            for j in range(self.n):
                self.canvas.create_rectangle(i*size, j*size, (i+1)*size, (j+1)*size, fill=color[self.mat[j][i]]) # création d'une cellule

    # --- Initialisation ---
    def bernoulli(self, p):
        i = 1
        while True: # calcul de probabilité sur l'état d'une cellule
            bit = random.randrange(2)
            if bit == 1:
                if (int(2**i*p)&1)==1 :
                    return 1
                else:
                    return 0
            else:
                i = i+1

    def init(self):
        self.running = True # jeu de la vie en cours
        self.n = self.max
        self.mat = [[0]*self.n for i in range(self.n)] # création de la matrice
        self.affichage() # nettoyage du damier
        self.n = self.taille.get() # récupération de la dimension du damier
        vie = 0 # compteur de celulle vivante
        for i in range(self.n):
            for j in range(self.n):
                self.mat[i][j] = self.bernoulli(self.vie.get()/100) # génération aléatoire de la cellule (i,j)
                if self.mat[i][j]==1:
                    vie = vie + 1 # incrémentation du compteur si cellule vivante générée
        self.vie.set(100*vie/self.n**2) # affectation de la valeur % de vie
        self.affichage() # affichage du damier

    # --- Lancement ---
    def nbVoisin(self, i, j):
        v = 0 # compteur du nombre de voisin
        k1 = i-1
        k2 = i+1
        l1 = j-1
        l2 = j+1
        if i==0: # cas particulier de bordure haute du damier
            k1 = self.n - 1
        if i==self.n-1:  # cas particulier de bordure basse du damier
            k2 = 0
        if j==0: # cas particulier de bordure gauche du damier
            l1 = self.n - 1
        if j==self.n-1: # cas particulier de bordure droite du damier
            l2 = -1
        if self.mat[k2][j]==1: # voisin bas
            v = v + 1
        if self.mat[k1][j]==1: # voisin haut
            v = v + 1
        if self.mat[i][l2]==1: # voisin droit
            v = v + 1
        if self.mat[i][l1]==1: # voisin gauche
            v = v + 1
        if self.mat[k2][l2]==1: # voisin bas-droit
            v = v + 1
        if self.mat[k2][l1]==1: # voisin bas-gauche
            v = v + 1
        if self.mat[k1][l2]==1: # voisin haut-droit
            v = v + 1
        if self.mat[k1][l1]==1: # voisin haut-gauche
            v = v + 1
        return v

    def evol(self):
        temp = [[0]*self.n for i in range(self.n)] # matrice temporaire
        for i in range(self.n):
            for j in range(self.n):
                v = self.nbVoisin(i, j) # calcul du nombre de voisin de la cellule (i,j)
                if (v==2 or v==3) and self.mat[i][j]==1:
                    temp[i][j] = 1 # survie d'une cellule
                if v>=4 and self.mat[i][j]==1:
                    temp[i][j] = 0 # mort d'une cellule par étouffement
                if v<=1 and self.mat[i][j]==1:
                    temp[i][j] = 0 # mort d'une cellule par isolement
                if v==3 and self.mat[i][j]==0:
                    temp[i][j] = 1 # naissance d'une cellule
        vie = 0 # compteur de cellule vivante
        for i in range(self.n):
            for j in range(self.n):
                self.mat[i][j] = temp[i][j] # copie de la cellule (i,j)
                if self.mat[i][j]==1:
                    vie = vie + 1 # incrémentation du compteur si cellule vivante copiée
        self.vie.set(100*vie/self.n**2) # affectation du curseur % de vie
        self.affichage() # affichage damier

    def cycle(self):
        if self.running==True:
            self.evol()  # évolution du damier si jeu de la vie en cours
            self.after(int(100/self.vitesse.get()), self.cycle) # boucle infinie par récurence avec laps de temps en fonction de la vitesse

    # --- Arrêt ---
    def stop(self):
        self.running = False # jeu de la vie arrêté

# --- Execution ---
fenetre =Tk() # fenêtre de l'interface graphique
fenetre.iconbitmap("logo.xbm") # icone de la fenêtre
fenetre.title("SR01 Jeu de la vie") # titre de la fenêtre
interface = Interface(fenetre)
interface.mainloop() # boucle infinie de l'interface
