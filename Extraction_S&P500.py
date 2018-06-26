import requests
from bs4 import BeautifulSoup
import csv

#Récupère les liens à partir du csv components
def getLinks() :
    path = 'sp500_constituents.csv'
    with open(path, 'r') as csvfile:
        spamreader = csv.reader(csvfile)
        K=list(spamreader)
    
    L,N=[],[]
    n=len(K)
    link = 'https://www.reuters.com/finance/stocks/financial-highlights/'
    
    for i in range(1,n) :
        name = K[i][0]
        L+=[link + name+'.N']
        N+=[name]
    
    return (L,N)


def extract(name,link):

    req = requests.get(link)
    soup = BeautifulSoup(req.text, "lxml")
    
    ta= soup.find_all('table')
    # Future liste des en-tetes
    L=[]
    # Future liste des valeurs
    R=[]
    # Une entreprise = 2 lignes : Une ligne de noms et une ligne de valeurs (On ne peut pas faire une seule ligne de noms pour toutes les entreprises à cause du pb dont j'avais parlé)
    L0=[]
    R0=[]
    
    #Table 0 à traiter indépendament car de structure différente
    #Celle-ci sera placée dans les derniere colonne pour mettre les données homogènes en premier
    table0=ta[0]
    table_rows = table0.find_all('tr') 
    A=''
    for tr in table_rows :
        th=tr.find_all('th')
        td=tr.find_all('td')
        row=[]
        if len(th) !=0 :
            rowH=[i.get_text(strip=True) for i in th]
 
        if len(td) !=0 :
            row =[i.get_text(strip=True) for i in td]
            
        if len(row) == 4 :
            A=row[0]
            B=row[1]
            res=['Revenue ('+ A + ' - ' + B +')','Earnings per share ('+ A + ' - ' + B+')']
            L0=L0+res
            R0=R0+[row[2],row[3]]
                    
        if len(row) ==3 :
            B=row[0]
            res=['Revenue : '+ A + ' / ' + B ,'Earnings per share : '+ A + ' / ' + B]
            L0=L0+res
            R0=R0+[row[1],row[2]]

    
    #table 1 à traiter séparément car de structure différente
    
    table1=ta[1]
    table_rows = table1.find_all('tr') 
    title=''
    rowH=[]
    for tr in table_rows :
        th=tr.find_all('th')
        td=tr.find_all('td')
        row=[]
        if len(th) !=0 :
            rowH=[i.get_text(strip=True) for i in th]
 
        if len(td) !=0 :
            if len(td)!=1:
                row =[i.get_text(strip=True) for i in td]
            else :
                row =[i.get_text(strip=True) for i in td]
                title =  row[0]
        if len(td) == 6 :    
            res = [title + ' /  ' + row[0] + ' / ' +rowH[i]  for i in range(1,len(rowH))]
            L=L+res
            R=R+row[1:]

    #Dernière table à traiter séparément
    
    tableq = ta[-1]
    table_rows = tableq.find_all('tr') 
    resq=[]
    lq=[]
    for tr in table_rows :
        td=tr.find_all('td')

        rowq =[i.text.strip() for i in td]
        lq+=[rowq[0]]
        resq+=[rowq[1]]

    #On supprime les tables qu'on a déja traité     
    del ta[-1]
    del ta[0]
    del ta[0]
    
    #Autres tables
    for t in ta :
        table_rows = t.find_all('tr') 
        for tr in table_rows :
            th=tr.find_all('th')
            td=tr.find_all('td')
            if len(th) !=0 :
                rowH=[i.get_text(strip=True) for i in th]
                
            if len(td) !=0 :
                row =[i.get_text(strip=True) for i in td]
                if len(td)!=1 :
                    l=[]
                    for i in range(1,len(rowH)) :
                        l=l+[row[0] + ' (' +rowH[i]+')']
                    res = row[1:]
        
                    L=L+l
                    R=R+res
                    
    #Ajout de la derniere table                
    L+=lq
    R+=resq  
    #Ajout de la premiere table  
    L+=L0
    R+=R0
    #Ahout de la colonne avec les noms
    L= ["Nom de l'entreprise"] +L  
    R=[name]+R
    E= L,R 
    return E

#extraction qui ne conserve qu'une ligne d'en-tête, ce qui biaise un peu les données au niveau du premier tableau (uniquement)
#A l'avantage d'etre plus lisible
def extract_all_oneHeadOnly()  :
    V1=[]
    V2=[]
    L,N= getLinks()
    n=len(L)
    flag=0
    Error=[]

    for i in range(10):
        print("Ecriture de ",N[i],'|| progression : ',i,'/',n)
        #Toutes les cotes des entreprise ne sont en XXX.N mais parfois en XXX.OQ : si on ne récupere rien avec le premier lien, on teste avec le second
#        try :
        try :
            EL,ER=extract(N[i],L[i])
            if flag == 0 :
                V1=V1 +[EL,ER]
                flag=1
            else :
                V1=V1+ [ER]
            print('done : Entreprise de catégorie 1')
        except :
            L[i]=(L[i]).replace(N[i]+'.N',N[i]+'.OQ')
            EL,ER=extract(N[i],L[i])
            if flag == 0 :
                V1=V1 +[EL,ER]
                flag=1
            else :
                V1=V1+ [ER]
            print('done : Entreprise de catégorie 2')
#        except :
#            print("Impossible de traiter l'entreprise n° ",i)
#            Error+=[i]
    return V1

#Renvoie les valeurs et les en-tetes pour chaque entreprise
#Dense et dur a lire mais précis
def extract_all_allHeads():
    V=[]
    L,N= getLinks()
    n=len(L)
    
    for i in range(n):
        print("Ecriture de ",N[i],'|| progression : ',i,'/',n)
        #Toutes les cotes des entreprise ne sont en XXX.N mais parfois en XXX.OQ : si on ne récupere rien avec le premier lien, on teste avec le second
        try :
            EL,ER=extract(N[i],L[i])
            V=V+ [EL,ER]
            print('done : Entreprise de catégorie 1')
        except :
            L[i]=(L[i]).replace(N[i]+'.N',N[i]+'.OQ')
            EL,ER=extract(N[i],L[i])
            V=V +[EL,ER]
            print('done : Entreprise de catégorie 2')
    return V



data_oneHead = extract_all_oneHeadOnly()
#data_allHeads = extract_all_allHeads()

c_one = csv.writer(open("data_one.csv", "w", newline=""),delimiter=',')
#c_all = csv.writer(open("data_all.csv", "w", newline=""),delimiter=',')

for l in data_oneHead :
    c_one.writerow(l)
    
#for l in data_allHeads :
#    c_all.writerow(l)



