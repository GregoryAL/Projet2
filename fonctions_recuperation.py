from bs4 import BeautifulSoup
import lxml
from lxml import html
import datetime
import requests
import csv
from pathlib import Path


def erreur_scrapping(url_non_joignable):
    """Ajoute l'URL de la page en erreur au fichier erreur.txt"""
    fichier_erreur = open('donnees/erreur.txt', "a")
    fichier_erreur.write("l'URL " + url_non_joignable + "n'est pas joignable" + "\n")
    fichier_erreur.close()
    exit()


def recuperation_et_parsing(url_a_scrapper_et_parser):
    """Récupère la page en argument, vérifie le bon fonctionnement et parse la page avec beautifulsoup.
    Renvoie la page parsée"""
    try:
        scrapped_page = requests.get(url_a_scrapper_et_parser)
        if scrapped_page.status_code == 200:
            soup = BeautifulSoup(scrapped_page.content, 'html.parser')
            return soup

        else:
            print('un problème a été rencontré avec ', url_a_scrapper_et_parser, ".")
            print(url_a_scrapper_et_parser, ' est enregistré dans le fichier erreur.txt')
            erreur_scrapping(url_a_scrapper_et_parser)
    except requests.exceptions.ConnectionError:
        print('un problème a été rencontré avec ', url_a_scrapper_et_parser, ".")
        print(url_a_scrapper_et_parser, ' est enregistré dans le fichier erreur.txt')
        erreur_scrapping(url_a_scrapper_et_parser)
        exit()


def recuperation_et_parsing_lxml(url_a_scrapper_et_parser):
    """Récupère la page en argument, vérifie le bon fonctionnement et parse la page avec lxml.
    Renvoie la page parsée"""
    try:
        scrapped_page = requests.get(url_a_scrapper_et_parser)
        if scrapped_page.status_code == 200:
            soup = lxml.html.fromstring(scrapped_page.content)
            return soup
        else:
            print('un problème a été rencontré avec ', url_a_scrapper_et_parser, ".")
            print(url_a_scrapper_et_parser, ' est enregistré dans le fichier erreur.txt')
            erreur_scrapping(url_a_scrapper_et_parser)
    except requests.exceptions.ConnectionError:
        print('un problème a été rencontré avec ', url_a_scrapper_et_parser, ".")
        print(url_a_scrapper_et_parser, ' est enregistré dans le fichier erreur.txt')
        erreur_scrapping(url_a_scrapper_et_parser)
        exit()


def clean_balises(ligne_a_cleaner, balise_html):
    """Clean la chaine de caractère pour ne garder que le contenu et supprimer les balises html"""
    balise_debut = '<' + balise_html + '>'
    balise_fin = '</' + balise_html + '>'
    if str(ligne_a_cleaner).startswith(str(balise_debut)) and str(ligne_a_cleaner).endswith(str(balise_fin)):
        contenu = str(ligne_a_cleaner).replace('<' + balise_html + '>', '').replace('</' + balise_html + '>', '')
    else:
        fichier_erreur = open('donnees/erreur.txt', "a")
        fichier_erreur.write("la balise" + balise_html + "était attendue pour l'information" + ligne_a_cleaner + "\n")
        fichier_erreur.close()
        contenu = ligne_a_cleaner
    return contenu


def clean_resultat_xpath(resultat):
    """ Renvoie la valeur récupérée avec xpath en supprimant les crochets et ' """
    if str(resultat).startswith("['") and str(resultat).endswith("']"):
        resultat_cleaned = str(resultat).strip(" [']")
    elif str(resultat).startswith('["') and str(resultat).endswith('"]'):
        resultat_cleaned = str(resultat).strip(' ["]')
    elif str(resultat) == "[]":
        resultat_cleaned = ""
    else:
        fichier_erreur = open('donnees/erreur.txt', "a")
        fichier_erreur.write("les caractères ['...'] étaient attendus pour l'information" + str(resultat) + "\n")
        fichier_erreur.close()
        resultat_cleaned = resultat
    return resultat_cleaned


def generation_nom_csv(categorie):
    """ Cree une variable pour le nom du fichier csv comprenant la date du jour"""
    date_du_jour = datetime.datetime.now()
    date_du_jour = date_du_jour.strftime('%Y%m%d')
    nom_fichier = "informations_books.toscrape_categorie_" + categorie + "_du_" + date_du_jour + ".csv"
    return nom_fichier


def create_csv_jour(nom_fichier, chemin):
    """ Cree un fichier csv qui contient la date du jour et ajoute les entêtes """
    fichier_chemin = Path(chemin) / nom_fichier
    with open(fichier_chemin, 'w', newline='', encoding='utf-8-sig') as csv_du_jour:
        writer = csv.writer(csv_du_jour, delimiter='\t', quotechar='|')
        writer.writerow(['product_page_url', 'universal_product_code (upc)', 'title', 'price_including_tax (£)',
                         'price_excluding_tax (£)', 'number_available', 'product_description', 'category',
                         'review_rating', 'image_url', 'local_image_link'])


def recuperation_info_livre(url_du_livre, categorie_livre):
    """Récupère les différentes informations nécessaires et les renvoie """
    # BookURL = récupère l'URL de la page d'un livre
    book_url = url_du_livre
    liste_infos_format_liste = [book_url]
    # BookURLScrapped = Vérifie et récupère le résultat de scrapping et parsing de la page book_url
    scrapped_page_bs4 = recuperation_et_parsing(book_url)
    scrapped_page_lxml = recuperation_et_parsing_lxml(book_url)
    # BookUPC = Récupère l'information dans les données récupérée et la nettoie
    if (scrapped_page_bs4.find("table", {"class": "table table-striped"}).find(string="UPC")) == "UPC":
        book_upc = scrapped_page_bs4.find("table", {"class": "table table-striped"}).find(string="UPC").find_next('td')
        book_upc = clean_balises(book_upc, 'td')
        liste_infos_format_liste.append(book_upc)
    else:
        fichier_erreur = open('donnees/erreur.txt', "a")
        fichier_erreur.write("Il n'y a pas de numéro UPC renseigné pour " + str(book_url) + "\n")
        fichier_erreur.close()
        liste_infos_format_liste.append("Pas de numéro UPC renseigné")
    # BookTitle = Récupère l'information dans les données récupérée et la nettoie
    if (scrapped_page_bs4.find("div", {"class": "col-sm-6 product_main"}).find('h1')) is None:
        fichier_erreur = open('donnees/erreur.txt', "a")
        fichier_erreur.write("Il n'y a pas de titre renseigné pour " + str(book_url) + "\n")
        fichier_erreur.close()
        liste_infos_format_liste.append("Pas de titre renseigné")
    else:
        book_title = scrapped_page_bs4.find("div", {"class": "col-sm-6 product_main"}).find('h1')
        book_title = clean_balises(book_title, 'h1')
        liste_infos_format_liste.append(book_title)
    # BookPriceWithTax = Récupère l'information dans les données récupérées et la nettoie
    if (clean_balises(scrapped_page_bs4.find("table", {"class": "table table-striped"}).find(string="Price (incl. tax)")
       .find_next('td'), 'td')) is None:
        fichier_erreur = open('donnees/erreur.txt', "a")
        fichier_erreur.write("Il n'y a pas de Prix avec taxe renseigné pour " + str(book_url) + "\n")
        fichier_erreur.close()
        liste_infos_format_liste.append("0")
    else:
        book_price_with_tax = scrapped_page_bs4.find("table", {"class": "table table-striped"}). \
         find(string="Price (incl. tax)").find_next('td')
        book_price_with_tax = clean_balises(book_price_with_tax, 'td').strip('£')
        liste_infos_format_liste.append(book_price_with_tax)
    # BookPriceWithoutTax = Récupère l'information dans les données récupérée et la nettoie
    if (clean_balises(scrapped_page_bs4.find("table", {"class": "table table-striped"}).find(string="Price (excl. tax)")
       .find_next('td'), 'td')) is None:
        fichier_erreur = open('donnees/erreur.txt', "a")
        fichier_erreur.write("Il n'y a pas de Prix sans taxe renseigné pour " + str(book_url) + "\n")
        fichier_erreur.close()
        liste_infos_format_liste.append("")
    else:
        book_price_without_tax = scrapped_page_bs4.find("table", {"class": "table table-striped"}). \
            find(string="Price (excl. tax)").find_next('td')
        book_price_without_tax = clean_balises(book_price_without_tax, 'td').strip('£')
        liste_infos_format_liste.append(book_price_without_tax)
    # BookNumberAvailable = Récupère l'information dans les données récupérée et la nettoie
    if (clean_balises(scrapped_page_bs4.find("table", {"class": "table table-striped"}).find(string="Availability")
       .find_next('td'), 'td')).startswith("In stock"):
        book_number_available = scrapped_page_bs4.find("table", {"class": "table table-striped"}) \
            .find(string="Availability").find_next('td')
        nombre_a_renvoyer = ''
        for is_char_a_number in str(book_number_available):
            if is_char_a_number.isdigit():
                nombre_a_renvoyer = nombre_a_renvoyer + str(is_char_a_number)
        liste_infos_format_liste.append(nombre_a_renvoyer)
    elif (clean_balises(scrapped_page_bs4.find("table", {"class": "table table-striped"}).find(string="Availability")
          .find_next('td'), 'td')).startswith("Out of stock"):
        liste_infos_format_liste.append(0)
    else:
        fichier_erreur = open('donnees/erreur.txt', "a")
        fichier_erreur.write("Il n'y a pas d'information de disponibilité renseigné pour " + str(book_url) + "\n")
        fichier_erreur.close()
        liste_infos_format_liste.append("")

    # BookDescription = Récupère l'information dans les données récupérée et la nettoie
    # vérifie également qu'une description est disponible
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
    # BookCategory = Récupère l'information dans les données récupérée et la nettoie
    liste_infos_format_liste.append(categorie_livre)
    # BookReviewRating = Récupère l'information dans les données récupérée et la nettoie
    if (scrapped_page_lxml.xpath('//article[@class="product_page"]'
                                 '/div[@class="row"]'
                                 '/div[@class="col-sm-6 product_main"]'
                                 '/p[starts-with(@class, "star-rating")]/@class'
                                 )) is None:
        fichier_erreur = open('donnees/erreur.txt', "a")
        fichier_erreur.write("Il n'y a pas de moyenne de review renseigné pour " + str(book_url) + "\n")
        fichier_erreur.close()
        liste_infos_format_liste.append("")
    else:
        book_rating = scrapped_page_lxml.xpath('//article[@class="product_page"]'
                                               '/div[@class="row"]'
                                               '/div[@class="col-sm-6 product_main"]'
                                               '/p[starts-with(@class, "star-rating")]/@class'
                                               )
        book_rating = clean_resultat_xpath(book_rating)
        book_rating = str(book_rating).replace("star-rating ", "")
        correspondance_str_int = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5", "Zero": "0"}
        book_rating_int = correspondance_str_int[book_rating]
        liste_infos_format_liste.append(book_rating_int)
    # BookImageUrl = Récupère l'information dans les données récupérée et la nettoie
    if (scrapped_page_lxml.xpath('//article[@class="product_page"]'
                                 '/div[@class="row"]'
                                 '/div[@class="col-sm-6"]'
                                 '/div[@id="product_gallery"]'
                                 '//img/@src'
                                 )) is None:
        fichier_erreur = open('donnees/erreur.txt', "a")
        fichier_erreur.write("Il n'y a pas de photo disponible pour " + str(book_url) + "\n")
        fichier_erreur.close()
        liste_infos_format_liste.append("Pas de photo disponible")
    else:
        book_pic_url = scrapped_page_lxml.xpath('//article[@class="product_page"]'
                                                '/div[@class="row"]'
                                                '/div[@class="col-sm-6"]'
                                                '/div[@id="product_gallery"]'
                                                '//img/@src'
                                                )
        book_pic_url = clean_resultat_xpath(book_pic_url)
        book_pic_url = str(book_pic_url).replace('../..', 'http://books.toscrape.com')
        liste_infos_format_liste.append(book_pic_url)
    # Retourne la liste des informations
    return liste_infos_format_liste


def renvoi_liste_url__livre_pour_toutes_pages_categorie(url_page):
    """" Recherche les urls des pages d'une catégorie """
    scrapped_page_categorie = recuperation_et_parsing_lxml(url_page)
    presence_next = scrapped_page_categorie.xpath('//div[@class="page_inner"]'
                                                  '//ul[@class="pager"]'
                                                  '/li[@class="next"]/a/text()')
    # initialisation de variables pour pouvoir les utiliser dans la boucle while
    next_url_parsed = scrapped_page_categorie
    liste_url_livres = [url_page]
    base_url = url_page.replace('index.html', '')
    while presence_next == ['next']:
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
    """ Liste toutes les url des livres d'une page de catégorie"""
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
