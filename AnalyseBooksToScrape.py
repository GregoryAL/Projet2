# Imports des librairies

import requests
from bs4 import BeautifulSoup


def erreurscrapping(urlnonjoignable):
    """Ajoute l url de la page en erreur au fichier erreur.txt"""
    fichiererreur = open('erreur.txt', "a")
    fichiererreur.write(urlnonjoignable + ', ')
    fichiererreur.close()


def recuperation_et_parsing(url_a_scrapper_et_parser):
    """Recupere la page en argument, verifie le bon fonctionnement, et parse la page. Renvoie la page parsée"""
    scrapped_page = requests.get(url_a_scrapper_et_parser)

    if scrapped_page.status_code == 200:
        soup = BeautifulSoup(scrapped_page.content, 'html.parser')
        return soup

    else:
        print('un probleme a été rencontré avec ', url_a_scrapper_et_parser, 'Passage au livre suivant. ')
        print(url_a_scrapper_et_parser, ' est loggé dans le fichier erreur.txt')
        erreurscrapping(url_a_scrapper_et_parser)


def recuperation_ligne_num_upc(scrapped_content):
    """Recupere le numéro UPC de la page precedement scrappée et parsée"""
    upc_ligne = scrapped_content.find("table", {"class": "table table-striped"}).find(string="UPC").findNext('td')
    return upc_ligne


def clean_balises(ligne_a_cleaner, balise_html):
    """Clean la chaine de caractere pour ne garder que le contenu et supprimer les balises html"""
    contenu = str(ligne_a_cleaner)
    contenu = contenu.replace('<'+balise_html+'>', '')
    contenu = contenu.replace('</'+balise_html+'>', '')
    return contenu


def clean_renvoi_nombre(ligne_a_cleaner):
    """Clean la chaine de caractere pour ne garder que les nombres"""
    contenu = str(ligne_a_cleaner)
    nombre_a_renvoyer = ''
    for i in range(len(contenu)):
        if contenu[i].isdigit():
            nombre_a_renvoyer = nombre_a_renvoyer + contenu[i]
    return nombre_a_renvoyer


def recuperation_titre(scrapped_content):
    """Recupere la ligne contenant le titre"""
    titre_ligne = scrapped_content.find("div", {"class": "col-sm-6 product_main"}).find('h1')
    return titre_ligne


def recuperation_ligne_price_with_tax(scrapped_content):
    """Recupere la ligne contenant le prix avec taxe"""
    price_with_tax = scrapped_content.find("table", {"class": "table table-striped"}).find(string="Price (incl. tax)").\
        findNext('td')
    return price_with_tax


def recuperation_ligne_price_without_tax(scrapped_content):
    """Recupere la ligne contenant le prix sans tax"""
    price_without_tax = scrapped_content.find("table", {"class": "table table-striped"}).find(string="Price (excl. tax)"
                                                                                              ).findNext('td')
    return price_without_tax


def recuperation_ligne_disponibilite(scrapped_content):
    """Recupere la ligne contenant la disponibilité"""
    table_disponibility = scrapped_content.find("table", {"class": "table table-striped"}).find(string="Availability").\
        findNext('td')
    return table_disponibility


def main():
    """Point d'entrée du programme de scrapping"""
    # Initialisation d'un fichier erreur
    fichier_d_erreur = open('erreur.txt', "w")
    fichier_d_erreur.close()

    # Creer un csv avec les entetes indiquées

    # BookURL = recupere l'url de la page d'un livre : Phase 1 : URL prédeterminée
    book_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    # BookURLScrapped = Vérifie et Recupere le resultat de scrapping et parsing de la page URLlivre
    scrapping_page = recuperation_et_parsing(book_url)
    # BookUPC = Recupere l'information dans les données scrappées et la clean
    book_upc = recuperation_ligne_num_upc(scrapping_page)
    book_upc = clean_balises(book_upc, 'td')
    print(book_upc)
    # BookTitle = Recupere l'information dans les données scappées et la clean
    book_title = recuperation_titre(scrapping_page)
    book_title = clean_balises(book_title, 'h1')
    print(book_title)
    # BookPriceWithTax = Recupere l'information dans les données scappées et la clean
    book_price_with_tax = recuperation_ligne_price_with_tax(scrapping_page)
    book_price_with_tax = clean_balises(book_price_with_tax, 'td')
    print(book_price_with_tax)
    # BookPriceWithoutTax = Recupere l'information dans les données scappées et la clean
    book_price_without_tax = recuperation_ligne_price_without_tax(scrapping_page)
    book_price_without_tax = clean_balises(book_price_without_tax, 'td')
    print(book_price_without_tax)
    # BookNumberAvailable = Recupere l'information dans les données scappées et la clean
    book_number_available = recuperation_ligne_disponibilite(scrapping_page)
    book_number_available = clean_renvoi_nombre(book_number_available)
    print(book_number_available)
    # BookDescription = Recupere l'information dans les données scappées et la clean
    # BookCategory =  Recupere l'information dans les données scappées et la clean
    # BookReviewRating =  Recupere l'information dans les données scappées et la clean
    # BookImageUrl =  Recupere l'information dans les données scappées et la clean
    # Ajouter les informations au CSV


if __name__ == "__main__":
    main()
