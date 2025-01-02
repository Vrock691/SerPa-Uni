# Introduction

Ce rapport a pour objectif de présenter les finalités de l'algorithme, d’en détailler son développement et d’en analyser les éventuelles forces et faibless avant de conclure par les possibles améliorations.

**Important :** Il était strictement interdit d'utiliser les différentes techniques de *machine learning* ou de réseau de neurones convolutifs.

*Dans le rapport à suivre, SerPa sera nommé entant que "Application", "Algorithme" ou "Programme".*

## Partie 1 : Les Applications et Usages

Le programme SerPa, également connu sous le nom de Searchin Pattern, est conçu pour exceller dans la reconnaissance de motifs spécifiques au sein d’images variées. Chaque pattern est associé à un nombre binaire à 4 bits. Ce codage repose sur un carré central, divisé en quatre sous-carrés. Chacun de ces sous-carrés est soit noir (représentant un bit de valeur 1) soit blanc (représentant un bit de valeur 0). La lecture s'effectue dans l'ordre suivant : haut gauche -> haut droite -> bas gauche -> bas droit. Dans sa version actuelle, SerPa est capable d’identifier jusqu’à 16 motifs différents sur des supports visuels divers, tels que des panneaux publicitaires, des affiches, des gobelets, etc.

L’intérêt principal de ce programme réside dans ses applications variées et innovantes :

- **Reconnaissance de motifs pour un accès VIP** : SerPa peut être utilisé dans des environnements événementiels pour détecter des motifs exclusifs. Par exemple, des motifs spécifiques pourraient servir de clé d’entrée pour des espaces réservés aux VIP, simplifiant l’accès tout en garantissant une confidentialité élevée.

- **Communication codée grâce à un système binaire** : Le programme est également capable de lire un code à 16 chiffres, construit à partir d'un format binaire (chaque case pouvant être noire ou blanche). Cette fonctionnalité permet d'utiliser SerPa comme outil pour échanger des messages cryptés ou sécurisés dans des environnements nécessitant une confidentialité élevée.

- **Événements et jeux immersifs** : Dans le cadre de chasses au trésor ou d’escape games, SerPa peut être utilisé pour scanner des motifs sur des objets ou des indices disséminés dans l’environnement. Cela ajoute une dimension interactive au jeu, permettant aux participants de progresser en décodant des motifs spécifiques.

***Remarque** : Le dernier exemple ne peut pas être utilisé actuellement, car SerPa ne contient aucune redirection vers un site externe. Bien que cette fonctionnalité ne soit pas complexe à implémenter, elle n’est pas encore en place.*

## Partie 2 : La Création

### Conception
Dès les premières étapes de la conception du programme, nous avons opté pour le framework Streamlit. Ce choix stratégique nous a permis de créer une interface utilisateur interactive et conviviale, sans dépendre d'un terminal. En hébergeant l’application sur une plateforme web, nous avons pu intégrer divers éléments d’interface tels qu’une dropzone pour le dépôt de fichiers, un titre descriptif, ainsi que des textes explicatifs pour guider l’utilisateur.

### Bibliothèques utilisées
Conformément aux consignes, nous avons exploité plusieurs bibliothèques pour répondre aux exigences du projet :

- **OpenCV** : Cette bibliothèque a été le cœur du traitement d’images. Elle nous a permis d’implémenter des algorithmes avancés comme SIFT et ORB pour diverses opérations, notamment :
    - Conversion des images en niveaux de gris.
    - Lecture et traitement des fichiers d'image.
    - Mise en place d’un système de correspondance des caractéristiques.

En complément, nous avons utilisé des bibliothèques supplémentaires pour enrichir les fonctionnalités :

- **NumPy** : Cette bibliothèque a été essentielle pour représenter les images sous forme de tableaux numériques. Elle a simplifié des tâches comme l’extraction des pixels et la délimitation de la région d'intérêt (*Region of Interest*, ROI). Cette délimitation permet à l’utilisateur de restreindre la zone de recherche d’un motif. Bien qu’imparfaite, cette approche s'est avérée rapide et adaptée au contexte.

- **PIL** : Grâce à cette bibliothèque, nous avons pu lire et manipuler directement, au sein du programme, les images traitées via Streamlit, garantissant une intégration fluide avec l’interface utilisateur.

### Structuration et Organisation
Afin d’optimiser la clarté et la maintenabilité du code, nous avons décidé de séparer les fonctions auxiliaires du fichier principal. Cette démarche a permis de réduire la taille du fichier principal tout en améliorant la lisibilité et la modularité du programme.

### Approche algorithmique
Pour l’analyse et la correspondance des motifs, nous avons principalement utilisé SIFT. Initialement, nous avions également testé ORB, mais les résultats se sont avérés décevants en raison de la sensibilité d’ORB aux déformations géométriques complexes et aux variations de perspective, ce qui a conduit à un taux de réussite insuffisant.

Dans une tentative d'amélioration, nous avons exploré une combinaison des algorithmes SIFT et ORB afin de profiter des points forts de chacun :

- **ORB** : Rapide, peu gourmand en ressources et robuste face aux variations d’éclairage.
- **SIFT** : Plus coûteux en termes de calcul, mais capable de gérer efficacement les transformations complexes, telles que les rotations, les changements d’échelle et les déformations.

Cependant, cette combinaison n’a pas produit d'amélioration notable des performances (*voir les sections détaillées sur les échecs*).

Pour surmonter ces limitations, nous avons repensé l'algorithme en adoptant une approche innovante. Tout d'abord, nous utilisons la détection de cercles disponible dans la bibliothèque OpenCV pour localiser les trois cercles noirs et le cercle blanc qui encadrent le motif à scanner. Pour ce faire, nous divisons la zone d'intérêt en quatre quadrants et enregistrons leurs coordonnées afin d’aplanir l’image à l’aide d’une transformation de perspective (warp) et ainsi rapprocher les motifs scannés de leur représentation idéale. Si aucun cercle n’est détecté ou si la détection est incomplète, cette fonction n’est pas exécutée pour éviter tout étirement destructeur.

Ensuite, les quatre parties de la zone d’intérêt sont soumises à une détection de contours pour identifier les éventuels carrés blancs ou noirs. Si les rectangles ne peuvent pas être détectés correctement, l’algorithme repasse la main à SIFT pour effectuer une reconnaissance basée sur les motifs enregistrés.

Bien que cette méthode soit plus complexe et coûteuse en termes de calcul, elle s’est avérée significativement plus efficace sur une partie du jeu de données et a permis une amélioration notable du taux de réussite global.

## Partie 3 : Les Réussites et Les Echecs

### L'Analyse des performances actuelles :

De manière générale, et sur la base des images testées, notre application atteint un taux de réussite de **49.03%**.

D'une part, bien que ce résultat reste mitigé, il reste néanmoins convenable dans certains cas spécifiques. En effet, notre algorithme excelle particulièrement dans les situations où :

- Le motif recherché se trouve sur un fond blanc uni, permettant une reconnaissance visuelle claire et sans ambiguïté.
- Le motif n'est pas sujet à des distorsions majeures. Il est capable de tolérer certaines déformations mineures sans altérer la détection (*comme observé avec l'image MEA-5-4G*).

Vous retrouverez, ci-dessous, la liste des images où SerPa a reussi à détecter un pattern

| Nom de l'Image           | Avec Recadrage | Sans Recadrage | Via Sift | Via Chiffres |
|:-------------------------|:--------------:|:--------------:|:--------:|:------------:|
| 3-3                      |                | X              | X        |              |
| 4-3                      |                | X              | X        |              |
| 1-3                      | X              |                | X        |              |
| 2-3                      | X              |                | X        |              |
| B-2-autre                |                | X              |          | X            |
| B-2                      | X              |                |          | X            |
| R-2                      | X              |                |          | X            |
| T-2                      | X              |                |          | X            |
| L-2                      |                | X              |          | X            |
| 4-4                      | X              |                |          | X            |
| 4-1                      | X              |                |          | X            |
| 2-2                      |                | X              |          | X            |
| 2-1                      |                | X              |          | X            |
| Patern2_MiseEnAbime      |                | X              |          | X            |
| Produit-1                | X              |                |          | X            |
| MEA-6-3G                 | X              |                |          | X            |
| MEA-8-3G                 |                | X              |          | X            |
| MEA-5-3G                 | X              |                |          | X            |
| MEA-4-3G                 | X              |                |          | X            |
| MEA-3-3G                 |                | X              |          | X            |
| MEA-14-4G                | X              | X              | X        | X            |
| MEA-7-4G                 | X              |                | X        | X            |
| MEA-6-4G                 | X              |                |          | X            |
| MEA-5-4G                 |                | X              |          | X            |
| MEA-4-4G                 |                | X              |          | X            |

Cela démontre que notre solution fonctionne de manière satisfaisante dans un environnement relativement contrôlé. Cependant, ses performances se dégradent rapidement lorsque ces conditions idéales ne sont plus respectées.

Par ailleurs, les données révèlent une faiblesse notable : dans **50,98 %** des cas, soit environ une fois sur deux, l'algorithme échoue à identifier correctement le motif au sein des images. Bien que ce taux d'échec soit significatif, il reste dans des limites que nous pouvons qualifier d'acceptables pour envisager une application opérationnelle. Néanmoins, pour garantir une efficacité optimale dans des scénarios diversifiés ou en conditions réelles, des améliorations devront être apportées à l'algorithme afin de réduire cette marge d'erreur.

### Points encourageants malgré tout :

Cependant, un point positif mérite d'être souligné : l'application fait preuve d'une grande fiabilité dans la gestion des images qui ne contiennent pas le motif recherché. En effet, elle parvient à éviter les correspondances erronées ou les "faux positifs" dans la majorité des cas, ce qui est un atout majeur pour garantir l'intégrité des résultats. Cela montre que, même si la reconnaissance des motifs reste un défi dans de nombreuses configurations, le système est capable de filtrer efficacement les cas invalides.

## Partie 4 : Les Améliorations Possibles

Pour améliorer les performances globales de SerPa, plusieurs axes d’amélioration méritent d’être explorés :

- **Optimisation des paramètres algorithmiques** : L’ajustement des paramètres de l’algorithme actuel pourrait permettre une meilleure gestion des motifs déformés, des arrière-plans complexes ou des variations d’éclairage, qui restent des défis majeurs pour l’efficacité de SerPa.
- **Amélioration des motifs existants** : Les motifs actuels présentent certaines limites, notamment les ronds, qui facilitent la correspondance mais sont également une source fréquente d’erreurs. Une optimisation du design des motifs pourrait réduire ces ambiguïtés et améliorer la fiabilité des détections.
- **Augmentation de la bibliothèque de motifs** : Actuellement limitée à 16 motifs, la bibliothèque restreinte explique en partie les difficultés rencontrées dans certaines situations. L’élargissement de cette bibliothèque, avec des motifs mieux adaptés et diversifiés, offrirait une plus grande flexibilité et des résultats plus convaincants.
- **Élargissement de la base de tests** : Tester l’algorithme sur un éventail plus large de situations permettrait de mieux identifier ses failles et d’y remédier. En affinant l’algorithme à partir d’images variées et complexes, nous pourrions améliorer sa robustesse face à des conditions moins idéales.

En somme, bien que les performances actuelles de SerPa soient encore en deçà des attentes dans des situations variées, les résultats encourageants obtenus dans des configurations spécifiques, ainsi que l’absence de faux positifs, constituent une base solide. Grâce à ces pistes d’amélioration, l’application pourrait évoluer significativement et répondre à des besoins plus larges avec une efficacité accrue.

## Partie 5 : Annexe
- Cloud Streamlit : [serpa-uni.streamlit.app](https://serpa-uni.streamlit.app/)
- Repository Github : [Vrock691/SerPa-Uni](https://github.com/Vrock691/SerPa-Uni)