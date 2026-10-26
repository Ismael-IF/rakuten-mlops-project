# API de prédiction

Application FastAPI servie par Uvicorn, avec une base utilisateurs MongoDB.
Documentation interactive générée automatiquement sur `http://localhost:8000/docs`.

## Authentification

1. `POST /Users/register_user` crée un compte.
2. `POST /token` échange les identifiants contre un JWT (`access_token`), dont la durée
   de vie est définie par `ACCESS_TOKEN_EXPIRE_MINUTES`.
3. Les appels suivants portent l'en-tête `Authorization: Bearer <token>`. Un middleware
   accepte également le schéma Basic.

Les comptes, leurs rôles et la date de dernière connexion sont stockés dans MongoDB. Les
mots de passe sont hachés avec bcrypt via `passlib`.

## Routes de prédiction

Toutes ces routes exigent un utilisateur authentifié.

| Méthode | Route | Entrée | Modèles mobilisés |
|---|---|---|---|
| POST | `/predict_with_text_Conv1D` | `designation` (requis), `description` (optionnel) | Conv1D |
| POST | `/predict_with_text_SimpleDN` | `designation` (requis), `description` (optionnel) | Simple DNN |
| POST | `/predict_with_image_Xception` | `image_file` | Xception |
| POST | `/predict_with_image_Inception` | `image_file` | InceptionV3 |
| POST | `/predict_with_text_and_image_Conv1D_SimpleDNN_Xception` | texte et `image_file` | Conv1D, Simple DNN, Xception |
| POST | `/predict_with_text_and_image_Conv1D_SimpleDNN_Inception` | texte et `image_file` | Conv1D, Simple DNN, InceptionV3 |

Le texte reçoit exactement le même nettoyage qu'à l'entraînement avant tokenisation. Les
images sont redimensionnées en 299 x 299 et normalisées. Le type MIME du fichier est
vérifié : une entrée non image renvoie un code 400.

## Format de réponse

| Champ | Contenu |
|---|---|
| `predicted_class` | le `prdtypecode` prédit, par exemple `2583` |
| `predicted_label` | le libellé de la catégorie correspondante |
| `precision` | chaîne de caractères, probabilité maximale de la distribution softmax exprimée en pourcentage, par exemple `"87.34%"`. Il s'agit d'un score de confiance sur la prédiction, et non de la métrique de précision calculée sur un jeu de test |

Les routes bimodales renvoient en plus le détail de chaque sous-modèle
(`..._text_Model1`, `..._text_Model2`, `..._image_model`), ce qui rend la décision finale
auditable : on voit sur quel modèle la fusion s'est appuyée.

## Fusion bimodale

La prédiction bimodale est une moyenne des distributions de probabilités des trois
modèles, pondérée par les scores de référence déclarés dans
`rakuten_api/app/config/inputs.py` et normalisée par la somme de ces poids :

| Modèle | Poids |
|---|---|
| Conv1D (texte) | 0.80 |
| Simple DNN (texte) | 0.81 |
| Xception (image) | 0.66 |
| InceptionV3 (image) | 0.64 |

La classe retenue est l'argmax de la distribution fusionnée. Le texte pèse donc plus que
l'image, ce qui reflète les performances respectives observées en phase de modélisation.

## Gestion des utilisateurs

| Méthode | Route | Portée |
|---|---|---|
| GET | `/` | public, vérification de disponibilité |
| POST | `/token` | public, obtention du JWT |
| POST | `/Users/register_user` | public |
| GET | `/Users/Me` | utilisateur authentifié |
| PUT | `/Users/update_user/{user_email}` | utilisateur authentifié |
| PUT | `/Users/deactivate_user/{user_email}` | utilisateur authentifié |
| POST | `/Admin/add_user` | administrateur |
| GET | `/Admin/current` | administrateur |
| GET | `/Admin/list_users/` | administrateur |
| PUT | `/Admin/update_user/{user_email}` | administrateur |
| DELETE | `/Admin/delete_user/{user_email}` | administrateur |

## Exemple d'appel

```bash
# 1. Obtenir un jeton
curl -X POST http://localhost:8000/token \
  -d "username=mon.email@example.com&password=mon_mot_de_passe"

# 2. Classer un produit à partir de son texte
curl -X POST http://localhost:8000/predict_with_text_Conv1D \
  -H "Authorization: Bearer <access_token>" \
  -F "designation=Coffret 4 manettes sans fil" \
  -F "description=Compatible console de salon, batterie rechargeable"
```

Des images produits d'exemple sont disponibles dans
`rakuten_api/prediction_image/image_samples/` pour tester les routes image et bimodales.

## Images de test

Trois images Docker dédiées contiennent des scripts exécutables en conteneurs isolés,
pour valider le comportement de l'API au plus près des conditions de production :

| Image | Périmètre |
|---|---|
| `authentication_image` | création de compte, obtention et validité du jeton |
| `authorization_image` | contrôle des droits sur les routes utilisateur et administrateur |
| `prediction_image` | appels aux routes de prédiction avec les images d'exemple |

## Chargement des modèles

`rakuten_api/app/config/inputs.py` déclare les chemins et noms de fichiers attendus dans
`app/models/trained_models/` et `app/models/tokenizer/`. Les modèles sont chargés en
cache (`functools.lru_cache`) au premier appel de chaque route, ce qui évite de recharger
TensorFlow à chaque requête mais allonge la première réponse après le démarrage du
conteneur. Voir [perimetre.md](perimetre.md) pour les fichiers de modèles absents du
dépôt.
