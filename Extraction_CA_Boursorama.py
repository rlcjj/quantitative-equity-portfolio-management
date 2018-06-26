import requests
from bs4 import BeautifulSoup
import csv

def extract(name,link):

    req = requests.get(link)
    soup = BeautifulSoup(req.text, "lxml")
    
    
    t= soup.find_all('table')
    
    """Chiffre d'affaire = 4e table"""
    table=t[3]
    
    table_rows = table.find_all('tr')
    
    L=[]
    table_head=table_rows[0]
    drg=table_head.find_all('th')
    L=[[i.text for i in drg]]
        
    del table_rows[0]
    for tr in table_rows :
        td=tr.find_all('td')
        row =[i.text for i in td]
        L=L+[row]
        
    """print(L)"""

    c = csv.writer(open(name, "w", newline=""))
    
    data = L
    for l in data :
        c.writerow(l)
  

def extract_all(L):
    n=int(len(L)/2)
    for i in range(n):
        name= L[2*i]
        link= L[2*i+1]
        extract(name,link)
  
L=["accor.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpac",
"air_liquide.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpai",
"airbus.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpair",
"arcelormittal.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1ramt",
"atos.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpato",
"axa.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpcs",
"bnp_Paribas_br-a.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpbnp",
"bouygues.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpen",
"capgemini.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpcap",
"carrefour.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpca",
"credit_agricole_sa.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpaca",
"danone.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpbn",
"engie.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpengi",
"essilor_intl.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpei",
"kering.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpker",
"l'oreal.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpor",
"lafargeholcim_n.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rplhn",
"legrand.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rplr",
"lvmh_moet_vuitton.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpmc",
"michelin_n.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpml",
"orange.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpora",
"pernod_ricard.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpri",
"peugeot.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpug",
"publicis_grp.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rppub",
"renault.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rprno",
"safran.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpsaf",
"saint-gobain.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpsgo",
"sanofi.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpsan",
"schneider_e.se.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpsu",
"societe_generale.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpgle",
"sodexo.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpsw",
"solvay.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=ff11-solb",
"stmicroelectr.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpstm",
"technipfmc.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpfti",
"total.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpfp",
"unibail-rodamco.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1raul",
"valeo.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpfr",
"veolia_environnem..csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpvie",
"vinci.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpdg",
"vivendi.csv",
"http://www.boursorama.com/bourse/profil/profil_finance.phtml?symbole=1rpviv"]


extract_all(L)


        



