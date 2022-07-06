# Projet : Récupération d'informations du site books.toscrape.com pour analyse de marché  


*Auteur : Grégory ALLEN*

## Fonctionnalité :  
  
Le programme a pour but de récupérer, pour tous les livres du site books.toscrape.com, les informations suivantes :  
- URL du livre
- Universal Product Code
- Titre
- Prix TTC
- Prix HT
- Nombre d'exemplaires disponible
- Description
- Catégorie
- Moyenne des avis
- URL de l'image de première de couverture  

Toutes ces informations seront stockées dans un fichier csv différent par catégorie.
Il récupèrera également localement l'image de première de couverture et en précise le lien local et le nom dans le fichier csv.

## Limitation :  

On ne peut pas récupérer les informations d'un livre qui ne se trouverait dans aucune catégorie.  
Le temps nécessaire à la récupération de toutes les informations est assez grand.
  
## Installation et utilisation :
  
### Créer un environnement virtuel Python : 
 
#### en ligne de commande, se placer dans le dossier de travail désiré :

*cd /chemin/vers_le/repertoire_desire*
     
#### créer un environnement virtuel dans le repertoire de travail désiré :
 
- sous Windows, saisir 

*python -m venv env*  

- sous Linux, saisir
   
*python3 -m venv env*
   
#### activer l'environnement virtuel
       
- sous Windows, saisir  
       
*env\Scripts\activate.bat*
       
- sous Linux, saisir  
      
*source env/bin/activate*  

### Préparer l'environnement virtuel pour qu'il puisse lancer notre script

#### Télécharger les scripts Python : *analyse_books_toscrape.py* et *fonctions_recuperation* ainsi que le fichier *requirements.txt* et placer ces fichiers dans *chemin/vers_le/repertoire_desire/*  

#### Récuperer les modules / packages nécessaires pour faire fonctionner notre script :
    
Toujours en étant dans */chemin/vers_le/repertoire_desire* saisir :  
    
*pip install -r requirements.txt*

### Lancer notre script de récupération d'informations  

#### En ligne de commande, toujours en étant dans *chemin/vers_le/repertoire_desire*, saisir :

*python .\analyse_books_toscrape.py*

## Résultat attendu :  
  
1. Le script va créer un dossier *donnee* dans *chemin/vers_le/repertoire_desire* 

2. Dans ce dossier il va créer un repertoire par catégorie

3. Dans ces sous dossiers il stockera un fichier csv au nom de la catégorie et a la date du jour qui stockera les informations de tous les livres de la catégorie

4. Il va créer également un sous dossier *image* dans celui de *categorie* et y stockera l'image de 1ère de couverture

5. En cas d'erreur lors du traitement, il créera un fichier *erreur.txt* dans *chemin/vers_le/repertoire_desire* et y stockera le type d'erreur ainsi que l'url / information pour laquelle elle s'est produite. Ce fichier écrasera l'ancien s'il en existait déjà un.






