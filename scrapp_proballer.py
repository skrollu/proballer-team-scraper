import mysql.connector
import pandas as pd
import requests as req
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

def connect_to_mysql(host: str, user: str, password: str, database: str):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

def create_table_if_not_exists(connection):
    cursor = connection.cursor()
   # Vérifier si la table existe
    cursor.execute("""
                   SHOW TABLES LIKE 'player'
                   """)
    table_exists = cursor.fetchone()

    # Si la table existe, la supprimer
    if table_exists:
        cursor.execute("""
                       DROP TABLE player
                       """)
        print("'player' table dropped")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player (
            nom     VARCHAR(255),
            taille  VARCHAR(255),
            age     INT,
            points  FLOAT,
            reb     FLOAT,
         	pd      FLOAT,
            d       INT,
            v_d     VARCHAR(255),
            min     FLOAT,
            2p_av   VARCHAR(255),
            3p_av   VARCHAR(255),
            fg_av   VARCHAR(255),
            ft_av   VARCHAR(255),
            ro      FLOAT,
            rebb    FLOAT,
            pdd     FLOAT,
            inn     FLOAT,
            bp      FLOAT,
            ct      FLOAT,
            fa      FLOAT,
            ptss    FLOAT,
            eva     FLOAT,
            ptsss   FLOAT,
            rebbb   FLOAT,
            ast     FLOAT,
            stl     FLOAT,
            blk     FLOAT,
            equipe  VARCHAR(255)
        )
    """)
    connection.commit()

# @Deprecated Not used any more
def insert_data_into_mysql(connection, data):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO player (nom, taille, age, points, reb, pd, d, v_d, min, 2p_av, 3p_av, fg_av, ft_av, ro, rebb, pdd, inn, bp, ct, fa, ptss, eva, ptsss, rebbb, ast, stl, blk, equipe)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, data)
    connection.commit()

# Fonction pour extraire les données d'une page HTML
def scrape_and_store_data(url: str, connection):
    tables = pd.read_html(url)
    
    # Reshape data
    players = tables[0]
    players.columns = ['nom', 'taille', 'age', 'points', 'reb', 'pd', 'd', 'v_d', 'min', '2p_av', '3p_av', 'fg_av', 'ft_av', 'ro', 'rebb', 'pdd', 'inn', 'bp', 'ct', 'fa', 'ptss', 'eva', 'ptsss', 'rebbb', 'ast', 'stl', 'blk']
    # add equipe column
    players['equipe'] = url.split("/").pop()
    players.drop(players.tail(3).index, inplace=True) # drop last 3 rows
    
    # Save data
    tables[0].to_sql('player', connection, if_exists='append', index=False)

# Return all french teams href from url
def get_fr_teams_href(url: str):
    response = req.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    target_a_tags = soup.find_all('a', class_='home-league__team-list__content__entry-team__presentation')
    href_values = []
    for tag in target_a_tags:
        href = tag.get('href')
        href_values.append(href)
    return href_values

def main():
    db_host='localhost'
    db_user='root'
    db_password='root'
    db_database='proballer'
    base_url = "https://www.proballers.com"
    fr_teams_enpoint = "/fr/basketball/ligue/82/france-nm-1/equipes"
    
    # Prepare mySQL db
    connection = connect_to_mysql()
    create_table_if_not_exists(connection)
    connection.close()
    
    # Get fr teams href from home page
    hrefs = get_fr_teams_href(base_url + fr_teams_enpoint)

    # Create sqlalchemy engine with a mysql connection
    engine = create_engine("mysql+mysqlconnector://"+db_user+":"+db_password+"@"+db_host+"/"+db_database)
    
    for href in hrefs:
        url = base_url + href
        print(url)
        scrape_and_store_data(url, engine)
        
if __name__ == "__main__":
    main()
