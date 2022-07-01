# Imports des librairies

import requests
from bs4 import BeautifulSoup
import lxml
from lxml import html
import csv
import datetime


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
        print('un probleme a été rencontré avec ', url_a_scrapper_et_parser, 'Passage au livre suivant. ')
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
        print('un probleme a été rencontré avec ', url_a_scrapper_et_parser, 'Passage au livre suivant. ')
        print(url_a_scrapper_et_parser, ' est loggé dans le fichier erreur.txt')
        erreurscrapping(url_a_scrapper_et_parser)


def recuperation_ligne_num_upc(scrapped_content):
    """Recupere le numéro UPC de la page precedement scrappée et parsée"""
    upc_ligne = scrapped_content.find("table", {"class": "table table-striped"}).find(string="UPC").find_next('td')
    return upc_ligne


def clean_balises(ligne_a_cleaner, balise_html):
    """Clean la chaine de caractere pour ne garder que le contenu et supprimer les balises html"""
    contenu = str(ligne_a_cleaner).strip(" ></"+balise_html)
    return contenu


def clean_renvoi_nombre(ligne_a_cleaner):
    """Clean la chaine de caractere pour ne garder que les nombres"""
    contenu = str(ligne_a_cleaner)
    nombre_a_renvoyer = ''
    for i in range(len(contenu)):
        if contenu[i].isdigit():
            nombre_a_renvoyer = nombre_a_renvoyer + contenu[i]
    return nombre_a_renvoyer


def clean_resultat_xpath(resultat):
    resultat = str(resultat).strip(" [']")
    return resultat


def clean_resultat_review(resultat):
    resultat = str(resultat).replace("star-rating ", "")
    if resultat == "One":
        resultat = "1"
    elif resultat == "Two":
        resultat = "2"
    elif resultat == "Three":
        resultat = "3"
    elif resultat == "Four":
        resultat = "4"
    elif resultat == "Five":
        resultat = "5"
    elif resultat == "Zero":
        resultat = "0"
    else:
        print("pas de review disponible")
    return resultat


def clean_resultat_pic_url(resultat):
    resultat = str(resultat).replace('../..', 'http://books.toscrape.com')
    return resultat


def recuperation_titre(scrapped_content):
    """Recupere la ligne contenant le titre"""
    titre_ligne = scrapped_content.find("div", {"class": "col-sm-6 product_main"}).find('h1')
    return titre_ligne


def recuperation_ligne_price_with_tax(scrapped_content):
    """Recupere la ligne contenant le prix avec taxe"""
    price_with_tax = scrapped_content.find("table", {"class": "table table-striped"}).find(string="Price (incl. tax)").\
        find_next('td')
    return price_with_tax


def recuperation_ligne_price_without_tax(scrapped_content):
    """Recupere la ligne contenant le prix sans tax"""
    price_without_tax = scrapped_content.find("table", {"class": "table table-striped"}).find(string="Price (excl. tax)"
                                                                                              ).find_next('td')
    return price_without_tax


def recuperation_ligne_disponibilite(scrapped_content):
    """Recupere la ligne contenant la disponibilité"""
    disponibility = scrapped_content.find("table", {"class": "table table-striped"}).find(string="Availability").\
        find_next('td')
    return disponibility


def recuperation_ligne_description(scrapped_content):
    """ Recuperer la ligne contenant la description du livre """
    description = scrapped_content.find("div", {"class": "sub-header"}).find_next('p')
    return description


def recuperation_ligne_categorie(scrapped_content):
    """ recupere la ligne contenant la catégorie du livre"""
    categorie = scrapped_content.xpath('//div[@class="page_inner"]'
                                       '/ul[@class="breadcrumb"]'
                                       '/li[last()-1]'
                                       '/a/text()')
    return categorie


def recuperation_ligne_rating(scrapped_content):
    """ recuperer la ligne contenant le rating du livre"""
    ratings = scrapped_content.xpath('//article[@class="product_page"]'
                                     '/div[@class="row"]'
                                     '/div[@class="col-sm-6 product_main"]'
                                     '/p[starts-with(@class, "star-rating")]/@class'
                                     )
    return ratings


def recuperation_ligne_pic_url(scrapped_content):
    """ recuperer la ligne contenant l url de la photo du livre """
    pics_url = scrapped_content.xpath('//article[@class="product_page"]'
                                      '/div[@class="row"]'
                                      '/div[@class="col-sm-6"]'
                                      '/div[@id="product_gallery"]'
                                      '//img/@src'
                                      )
    return pics_url


def generation_nom_csv():
    date_du_jour = datetime.datetime.now()
    date_du_jour = date_du_jour.strftime('%Y%m%d')
    nomfichier = "donnees/informations_bookstoscrape_du_" + date_du_jour + ".csv"
    return nomfichier


def create_csv_jour(nomfichier):
    with open(nomfichier, 'w', newline='') as csv_du_jour:
        writer = csv.writer(csv_du_jour, delimiter='²', quotechar='|')
        writer.writerow(['product_page_url', 'universal_product_code (upc)', 'title', 'price_including_tax',
                         'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating',
                         'image_url'])
    return csv_du_jour


def recuperation_info_livre(url_du_livre):
    # BookURL = recupere l'url de la page d'un livre : Phase 1 : URL prédeterminée
    book_url = url_du_livre
    liste_des_infos = str(book_url)
    # BookURLScrapped = Vérifie et Recupere le resultat de scrapping et parsing de la page URLlivre
    scrapped_page_bs4 = recuperation_et_parsing(book_url)
    scrapped_page_lxml = recuperation_et_parsing_lxml(book_url)
    # BookUPC = Recupere l'information dans les données scrappées et la clean
    book_upc = recuperation_ligne_num_upc(scrapped_page_bs4)
    book_upc = clean_balises(book_upc, 'td')
    liste_des_infos = liste_des_infos+'²'+str(book_upc)
    # BookTitle = Recupere l'information dans les données scappées et la clean
    book_title = recuperation_titre(scrapped_page_bs4)
    book_title = clean_balises(book_title, 'h1')
    liste_des_infos = liste_des_infos+'²'+str(book_title)
    # BookPriceWithTax = Recupere l'information dans les données scappées et la clean
    book_price_with_tax = recuperation_ligne_price_with_tax(scrapped_page_bs4)
    book_price_with_tax = clean_balises(book_price_with_tax, 'td')
    liste_des_infos = liste_des_infos+'²'+str(book_price_with_tax)
    # BookPriceWithoutTax = Recupere l'information dans les données scappées et la clean
    book_price_without_tax = recuperation_ligne_price_without_tax(scrapped_page_bs4)
    book_price_without_tax = clean_balises(book_price_without_tax, 'td')
    liste_des_infos = liste_des_infos+'²'+str(book_price_without_tax)
    # BookNumberAvailable = Recupere l'information dans les données scappées et la clean
    book_number_available = recuperation_ligne_disponibilite(scrapped_page_bs4)
    book_number_available = clean_renvoi_nombre(book_number_available)
    liste_des_infos = liste_des_infos+'²'+str(book_number_available)
    # BookDescription = Recupere l'information dans les données scappées et la clean
    book_description = recuperation_ligne_description(scrapped_page_bs4)
    book_description = clean_balises(book_description, 'p')
    liste_des_infos = liste_des_infos+'²'+str(book_description)
    # BookCategory =  Recupere l'information dans les données scappées et la clean
    book_category = recuperation_ligne_categorie(scrapped_page_lxml)
    book_category = clean_resultat_xpath(book_category)
    liste_des_infos = liste_des_infos+'²'+str(book_category)
    # BookReviewRating =  Recupere l'information dans les données scappées et la clean
    book_rating = recuperation_ligne_rating(scrapped_page_lxml)
    book_rating = clean_resultat_xpath(book_rating)
    book_rating = clean_resultat_review(book_rating)
    liste_des_infos = liste_des_infos+'²'+str(book_rating)
    # BookImageUrl =  Recupere l'information dans les données scappées et la clean
    book_pic_url = recuperation_ligne_pic_url(scrapped_page_lxml)
    book_pic_url = clean_resultat_xpath(book_pic_url)
    book_pic_url = clean_resultat_pic_url(book_pic_url)
    liste_des_infos = liste_des_infos+'²'+str(book_pic_url)
    return liste_des_infos

def main():
    """Point d'entrée du programme de scrapping"""
    # Initialisation d'un fichier erreur
    fichier_d_erreur = open('donnees/erreur.txt', "w")
    fichier_d_erreur.close()
    # Creer un csv avec les entetes indiquées à la date du jour
    nom_fichier_csv = generation_nom_csv()
    dico_csv = create_csv_jour(nom_fichier_csv)
    # Lance fonction recuperation d'information et ajout dans le csv a partir d une url
    liste_info = recuperation_info_livre('http://books.toscrape.com/catalogue/a-summer-in-europe_458/index.html')
    # Ajouter les informations au CSV
    with open(nom_fichier_csv, 'a', newline='') as dico_csv:
        writercsv = csv.writer(dico_csv, delimiter='²', quotechar='|')
        writercsv.writerow([liste_info])




if __name__ == "__main__":
    main()
