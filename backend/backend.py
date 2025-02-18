# Libreria in grado di creare API
from fastapi import FastAPI
# Librerie per effettuare richieste HTTP
import requests
# Libreria per analizzare pagine HTML
from bs4 import BeautifulSoup
# Libreria per eseguire il server API
import uvicorn

# gestisce le richieste GET per fornire i dati al frontend
app = FastAPI()

# Parole chiave per identificare lattosio e glutine
ingredienti_lattosio = ["latte", "burro", "formaggio", "yogurt", "panna", "mozzarella", "ricotta", "besciamella", "parmigiano", "dado"]
ingredienti_glutine = ["farina", "pane", "pasta", "pizza", "biscotti", "grano", "orzo", "segale", "malto", "dado"]

# Funzione per estrarre il menù
def estrai_menu():
    url = 'https://aiuto.elis.org/menu/'
    risposta = requests.get(url)

    # Converto il codice html in un oggetto manipolabile in python
    parsingHtml = BeautifulSoup(risposta.text, 'html.parser')

    # Lista per contenere i dati dei piatti
    menu = []

    # Estrazione delle categorie di piatti
    categorie = parsingHtml.find_all('h3', class_='pietanze')

    for categoria in categorie:
        categoria_nome = categoria.get_text()
        nextDiv = categoria.find_next_sibling('div')
        piatti = nextDiv.find_all('h5', class_='ml-4 descrizionePietanza')
        ingredienti_tags = nextDiv.find_all('span', class_='ingredienti d-block')

        lista_piatti = []
        for i in range(len(piatti)):
            nome_piatto = piatti[i].get_text().strip()

            # Controllo se ci sono ingredienti disponibili
            if i < len(ingredienti_tags):
                dettagli = ingredienti_tags[i].get_text().strip().replace("\n", " ").replace("  ", " ")
            else:
                dettagli = "Ingredienti non disponibili"

            # Verifica presenza di lattosio e glutine
            contiene_lattosio = any(lattosio in dettagli.lower() for lattosio in ingredienti_lattosio)
            contiene_glutine = any(glutine in dettagli.lower() for glutine in ingredienti_glutine)

            lista_piatti.append({
                "nome": nome_piatto,
                "ingredienti": dettagli,
                "contiene_lattosio": contiene_lattosio,
                "contiene_glutine": contiene_glutine,
                "senza_lattosio": not contiene_lattosio,
                "senza_glutine": not contiene_glutine
            })

        menu.append({
            "categoria": categoria_nome,
            "pietanze": lista_piatti
        })

    return menu

@app.get("/menu")
def get_menu():
    return estrai_menu()

@app.get("/")
def home():
    return {"message": "Benvenuto! L'API è attiva."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
