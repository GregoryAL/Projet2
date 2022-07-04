# Imports des librairies

import requests
from bs4 import BeautifulSoup
import lxml
from lxml import html
import csv
import datetime
import pathlib


def erreurscrapping(urlnonjoignable):
    """Ajoute l url de la page en erreur au fichier erreur.txt"""
    fichiererreur = open('donnees/erreur.txt', "a")
    fichiererreur.write(urlnonjoignable + ', ')
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
    contenu = str(ligne_a_cleaner).replace('<'+balise_html+'>', '').replace('</'+balise_html+'>', '')
    return contenu


def clean_resultat_xpath(resultat):
    """ renvoie la valeur recuperée avec xpath en supprimant les crochets et ' """
    resultat = str(resultat).strip(" [']")
    return resultat


def generation_nom_csv():
    """ cree une variable pour le nom du fichier csv comprenant la date du jour"""
    date_du_jour = datetime.datetime.now()
    date_du_jour = date_du_jour.strftime('%Y%m%d')
    nomfichier = "donnees/informations_bookstoscrape_du_" + date_du_jour + ".csv"
    return nomfichier


def create_csv_jour(nomfichier):
    """ cree un fichier csv qui contient la date du jour et ajoute les entetes """
    with open(nomfichier, 'w', newline='', encoding='utf-8-sig') as csv_du_jour:
        writer = csv.writer(csv_du_jour, delimiter='²', quotechar='|')
        writer.writerow(['product_page_url', 'universal_product_code (upc)', 'title', 'price_including_tax',
                         'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
                         'image_url'])


def recuperation_info_livre(url_du_livre):
    """recupere les differentes infos necessaires et les renvoi """
    # BookURL = recupere l'url de la page d'un livre : Phase 1 : URL prédeterminée
    book_url = url_du_livre
    liste_des_infos = str(book_url)
    # BookURLScrapped = Vérifie et Recupere le resultat de scrapping et parsing de la page URLlivre
    scrapped_page_bs4 = recuperation_et_parsing(book_url)
    scrapped_page_lxml = recuperation_et_parsing_lxml(book_url)
    # BookUPC = Recupere l'information dans les données scrappées et la clean
    book_upc = scrapped_page_bs4.find("table", {"class": "table table-striped"}).find(string="UPC").find_next('td')
    book_upc = clean_balises(book_upc, 'td')
    liste_des_infos = liste_des_infos+'²'+str(book_upc)
    # BookTitle = Recupere l'information dans les données scappées et la clean
    book_title = scrapped_page_bs4.find("div", {"class": "col-sm-6 product_main"}).find('h1')
    book_title = clean_balises(book_title, 'h1')
    liste_des_infos = liste_des_infos+'²'+str(book_title)
    # BookPriceWithTax = Recupere l'information dans les données scappées et la clean
    book_price_with_tax = scrapped_page_bs4.find("table", {"class": "table table-striped"}).\
        find(string="Price (incl. tax)").find_next('td')
    book_price_with_tax = clean_balises(book_price_with_tax, 'td').strip('£')
    print(book_price_with_tax)
    liste_des_infos = liste_des_infos+'²'+str(book_price_with_tax)
    # BookPriceWithoutTax = Recupere l'information dans les données scappées et la clean
    book_price_without_tax = scrapped_page_bs4.find("table", {"class": "table table-striped"}).\
        find(string="Price (excl. tax)").find_next('td')
    book_price_without_tax = clean_balises(book_price_without_tax, 'td').strip('£')
    liste_des_infos = liste_des_infos+'²'+str(book_price_without_tax)
    # BookNumberAvailable = Recupere l'information dans les données scappées et la clean
    book_number_available = scrapped_page_bs4.find("table", {"class": "table table-striped"}).\
        find(string="Availability").find_next('td')
    book_number_available = str(book_number_available)
    nombre_a_renvoyer = ''
    for i in range(len(book_number_available)):
        if book_number_available[i].isdigit():
            nombre_a_renvoyer = nombre_a_renvoyer + book_number_available[i]
    book_number_available = nombre_a_renvoyer
    liste_des_infos = liste_des_infos+'²'+str(book_number_available)
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
    liste_des_infos = liste_des_infos+'²'+str(book_description)
    # BookCategory =  Recupere l'information dans les données scappées et la clean
    book_category = scrapped_page_lxml.xpath('//div[@class="page_inner"]'
                                             '/ul[@class="breadcrumb"]'
                                             '/li[last()-1]'
                                             '/a/text()')
    book_category = clean_resultat_xpath(book_category)
    liste_des_infos = liste_des_infos+'²'+str(book_category)
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
    liste_des_infos = liste_des_infos+'²'+str(book_rating)
    # BookImageUrl =  Recupere l'information dans les données scappées et la clean
    book_pic_url = scrapped_page_lxml.xpath('//article[@class="product_page"]'
                                            '/div[@class="row"]'
                                            '/div[@class="col-sm-6"]'
                                            '/div[@id="product_gallery"]'
                                            '//img/@src'
                                            )
    book_pic_url = clean_resultat_xpath(book_pic_url)
    book_pic_url = str(book_pic_url).replace('../..', 'http://books.toscrape.com')
    liste_des_infos = liste_des_infos+'²'+str(book_pic_url)
    return liste_des_infos


def recherche_nombre_de_page(url_parsed):
    """" recherche le nombre de page et renvoie le nombre """
    nombre_livre_par_page = 20
    nombre_de_page = url_parsed.xpath('//div[@class="row"]//form[@class="form-horizontal"]/strong[1]/text()')
    nombre_de_page = clean_resultat_xpath(nombre_de_page)
    nombre_de_page = (int(nombre_de_page)/nombre_livre_par_page).__ceil__()
    return nombre_de_page


def lister_url_categorie(url_page_1, nombre_de_page):
    """ liste toutes les urls des pages d'une catégorie """
    liste_url_livres = [url_page_1]
    for i in range(nombre_de_page-1):
        liste_url_livres.append(url_page_1.replace('index.html', 'page-' + str(i+2) + '.html'))
    return liste_url_livres


def recuperation_books_url_from_page(category_url_page):
    """ liste toutes les url des livres d'une page de catégorie"""
    categorie_scrapped_lxml = recuperation_et_parsing_lxml(category_url_page)
    books_url_from_category = categorie_scrapped_lxml.xpath('//div[@class="row"]'
                                                            '/div[@class="col-sm-8 col-md-9"]'
                                                            '//ol[@class="row"]'
                                                            '//article/h3/a/@href')
    total_url_page = []
    for i in range(len(books_url_from_category)):

        total_url_page.append(str(books_url_from_category[i]).replace('../../../', 'http://books.toscrape.com'
                                                                                   '/catalogue/'))
    return total_url_page


def search_all_categories_url(main_parsed):
    """ listes les urls de toutes les catégories"""
    list_of_categories_url = main_parsed.xpath('//div[@class="side_categories"]'
                                               '/ul[@class="nav nav-list"]/li/ul/li/a/@href'
                                               )
    all_categories_url = []
    for i in range(len(list_of_categories_url)):

        all_categories_url.append("http://books.toscrape.com/"+str(list_of_categories_url[i]))
    return all_categories_url


"""def main():
    # Pour test
    # Initialisation d'un fichier erreur
    fichier_d_erreur = open('donnees/erreur.txt', "w")
    fichier_d_erreur.close()
    # Creer un csv avec les entetes indiquées à la date du jour
    nom_fichier_csv = generation_nom_csv()
    create_csv_jour(nom_fichier_csv)
    liste_info = recuperation_info_livre('http://books.toscrape.com/catalogue/alice-in-wonderland-alices-adventures-in-
    wonderland-1_5/index.html')
    #liste_info = recuperation_info_livre(
    #    'http://books.toscrape.com/catalogue/in-the-woods-dublin-murder-squad-1_433/index.html')
    # Ajouter les informations au CSV
    with open(nom_fichier_csv, 'a', newline='', encoding='utf-8') as dico_csv:
        writercsv = csv.writer(dico_csv, delimiter='²', quotechar='|')
        writercsv.writerow([liste_info])
    print(liste_info)"""


def main():
    """Point d'entrée du programme de scrapping"""

    # Initialisation d'un fichier erreur
    fichier_d_erreur = open('donnees/erreur.txt', "w")
    fichier_d_erreur.close()
    # Lance recuperation et parsing des données de la page d'acceuil de books.tosrape
    site_url = 'http://books.toscrape.com/'
    site_scrapped_lxml = recuperation_et_parsing_lxml(site_url)
    # Recupere toutes les catégories
    categories_url_whole_site = search_all_categories_url(site_scrapped_lxml)
    categories_dictionnaire = {}
    urls_of_categories = site_scrapped_lxml.xpath('//div[@class="side_categories"]'
                                               '/ul[@class="nav nav-list"]/li/ul/li/a/@href'
                                               )
    print(urls_of_categories)
    name_of_categories = []
    name_of_categories_brut = site_scrapped_lxml.xpath('//div[@class="side_categories"]'
                                               '/ul[@class="nav nav-list"]/li/ul/li/a/text()'
                                               )
    for each_name in name_of_categories_brut:
        name_of_categories.append(each_name.replace(" ","").replace("\n", ""))
    print(name_of_categories)
    print(len(urls_of_categories))
    for each_url in urls_of_categories:
        index_list = urls_of_categories.index(each_url)
        categories_dictionnaire[name_of_categories[index_list]] = each_url
    print(categories_dictionnaire)
    # Creer un csv avec les entetes indiquées à la date du jour
    nom_fichier_csv = generation_nom_csv()
    create_csv_jour(nom_fichier_csv)
    # Applique le scrapping de tous les livres d'une catégorie à toutes les catégories
    for i in range(len(categories_url_whole_site)):
        # Lance recuperation et parsing des données d'une catégorie
        premiere_page_categorie_url = categories_url_whole_site[i]
        categorie_scrapped_lxml = recuperation_et_parsing_lxml(premiere_page_categorie_url)
        # Lance fonction de recherche du nombre de page de la catégorie
        nombre_de_page = recherche_nombre_de_page(categorie_scrapped_lxml)
        # fonction listant url des pages de catégorie
        liste_url_categorie = lister_url_categorie(premiere_page_categorie_url, int(nombre_de_page))
        # Lance fonction de recuperation des url des livres des pages d'une catégories dans une liste
        for j in range(len(liste_url_categorie)):
            i_url = liste_url_categorie[j]
            books_url_list_for_category = recuperation_books_url_from_page(i_url)
            # Lance fonction recuperation d'information et ajout dans le csv a partir d une url
            for k in range(len(books_url_list_for_category)):
                liste_info = recuperation_info_livre(books_url_list_for_category[k])
                # Ajouter les informations au CSV
                with open(nom_fichier_csv, 'a', newline='', encoding='utf-8') as dico_csv:
                    writercsv = csv.writer(dico_csv, delimiter='²', quotechar='|')
                    writercsv.writerow([liste_info])


if __name__ == "__main__":
    main()
