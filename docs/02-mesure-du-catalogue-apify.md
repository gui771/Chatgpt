# Mesure du catalogue Apify — test de la stratégie retenue

Date : 10 novembre 2026. Dépense : 0 $. Aucun compte créé, rien de publié.

## Conclusion

**Les données contredisent mon scénario central.** J'annonçais 50 à 300 $ par mois à 6 mois pour un portefeuille d'Actors. La mesure du catalogue situe l'auteur médian autour de 11 $ par mois, et 1 000 $ par mois autour des 4 à 5 % d'auteurs les mieux placés. La partie du marché compatible avec vos règles (pas de contournement des conditions d'utilisation) est la plus encombrée et la moins demandée.

## Ce qui a été mesuré

- Source : API publique du catalogue Apify, sans compte ni jeton.
- Couverture : 87 717 Actors enregistrés sur environ 116 000 annoncés par l'API (76 %). L'API ne renvoie rien au-delà du 15 000e résultat d'une requête ; le catalogue a donc été parcouru par tri et par catégorie. Les Actors manquants sont surtout peu utilisés.
- Périmètre des chiffres : 87 600 Actors de la communauté, 4 640 auteurs, hors compte officiel `apify`.
- « Utilisateurs » : utilisateurs uniques sur 30 jours par Actor, comptes gratuits compris.

## Résultats [mesurés]

| Constat | Valeur |
|---|---|
| Actors avec au plus 1 utilisateur sur 30 jours | 72,8 % |
| Actors avec au plus 10 utilisateurs | 94,0 % |
| Actors avec au plus 50 utilisateurs | 98,2 % |
| Part de l'usage captée par le 1 % d'Actors les plus utilisés | 72,4 % |
| Part de l'usage captée par les 10 % les plus utilisés | 90,1 % |
| Auteur médian, tous ses Actors cumulés | 6 utilisateurs par mois |
| Auteur au 75e centile | 25 |
| Auteur au 90e centile | 136 |
| Auteur au 95e centile | 456 |
| Part de l'usage sur les grandes plateformes (réseaux sociaux, LinkedIn, Google, Amazon…) | 75,7 % |

Un Actor à 1 utilisateur est le plus souvent utilisé par son seul auteur.

## Traduction en revenus [estimation grossière]

Apify déclare verser environ 1,7 M$ par mois aux développeurs (source secondaire, non auditée). Divisé par l'usage mesuré, cela donne environ **1,9 $ par utilisateur et par mois**. Cette moyenne masque de très grands écarts, et l'échantillon à 76 % la surestime un peu.

| Objectif mensuel | Utilisateurs nécessaires | Auteurs qui y sont | Part des auteurs |
|---|---|---|---|
| 100 $ | environ 52 | 767 | 16,5 % |
| 500 $ | environ 262 | 307 | 6,6 % |
| 1 000 $ | environ 524 | 208 | 4,5 % |

Auteur médian : environ 11 $ par mois. 75e centile : environ 48 $. 90e centile : environ 260 $.

## Pourquoi votre cas est plus difficile que la moyenne

- **Les données ouvertes sont saturées.** C'était le segment que je visais, parce qu'il est légal et stable. Exemples : 798 Actors sur les dépôts SEC pour un leader à 18 utilisateurs ; 265 sur la FDA pour un leader à 3 ; 146 sur les appels d'offres TED pour un leader à 22.
- **La demande est ailleurs.** Trois quarts de l'usage portent sur des plateformes qui interdisent ou combattent la collecte automatisée. Y aller contredit votre règle 8 et demande des proxys payants et une maintenance constante.
- **Le premier arrivé garde tout.** Sur les cibles de niche, un seul Actor concentre l'usage et des dizaines de copies restent à 1 utilisateur.
- **Presque aucune place à reprendre.** Un seul Actor hors grandes plateformes est à la fois très utilisé (277 utilisateurs) et défaillant (29 % d'échecs) : un comparateur de prix d'une enseigne australienne.

## Ce que cela ne dit pas

- Les revenus réels par Actor ne sont pas publics ; le chiffre de 1,9 $ est un ordre de grandeur.
- Le catalogue ne montre que la demande déjà servie. Une cible sans aucun Actor mais avec des clients potentiels y est invisible.
- La liste des « grandes plateformes » est indicative et n'a pas de valeur juridique.

## Reproduire

```
python3 -m engine.catalog data/catalog.jsonl   # environ 10 minutes
python3 -m engine.gaps data/catalog.jsonl      # rapport JSON
python3 -m unittest discover -s tests          # 19 tests
```

Statuts : téléchargement et analyse **exécutés** sur les données réelles ; tests **passés** (19 sur 19) ; reprises réseau de `http_get_json` **non testées** automatiquement.
