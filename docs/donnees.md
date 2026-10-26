# Données

Jeu de données du challenge Rakuten France Multimodal Product Data Classification.
Chaque produit est décrit par un titre (`designation`), une description libre et une
photo. La cible est le `prdtypecode`, soit 27 catégories.

Les fichiers ne sont pas versionnés et doivent être déposés dans `data/raw_csv/` avant le
premier run du pipeline.

| Fichier attendu | Contenu |
|---|---|
| `X_train_update.csv` | `designation`, `description`, `productid`, `imageid` |
| `Y_train_CVw08PX.csv` | `prdtypecode`, la cible |
| `X_test_update.csv` | jeu de test du challenge, sans label |

Le dossier `data/` est monté sur `/data` dans tous les conteneurs. Le DAG d'entraînement
lit `/data/raw_csv` et écrit ses sorties dans `/data/processed` :
`X_train_split.csv`, `X_val_split.csv` et `X_test.csv`.

Le split train / validation est de 80/20, stratifié sur la cible encodée, avec
`random_state=42`. Le `X_test` du challenge n'étant pas labellisé, il sert uniquement à
produire des prédictions, pas à mesurer une performance.

## Nettoyage du texte

Le même traitement est appliqué à l'entraînement
(`plugins/src/data_preprocessing/text_cleaning.py`) et à l'inférence
(`rakuten_api/app/cleaning/text_cleaning.py`), ce qui évite tout écart entre les deux :

1. fusion de `designation` et `description` ;
2. suppression des tokens dupliqués ;
3. passage en minuscules, suppression des accents et des balises HTML ;
4. filtrage des caractères non alphabétiques ;
5. retrait des stopwords français, anglais et allemands, complétés par une liste de mots
   vides spécifique au corpus (`plus`, `peut`, `tout`, `comme`, entités HTML résiduelles
   comme `eacute` ou `nbsp`) ;
6. suppression des mots de moins de 3 caractères.

## Les 27 catégories

Les codes produits sont ré-encodés en labels `0` à `26` par ordre croissant de code. Le
mapping est conservé pour l'inférence : l'API renvoie le `prdtypecode` d'origine, pas le
label encodé.

| Label | Code | Catégorie |
|---|---|---|
| 0 | 10 | Adult Books |
| 1 | 40 | Imported Video Games |
| 2 | 50 | Video Games Accessories |
| 3 | 60 | Games and Consoles |
| 4 | 1140 | Figurines and Toy Pop |
| 5 | 1160 | Playing Cards |
| 6 | 1180 | Figurines, Masks, Role-Playing Games |
| 7 | 1280 | Toys for Children |
| 8 | 1281 | Board Games |
| 9 | 1300 | Remote Controlled Models |
| 10 | 1301 | Accessories for Children |
| 11 | 1302 | Toys, Outdoor Playing and Clothes |
| 12 | 1320 | Early Childhood |
| 13 | 1560 | Interior Furniture and Bedding |
| 14 | 1920 | Interior Accessories |
| 15 | 1940 | Food |
| 16 | 2060 | Decoration Interior |
| 17 | 2220 | Supplies for Domestic Animals |
| 18 | 2280 | Magazines |
| 19 | 2403 | Children Books and Magazines |
| 20 | 2462 | Games |
| 21 | 2522 | Stationery |
| 22 | 2582 | Furniture, Kitchen and Garden |
| 23 | 2583 | Piscine and Spa |
| 24 | 2585 | Gardening and DIY |
| 25 | 2705 | Books |
| 26 | 2905 | Online Distribution of Video Games |

Le catalogue est déséquilibré : des poids de classes `balanced` sont calculés à
l'entraînement pour compenser.
