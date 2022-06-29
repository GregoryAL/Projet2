# Imports des librairies

import requests
from bs4 import BeautifulSoup


def erreurscrapping(URLnonJoignable):
    """Ajoute l url de la page en erreur au fichier erreur.txt"""
    fichiererreur = open('erreur.txt', "a")
    fichiererreur.write(URLnonJoignable + ', ')
    fichiererreur.close()

def RecuperationEtParsing(URLaScrapperEtParser):
    """Recupere la page en argument, verifie le bon fonctionnement, et parse la page. Renvoie la page parsée"""
    ScrappedPage = requests.get(URLaScrapperEtParser)

    if ScrappedPage.status_code == 200:
        soup = BeautifulSoup(ScrappedPage.content, 'html.parser')
        return(soup)

    else:
        print('un probleme a été rencontré avec ', URLaScrapperEtParser, 'Passage au livre suivant. ', URLaScrapperEtParser,
              ' est loggé dans le fichier erreur.txt')
        erreurscrapping(URLaScrapperEtParser)

def RecuperationLigneNumUPC(ScrappedContent):
    """Recupere le numéro UPC de la page precedement scrappée et parsée"""
    UPCLigne=ScrappedContent.find(string="UPC")
    UPCnumLigne = UPCLigne.next_element
    return UPCnumLigne

def CleanLignetd(LigneACleaner):
    """Clean la chaine de caractere pour ne garder que le contenu et supprimer les balises html"""
    contenu = str(LigneACleaner)
    contenu = contenu.replace('<td>', '')
    contenu = contenu.replace('</td>', '')
    return contenu

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
    TDdeUPC = RecuperationLigneNumUPC(ScrappingPage)
    BookUPC = CleanLignetd(TDdeUPC)

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
