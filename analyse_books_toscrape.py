# Imports des librairies

import requests
import csv
from pathlib import Path
import fonctions_recuperation


""" Point d'entrée du programme de scrapping """


# Creation d'un dossier donnees s'il n'existe pas à la racine du projet
chemin_donnees = Path.cwd() / "donnees"
chemin_donnees.mkdir(exist_ok=True)

# Initialisation d'un fichier erreur
fichier_d_erreur = open('donnees/erreur.txt', "w")
fichier_d_erreur.close()
# Lance recuperation et parsing des données de la page d'accueil de books.toscrape
site_url = 'http://books.toscrape.com/'
site_scrapped_lxml = fonctions_recuperation.recuperation_et_parsing_lxml(site_url)
# Récupère tous les noms et urls de catégorie et les stocke dans un dictionnaire
categories_dictionnaire = {}
urls_of_categories = []
urls_of_categories_brut = site_scrapped_lxml.xpath('//div[@class="side_categories"]'
                                                   '/ul[@class="nav nav-list"]/li/ul/li/a/@href'
                                                   )
for urls in urls_of_categories_brut:
    urls_of_categories.append("http://books.toscrape.com/" + str(urls))
name_of_categories = []
name_of_categories_brut = site_scrapped_lxml.xpath('//div[@class="side_categories"]'
                                                   '/ul[@class="nav nav-list"]/li/ul/li/a/text()'
                                                   )
for each_name in name_of_categories_brut:
    name_of_categories.append(each_name.replace(" ", "").replace("\n", ""))
for each_url in urls_of_categories:
    index_list = urls_of_categories.index(each_url)
    categories_dictionnaire[name_of_categories[index_list]] = each_url
# Créer un csv avec les entêtes indiquées à la date du jour pour chaque catégorie
for categorie_name in categories_dictionnaire:
    categorie_path = chemin_donnees / categorie_name
    categorie_path.mkdir(exist_ok=True)
    categorie_image_path = categorie_path / "image"
    categorie_image_path.mkdir(exist_ok=True)
    nom_fichier_csv = fonctions_recuperation.generation_nom_csv(categorie_name)
    fonctions_recuperation.create_csv_jour(nom_fichier_csv, categorie_path)
    # Lance fonction de recherche de la liste des urls d'une categorie
    liste_url_categorie = fonctions_recuperation.renvoi_liste_url__livre_pour_toutes_pages_categorie(
        categories_dictionnaire[categorie_name])
    # Lance fonction de recuperation des url des livres des pages d'une catégorie dans une liste
    for liste_url in liste_url_categorie:
        books_url_list_for_category = fonctions_recuperation.recuperation_books_url_from_page(liste_url)
        # Lance fonction recuperation d'information et ajout dans le csv à partir d'une url
        for books_url in books_url_list_for_category:
            # Recuperation des informations pour chaque livre
            liste_info = fonctions_recuperation.recuperation_info_livre(books_url, categorie_name)
            # Recuperation de la photo pour chaque livre
            if str(liste_info[9]) == "Pas de photo disponible":
                liste_info.append("Pas de photo disponible")
            else:
                url_image = liste_info[9]
                nom_image = liste_info[1]+"."+str(liste_info[9])[-3:]
                repertoire_et_nom_image = categorie_image_path / nom_image
                image_raw = requests.get(url_image)
                image_recuperee = open(repertoire_et_nom_image, "wb")
                image_recuperee.write(image_raw.content)
                image_recuperee.close()
                lien_photo_local = '=LIEN_HYPERTEXTE("'+str(repertoire_et_nom_image)+'";"'+nom_image+'")'
                liste_info.append(lien_photo_local)
            # Ajouter les informations au CSV
            fichier_chemin_complet = Path(categorie_path) / nom_fichier_csv
            with open(fichier_chemin_complet, 'a', newline='', encoding='utf-8') as dico_csv:
                writercsv = csv.writer(dico_csv, delimiter='\t', quotechar='|')
                writercsv.writerow(liste_info)
