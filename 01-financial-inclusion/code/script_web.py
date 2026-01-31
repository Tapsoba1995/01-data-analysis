import pandas as pd
import requests

# Pays UEMOA (ISO3)
pays_uemoa = ['BEN', 'BFA', 'CIV', 'GNB', 'MLI', 'NER', 'SEN', 'TGO']

# Indicateurs WDI reprenant la liste R
indicateurs = {
    'COMPTE': 'FB.CBK.DPTR.P3',                # Adultes possédant un compte (%)
    'CREDIT': 'FB.CBK.BRWR.P3',             # Remplacement FB.CBK.CRED.PC.ZS si indisponible
    'TRANSFERTS_USD': 'NY.TRF.NCTR.CN',    # Transferts reçus (USD)
    'PIB_HABITANT': 'NY.GDP.PCAP.CD',         # PIB par habitant (USD courants)
    'URBAIN': 'SP.URB.TOTL.IN.ZS',            # Population urbaine (%)
    'ALPHAB': 'SE.ADT.LITR.ZS',               # Alphabétisation adultes (%)
    'INTERNET': 'IT.NET.USER.ZS',             # Utilisateurs Internet (%)
    'INFLATION': 'FP.CPI.TOTL.ZG',            # Inflation (%)
    'CHOMAGE': 'SL.UEM.TOTL.ZS',              # Taux de chômage (%)
    'DENSITE_POP': 'EN.POP.DNST',             # Densité population (habitants/km²)
    'EPARGNE': 'NY.GNS.ICTR.ZS',              # Épargne brute (% PIB)
    'INVESTISSEMENT': 'NE.GDI.TOTL.ZS',       # Investissement privé (% PIB)
     'DEPENSES_EDU': 'SE.XPD.TOTL.GB.ZS',    # Optionnel
    'DETTE_PUBLIQUE': 'GC.DOD.TOTL.GD.ZS',    # Dette publique (% PIB)
    #'DEPENDANCE': 'SP.POP.DPND'               # Taux de dépendance (%)
}

print("Récupération des données WDI pour l'UEMOA...")
print("=" * 50)

donnees_completes = []

for nom_indicateur, code_indicateur in indicateurs.items():
    print(f"Téléchargement : {nom_indicateur}...")
    
    url = f"http://api.worldbank.org/v2/country/{';'.join(pays_uemoa)}/indicator/{code_indicateur}"
    params = {
        'format': 'json',
        'date': '2000:2024',
        'per_page': 10000
    }
    
    try:
        reponse = requests.get(url, params=params, timeout=45)
        
        if reponse.status_code == 200:
            donnees = reponse.json()
            
            if len(donnees) > 1 and isinstance(donnees[1], list):
                for item in donnees[1]:
                    if item.get('value') is not None:
                        donnees_completes.append({
                            'PAYS_CODE': item['countryiso3code'],
                            'PAYS_NOM': item['country']['value'],
                            'ANNEE': int(item['date']),
                            'VARIABLE': nom_indicateur,
                            'VALEUR': float(item['value']),
                            'SOURCE': 'WDI'
                        })
                nb = len([d for d in donnees_completes if d['VARIABLE'] == nom_indicateur])
                print(f"  ✓ {nom_indicateur} : {nb} données")
            else:
                print(f"  ✗ {nom_indicateur} : Structure de données incorrecte")
        else:
            print(f"  ✗ {nom_indicateur} : Erreur HTTP {reponse.status_code}")
            
    except Exception as e:
        print(f"  ✗ {nom_indicateur} : Erreur - {str(e)}")

# Création du DataFrame
if donnees_completes:
    df_wdi = pd.DataFrame(donnees_completes)
    
    # Pivot pour avoir une colonne par indicateur
    df_pivot = df_wdi.pivot_table(index=['PAYS_CODE','PAYS_NOM','ANNEE'],
                                  columns='VARIABLE',
                                  values='VALEUR').reset_index()
    
  
    # Sauvegarde CSV et Excel
    
    
    df_pivot.to_csv('UEMOA11.csv', index=False, encoding='utf-8-sig')
    
    df_pivot.to_excel('Bas11e.xlsx', index=False)
    
    print("\n✅ Fichier UEMOA11.csv et Bas11e.xlsx créés avec succès !")
else:
    print("❌ Aucune donnée téléchargée.")
