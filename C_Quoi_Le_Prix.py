#Importation des modules nécéssaires
import requests
import json
import random
import time
from flask import Flask , render_template , request , session

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game' ,methods = ['get','post'])
def LaunchGame():

    KeywordsByCat = {
                'Computers':['souris','ordinateur','clavier','tapis de souris','ecran'],
                'Vehicles' :['Jantes','Pare-Brise','Essuie-glaces'],
                'Kitchen'  :['Casseroles','eponges']
            }
    
    randomCategory = request.form['cat']
    randomKeyword = KeywordsByCat[randomCategory][random.randint(0,len(KeywordsByCat[randomCategory])-1)]
    print(randomCategory , randomKeyword)
    parameters = {
        "ApiKey": "b3b33725-547b-4368-9373-e97d94783a4d",
        "SearchRequest": {
        "Keyword": randomKeyword,
        "Pagination": {
            "ItemsPerPage": 10,
            "PageNumber": 0
        },
        "Filters": {
            "Price": {
            "Min": 0,
            "Max": 0
            },
            "Navigation": randomCategory,
            "IncludeMarketPlace": "true"
        }
        }
    }
    Url = "https://api.cdiscount.com/OpenApi/json/Search"
    response = requests.post(Url, data=json.dumps(parameters))
    response = response.json()
    randomArticle = response['Products'][random.randint(0,len(response['Products'])-1)]
    articleName=(randomArticle['Name'])
    articleImg=(randomArticle['MainImageUrl'])
    articleId=(randomArticle['Id'])

    try:
        nbParties=request.form['nbParties']
    except:
        nbParties=0
    
    try:
        absecart=round(float(request.form['absecart'])*100)/100
    except:
        absecart=0

    newTime = time.time()

    try:
        score=request.form['score']
    except:
        score="\n"


    return render_template('game.html',score=score,aName = articleName,aImg = articleImg,aId = articleId,nbParties=nbParties,absecart=absecart,timeDebut=newTime)

@app.route('/try',methods = ['get','post'])
def verifPrice():

    timeFin = time.time()-float(request.form['timeDebut'])
    timeFin = (round(timeFin*100))/100

    url="https://api.cdiscount.com/OpenApi/json/GetProduct"

    parameters={
    "ApiKey": "b3b33725-547b-4368-9373-e97d94783a4d",
    "ProductRequest": {
        "ProductIdList": [
        request.form['id']
        ],
        "Scope": {
        "Offers": "false",
        "AssociatedProducts": "false",
        "Images": "false",
        "Ean": "false"
        }
    }
    }
    response = requests.post(url, data=json.dumps(parameters))
    response = response.json()
    correctPrice =float(response['Products'][0]['BestOffer']['SalePrice'])
    articleName= response['Products'][0]['Name']
    articleImg = response['Products'][0]['MainImageUrl']
    PriceEntry =float(request.form['priceEntry']) 
    try:
        ecart=ecart
    except NameError:
        ecart=0

    ecart = ecart + 100-((correctPrice*100)/PriceEntry)/(int(request.form['nbParties'])+1)
    ecart =(round(ecart*100))/100
    absecart=abs(ecart)

    ecartdirect = 100-((correctPrice*100)/PriceEntry)
    ecartdirect =(round(ecartdirect*100))/100
    ecartdirect = abs(ecartdirect)


    return render_template('try.html',
    aName = articleName,
    aImg = articleImg,
    correctPrice = correctPrice,
    priceEntry = PriceEntry,
    ecartdirect=ecartdirect,
    absecart=absecart,
    nbParties=int(request.form['nbParties'])+1,
    timeFin=timeFin,
    )


    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
