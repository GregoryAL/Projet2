# Imports des librairies

import requests
from bs4 import BeautifulSoup
import lxml
from lxml import html
import csv
import datetime
from pathlib import Path


def erreurscrapping(urlnonjoignable):
    """Ajoute l url de la page en erreur au fichier erreur.txt"""
    fichiererreur = open('donnees/erreur.txt', "a")
    fichiererreur.write("l'url " + urlnonjoignable + "n'est pas joignable" + "\n")
    fichiererreur.close()
    exit()


def recuperation_et_parsing(url_a_scrapper_et_parser):
    """Recupere la page en argument, verifie le bon fonctionnement, et parse la page avec beautifulsoup.
    Renvoie la page parsée"""
    scrapped_page = requests.get(url_a_scrapper_et_parser)
    if scrapped_page.status_code == 200:
        soup = BeautifulSoup(scrapped_page.content, 'html.parser')
        return soup

    else:
        print('un probleme a été rencontré avec ', url_a_scrapper_et_parser, "Passage à l'étape suivante. ")
        print(url_a_scrapper_et_parser, ' est loggé dans le fichier erreur.txt')
        erreurscrapping(url_a_scrapper_et_parser)


def recuperation_et_parsing_lxml(url_a_scrapper_et_parser):
    """Recupere la page en argument, verifie le bon fonctionnement, et parse la page avec lxml.
    Renvoie la page parsée"""
    scrapped_page = requests.get(url_a_scrapper_et_parser)
    if scrapped_page.status_code == 200:
        soup = lxml.html.fromstring(scrapped_page.content)
        return soup
    else:
        print('un probleme a été rencontré avec ', url_a_scrapper_et_parser, "Passage à l'étape suivante. ")
        print(url_a_scrapper_et_parser, ' est loggé dans le fichier erreur.txt')
        erreurscrapping(url_a_scrapper_et_parser)


def clean_balises(ligne_a_cleaner, balise_html):
    """Clean la chaine de caractere pour ne garder que le contenu et supprimer les balises html"""
    balise_debut = '<' + balise_html + '>'
    balise_fin = '</' + balise_html + '>'
    if str(ligne_a_cleaner).startswith(str(balise_debut)) and str(ligne_a_cleaner).endswith(str(balise_fin)):
        contenu = str(ligne_a_cleaner).replace('<'+balise_html+'>', '').replace('</'+balise_html+'>', '')
    else:
        fichiererreur = open('donnees/erreur.txt', "a")
        fichiererreur.write("la balise" + balise_html + "était attendue pour l'information" + ligne_a_cleaner + "\n")
        fichiererreur.close()
        contenu = ligne_a_cleaner
    return contenu


def clean_resultat_xpath(resultat):
    """ renvoie la valeur recuperée avec xpath en supprimant les crochets et ' """
    if str(resultat).startswith("['") and str(resultat).endswith("']"):
        resultat_cleaned = str(resultat).strip(" [']")
    elif str(resultat).startswith('["') and str(resultat).endswith('"]'):
        resultat_cleaned = str(resultat).strip(' ["]')
    else:
        fichiererreur = open('donnees/erreur.txt', "a")
        fichiererreur.write("les caracteres ['...'] étaient attendus pour l'information" + str(resultat) + "\n")
        fichiererreur.close()
        resultat_cleaned = resultat
    return resultat_cleaned


def generation_nom_csv(categorie):
    """ cree une variable pour le nom du fichier csv comprenant la date du jour"""
    date_du_jour = datetime.datetime.now()
    date_du_jour = date_du_jour.strftime('%Y%m%d')
    nomfichier = "informations_bookstoscrape_categorie_" + categorie + "_du_" + date_du_jour + ".csv"
    return nomfichier


def create_csv_jour(nomfichier, chemin):
    """ cree un fichier csv qui contient la date du jour et ajoute les entetes """
    fichier_chemin = Path(chemin) / nomfichier
    print(fichier_chemin)
    with open(fichier_chemin, 'w', newline='', encoding='utf-8-sig') as csv_du_jour:
        writer = csv.writer(csv_du_jour, delimiter='²', quotechar='|')
        writer.writerow(['product_page_url', 'universal_product_code (upc)', 'title', 'price_including_tax',
                         'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
                         'image_url'])


def recuperation_info_livre(url_du_livre):
    """recupere les differentes infos necessaires et les renvoi """
    # BookURL = recupere l'url de la page d'un livre : Phase 1 : URL prédeterminée
    book_url = url_du_livre
    liste_infos_format_liste = [book_url]
    # BookURLScrapped = Vérifie et Recupere le resultat de scrapping et parsing de la page URLlivre
    scrapped_page_bs4 = recuperation_et_parsing(book_url)
    scrapped_page_lxml = recuperation_et_parsing_lxml(book_url)
    # BookUPC = Recupere l'information dans les données scrappées et la clean
    if (scrapped_page_bs4.find("table", {"class": "table table-striped"}).find(string="UPC")) == "UPC":
        book_upc = scrapped_page_bs4.find("table", {"class": "table table-striped"}).find(string="UPC").find_next('td')
        book_upc = clean_balises(book_upc, 'td')
        liste_infos_format_liste.append(book_upc)
    else:
        fichiererreur = open('donnees/erreur.txt', "a")
        fichiererreur.write("Il n'y a pas de numéro UPC renseigné pour " + str(book_url) + "\n")
        fichiererreur.close()
        liste_infos_format_liste.append("Pas de numéro UPC")


    # BookTitle = Recupere l'information dans les données scappées et la clean
    book_title = scrapped_page_bs4.find("div", {"class": "col-sm-6 product_main"}).find('h1')
    book_title = clean_balises(book_title, 'h1')
    liste_infos_format_liste.append(book_title)
    # BookPriceWithTax = Recupere l'information dans les données scappées et la clean
    book_price_with_tax = scrapped_page_bs4.find("table", {"class": "table table-striped"}).\
        find(string="Price (incl. tax)").find_next('td')
    book_price_with_tax = clean_balises(book_price_with_tax, 'td').strip('£')
    liste_infos_format_liste.append(book_price_with_tax)
    # BookPriceWithoutTax = Recupere l'information dans les données scappées et la clean
    book_price_without_tax = scrapped_page_bs4.find("table", {"class": "table table-striped"}).\
        find(string="Price (excl. tax)").find_next('td')
    book_price_without_tax = clean_balises(book_price_without_tax, 'td').strip('£')
    liste_infos_format_liste.append(book_price_without_tax)
    # BookNumberAvailable = Recupere l'information dans les données scappées et la clean
    book_number_available = scrapped_page_bs4.find("table", {"class": "table table-striped"}).\
        find(string="Availability").find_next('td')
    book_number_available = str(book_number_available)
    nombre_a_renvoyer = ''
    for i in range(len(book_number_available)):
        if book_number_available[i].isdigit():
            nombre_a_renvoyer = nombre_a_renvoyer + book_number_available[i]
    book_number_available = nombre_a_renvoyer
    liste_infos_format_liste.append(book_number_available)
    # BookDescription = Recupere l'information dans les données scappées et la clean
    # Verifie également qu'une description est disponible
    test_description = scrapped_page_lxml.xpath('//article[@class="product_page"]'
                                                '/div[@id="product_description"]'
                                                '/h2/text()')
    test_description = clean_resultat_xpath(test_description)
    if test_description == "Product Description":
        book_description = scrapped_page_lxml.xpath('//article[@class="product_page"]'
                                                    '/p/text()')
        book_description = clean_resultat_xpath(book_description)
    else:
        book_description = "No Description Available"
    liste_infos_format_liste.append(book_description)
    # BookCategory =  Recupere l'information dans les données scappées et la clean
    book_category = scrapped_page_lxml.xpath('//div[@class="page_inner"]'
                                             '/ul[@class="breadcrumb"]'
                                             '/li[last()-1]'
                                             '/a/text()')
    book_category = clean_resultat_xpath(book_category)
    liste_infos_format_liste.append(book_category)
    # BookReviewRating =  Recupere l'information dans les données scappées et la clean
    book_rating = scrapped_page_lxml.xpath('//article[@class="product_page"]'
                                           '/div[@class="row"]'
                                           '/div[@class="col-sm-6 product_main"]'
                                           '/p[starts-with(@class, "star-rating")]/@class'
                                           )
    book_rating = clean_resultat_xpath(book_rating)
    book_rating = str(book_rating).replace("star-rating ", "")
    if book_rating == "One":
        book_rating = "1"
    elif book_rating == "Two":
        book_rating = "2"
    elif book_rating == "Three":
        book_rating = "3"
    elif book_rating == "Four":
        book_rating = "4"
    elif book_rating == "Five":
        book_rating = "5"
    elif book_rating == "Zero":
        book_rating = "0"
    else:
        book_rating = "None"
    liste_infos_format_liste.append(book_rating)
    # BookImageUrl =  Recupere l'information dans les données scappées et la clean
    book_pic_url = scrapped_page_lxml.xpath('//article[@class="product_page"]'
                                            '/div[@class="row"]'
                                            '/div[@class="col-sm-6"]'
                                            '/div[@id="product_gallery"]'
                                            '//img/@src'
                                            )
    book_pic_url = clean_resultat_xpath(book_pic_url)
    book_pic_url = str(book_pic_url).replace('../..', 'http://books.toscrape.com')
    liste_infos_format_liste.append(book_pic_url)
    return liste_infos_format_liste


def renvoi_nombre_de_page_par_categorie(url_page):
    """" recherche le nombre de page et renvoie le nombre """
    nombre_de_page = 1
    scrapped_page_categorie = recuperation_et_parsing_lxml(url_page)
    presence_next = scrapped_page_categorie.xpath('//div[@class="page_inner"]'
                                                  '//ul[@class="pager"]'
                                                  '/li[@class="next"]/a/text()')
    # initialisation de variables pour pouvoir les utiliser dans la boucle while
    next_url_parsed = scrapped_page_categorie
    liste_url_livres = [url_page]
    base_url = url_page.replace('index.html', '')
    while presence_next == ['next']:
        nombre_de_page = nombre_de_page + 1
        suffixe_url = clean_resultat_xpath(next_url_parsed.xpath('//div[@class="page_inner"]'
                                                                 '//ul[@class="pager"]'
                                                                 '/li[@class="next"]/a/@href'))
        prochaine_page_categorie = base_url + suffixe_url
        liste_url_livres.append(prochaine_page_categorie)
        next_url_parsed = recuperation_et_parsing_lxml(prochaine_page_categorie)
        presence_next = next_url_parsed.xpath('//div[@class="page_inner"]'
                                              '//ul[@class="pager"]'
                                              '/li[@class="next"]/a/text()')
    return liste_url_livres


def recuperation_books_url_from_page(category_url_page):
    """ liste toutes les url des livres d'une page de catégorie"""
    categorie_scrapped_lxml = recuperation_et_parsing_lxml(category_url_page)
    books_url_from_category = categorie_scrapped_lxml.xpath('//div[@class="row"]'
                                                            '/div[@class="col-sm-8 col-md-9"]'
                                                            '//ol[@class="row"]'
                                                            '//article/h3/a/@href')
    total_url_page = []
    for single_book_url in books_url_from_category:
        total_url_page.append(str(single_book_url).replace('../../../', 'http://books.toscrape.com'
                                                           '/catalogue/'))

    return total_url_page


"""Point d'entrée du programme de scrapping"""

# Creation d'un dossier donnees s'il n'existe pas à la racine du projet
chemin_donnees = Path.cwd() / "donnees"
chemin_donnees.mkdir(exist_ok=True)

# Initialisation d'un fichier erreur
fichier_d_erreur = open('donnees/erreur.txt', "w")
fichier_d_erreur.close()
# Lance recuperation et parsing des données de la page d'acceuil de books.tosrape
site_url = 'http://books.toscrape.com/'
site_scrapped_lxml = recuperation_et_parsing_lxml(site_url)
# Recupere tous les noms et urls de catégorie et les stocke dans un dictionnaire
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
# Creer un csv avec les entetes indiquées à la date du jour pour chaque catégorie
for categorie_name in categories_dictionnaire:
    categorie_path = chemin_donnees / categorie_name
    categorie_path.mkdir(exist_ok=True)
    nom_fichier_csv = generation_nom_csv(categorie_name)
    create_csv_jour(nom_fichier_csv, categorie_path)
    # Lance fonction de recherche de la liste des urls d une categorie
    liste_url_categorie = renvoi_nombre_de_page_par_categorie(categories_dictionnaire[categorie_name])
    # Lance fonction de recuperation des url des livres des pages d'une catégories dans une liste
    for liste_url in liste_url_categorie:
        books_url_list_for_category = recuperation_books_url_from_page(liste_url)
        # Lance fonction recuperation d'information et ajout dans le csv a partir d une url
        for books_url in books_url_list_for_category:
            liste_info = recuperation_info_livre(books_url)
            # Ajouter les informations au CSV
            fichier_chemin_complet = Path(categorie_path) / nom_fichier_csv
            with open(fichier_chemin_complet, 'a', newline='', encoding='utf-8') as dico_csv:
                writercsv = csv.writer(dico_csv, delimiter='²', quotechar='|')
                writercsv.writerow(liste_info)
