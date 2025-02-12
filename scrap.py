##
## EPITECH PROJECT, 2024
## workshop_scraping
## File description:
## main
##

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import requests

def selenium_method() -> int :
    #? Ouvre un webdriver chrome (utilisable aussi avec Firefox)
    driver = webdriver.Chrome()

    #? Création du dataframe pour stocker les données (libre à vous de rajouter des colonnes)
    COLUMNS = ["name", "national_id", "types", "species"]
    df = pd.DataFrame(columns=COLUMNS)

    #? Se connecte à l'URL souhaitée
    driver.get("https://pokemondb.net/pokedex/national")

    #? Utilisation de BeautifulSoup pour parse les données
    soup = BeautifulSoup(driver.page_source, "html.parser")
    infocards = soup.find_all("div", {"class": "infocard"})
    sheet_links = []
    for card in infocards:
        sheet_links.append("https://pokemondb.net/" + card.find("a")["href"])

    #? Browse les links
    # i = 0
    for link in sheet_links:
        #! break temporaire
        # if i > 10:
        #     break

        driver.get(link)
        print(f"Current link = {link}")

        #? Parse les données
        sheet_data = {}
        soup = BeautifulSoup(driver.page_source, "html.parser")
        sheet_data["name"] = soup.find("h1").getText()
        td = soup.find("table", {"class": "vitals-table"}).find_all("td")
        sheet_data["national_id"] = td[0].getText()
        sheet_data["types"] = td[1].find_all("a")
        sheet_data["species"] = td[2].getText()

        #? Ajout des données du pokemon actuel dans notre dataframe
        df = df._append(sheet_data, ignore_index=True)
        print(f"{df}\n")

        # i += 1
        # sleep(1)

    #? Ferme le webdriver
    # input("Appuyez sur une entrée pour quitter.")
    driver.quit()

    #? Enregistre le dataframe dans un fichier (libre à vous de choisir l'extension)
    print(df)
    df.to_csv("pokemon.csv", index=False)


def requests_method() -> int :
    COLUMNS = ["name", "national_id", "types", "species"]
    df = pd.DataFrame(columns=COLUMNS)

    res = requests.get("https://pokemondb.net/pokedex/national")

    soup = BeautifulSoup(res.content, "html.parser")
    infocards = soup.find_all("div", {"class": "infocard"})
    sheet_links = []
    for card in infocards:
        sheet_links.append("https://pokemondb.net/" + card.find("a")["href"])

    for link in sheet_links:
        res = requests.get(link)
        print(f"Current link = {link}")

        sheet_data = {}
        soup = BeautifulSoup(res.content, "html.parser")
        sheet_data["name"] = soup.find("h1").getText()
        td = soup.find("table", {"class": "vitals-table"}).find_all("td")
        sheet_data["national_id"] = td[0].getText()
        sheet_data["types"] = td[1].find_all("a")
        sheet_data["species"] = td[2].getText()

        df = df._append(sheet_data, ignore_index=True)
        print(f"{df}\n")

    print(df)
    df.to_csv("pokemon.csv", index=False)

if __name__ == "__main__":
    #? Voici 2 méthodes, une avec selenium et une autre avec requests
    selenium_method();
    # requests_method();

#* Possibilité d'ajouter des fonctions / méthodes pour actions répétitives
#* Possibilité d'ajouter des try & catch pour sécuriser le code (sur de long scraping notamment)
#* Possibilité de remplacer selenium par requests pour aller + vite (attention aux pages dynamiques)
#* Possibilité de rajouter des sleep pour coutourner les captchas (ou autre moyen comme des solvers)
