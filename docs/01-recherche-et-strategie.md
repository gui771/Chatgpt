# Étapes 1 à 3 — Recherche, évaluation et stratégie recommandée

Date : 10 novembre 2026. Budget : 100 $. Statut global : **recherche faite, rien de construit, rien de dépensé, rien de déployé.**

> **Mise à jour.** Les estimations de revenus Apify de ce document sont remplacées par les mesures de `02-mesure-du-catalogue-apify.md`, nettement moins favorables. L'utilisateur réside en Suisse, non en France. La section sur la publication X décrit le compte en général : une autre analyse indique que le post porte sur un scanner de memecoins Solana, ce que je n'ai pas pu vérifier.

Légende des statuts : **[V]** vérifié sur source primaire ou presse reconnue · **[D]** déclaré par un tiers, non audité · **[E]** estimation de ma part · **[NV]** non vérifié.

## Limites de cette recherche

- Le réseau de cette session bloque la plupart des sites (x.com, apify.com, dev.to, indiehackers.com, API open data). Je n'ai pu lire que des résultats de moteur de recherche, pas les pages elles-mêmes.
- **La publication X fournie n'a pas pu être lue** (voir section dédiée). Je n'en invente pas le contenu.
- Aucun chiffre de revenu ci-dessous n'est audité. Les seules données quasi primaires sont les montants que les plateformes déclarent verser.

## A. Résumé exécutif

1. **L'objectif de 1 000 $ nets par mois avec 100 $ et presque aucune intervention humaine n'est pas le résultat central d'aucun modèle étudié.** C'est un résultat de queue de distribution, atteignable en 9 à 18 mois dans le meilleur modèle, sans garantie.
2. **Tout ce qui est trading est éliminé.** Avec 100 $ de capital, même un rendement exceptionnel de 5 % par mois donne 5 $. Atteindre 1 000 $ par mois exigerait 1 000 % mensuels, ce qui n'existe qu'avec un levier qui détruit le capital.
3. **Le vrai goulot n'est pas la technique mais la distribution.** Les modèles qui exigent de trouver soi-même des clients (SaaS, newsletter, extension) échouent le plus souvent à 0 client. Les modèles viables avec 100 $ sont ceux où une place de marché fournit déjà les acheteurs, la facturation et l'hébergement.
4. **Recommandation : un portefeuille d'« Actors » sur l'Apify Store, facturés à l'usage, choisis par une analyse chiffrée des manques du catalogue.** Coût de lancement proche de 0 $. Attente réaliste : 0 à 300 $ par mois à 6 mois.
5. **Mon idée de niche initiale (données publiques françaises) est déjà saturée** : au moins 8 Actors BODACC et 15 Actors BOAMP/TED existent. La niche doit donc être choisie par les données, pas par intuition. C'est la première chose à construire.

## B. La publication X (dan1ro0)

- **Accès : impossible.** x.com est hors de la liste réseau autorisée, et la recherche n'a pas indexé ce statut précis. **Merci de coller le texte de la publication** si vous voulez une analyse de ce post exact.
- **Ce qui est vérifiable sur le compte [V]** : « Daniro » publie en série des posts du type « ce trader a utilisé Claude pour construire un bot quant et a gagné +127 020 $ sur Polymarket ». Ce sont des portefeuilles de tiers, sur les marchés crypto « Up/Down » de courte durée.
- **Analyse de cette famille d'affirmations** (pas du post lui-même) :

| Point | Constat | Statut |
|---|---|---|
| Preuve de gains | Un portefeuille gagnant existe sans doute, mais il est choisi après coup parmi des millions. Rien ne relie le portefeuille à « un étudiant » ou à « Claude ». | [NV] |
| Base de comparaison | Étude Toronto / HEC Montréal / ESSEC sur 2,4 M d'utilisateurs : 68,8 % perdent, le 1 % supérieur capte 76,5 % des profits. | [V presse] |
| Pertes déclarées | Bloomberg, avril 2026 : plus de 100 000 comptes ont perdu au moins 1 000 $ depuis 2025, près du double des comptes gagnants. | [V presse] |
| Coûts cachés | Frais « taker » ajoutés en janvier 2026 sur ces marchés, jusqu'à environ 3 % près de 50 %. L'avantage d'un bot à 53–56 % de réussite est du même ordre que ces frais. | [V presse] |
| Reproductibilité | Les gagnants sont des teneurs de marché rapides, avec capital et infrastructure à faible latence. Non reproductible avec 100 $. | [E] |
| Légalité | Polymarket est bloqué en France (ANJ, juillet 2026) et restreint dans plus de 30 juridictions. Le contourner viole vos règles. | [V presse] |
| Contre-exemple | Un test publié rapporte environ 140 trades, 13 gagnés et 24 perdus, soldé en perte. | [D] |

**Verdict : à écarter.** Techniquement programmable, économiquement sans avantage démontré pour un petit compte, et probablement illégal selon votre pays.

## C. Tableau comparatif de 21 opportunités

Notation sur 100 : Rentabilité nette (20), Faisabilité avec 100 $ (20), Autonomie (20), Demande réelle (15), Maîtrise du risque (15), Simplicité (10). Toutes les notes sont des jugements **[E]**.

Règle éliminatoire : un modèle dont le plafond de gain avec 100 $ est inférieur à 100 $ par mois est exclu, quelle que soit sa note.

| # | Opportunité | Qui paie | Rent. | Fais. | Auto. | Dem. | Risq. | Simp. | Total | Confiance | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Portefeuille d'Actors Apify facturés à l'usage | Développeurs, équipes data, agents IA | 11 | 19 | 16 | 10 | 13 | 7 | **76** | Moyenne | **Retenu** |
| 2 | API de données sur places de marché (RapidAPI et autres) | Développeurs | 7 | 18 | 16 | 5 | 13 | 7 | **66** | Faible | Top 5 |
| 3 | Micro-SaaS d'alertes B2B de niche par abonnement | PME | 12 | 14 | 12 | 9 | 12 | 5 | **64** | Faible | Top 5, secours |
| 4 | Produits numériques (jeux de données, modèles n8n) | Particuliers, indépendants | 6 | 17 | 14 | 6 | 13 | 8 | **64** | Faible | Top 5 |
| 5 | Extension Chrome freemium | Utilisateurs finaux | 9 | 16 | 13 | 7 | 11 | 6 | **62** | Faible | Top 5 |
| 6 | Serveur MCP payant (x402, paiements d'agents) | Agents IA | 4 | 18 | 16 | 3 | 13 | 7 | 61 | Incertitude élevée | Trop tôt |
| 7 | Newsletter de niche automatisée et sponsorisée | Sponsors | 7 | 16 | 11 | 6 | 13 | 7 | 60 | Faible | Audience lente |
| 8 | Bot Telegram ou Discord d'alertes premium | Particuliers | 5 | 17 | 14 | 5 | 11 | 7 | 59 | Faible | Petit panier |
| 9 | Agence d'automatisation IA pour PME | PME | 14 | 14 | 2 | 10 | 12 | 4 | 56 | Moyenne | Rentable mais manuel |
| 10 | Site SEO programmatique et affiliation | Annonceurs | 7 | 15 | 13 | 5 | 8 | 6 | 54 | Moyenne | Risque Google |
| 11 | Service B2B productisé (rapports automatiques) | PME | 9 | 13 | 9 | 6 | 12 | 5 | 54 | Faible | Acquisition |
| 12 | Livres IA sur Amazon KDP | Lecteurs | 3 | 16 | 10 | 3 | 7 | 7 | 46 | Incertitude élevée | Saturé |
| 13 | Impression à la demande avec visuels IA | Particuliers | 3 | 14 | 10 | 3 | 9 | 6 | 45 | Incertitude élevée | Saturé |
| 14 | Agent de prospection sortante B2B | Clients B2B | 10 | 8 | 6 | 6 | 6 | 4 | 40 | Faible | RGPD, vente manuelle |
| 15 | Chaîne YouTube sans visage générée par IA | Publicité | 5 | 12 | 8 | 5 | 4 | 4 | 38 | Moyenne | Démonétisations 2026 |
| 16 | Trading algorithmique directionnel | Le marché | 2 | 8 | 14 | 3 | 4 | 4 | 35 | Moyenne | Éliminé |
| 17 | Tenue de marché, bots de grille | Le marché | 2 | 6 | 14 | 3 | 4 | 4 | 33 | Moyenne | Éliminé |
| 18 | Bot Polymarket (type publication X) | Autres parieurs | 3 | 6 | 14 | 2 | 2 | 3 | 30 | Moyenne | Éliminé |
| 19 | Arbitrage crypto entre plateformes, MEV | Le marché | 1 | 3 | 14 | 2 | 4 | 2 | 26 | Moyenne | Éliminé |
| 20 | Arbitrage de taux de financement neutre | Traders à levier | 1 | 10 | 15 | 8 | 9 | 5 | 48 | Moyenne | Éliminé (plafond) |
| 21 | Rendement stablecoins ou DeFi | Emprunteurs | 0 | 18 | 19 | 15 | 10 | 9 | 71 | Élevée | Éliminé (plafond) |

Justifications clés :

- **1 (Apify)** : la plateforme déclare verser environ 1,6 à 1,7 M$ par mois à environ 4 500 développeurs [D], soit une moyenne d'environ 375 $ par développeur. La médiane est inconnue et sûrement bien plus basse, car le catalogue compte environ 89 000 Actors [D]. Un seul témoignage chiffré trouvé : 55,82 $ puis 177,98 $ sur les deux premiers mois d'un Actor de niche [D]. Commission : vous gardez 80 % du revenu moins le coût de calcul [D, à confirmer sur les conditions officielles].
- **2 (API)** : même logique, mais aucune donnée de versement trouvée pour RapidAPI, passé chez Nokia fin 2024 [NV].
- **3 (alertes B2B)** : la demande est prouvée par les prix du marché (veille d'appels d'offres de 20 à 299 $ par mois [D]). L'obstacle est l'acquisition, pas le produit.
- **6 (MCP payant)** : un développeur rapporte 0 $ après six semaines ; « 95 % des serveurs MCP ne gagnent rien » circule sans source [NV].
- **9 (agence)** : c'est probablement le moyen le plus sûr de gagner 1 000 $, mais il viole votre contrainte d'intervention minimale.
- **10 (SEO)** : plusieurs sources rapportent 50 à 80 % de trafic perdu par les sites programmatiques pauvres après mars 2026 [D].
- **15 (YouTube)** : 16 chaînes totalisant 35 M d'abonnés fermées en janvier 2026 sous la règle « contenu inauthentique » [D].
- **20 (financement)** : environ 11 % par an au taux BTC courant, soit environ 11 $ par an sur 100 $, avant frais [E].
- **21 (rendement)** : sans risque majeur mais rapporte moins de 1 $ par mois.

## D. Scénarios financiers des cinq meilleures

Tous les montants sont des **estimations [E]**, à 6 mois, en dollars par mois, avant impôts. Aucune probabilité chiffrée : je n'ai pas de données pour en produire.

| Stratégie | Coût initial | Coût mensuel | Pessimiste | Central | Optimiste | Premiers revenus | Point mort | Maintenance |
|---|---|---|---|---|---|---|---|---|
| 1. Actors Apify | 0 $ | 0 à 10 $ | 0 à 20 $ | 50 à 300 $ | 1 000 $ et plus | 2 à 6 semaines | Dès le 1er dollar | 1 à 2 h par semaine |
| 2. API sur places de marché | 0 $ | 0 à 7 $ | 0 $ | 10 à 100 $ | 500 $ | 1 à 3 mois | 1 à 3 mois | 1 h par semaine |
| 3. Alertes B2B par abonnement | 15 $ (domaine) | 10 à 25 $ | −25 $ (0 client) | 0 à 150 $ | 1 000 $ (35 clients à 29 $) | 2 à 4 mois | 1 client | 2 à 4 h par semaine |
| 4. Produits numériques | 0 à 20 $ | 0 à 10 $ | 0 $ | 10 à 80 $ | 400 $ | 1 à 2 mois | 1 à 2 ventes | 1 h par semaine |
| 5. Extension Chrome | 5 $ (frais Google) | 0 à 10 $ | 0 $ | 0 à 100 $ | 1 000 $ et plus | 2 à 4 mois | 1 à 2 ventes | 2 h par semaine |

Conditions de réussite du scénario optimiste Apify : au moins un Actor sur un besoin fréquent et mal servi, un coût de calcul inférieur à 20 % du prix, et aucune rupture de la source de données.

Les 30 premiers jours de la stratégie 1 coûtent au plus 20 $, donc restent financés par les 100 $.

## E. Stratégie retenue (étape 3)

**1. Quel système ?** Une « fabrique d'Actors » en quatre modules :
1. Un analyseur du catalogue Apify qui mesure demande (utilisateurs par Actor) et offre (nombre et qualité des concurrents) pour désigner les niches mal servies.
2. Des Actors construits sur ces niches, en priorité sur des API officielles stables, pour limiter les pannes.
3. Une surveillance quotidienne : test de santé de chaque Actor, marge par exécution, alerte seulement en cas d'anomalie.
4. Un registre des revenus et dépenses avec plafond de dépense bloquant.

**2. Pourquoi supérieure ?** C'est le seul modèle où le coût d'entrée est nul, où les clients arrivent par le catalogue, et où la plateforme héberge, facture et fait tourner le service 24 h/24 ordinateur éteint. Perte maximale : votre temps et quelques dollars.

**3. Qui paie ?** Les utilisateurs d'Apify (développeurs, équipes marketing et data, agents IA via le serveur MCP d'Apify), à chaque résultat produit.

**4. Premiers revenus ?** Dès qu'un utilisateur externe exécute un Actor payant. Apify verse mensuellement.

**5. Acquisition sans travail quotidien ?** Recherche interne du catalogue, référencement Google des pages d'Actor, et découverte par les agents IA. Aucune prospection.

**6. Risques principaux.** Saturation du catalogue, dépendance à une seule plateforme, sources de données qui cassent.

**7. Tâches non automatisables.**
- Création du compte Apify, vérification d'identité, formulaires fiscaux, réception des paiements : vous, une fois, environ 1 à 2 h.
- Statut légal pour facturer (par exemple micro-entreprise en France) et déclarations : vous.
- Réponse aux tickets des utilisateurs et réparation des Actors cassés : environ 1 à 2 h par semaine. Je peux faire les correctifs, mais il faut ouvrir une session.

**8. Délais réalistes [E].**

| Palier net mensuel | Délai | Appréciation |
|---|---|---|
| 100 $ | 2 à 4 mois | Plausible |
| 500 $ | 6 à 12 mois | Incertain, demande un Actor qui « prend » |
| 1 000 $ | 9 à 18 mois | Résultat minoritaire, non garanti |

**9. Validation rapide à 0 $.**

| Étape | Durée | Critère de passage | Sinon |
|---|---|---|---|
| Analyse des manques du catalogue | Jours 1 à 3 | Au moins 5 niches avec demande mesurée et moins de 3 concurrents fiables | Arrêt, passage au secours |
| Publication de 3 Actors | Jours 4 à 14 | Tests verts, publication acceptée | Correction |
| Mesure | Jour 30 | Au moins 10 utilisateurs externes au total | Changer de niches |
| Mesure | Jour 60 | Au moins 20 $ de revenu cumulé | Arrêt ou secours |

Plafond de dépense sur ces 60 jours : 20 $.

**Test de réalité — trois causes d'échec.**

| Cause | Prévention | Indicateur |
|---|---|---|
| Personne ne trouve les Actors | Choisir les niches par la demande mesurée, soigner titre et description | Utilisateurs uniques par Actor à 14 jours |
| Marge négative (calcul plus cher que le prix, abus des comptes gratuits) | Prix par événement calculé sur le coût mesuré, limites par exécution | Marge par exécution, alerte sous 50 % |
| Changement de règles d'Apify ou panne de source | Code portable, API officielles, test de santé quotidien | Taux de succès des exécutions, alerte sous 95 % |

**Stratégie de secours.** Réutiliser les mêmes collecteurs de données pour un service d'alertes B2B par abonnement (opportunité 3), vendu en direct. À n'engager que si un Actor montre une demande répétée d'un même type de client.

## F. Ce que je peux faire, et ce qui dépend de vous

Je peux programmer et tester ici : l'analyseur de catalogue, les Actors, les tests, la surveillance, le registre, les scripts de publication.

Dépend de vous :
1. **Accord sur la stratégie** (validation exigée par l'étape 3).
2. **Autoriser `api.apify.com` et `apify.com`** dans les réglages réseau de l'environnement. Sans cela je ne peux ni analyser le catalogue ni publier.
3. **Créer un compte Apify gratuit** (engagement de compte, donc votre décision) et fournir le jeton par le formulaire sécurisé, jamais dans le chat.
4. **Votre pays de résidence**, pour le cadre fiscal et légal.
5. Facultatif : coller le texte de la publication X.

## Sources

- Compte Dan1ro0 : https://x.com/Dan1ro0 · https://x.com/Dan1ro0/status/2078561762681721079
- Pertes Polymarket : https://www.kucoin.com/news/flash/84-of-polymarket-traders-are-losing-money-0-033-capture-majority-profits · https://www.kucoin.com/news/flash/100-000-polymarket-accounts-lose-over-1000-since-2025 · https://telonex.io/research/top-crypto-traders-polymarket-15m
- Frais Polymarket : https://cointelegraph.com/news/polymarket-quietly-adds-taker-fees-15-minute-crypto-markets · https://www.theblock.co/post/384461/polymarket-adds-taker-fees-to-15-minute-crypto-markets-to-fund-liquidity-rebates
- Blocage en France : https://cryptoslate.com/polymarket-blocked-french-transactions-but-578751-users-later-france-blocked-the-entire-site/ · https://thepaypers.com/crypto-web3-and-cbdc/news/france-blocks-polymarket-over-gambling-law-breaches
- Contre-exemple de bot : https://startupfortune.com/i-actually-gave-an-ai-money-to-trade-on-polymarket-heres-what-nobody-on-twitter-wants-you-to-know/
- Apify, versements et règles : https://affstudio.org/2026/10/23/how-much-can-you-earn-selling-apify-actors/ · https://help.apify.com/en/articles/8684010-make-money-publishing-your-actors-on-apify-store · https://docs.apify.com/platform/actors/publishing/monetize · https://apify.com/challenge
- Témoignage Apify : https://www.indiehackers.com/post/i-charge-5-per-1-000-results-my-niche-apify-actor-tripled-its-revenue-in-month-two-c9e85e2046
- Concurrence données françaises : https://apify.com/parseforge/france-bodacc-gazette-scraper · https://apify.com/tagadanar/french-public-tenders · https://apify.com/dltik/boamp-fr-scraper
- Micro-SaaS : https://dev.to/agenthustler/i-scraped-4500-indiehackers-products-heres-what-the-mrr-data-reveals-18ki · https://techstartups.com/2026/09/28/what-percentage-of-indie-hacker-products-make-100k-in-arr/
- Veille d'appels d'offres, prix : https://govcontractfinder.com/tools/government-contracting-software-pricing-guide
- MCP payant : https://dev.to/kirothebot/the-state-of-mcp-monetization-in-2026-where-builders-actually-get-paid-34k9
- SEO programmatique : https://www.searchenginejournal.com/scaled-ai-content-often-fails-googles-crawl-economics-explain-why/ · https://alexcloudstar.com/blog/programmatic-seo-2026-indie-hackers/
- YouTube : https://thenextweb.com/news/youtube-ai-slop-crackdown-faceless-creators-collateral-damage
- Taux de financement : https://www.kucoin.com/blog/how-to-earn-passive-income-in-a-bear-market-funding-rate-arbitrage-explained
