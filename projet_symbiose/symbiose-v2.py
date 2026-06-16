import pygame
import math
import cv2
import json
import os
import random
import webbrowser

# ============================================================
#   CLASSE CARTE
# ============================================================

class Carte:
    """Représente une carte du jeu avec ses caractéristiques."""
    def __init__(self, animal, couleur, condition, nombre, image_fichier):
        self.animal = str(animal).strip()       # ex: 'e' = escargot
        self.couleur = str(couleur).strip()     # ex: 'r' = rouge
        self.condition = str(condition).strip() # ex: 'None' si points fixes, sinon animal/couleur cible
        self.points = int(nombre)               # valeur de base de la carte
        self.image_fichier = image_fichier      # nom du fichier image associé
        self.face_visible = False               # True si la carte est retournée face visible

# ============================================================
#   DÉFINITION DE TOUTES LES CARTES
# ============================================================

# -- Escargots --
eb_r = Carte('e', 'b', 'r', '2', 'e b + r.jpeg')
er_v = Carte('e', 'r', 'v', '3', 'e r + v.jpeg')
ev_o = Carte('e', 'v', 'o', '4', 'e v + o.jpeg')
er   = Carte('e', 'r', 'None', '6', 'e r.jpeg')
ev_l = Carte('e', 'v', 'l', '2', 'e v + l.jpeg')
er_p = Carte('e', 'r', 'p', '3', 'e r + p.jpeg')
eo_l = Carte('e', 'o', 'l', '2', 'e o + l.jpeg')
ev   = Carte('e', 'v', 'None', '5', 'e v.jpeg')

# -- Grenouilles --
go_r = Carte('g', 'o', 'r', '2', 'g o + r.jpeg')
gr_e = Carte('g', 'r', 'e', '4', 'g r + e.jpeg')
gr_o = Carte('g', 'r', 'o', '4', 'g r + o.jpeg')
gr   = Carte('g', 'r', 'None', '5', 'g r.jpeg')
gv_l = Carte('g', 'v', 'l', '2', 'g v + l.jpeg')
gv_p = Carte('g', 'v', 'p', '3', 'g v + p.jpeg')

# -- Libellules --
lb_e = Carte('l', 'b', 'e', '4', 'l b + e.jpeg')
lb_o = Carte('l', 'b', 'o', '4', 'l b + o.jpeg')
lb   = Carte('l', 'b', 'None', '5', 'l b.jpeg')
lo_p = Carte('l', 'o', 'p', '3', 'l o + p.jpeg')
lo_v = Carte('l', 'o', 'v', '3', 'l o + v.jpeg')
lo   = Carte('l', 'o', 'None', '6', 'l o.jpeg')
lr_p = Carte('l', 'r', 'p', '3', 'l r + p.jpeg')
lr_v = Carte('l', 'r', 'v', '3', 'l r + v.jpeg')
lr   = Carte('l', 'r', 'None', '8', 'l r.jpeg')
lv_b = Carte('l', 'v', 'b', '5', 'l v + b.jpeg')
lv_g = Carte('l', 'v', 'g', '5', 'l v + g.jpeg')
lv   = Carte('l', 'v', 'None', '8', 'l v.jpeg')

# -- Poissons --
pb_l = Carte('p', 'b', 'l', '2', 'p b + l.jpeg')
pb_v = Carte('p', 'b', 'v', '3', 'p b + v.jpeg')
po_e = Carte('p', 'o', 'e', '4', 'p o + e.jpeg')
po_r = Carte('p', 'o', 'r', '2', 'p o + r.jpeg')
po   = Carte('p', 'o', 'None', '5', 'p o.jpeg')
pr_g = Carte('p', 'r', 'g', '5', 'p r + g.jpeg')
pr_b = Carte('p', 'r', 'b', '5', 'p r + b.jpeg')
pr   = Carte('p', 'r', 'None', '8', 'p r.jpeg')
pv_r = Carte('p', 'v', 'r', '2', 'p v + r.jpeg')
pv   = Carte('p', 'v', 'None', '6', 'p v.jpeg')

# Liste complète des 36 cartes du jeu
liste_toutes_les_cartes = [
    eb_r, er_v, ev_o, er, ev_l, er_p, eo_l, ev,
    go_r, gr_e, gr_o, gr, gv_l, gv_p,
    lb_e, lb_o, lb, lo_p, lo_v, lo, lr_p, lr_v, lr, lv_b, lv_g, lv,
    pb_l, pb_v, po_e, po_r, po, pr_g, pr_b, pr, pv_r, pv
]

# ============================================================
#   INITIALISATION PYGAME
# ============================================================

pygame.init()
pygame.mixer.init()
pygame.font.init()

pygame.display.set_caption("Symbiose")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# ============================================================
#   CHARGEMENT DES IMAGES DE CARTES
# ============================================================

taille_carte = (90, 130)

# Image du dos de carte
carte_dos = pygame.image.load('arriere carte.jpeg')
carte_dos = pygame.transform.scale(carte_dos, taille_carte)

# Dictionnaire qui stocke les images chargées pour éviter de les recharger plusieurs fois
images_cartes_chargees = {}

for carte in liste_toutes_les_cartes:
    if carte.image_fichier not in images_cartes_chargees:
        nom_base = os.path.splitext(carte.image_fichier)[0]
        extensions_possibles = ['.jpeg', '.jpg', '.png', '.JPG', '.JPEG', '.PNG']
        image_trouvee = False

        # On essaie d'abord avec le nom exact, puis avec différentes extensions
        if os.path.exists(carte.image_fichier):
            img_temp = pygame.image.load(carte.image_fichier)
            images_cartes_chargees[carte.image_fichier] = pygame.transform.scale(img_temp, taille_carte)
            image_trouvee = True
        else:
            for ext in extensions_possibles:
                chemin_test = nom_base + ext
                if os.path.exists(chemin_test):
                    img_temp = pygame.image.load(chemin_test)
                    images_cartes_chargees[carte.image_fichier] = pygame.transform.scale(img_temp, taille_carte)
                    image_trouvee = True
                    break

        # Si l'image est introuvable, on affiche le dos avec le nom en rouge
        if not image_trouvee:
            surf_err = carte_dos.copy()
            police_err = pygame.font.Font(None, 22)
            txt_err = police_err.render(nom_base, True, (255, 0, 0))
            surf_err.blit(txt_err, (5, 55))
            images_cartes_chargees[carte.image_fichier] = surf_err

# ============================================================
#   POLICES D'ÉCRITURE
# ============================================================

police               = pygame.font.Font(None, 40)
police_grosse        = pygame.font.Font(None, 60)
police_pseudo        = pygame.font.Font(None, 45)
police_etape_actif   = pygame.font.Font(None, 40)
police_etape_inactif = pygame.font.Font(None, 30)

# ============================================================
#   CLASSE COMPTE + SAUVEGARDE JSON
# ============================================================

FICHIER_SAUVEGARDE = "comptes.json"

class Compte:
    #Représente le profil d'un joueur avec son pseudo et ses stats.
    def __init__(self, pseudo, gagner, parties):
        self.pseudo  = pseudo
        self.gagner  = gagner
        self.parties = parties

    def victoire(self):
        #Incrémente le compteur de victoires et sauvegarde.
        self.gagner += 1
        sauvegarder_comptes()

    def partie(self):
        #Incrémente le compteur de parties jouées et sauvegarde.
        self.parties += 1
        sauvegarder_comptes()

    def to_dict(self):
        return {"pseudo": self.pseudo, "gagner": self.gagner, "parties": self.parties}

    @classmethod
    def from_dict(cls, data):
        return cls(data["pseudo"], data.get("gagner", 0), data.get("parties", 0))


def charger_comptes():
    #Charge les comptes depuis le fichier JSON. Retourne une liste vide si le fichier n'existe pas.
    if os.path.exists(FICHIER_SAUVEGARDE):
        with open(FICHIER_SAUVEGARDE, "r", encoding="utf-8") as f:
            donnees = json.load(f)
            return [Compte.from_dict(d) for d in donnees]
    return []


def sauvegarder_comptes():
    #Sauvegarde tous les comptes dans le fichier JSON.
    with open(FICHIER_SAUVEGARDE, "w", encoding="utf-8") as f:
        json.dump([c.to_dict() for c in liste_comptes], f, indent=4)


# Chargement initial des comptes
liste_comptes = charger_comptes()
comptes_assignes = {1: None, 2: None, 3: None, 4: None}

# ============================================================
#   VARIABLES GLOBALES DE L'INTERFACE / NAVIGATION
# ============================================================

input_text             = ""   # Texte saisi dans le champ de création de compte
message_erreur_creation = ""  # Message d'erreur affiché si le pseudo existe déjà
scroll_y               = 0    # Décalage pour le scroll de la liste des comptes
joueur_en_selection    = 0    # Quel joueur est en train de choisir son compte
plein_ecran            = True # État plein écran

# ============================================================
#   CHARGEMENT DES IMAGES DE L'INTERFACE
# ============================================================

background = pygame.image.load('background1.jpg')
bg_jeu     = pygame.image.load('background_jeu.png')
bg_jeu     = pygame.transform.scale(bg_jeu, (1920, 1060))
flou       = pygame.image.load('flou.jpg')

esigelec      = pygame.image.load('Esigelec.png')
esigelec      = pygame.transform.scale(esigelec, (100, 75))
esigelec_rect = esigelec.get_rect()
esigelec_rect.x, esigelec_rect.y = 1780, 900

image_rond = pygame.image.load('rond.png')
image_rond = pygame.transform.scale(image_rond, (100, 100))

bg_charge = pygame.image.load('charge.png')
bg_charge = pygame.transform.scale(bg_charge, (1920, 1060))

# Images des panneaux de compte (emplacements joueurs)
Compte1 = pygame.image.load('Compte1.jpg')
Compte1 = pygame.transform.scale(Compte1, (400, 750))
Compte2 = pygame.image.load('Compte2.jpg')
Compte2 = pygame.transform.scale(Compte2, (400, 750))
Compte3 = pygame.image.load('Compte3.jpg')
Compte3 = pygame.transform.scale(Compte3, (400, 750))
Compte4 = pygame.image.load('Compte4.jpg')
Compte4 = pygame.transform.scale(Compte4, (400, 750))

# Boutons invisibles pour ajouter les joueurs 2/3/4
Compte2_button      = pygame.image.load('vide.png')
Compte2_button      = pygame.transform.scale(Compte2_button, (400, 750))
Compte2_button_rect = Compte2_button.get_rect()
Compte2_button_rect.x, Compte2_button_rect.y = 550, 200

Compte3_button      = pygame.image.load('vide.png')
Compte3_button      = pygame.transform.scale(Compte3_button, (400, 750))
Compte3_button_rect = Compte3_button.get_rect()
Compte3_button_rect.x, Compte3_button_rect.y = 1000, 200

Compte4_button      = pygame.image.load('vide.png')
Compte4_button      = pygame.transform.scale(Compte4_button, (400, 750))
Compte4_button_rect = Compte4_button.get_rect()
Compte4_button_rect.x, Compte4_button_rect.y = 1450, 200

# Bouton croix pour retirer un joueur
bouton_retour_img    = pygame.image.load('croix_quitte.png')
bouton_retour_img    = pygame.transform.scale(bouton_retour_img, (50, 50))

bouton_retour2_rect  = bouton_retour_img.get_rect()
bouton_retour2_rect.x, bouton_retour2_rect.y = 725, 960

bouton_retour3_rect  = bouton_retour_img.get_rect()
bouton_retour3_rect.x, bouton_retour3_rect.y = 1175, 960

bouton_retour4_rect  = bouton_retour_img.get_rect()
bouton_retour4_rect.x, bouton_retour4_rect.y = 1625, 960

# Bouton quitter l'application (coin haut droit)
quit_app_button      = pygame.image.load('croix_quitte.png')
quit_app_button      = pygame.transform.scale(quit_app_button, (75, 75))
quit_app_button_rect = quit_app_button.get_rect()
quit_app_button_rect.x, quit_app_button_rect.y = 1920 - 75 - 50, 65

# Logo du jeu
banner = pygame.image.load('final logo.png')
banner = pygame.transform.scale(banner, (750, 250))

# Bouton Jouer
play_button      = pygame.image.load('bouton_jouer.png')
play_button_rect = play_button.get_rect()
play_button_rect.x, play_button_rect.y = 180, 330

# Bouton Règles
rules_button      = pygame.image.load('bouton_regles.png')
rules_button      = pygame.transform.scale(rules_button, (450, 150))
rules_button_rect = rules_button.get_rect()
rules_button_rect.x, rules_button_rect.y = 180, 740

# Bouton Scores
bouton_scores      = pygame.image.load('bouton_scores.png')
bouton_scores      = pygame.transform.scale(bouton_scores, (450, 150))
bouton_scores_rect = rules_button.get_rect()
bouton_scores_rect.x, bouton_scores_rect.y = 180, 575

# Bouton menu (dans le jeu, ouvre le menu pause)
menu_button      = pygame.image.load('croix_quitte.png')
menu_button      = pygame.transform.scale(menu_button, (75, 75))
menu_button_rect = menu_button.get_rect()
menu_button_rect.x, menu_button_rect.y = 50, 65

# Bouton valider la sélection des joueurs
bouton_valider      = pygame.image.load('bouton_jouer.png')
bouton_valider      = pygame.transform.scale(bouton_valider, (150, 50))
bouton_valider_rect = bouton_valider.get_rect()
bouton_valider_rect.x, bouton_valider_rect.y = 1700, 75

# Bouton créer un nouveau compte
New_c_button      = pygame.image.load('bouton_nouveau_compte.png')
New_c_button      = pygame.transform.scale(New_c_button, (150, 50))
New_c_button_rect = New_c_button.get_rect()
New_c_button_rect.x, New_c_button_rect.y = 1700, 130

# Bouton traits (ouvre le menu pause pendant la partie)
bouton_traits_img  = pygame.image.load('traits.png')
bouton_traits_img  = pygame.transform.scale(bouton_traits_img, (75, 75))
bouton_traits_rect = bouton_traits_img.get_rect()
bouton_traits_rect.x, bouton_traits_rect.y = 50, 65

# Panneau du menu pause (affiché au centre de l'écran)
panneau_menu_img  = pygame.image.load('menu.png')
panneau_menu_img  = pygame.transform.scale(panneau_menu_img, (400, 150))
panneau_menu_rect = panneau_menu_img.get_rect(center=(1920 // 2, 1060 // 2))

# Bouton de validation pour créer un compte
bouton_valider_creation_rect = pygame.Rect(800, 600, 320, 60)

# Boutons type joueur (humain / robot)
int_g_img = pygame.image.load('int_g.png')
int_g_img = pygame.transform.scale(int_g_img, (100, 65))
int_p_img = pygame.image.load('int_d.png')
int_p_img = pygame.transform.scale(int_p_img, (100, 65))

int1_rect = int_g_img.get_rect()
int1_rect.x, int1_rect.y = 250, 880
int2_rect = int_g_img.get_rect()
int2_rect.x, int2_rect.y = 700, 880
int3_rect = int_g_img.get_rect()
int3_rect.x, int3_rect.y = 1150, 880
int4_rect = int_g_img.get_rect()
int4_rect.x, int4_rect.y = 1600, 880

# ============================================================
#   PORTRAITS DES PERSONNAGES
# ============================================================

taille_profil = (240, 360)
pos_p1 = (175, 300)
pos_p2 = (625, 300)
pos_p3 = (1075, 300)
pos_p4 = (1525, 300)

# Zones cliquables pour les portraits et les noms
rect_p1 = pygame.Rect(pos_p1[0], pos_p1[1], taille_profil[0], taille_profil[1])
rect_p2 = pygame.Rect(pos_p2[0], pos_p2[1], taille_profil[0], taille_profil[1])
rect_p3 = pygame.Rect(pos_p3[0], pos_p3[1], taille_profil[0], taille_profil[1])
rect_p4 = pygame.Rect(pos_p4[0], pos_p4[1], taille_profil[0], taille_profil[1])

rect_nom_p1 = pygame.Rect(pos_p1[0], pos_p1[1] + taille_profil[1] + 10, taille_profil[0], 40)
rect_nom_p2 = pygame.Rect(pos_p2[0], pos_p2[1] + taille_profil[1] + 10, taille_profil[0], 40)
rect_nom_p3 = pygame.Rect(pos_p3[0], pos_p3[1] + taille_profil[1] + 10, taille_profil[0], 40)
rect_nom_p4 = pygame.Rect(pos_p4[0], pos_p4[1] + taille_profil[1] + 10, taille_profil[0], 40)

# Chargement des 8 portraits humains et robots
portraits_humains = {}
portraits_robots  = {}
for i in range(1, 9):
    img_h = pygame.image.load('P' + str(i) + '_NR.png')
    portraits_humains[i] = pygame.transform.scale(img_h, taille_profil)
    img_r = pygame.image.load('P' + str(i) + '_R.png')
    portraits_robots[i] = pygame.transform.scale(img_r, taille_profil)

# ============================================================
#   VIDÉO RÈGLES + AUDIO
# ============================================================

cap          = cv2.VideoCapture('Ludochrono - Symbiose.mp4')
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps          = cap.get(cv2.CAP_PROP_FPS)

pygame.mixer.music.load('Ludochrono-Symbiose.mp3')
audio_demarre = False

vid_width, vid_height = 1000, 562
video_rect  = pygame.Rect((1920 - vid_width) // 2, 200, vid_width, vid_height)
bar_rect    = pygame.Rect(video_rect.x, video_rect.y + vid_height + 10, vid_width, 20)
video_playing   = True
last_video_surf = None

# ============================================================
#   VARIABLES D'ÉTAT DU JEU
# ============================================================

# Écran affiché au démarrage
ecran_actuel          = "CHARGEMENT"
duree_chargement      = random.randint(5000, 10000)  # Durée aléatoire de l'écran de chargement
temps_debut_chargement = pygame.time.get_ticks()
angle_chargement      = 0
en_fondu_chargement   = False
alpha_fondu           = 255
temps_debut_fondu     = 0

# Présence des joueurs ("0" = absent, "1" = présent)
joueur1 = "0"
joueur2 = "0"
joueur3 = "0"
joueur4 = "0"

# Type de joueur (0 = humain, 1 = robot)
etat_int1 = 0
etat_int2 = 0
etat_int3 = 0
etat_int4 = 0

# Personnage choisi par chaque joueur (1 à 8)
id_perso1 = 1
id_perso2 = 2
id_perso3 = 3
id_perso4 = 4

# Variables de la partie en cours
deck_actuel                    = []
riviere_actuelle               = []
mares_actuelles                = {}
joueur_courant                 = 1
index_carte_riviere_selectionnee = None
doit_retourner_carte_bonus     = False
temps_reflexion_ia             = 0
jeu_en_pause                   = False

# Résultats de fin de partie
scores_finaux = {}
gagnant_id    = None

clock   = pygame.time.Clock()
running = True

# ============================================================
#   FONCTIONS UTILITAIRES
# ============================================================

def est_robot(j_id):
    #Retourne True si le joueur j_id est un robot.
    if j_id == 1 and etat_int1 == 1: return True
    if j_id == 2 and etat_int2 == 1: return True
    if j_id == 3 and etat_int3 == 1: return True
    if j_id == 4 and etat_int4 == 1: return True
    return False


def joueur_suivant(courant, j2_actif, j3_actif, j4_actif):
    #Retourne l'id du prochain joueur actif dans l'ordre 1->2->3->4->1.
    if courant == 1 and j2_actif == "1": return 2
    if courant in [1, 2] and j3_actif == "1": return 3
    if courant in [1, 2, 3] and j4_actif == "1": return 4
    return 1


def reinitialiser_jeu_et_persos():
    #Remet toutes les variables de jeu à zéro (appelé en revenant au menu).
    global joueur2, joueur3, joueur4, comptes_assignes
    global etat_int1, etat_int2, etat_int3, etat_int4
    global id_perso1, id_perso2, id_perso3, id_perso4
    global deck_actuel, riviere_actuelle, mares_actuelles
    global joueur_courant, index_carte_riviere_selectionnee, doit_retourner_carte_bonus, temps_reflexion_ia
    global scores_finaux, gagnant_id

    joueur2 = "0"
    joueur3 = "0"
    joueur4 = "0"
    comptes_assignes = {1: None, 2: None, 3: None, 4: None}

    etat_int1 = 0
    etat_int2 = 0
    etat_int3 = 0
    etat_int4 = 0

    id_perso1 = 1
    id_perso2 = 2
    id_perso3 = 3
    id_perso4 = 4

    deck_actuel    = []
    riviere_actuelle = []
    mares_actuelles  = {}

    joueur_courant                   = 1
    index_carte_riviere_selectionnee = None
    doit_retourner_carte_bonus       = False
    temps_reflexion_ia               = 0

    scores_finaux = {}
    gagnant_id    = None


def initialiser_partie(joueurs_actifs):
    #Mélange le deck et distribue les cartes :
    #- 4 cartes face visible dans la rivière
    #- 8 cartes face cachée dans la mare de chaque joueur
    deck = liste_toutes_les_cartes.copy()
    random.shuffle(deck)

    # Remplissage de la rivière
    riviere = []
    for _ in range(4):
        c = deck.pop()
        c.face_visible = True
        riviere.append(c)

    # Distribution des mares
    mares_des_joueurs = {}
    for joueur_id in joueurs_actifs:
        mare = []
        for _ in range(8):
            c = deck.pop()
            c.face_visible = False
            mare.append(c)
        mares_des_joueurs[joueur_id] = mare

    return deck, riviere, mares_des_joueurs

# ============================================================
#   CALCUL DES POINTS
# ============================================================

def calculer_points_carte(carte, index_dans_mare, mare, mare_verticale=False):
    if carte.condition == 'None':
        return carte.points

    cible = carte.condition

    # La colonne logique de scoring est toujours index % 4,
    # que la mare soit horizontale ou verticale.
    # (Pour les mares verticales, la "ligne" visuelle = "colonne" logique de scoring)
    colonne = index_dans_mare % 4

    if colonne == 0:
        # Colonne gauche -> moitié gauche de la mare (4 cartes)
        # Indices des 4 cartes de gauche (col 0 + col 1 pour horiz, lignes 0+1 pour vert)
        zone = [0, 1, 4, 5]
    elif colonne == 1 or colonne == 2:
        # Colonnes centrales -> toute la mare (8 cartes)
        zone = list(range(8))
    else:  # colonne == 3
        # Colonne droite -> moitié droite de la mare (4 cartes)
        # Indices des 4 cartes de droite (col 2 + col 3 pour horiz, lignes 2+3 pour vert)
        zone = [2, 3, 6, 7]

    # Comptage des cartes correspondant à la cible dans la zone
    compteur = 0
    for idx in zone:
        c = mare[idx]
        if c.animal == cible or c.couleur == cible:
            compteur += 1

    return compteur * carte.points


def verifier_fin_partie_symbiose():
    # Vérifie si toutes les cartes de tous les joueurs sont visibles.
    #Si oui, calcule les scores et passe à l'écran de résultats.
    global ecran_actuel, scores_finaux, gagnant_id, riviere_actuelle

    joueurs_actifs = [1]
    if joueur2 == "1": joueurs_actifs.append(2)
    if joueur3 == "1": joueurs_actifs.append(3)
    if joueur4 == "1": joueurs_actifs.append(4)

    # On vérifie qu'il ne reste plus aucune carte cachée
    toutes_visibles = True
    for j in joueurs_actifs:
        if j in mares_actuelles:
            for carte in mares_actuelles[j]:
                if not carte.face_visible:
                    toutes_visibles = False
                    break

    if toutes_visibles:
        # On retourne aussi toutes les cartes de la rivière
        for carte_riviere in riviere_actuelle:
            carte_riviere.face_visible = True

        scores_finaux.clear()
        meilleur_score = -1
        gagnant_id     = None

        for j in joueurs_actifs:
            score_joueur = 0
            if j in mares_actuelles:
                mare = mares_actuelles[j]
                # J2 et J4 ont leurs mares affichées verticalement (2 colonnes de 4)
                mare_verticale = (j == 2 or j == 4)

                for i, carte in enumerate(mare):
                    points_carte = calculer_points_carte(carte, i, mare, mare_verticale)
                    score_joueur += points_carte


            scores_finaux[j] = score_joueur

            if score_joueur > meilleur_score:
                meilleur_score = score_joueur
                gagnant_id     = j

        # Mise à jour des stats des comptes
        for j in joueurs_actifs:
            compte = comptes_assignes[j]
            if compte is not None:
                compte.partie()
                if j == gagnant_id:
                    compte.victoire()

        ecran_actuel = "CALCUL_SCORES"

# ============================================================
#   BOUCLE PRINCIPALE DU JEU
# ============================================================

while running:
    clock.tick(fps)

    # -- Tour ROBOT (fait par Gemini) --
    if ecran_actuel in ["JEU_3_JOUEURS", "JEU_4_JOUEURS"] and not jeu_en_pause:
        if est_robot(joueur_courant):
            temps_actuel = pygame.time.get_ticks()

            if temps_reflexion_ia == 0:
                temps_reflexion_ia = temps_actuel + 1500
            elif temps_actuel >= temps_reflexion_ia:
                mare = mares_actuelles[joueur_courant]

                if not doit_retourner_carte_bonus:
                    idx_meilleure_riv = max(range(len(riviere_actuelle)), key=lambda i: riviere_actuelle[i].points)

                    visibles = [i for i, c in enumerate(mare) if c.face_visible]
                    cachees  = [i for i, c in enumerate(mare) if not c.face_visible]

                    idx_choix_mare = None
                    if visibles:
                        idx_pire_vis = min(visibles, key=lambda i: mare[i].points)
                        if mare[idx_pire_vis].points < riviere_actuelle[idx_meilleure_riv].points:
                            idx_choix_mare = idx_pire_vis
                        else:
                            idx_choix_mare = random.choice(cachees) if cachees else idx_pire_vis
                    else:
                        idx_choix_mare = random.choice(cachees)

                    c_riv = riviere_actuelle[idx_meilleure_riv]
                    c_mar = mare[idx_choix_mare]
                    etait_vis = c_mar.face_visible

                    riviere_actuelle[idx_meilleure_riv] = c_mar
                    mare[idx_choix_mare] = c_riv

                    riviere_actuelle[idx_meilleure_riv].face_visible = True
                    mare[idx_choix_mare].face_visible = True

                    if etait_vis:
                        reste_cachee = any(not c.face_visible for c in mare)
                        if reste_cachee:
                            doit_retourner_carte_bonus = True
                        else:
                            joueur_courant = joueur_suivant(joueur_courant, joueur2, joueur3, joueur4)
                            verifier_fin_partie_symbiose()
                    else:
                        joueur_courant = joueur_suivant(joueur_courant, joueur2, joueur3, joueur4)
                        verifier_fin_partie_symbiose()
                else:
                    cachees = [i for i, c in enumerate(mare) if not c.face_visible]
                    if cachees:
                        idx = random.choice(cachees)
                        mare[idx].face_visible = True

                    doit_retourner_carte_bonus = False
                    joueur_courant = joueur_suivant(joueur_courant, joueur2, joueur3, joueur4)
                    verifier_fin_partie_symbiose()

                temps_reflexion_ia = 0

    # --------------------------------------------------------
    #   GESTION DES ÉVÉNEMENTS
    # --------------------------------------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()

        # Touche F11 : basculer plein écran / fenêtré
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                plein_ecran = not plein_ecran
                if plein_ecran:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((1920, 1060), pygame.RESIZABLE)

            elif ecran_actuel == "CREATION":
                # Saisie du pseudo dans le champ de création de compte
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    input_text += event.unicode

        # Molette de la souris : scroll dans la liste des comptes
        if event.type == pygame.MOUSEWHEEL:
            if ecran_actuel == "SELECTION_COMPTE":
                scroll_y += event.y * 20
                if scroll_y > 0:
                    scroll_y = 0
                nb_comptes_dispos = sum(1 for c in liste_comptes if not any(
                    comptes_assignes[j] == c for j in range(1, 5) if j != joueur_en_selection))
                hauteur_totale_liste = nb_comptes_dispos * 50
                max_scroll = min(0, taille_profil[1] - hauteur_totale_liste)
                if scroll_y < max_scroll:
                    scroll_y = max_scroll

        # Clics de souris
        if event.type == pygame.MOUSEBUTTONDOWN:

            # -- ÉCRAN CHARGEMENT --
            if ecran_actuel == "CHARGEMENT":
                pass

            # -- MENU PRINCIPAL --
            elif ecran_actuel == "MENU":
                if play_button_rect.collidepoint(event.pos):
                    ecran_actuel = "PERSO"
                elif rules_button_rect.collidepoint(event.pos):
                    ecran_actuel = "REGLES"
                elif bouton_scores_rect.collidepoint(event.pos):
                    ecran_actuel = "SCORES"
                elif quit_app_button_rect.collidepoint(event.pos):
                    running = False
                    pygame.quit()
                    exit()
                elif esigelec_rect.collidepoint(event.pos):
                    webbrowser.open("https://www.esigelec.fr")

            # -- ÉCRAN DE JEU (3 ou 4 joueurs) --
            elif ecran_actuel in ["JEU_3_JOUEURS", "JEU_4_JOUEURS"]:

                if jeu_en_pause:
                    # Clic sur le bouton traits : fermer le menu pause
                    if bouton_traits_rect.collidepoint(event.pos):
                        jeu_en_pause = False
                    # Clic sur le panneau menu : retour au menu principal
                    elif panneau_menu_rect.collidepoint(event.pos):
                        jeu_en_pause = False
                        ecran_actuel = "MENU"
                        reinitialiser_jeu_et_persos()

                elif not est_robot(joueur_courant):
                    # Ouvrir le menu pause
                    if bouton_traits_rect.collidepoint(event.pos):
                        jeu_en_pause = True
                    else:
                        mouseX, mouseY = event.pos
                        w_c, h_c = 90, 130
                        gap = 15

                        taille_riviere = len(riviere_actuelle)
                        riviere_x = 1920 // 2 - (taille_riviere * w_c + (taille_riviere - 1) * gap) // 2
                        riviere_y = 1060 // 2 - h_c // 2

                        joueurs_actifs = [1]
                        if joueur2 == "1": joueurs_actifs.append(2)
                        if joueur3 == "1": joueurs_actifs.append(3)
                        if joueur4 == "1": joueurs_actifs.append(4)

                        # Clic sur une carte de la rivière (sélection pour l'échange)
                        if not doit_retourner_carte_bonus:
                            for i in range(taille_riviere):
                                x_carte = riviere_x + i * (w_c + gap)
                                rect_carte = pygame.Rect(x_carte, riviere_y, w_c, h_c)
                                if rect_carte.collidepoint(mouseX, mouseY):
                                    if index_carte_riviere_selectionnee == i:
                                        index_carte_riviere_selectionnee = None
                                    else:
                                        index_carte_riviere_selectionnee = i
                                    break

                        # Clic sur une carte de la mare du joueur courant
                        if joueur_courant in joueurs_actifs and joueur_courant in mares_actuelles:
                            if joueur_courant == 1:
                                p_x = 1920 // 2 - (4 * w_c + 3 * gap) // 2
                                p_y = 1060 - (2 * h_c + gap) - 30
                                est_vertical = False
                            elif joueur_courant == 2:
                                p_x = 40
                                p_y = 1060 // 2 - (4 * h_c + 3 * gap) // 2
                                est_vertical = True
                            elif joueur_courant == 3:
                                p_x = 1920 // 2 - (4 * w_c + 3 * gap) // 2
                                p_y = 30
                                est_vertical = False
                            elif joueur_courant == 4:
                                p_x = 1920 - (2 * w_c + gap) - 40
                                p_y = 1060 // 2 - (4 * h_c + 3 * gap) // 2
                                est_vertical = True

                            for i in range(8):
                                if est_vertical:
                                    col, row = i // 4, i % 4
                                else:
                                    row, col = i // 4, i % 4

                                x_carte = p_x + col * (w_c + gap)
                                y_carte = p_y + row * (h_c + gap)
                                rect_carte = pygame.Rect(x_carte, y_carte, w_c, h_c)

                                if rect_carte.collidepoint(mouseX, mouseY):

                                    # Phase 2 du tour : retourner une carte cachée (bonus)
                                    if doit_retourner_carte_bonus:
                                        if not mares_actuelles[joueur_courant][i].face_visible:
                                            mares_actuelles[joueur_courant][i].face_visible = True
                                            doit_retourner_carte_bonus = False
                                            index_carte_riviere_selectionnee = None
                                            joueur_courant = joueur_suivant(joueur_courant, joueur2, joueur3, joueur4)
                                            verifier_fin_partie_symbiose()

                                    # Phase 1 du tour : échange avec la rivière
                                    else:
                                        if index_carte_riviere_selectionnee is not None:
                                            carte_riviere = riviere_actuelle[index_carte_riviere_selectionnee]
                                            carte_mare    = mares_actuelles[joueur_courant][i]
                                            etait_visible = carte_mare.face_visible

                                            # Échange des cartes
                                            riviere_actuelle[index_carte_riviere_selectionnee] = carte_mare
                                            mares_actuelles[joueur_courant][i] = carte_riviere

                                            # Les deux cartes sont maintenant visibles
                                            riviere_actuelle[index_carte_riviere_selectionnee].face_visible = True
                                            mares_actuelles[joueur_courant][i].face_visible = True

                                            index_carte_riviere_selectionnee = None

                                            # Si la carte échangée était déjà visible, le joueur peut retourner un bonus
                                            if etait_visible:
                                                reste_cachee = any(not c.face_visible for c in mares_actuelles[joueur_courant])
                                                if reste_cachee:
                                                    doit_retourner_carte_bonus = True
                                                else:
                                                    joueur_courant = joueur_suivant(joueur_courant, joueur2, joueur3, joueur4)
                                                    verifier_fin_partie_symbiose()
                                            else:
                                                joueur_courant = joueur_suivant(joueur_courant, joueur2, joueur3, joueur4)
                                                verifier_fin_partie_symbiose()
                                    break

            # -- ÉCRAN SÉLECTION DES JOUEURS --
            elif ecran_actuel == "PERSO":
                if menu_button_rect.collidepoint(event.pos):
                    ecran_actuel = "MENU"
                elif New_c_button_rect.collidepoint(event.pos):
                    ecran_actuel = "CREATION"
                    input_text = ""
                    message_erreur_creation = ""

                # Ajouter / retirer les joueurs 2, 3, 4
                elif Compte2_button_rect.collidepoint(event.pos) and joueur2 == "0":
                    joueur2 = "1"
                elif Compte3_button_rect.collidepoint(event.pos) and joueur3 == "0":
                    joueur3 = "1"
                elif Compte4_button_rect.collidepoint(event.pos) and joueur4 == "0":
                    joueur4 = "1"
                elif bouton_retour2_rect.collidepoint(event.pos) and joueur2 == "1":
                    joueur2 = "0"
                    comptes_assignes[2] = None
                elif bouton_retour3_rect.collidepoint(event.pos) and joueur3 == "1":
                    joueur3 = "0"
                    comptes_assignes[3] = None
                elif bouton_retour4_rect.collidepoint(event.pos) and joueur4 == "1":
                    joueur4 = "0"
                    comptes_assignes[4] = None

                # Basculer humain/robot pour chaque joueur
                elif int1_rect.collidepoint(event.pos):
                    etat_int1 = 1 - etat_int1
                    comptes_assignes[1] = None
                elif int2_rect.collidepoint(event.pos) and joueur2 == "1":
                    etat_int2 = 1 - etat_int2
                    comptes_assignes[2] = None
                elif int3_rect.collidepoint(event.pos) and joueur3 == "1":
                    etat_int3 = 1 - etat_int3
                    comptes_assignes[3] = None
                elif int4_rect.collidepoint(event.pos) and joueur4 == "1":
                    etat_int4 = 1 - etat_int4
                    comptes_assignes[4] = None

                # Changer le personnage en cliquant sur les "avatars"
                elif rect_p1.collidepoint(event.pos):
                    id_perso1 = (id_perso1 % 8) + 1
                    while id_perso1 in [id_perso2 if joueur2 == "1" else 0,
                                        id_perso3 if joueur3 == "1" else 0,
                                        id_perso4 if joueur4 == "1" else 0]:
                        id_perso1 = (id_perso1 % 8) + 1
                elif rect_p2.collidepoint(event.pos) and joueur2 == "1":
                    id_perso2 = (id_perso2 % 8) + 1
                    while id_perso2 in [id_perso1,
                                        id_perso3 if joueur3 == "1" else 0,
                                        id_perso4 if joueur4 == "1" else 0]:
                        id_perso2 = (id_perso2 % 8) + 1
                elif rect_p3.collidepoint(event.pos) and joueur3 == "1":
                    id_perso3 = (id_perso3 % 8) + 1
                    while id_perso3 in [id_perso1,
                                        id_perso2 if joueur2 == "1" else 0,
                                        id_perso4 if joueur4 == "1" else 0]:
                        id_perso3 = (id_perso3 % 8) + 1
                elif rect_p4.collidepoint(event.pos) and joueur4 == "1":
                    id_perso4 = (id_perso4 % 8) + 1
                    while id_perso4 in [id_perso1,
                                        id_perso2 if joueur2 == "1" else 0,
                                        id_perso3 if joueur3 == "1" else 0]:
                        id_perso4 = (id_perso4 % 8) + 1

                # Clic sur la zone nom -> sélection du compte
                elif rect_nom_p1.collidepoint(event.pos) and etat_int1 == 0:
                    ecran_actuel = "SELECTION_COMPTE"
                    joueur_en_selection = 1
                    scroll_y = 0
                elif rect_nom_p2.collidepoint(event.pos) and joueur2 == "1" and etat_int2 == 0:
                    ecran_actuel = "SELECTION_COMPTE"
                    joueur_en_selection = 2
                    scroll_y = 0
                elif rect_nom_p3.collidepoint(event.pos) and joueur3 == "1" and etat_int3 == 0:
                    ecran_actuel = "SELECTION_COMPTE"
                    joueur_en_selection = 3
                    scroll_y = 0
                elif rect_nom_p4.collidepoint(event.pos) and joueur4 == "1" and etat_int4 == 0:
                    ecran_actuel = "SELECTION_COMPTE"
                    joueur_en_selection = 4
                    scroll_y = 0

                # Bouton valider : lancer la partie si assez de joueurs
                elif bouton_valider_rect.collidepoint(event.pos):
                    joueurs_actifs = [1]
                    if joueur2 == "1": joueurs_actifs.append(2)
                    if joueur3 == "1": joueurs_actifs.append(3)
                    if joueur4 == "1": joueurs_actifs.append(4)

                    nombre_de_joueurs = len(joueurs_actifs)

                    if nombre_de_joueurs >= 3:
                        deck_actuel, riviere_actuelle, mares_actuelles = initialiser_partie(joueurs_actifs)
                        index_carte_riviere_selectionnee = None
                        doit_retourner_carte_bonus = False
                        joueur_courant = 1
                        temps_reflexion_ia = 0

                        if nombre_de_joueurs == 3:
                            ecran_actuel = "JEU_3_JOUEURS"
                        elif nombre_de_joueurs == 4:
                            ecran_actuel = "JEU_4_JOUEURS"

            # -- CRÉATION DE COMPTE --
            elif ecran_actuel == "CREATION":
                if bouton_valider_creation_rect.collidepoint(event.pos) and len(input_text) > 0:
                    # Vérification que le pseudo n'existe pas déjà
                    nom_existe_deja = any(c.pseudo.lower() == input_text.lower() for c in liste_comptes)

                    if not nom_existe_deja:
                        liste_comptes.append(Compte(input_text, 0, 0))
                        sauvegarder_comptes()
                        message_erreur_creation = ""
                        ecran_actuel = "PERSO"
                    else:
                        message_erreur_creation = "Ce compte existe deja !"
                        input_text = ""

                if menu_button_rect.collidepoint(event.pos):
                    message_erreur_creation = ""
                    ecran_actuel = "PERSO"

            # -- SÉLECTION DE COMPTE --
            elif ecran_actuel == "SELECTION_COMPTE":
                pos_x_liste = [pos_p1[0], pos_p2[0], pos_p3[0], pos_p4[0]][joueur_en_selection - 1]
                pos_y_liste = 300

                # Croix pour fermer la liste
                croix_rect = pygame.Rect(pos_x_liste + taille_profil[0] - 30, pos_y_liste - 40, 30, 30)
                if croix_rect.collidepoint(event.pos):
                    ecran_actuel = "PERSO"
                else:
                    affichage_index = 0
                    compte_a_supprimer = None

                    for compte in liste_comptes:
                        # On n'affiche pas les comptes déjà assignés à un autre joueur
                        compte_indisponible = False
                        for j_id in range(1, 5):
                            if j_id != joueur_en_selection and comptes_assignes[j_id] == compte:
                                compte_indisponible = True
                                break

                        if not compte_indisponible:
                            item_rect = pygame.Rect(
                                pos_x_liste,
                                pos_y_liste + affichage_index * 50 + scroll_y,
                                taille_profil[0], 40
                            )

                            if item_rect.collidepoint(event.pos) and pos_y_liste <= item_rect.y <= pos_y_liste + taille_profil[1]:
                                if event.pos[0] >= item_rect.right - 50:
                                    # Clic sur la croix rouge -> suppression du compte
                                    compte_a_supprimer = compte
                                else:
                                    # Clic sur le nom -> sélection du compte
                                    comptes_assignes[joueur_en_selection] = compte
                                    ecran_actuel = "PERSO"
                                break
                            affichage_index += 1

                    # Suppression effective du compte
                    if compte_a_supprimer:
                        liste_comptes.remove(compte_a_supprimer)
                        for j_id in range(1, 5):
                            if comptes_assignes[j_id] == compte_a_supprimer:
                                comptes_assignes[j_id] = None
                        sauvegarder_comptes()

            # -- TABLEAU DES SCORES --
            elif ecran_actuel == "SCORES":
                if menu_button_rect.collidepoint(event.pos):
                    ecran_actuel = "MENU"

            # -- RÉSULTATS DE PARTIE --
            elif ecran_actuel == "CALCUL_SCORES":
                if menu_button_rect.collidepoint(event.pos):
                    ecran_actuel = "SCORES"
                    reinitialiser_jeu_et_persos()

            # -- ÉCRAN RÈGLES (vidéo) --
            elif ecran_actuel == "REGLES":
                if menu_button_rect.collidepoint(event.pos):
                    ecran_actuel = "MENU"
                    pygame.mixer.music.stop()
                    video_playing = False
                elif video_rect.collidepoint(event.pos):
                    # Clic sur la vidéo : pause / reprise
                    video_playing = not video_playing
                    if video_playing:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                elif bar_rect.collidepoint(event.pos):
                    # Clic sur la barre de progression : seek
                    click_x = event.pos[0] - bar_rect.x
                    pourcentage = click_x / bar_rect.width
                    nouvelle_frame = int(total_frames * pourcentage)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, nouvelle_frame)
                    temps_en_secondes = nouvelle_frame / fps
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_pos(temps_en_secondes)
                    if not video_playing:
                        pygame.mixer.music.pause()
                    ret, frame = cap.read()
                    if ret:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame = cv2.resize(frame, (vid_width, vid_height))
                        last_video_surf = pygame.image.frombuffer(frame.tobytes(), (vid_width, vid_height), "RGB")

    # ============================================================
    #   AFFICHAGE DE CHAQUE ÉCRAN
    # ------------------------------------------------------------

    # -- CHARGEMENT --
    if ecran_actuel == "CHARGEMENT":
        temps_actuel = pygame.time.get_ticks()
        temps_ecoule = temps_actuel - temps_debut_chargement

        if not en_fondu_chargement and temps_ecoule >= duree_chargement:
            en_fondu_chargement = True
            temps_debut_fondu   = temps_actuel

        if en_fondu_chargement:
            progression = (temps_actuel - temps_debut_fondu) / 1000.0
            alpha_fondu = max(0, int(255 * (1.0 - progression)))
            if alpha_fondu <= 0:
                ecran_actuel        = "MENU"
                en_fondu_chargement = False

        screen.blit(background, (0, 0))
        screen.blit(banner, (550, 65))
        screen.blit(esigelec, (1780, 900))
        screen.blit(play_button, play_button_rect)
        screen.blit(rules_button, rules_button_rect)
        screen.blit(bouton_scores, bouton_scores_rect)
        screen.blit(quit_app_button, quit_app_button_rect)

        # Superposition de l'écran de chargement qui disparaît progressivement
        if alpha_fondu > 0:
            splash_surf = pygame.Surface((1920, 1060))
            splash_surf.blit(bg_charge, (0, 0))
            angle_chargement -= 4
            img_tournee   = pygame.transform.rotate(image_rond, angle_chargement)
            rect_tourne   = img_tournee.get_rect(center=(1800, 950))
            splash_surf.blit(img_tournee, rect_tourne)
            splash_surf.set_alpha(alpha_fondu)
            screen.blit(splash_surf, (0, 0))

    # -- MENU PRINCIPAL --
    elif ecran_actuel == "MENU":
        screen.blit(background, (0, 0))
        screen.blit(banner, (550, 65))
        screen.blit(esigelec, esigelec_rect)
        screen.blit(play_button, play_button_rect)
        screen.blit(rules_button, rules_button_rect)
        screen.blit(bouton_scores, bouton_scores_rect)
        screen.blit(quit_app_button, quit_app_button_rect)

    # -- SÉLECTION DES JOUEURS --
    elif ecran_actuel == "PERSO":
        screen.blit(flou, (0, 0))
        screen.blit(menu_button, menu_button_rect)
        screen.blit(New_c_button, New_c_button_rect)

        # Panneaux des 4 emplacements joueurs
        screen.blit(Compte1, (100, 200))
        screen.blit(Compte2, (550, 200))
        screen.blit(Compte3, (1000, 200))
        screen.blit(Compte4, (1450, 200))

        # Portraits des joueurs
        screen.blit(portraits_humains[id_perso1] if etat_int1 == 0 else portraits_robots[id_perso1], pos_p1)
        if joueur2 == "1":
            screen.blit(portraits_humains[id_perso2] if etat_int2 == 0 else portraits_robots[id_perso2], pos_p2)
        if joueur3 == "1":
            screen.blit(portraits_humains[id_perso3] if etat_int3 == 0 else portraits_robots[id_perso3], pos_p3)
        if joueur4 == "1":
            screen.blit(portraits_humains[id_perso4] if etat_int4 == 0 else portraits_robots[id_perso4], pos_p4)

        def dessiner_nom(rect, joueur_id, est_robot_val):
            #Affiche le pseudo (ou ROBOT / Sélectionner) sous l'avatar
            pygame.draw.rect(screen, (50, 50, 50), rect)
            if est_robot_val == 1:
                texte = "ROBOT"
            elif comptes_assignes[joueur_id]:
                texte = comptes_assignes[joueur_id].pseudo
            else:
                texte = "Selectionner"
            surface_txt = police.render(texte, True, (255, 255, 255))
            screen.blit(surface_txt, (rect.x + 10, rect.y + 5))

        dessiner_nom(rect_nom_p1, 1, etat_int1)
        if joueur2 == "1": dessiner_nom(rect_nom_p2, 2, etat_int2)
        if joueur3 == "1": dessiner_nom(rect_nom_p3, 3, etat_int3)
        if joueur4 == "1": dessiner_nom(rect_nom_p4, 4, etat_int4)

        # Boutons humain / robot
        screen.blit(int_g_img if etat_int1 == 0 else int_p_img, int1_rect)
        if joueur2 == "1": screen.blit(int_g_img if etat_int2 == 0 else int_p_img, int2_rect)
        if joueur3 == "1": screen.blit(int_g_img if etat_int3 == 0 else int_p_img, int3_rect)
        if joueur4 == "1": screen.blit(int_g_img if etat_int4 == 0 else int_p_img, int4_rect)

        screen.blit(bouton_valider, bouton_valider_rect)

        # Boutons ajouter / retirer joueurs
        if joueur2 == "0":
            screen.blit(Compte2_button, Compte2_button_rect)
        else:
            screen.blit(bouton_retour_img, bouton_retour2_rect)
        if joueur3 == "0":
            screen.blit(Compte3_button, Compte3_button_rect)
        else:
            screen.blit(bouton_retour_img, bouton_retour3_rect)
        if joueur4 == "0":
            screen.blit(Compte4_button, Compte4_button_rect)
        else:
            screen.blit(bouton_retour_img, bouton_retour4_rect)

    # -- CRÉATION DE COMPTE --
    elif ecran_actuel == "CREATION":
        screen.blit(flou, (0, 0))
        screen.blit(menu_button, menu_button_rect)

        txt_surface = police.render(input_text, True, (255, 255, 255))
        input_box   = pygame.Rect(800, 400, max(320, txt_surface.get_width() + 10), 50)
        pygame.draw.rect(screen, (30, 30, 30), input_box)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 10))

        pygame.draw.rect(screen, (0, 150, 0), bouton_valider_creation_rect)
        valider_txt = police.render("Creer le compte", True, (255, 255, 255))
        screen.blit(valider_txt, (bouton_valider_creation_rect.x + 40, bouton_valider_creation_rect.y + 15))

        if message_erreur_creation:
            err_surf = police.render(message_erreur_creation, True, (255, 50, 50))
            screen.blit(err_surf, (800, 350))

    # -- SÉLECTION DE COMPTE --
    elif ecran_actuel == "SELECTION_COMPTE":
        screen.blit(flou, (0, 0))
        mx, my = pygame.mouse.get_pos()

        pos_x_liste = [pos_p1[0], pos_p2[0], pos_p3[0], pos_p4[0]][joueur_en_selection - 1]
        pos_y_liste = 300

        zone_liste_rect = pygame.Rect(pos_x_liste, pos_y_liste, taille_profil[0], taille_profil[1])
        pygame.draw.rect(screen, (20, 20, 20), zone_liste_rect)
        pygame.draw.rect(screen, (255, 255, 255), zone_liste_rect, 2)

        # Bouton X pour fermer
        pygame.draw.rect(screen, (200, 0, 0), (pos_x_liste + taille_profil[0] - 30, pos_y_liste - 40, 30, 30))
        croix_txt = police.render("X", True, (255, 255, 255))
        screen.blit(croix_txt, (pos_x_liste + taille_profil[0] - 25, pos_y_liste - 40))

        screen.set_clip(zone_liste_rect)
        affichage_index = 0
        for compte in liste_comptes:
            compte_indisponible = False
            for j_id in range(1, 5):
                if j_id != joueur_en_selection and comptes_assignes[j_id] == compte:
                    compte_indisponible = True
                    break

            if not compte_indisponible:
                item_rect = pygame.Rect(
                    pos_x_liste,
                    pos_y_liste + affichage_index * 50 + scroll_y,
                    taille_profil[0], 40
                )
                pygame.draw.rect(screen, (70, 70, 70), item_rect)
                nom_txt = police.render(compte.pseudo, True, (255, 255, 255))
                screen.blit(nom_txt, (item_rect.x + 10, item_rect.y + 5))
                pygame.draw.rect(screen, (100, 100, 100), item_rect, 1)

                # Bouton supprimer (croix rouge) au survol
                if item_rect.collidepoint(mx, my):
                    croix_suppr_rect = pygame.Rect(item_rect.right - 40, item_rect.y, 40, 40)
                    pygame.draw.rect(screen, (200, 0, 0), croix_suppr_rect)
                    txt_x = police.render("X", True, (255, 255, 255))
                    screen.blit(txt_x, (croix_suppr_rect.x + 10, croix_suppr_rect.y + 5))
                    pygame.draw.rect(screen, (255, 255, 255), croix_suppr_rect, 1)

                affichage_index += 1
        screen.set_clip(None)

    # -- ÉCRAN RÈGLES (vidéo) --
    elif ecran_actuel == "REGLES":
        screen.blit(flou, (0, 0))
        screen.blit(menu_button, menu_button_rect)

        if video_playing:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (vid_width, vid_height))
                last_video_surf = pygame.image.frombuffer(frame.tobytes(), (vid_width, vid_height), "RGB")

        if last_video_surf:
            screen.blit(last_video_surf, video_rect.topleft)

        pygame.draw.rect(screen, (100, 100, 100), bar_rect)
        if total_frames > 0:
            frame_actuelle      = cap.get(cv2.CAP_PROP_POS_FRAMES)
            progression_largeur = int((frame_actuelle / total_frames) * bar_rect.width)
            progression_rect    = pygame.Rect(bar_rect.x, bar_rect.y, progression_largeur, bar_rect.height)
            pygame.draw.rect(screen, (150, 255, 0), progression_rect)

    # -- TABLEAU DES SCORES --
    elif ecran_actuel == "SCORES":
        screen.blit(flou, (0, 0))
        screen.blit(menu_button, menu_button_rect)

        titre = police.render("TABLEAU DES SCORES", True, (255, 215, 0))
        screen.blit(titre, (800, 50))

        comptes_tries = sorted(liste_comptes, key=lambda c: (-c.gagner, c.parties))

        y_offset = 150
        entetes  = police.render("Pseudo               | Victoires   | Parties", True, (200, 200, 200))
        screen.blit(entetes, (600, y_offset))
        pygame.draw.line(screen, (255, 255, 255), (600, y_offset + 40), (1300, y_offset + 40), 2)
        y_offset += 60

        for i, c in enumerate(comptes_tries[:10]):
            texte = str(i + 1) + ". " + c.pseudo[:15].ljust(17) + " | " + str(c.gagner).ljust(11) + " | " + str(c.parties)
            surf  = police.render(texte, True, (255, 255, 255))
            screen.blit(surf, (600, y_offset))
            y_offset += 45

    # -- RÉSULTATS DE PARTIE --
    elif ecran_actuel == "CALCUL_SCORES":
        screen.blit(bg_jeu, (0, 0))
        overlay = pygame.Surface((1920, 1060), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        screen.blit(menu_button, menu_button_rect)

        titre = police.render("RESULTATS DE LA PARTIE", True, (255, 215, 0))
        screen.blit(titre, (1920 // 2 - titre.get_width() // 2, 150))

        y_offset = 350
        for j, score in scores_finaux.items():
            if j == 1:
                nom = "ROBOT" if etat_int1 == 1 else (comptes_assignes[1].pseudo if comptes_assignes[1] else "Inconnu")
            elif j == 2:
                nom = "ROBOT" if etat_int2 == 1 else (comptes_assignes[2].pseudo if comptes_assignes[2] else "Inconnu")
            elif j == 3:
                nom = "ROBOT" if etat_int3 == 1 else (comptes_assignes[3].pseudo if comptes_assignes[3] else "Inconnu")
            elif j == 4:
                nom = "ROBOT" if etat_int4 == 1 else (comptes_assignes[4].pseudo if comptes_assignes[4] else "Inconnu")

            texte = "Joueur " + str(j) + " (" + nom + ") : " + str(score) + " points"

            if j == gagnant_id:
                texte  += "  <-- GAGNANT !"
                couleur = (0, 255, 0)
            else:
                couleur = (255, 255, 255)

            surf = police.render(texte, True, couleur)
            screen.blit(surf, (1920 // 2 - surf.get_width() // 2, y_offset))
            y_offset += 80

    # -- JEU (3 ou 4 joueurs) --
    elif ecran_actuel in ["JEU_3_JOUEURS", "JEU_4_JOUEURS"]:
        screen.blit(bg_jeu, (0, 0))

        w_c, h_c  = 90, 130
        gap       = 15
        taille_av = (90, 130)

        # Affichage de la rivière (cartes centrales)
        if riviere_actuelle:
            taille_riviere = len(riviere_actuelle)
            riviere_x = 1920 // 2 - (taille_riviere * w_c + (taille_riviere - 1) * gap) // 2
            riviere_y = 1060 // 2 - h_c // 2

            for index, carte_riviere in enumerate(riviere_actuelle):
                x_carte = riviere_x + index * (w_c + gap)
                carte_riviere.face_visible = True
                screen.blit(images_cartes_chargees[carte_riviere.image_fichier], (x_carte, riviere_y))

                # Surligné en rouge si la carte est sélectionnée
                if index_carte_riviere_selectionnee == index:
                    pygame.draw.rect(screen, (255, 0, 0), (x_carte, riviere_y, w_c, h_c), 3)

        # -- Joueur 1 (en bas) --
        p1_x = 1920 // 2 - (4 * w_c + 3 * gap) // 2
        p1_y = 1060 - (2 * h_c + gap) - 30

        av1   = pygame.transform.scale(portraits_humains[id_perso1] if etat_int1 == 0 else portraits_robots[id_perso1], taille_av)
        av1_x = p1_x - w_c - 40
        av1_y = p1_y + (2 * h_c + gap) // 2 - h_c // 2
        screen.blit(av1, (av1_x, av1_y))

        nom1 = "ROBOT" if etat_int1 == 1 else (comptes_assignes[1].pseudo if comptes_assignes[1] else "Inconnu")
        txt1 = police.render(nom1, True, (255, 255, 255))
        screen.blit(txt1, (av1_x - txt1.get_width() - 15, av1_y + h_c // 2 - 20))

        if 1 in mares_actuelles:
            for index, carte in enumerate(mares_actuelles[1]):
                row    = index // 4
                col    = index % 4
                x_carte = p1_x + col * (w_c + gap)
                y_carte = p1_y + row * (h_c + gap)
                if carte.face_visible:
                    screen.blit(images_cartes_chargees[carte.image_fichier], (x_carte, y_carte))
                else:
                    screen.blit(carte_dos, (x_carte, y_carte))

        # -- Joueur 2 (à gauche) --
        if joueur2 == "1" and 2 in mares_actuelles:
            p2_x = 40
            p2_y = 1060 // 2 - (4 * h_c + 3 * gap) // 2

            av2   = pygame.transform.scale(portraits_humains[id_perso2] if etat_int2 == 0 else portraits_robots[id_perso2], taille_av)
            av2_x = p2_x + (2 * w_c + gap) // 2 - w_c // 2
            av2_y = p2_y - h_c - 20
            screen.blit(av2, (av2_x, av2_y))

            nom2 = "ROBOT" if etat_int2 == 1 else (comptes_assignes[2].pseudo if comptes_assignes[2] else "Inconnu")
            txt2 = police.render(nom2, True, (255, 255, 255))
            screen.blit(txt2, (av2_x + taille_av[0] + 15, av2_y + h_c // 2 - 20))

            for index, carte in enumerate(mares_actuelles[2]):
                col    = index // 4
                row    = index % 4
                x_carte = p2_x + col * (w_c + gap)
                y_carte = p2_y + row * (h_c + gap)
                if carte.face_visible:
                    screen.blit(images_cartes_chargees[carte.image_fichier], (x_carte, y_carte))
                else:
                    screen.blit(carte_dos, (x_carte, y_carte))

        # -- Joueur 3 (en haut) --
        if joueur3 == "1" and 3 in mares_actuelles:
            p3_x = 1920 // 2 - (4 * w_c + 3 * gap) // 2
            p3_y = 30

            av3   = pygame.transform.scale(portraits_humains[id_perso3] if etat_int3 == 0 else portraits_robots[id_perso3], taille_av)
            av3_x = p3_x + (4 * w_c + 3 * gap) + 40
            av3_y = p3_y + (2 * h_c + gap) // 2 - h_c // 2
            screen.blit(av3, (av3_x, av3_y))

            nom3 = "ROBOT" if etat_int3 == 1 else (comptes_assignes[3].pseudo if comptes_assignes[3] else "Inconnu")
            txt3 = police.render(nom3, True, (255, 255, 255))
            screen.blit(txt3, (av3_x + w_c + 15, av3_y + h_c // 2 - 20))

            for index, carte in enumerate(mares_actuelles[3]):
                row    = index // 4
                col    = index % 4
                x_carte = p3_x + col * (w_c + gap)
                y_carte = p3_y + row * (h_c + gap)
                if carte.face_visible:
                    screen.blit(images_cartes_chargees[carte.image_fichier], (x_carte, y_carte))
                else:
                    screen.blit(carte_dos, (x_carte, y_carte))

        # -- Joueur 4 (à droite) --
        if joueur4 == "1" and 4 in mares_actuelles:
            p4_x = 1920 - (2 * w_c + gap) - 40
            p4_y = 1060 // 2 - (4 * h_c + 3 * gap) // 2

            av4   = pygame.transform.scale(portraits_humains[id_perso4] if etat_int4 == 0 else portraits_robots[id_perso4], taille_av)
            av4_x = p4_x + (2 * w_c + gap) // 2 - w_c // 2
            av4_y = p4_y + (4 * h_c + 3 * gap) + 20
            screen.blit(av4, (av4_x, av4_y))

            nom4 = "ROBOT" if etat_int4 == 1 else (comptes_assignes[4].pseudo if comptes_assignes[4] else "Inconnu")
            txt4 = police.render(nom4, True, (255, 255, 255))
            screen.blit(txt4, (av4_x - txt4.get_width() - 15, av4_y + h_c // 2 - 20))

            for index, carte in enumerate(mares_actuelles[4]):
                col    = index // 4
                row    = index % 4
                x_carte = p4_x + col * (w_c + gap)
                y_carte = p4_y + row * (h_c + gap)
                if carte.face_visible:
                    screen.blit(images_cartes_chargees[carte.image_fichier], (x_carte, y_carte))
                else:
                    screen.blit(carte_dos, (x_carte, y_carte))

        # Cadre vert autour du portrait du joueur dont c'est le tour
        epaisseur_cadre = 5
        couleur_tour    = (0, 255, 0)
        if joueur_courant == 1:
            pygame.draw.rect(screen, couleur_tour, (av1_x - epaisseur_cadre, av1_y - epaisseur_cadre,
                             taille_av[0] + epaisseur_cadre * 2, taille_av[1] + epaisseur_cadre * 2), epaisseur_cadre)
        elif joueur_courant == 2 and joueur2 == "1":
            pygame.draw.rect(screen, couleur_tour, (av2_x - epaisseur_cadre, av2_y - epaisseur_cadre,
                             taille_av[0] + epaisseur_cadre * 2, taille_av[1] + epaisseur_cadre * 2), epaisseur_cadre)
        elif joueur_courant == 3 and joueur3 == "1":
            pygame.draw.rect(screen, couleur_tour, (av3_x - epaisseur_cadre, av3_y - epaisseur_cadre,
                             taille_av[0] + epaisseur_cadre * 2, taille_av[1] + epaisseur_cadre * 2), epaisseur_cadre)
        elif joueur_courant == 4 and joueur4 == "1":
            pygame.draw.rect(screen, couleur_tour, (av4_x - epaisseur_cadre, av4_y - epaisseur_cadre,
                             taille_av[0] + epaisseur_cadre * 2, taille_av[1] + epaisseur_cadre * 2), epaisseur_cadre)

        # Nom du joueur courant affiché en bas à gauche
        if joueur_courant == 1:
            nom_jc = "ROBOT" if etat_int1 == 1 else (comptes_assignes[1].pseudo if comptes_assignes[1] else "Inconnu")
        elif joueur_courant == 2:
            nom_jc = "ROBOT" if etat_int2 == 1 else (comptes_assignes[2].pseudo if comptes_assignes[2] else "Inconnu")
        elif joueur_courant == 3:
            nom_jc = "ROBOT" if etat_int3 == 1 else (comptes_assignes[3].pseudo if comptes_assignes[3] else "Inconnu")
        elif joueur_courant == 4:
            nom_jc = "ROBOT" if etat_int4 == 1 else (comptes_assignes[4].pseudo if comptes_assignes[4] else "Inconnu")

        # Indicateur de tour et des étapes disponibles
        c_actif   = (255, 255, 255)
        c_inactif = (120, 120, 120)

        txt_pseudo_indic = police_pseudo.render("[" + nom_jc + "] :", True, (255, 215, 0))

        if not doit_retourner_carte_bonus:
            txt_etape1 = police_etape_actif.render("~ Echange avec la riviere", True, c_actif)
            txt_etape2 = police_etape_inactif.render("~ Reveler une autre carte", True, c_inactif)
        else:
            txt_etape1 = police_etape_inactif.render("~ Echange avec la riviere", True, c_inactif)
            txt_etape2 = police_etape_actif.render("~ Reveler une autre carte", True, c_actif)

        base_x, base_y = 40, 860
        screen.blit(txt_pseudo_indic, (base_x, base_y))
        screen.blit(txt_etape1, (base_x + 20, base_y + 50))
        screen.blit(txt_etape2, (base_x + 20, base_y + 100))

        # Bouton pause / menu
        if not jeu_en_pause:
            screen.blit(bouton_traits_img, bouton_traits_rect)
        else:
            overlay = pygame.Surface((1920, 1060), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))
            screen.blit(menu_button, bouton_traits_rect)
            screen.blit(panneau_menu_img, panneau_menu_rect)

    pygame.display.flip()
