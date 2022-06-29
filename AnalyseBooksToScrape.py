# Imports des librairies

import requests
from bs4 import BeautifulSoup


def erreurscrapping(URLnonJoignable):
    fichiererreur = open('erreur.txt', "a")
    fichiererreur.write(URLnonJoignable + ', ')
    fichiererreur.close()

def RecuperationEtParsing(URLaScrapperEtParser):
    ScrappedPage = requests.get(URLaScrapperEtParser)

    if ScrappedPage.status_code == 200:
        soup = BeautifulSoup(ScrappedPage.content, 'html.parser')
        print('Scrapping ok')
        return(soup)

    else:
        print('un probleme a été rencontré avec ', URLaScrapperEtParser, 'Passage au livre suivant. ', URLaScrapperEtParser,
              ' est loggé dans le fichier erreur.txt')
        erreurscrapping(URLaScrapperEtParser)

def main():
    """Point d'entrée du programme de scrapping"""
    # Initialisation d'un fichier erreur
    fichierDErreur = open('erreur.txt', "w")
    fichierDErreur.close()

    # Creer un csv avec les entetes indiquées

    # BookURL = recupere l'url de la page d'un livre : Phase 1 : URL prédeterminée
    BookURL = ('http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')
    # BookURLScrapped = Vérifie et Recupere le resultat de scrapping et parsing de la page URLlivre
    ScrappingPage = RecuperationEtParsing(BookURL)


    # BookUPC = Recupere l'information dans les données scrappées et la clean

    # BookTitle = Recupere l'information dans les données scappées et la clean
    # BookPriceWithTax = Recupere l'information dans les données scappées et la clean
    # BookPriceWithoutTax = Recupere l'information dans les données scappées et la clean
    # BookNumberAvailable = Recupere l'information dans les données scappées et la clean
    # BookDescription = Recupere l'information dans les données scappées et la clean
    # BookCategory =  Recupere l'information dans les données scappées et la clean
    # BookReviewRating =  Recupere l'information dans les données scappées et la clean
    # BookImageUrl =  Recupere l'information dans les données scappées et la clean
    # Ajouter les informations au CSV


if __name__ == "__main__":
    main()
