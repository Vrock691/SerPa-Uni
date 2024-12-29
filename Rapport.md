# Introduction

Ce rapport a pour objectif de présenter les finalités de l'algorithme, d’en détailler son développement et d’en analyser les éventuelles forces et faibless avant de conclure par les possibles améliorations.

**Important :** Il était strictement interdit d'utiliser les différentes techniques de *machine learning* ou de réseau de neurones convolutifs.

*Dans le rapport à suivre, SerPa sera nommé entant que "Application", "Algorithme" ou "Programme".*

## Partie 1 : Les Applications et Usages

Le programme SerPa, également connu sous le nom de Searchin Pattern, est conçu pour exceller dans la reconnaissance de motifs spécifiques au sein d’images variées. Dans sa version actuelle, SerPa est capable d’identifier jusqu’à 16 motifs différents sur des supports visuels divers, tels que des panneaux publicitaires, des affiches, des gobelets, etc.

L’intérêt principal de ce programme réside dans ses applications variées et innovantes :

- **Reconnaissance de motifs pour un accès VIP** : SerPa peut être utilisé dans des environnements événementiels pour détecter des motifs exclusifs. Par exemple, des motifs spécifiques pourraient servir de clé d’entrée pour des espaces réservés aux VIP, simplifiant l’accès tout en garantissant une confidentialité élevée.

- **Communication codée grâce à un système binaire** : Le programme est également capable de lire un code à 16 chiffres, construit à partir d'un format binaire (chaque case pouvant être noire ou blanche). Cette fonctionnalité permet d'utiliser SerPa comme outil pour échanger des messages cryptés ou sécurisés dans des environnements nécessitant une confidentialité élevée.

- **Événements et jeux immersifs** : Dans le cadre de chasses au trésor ou d’escape games, SerPa peut être utilisé pour scanner des motifs sur des objets ou des indices disséminés dans l’environnement. Cela ajoute une dimension interactive au jeu, permettant aux participants de progresser en décodant des motifs spécifiques.

***Remarque** : Le dernier exemple ne peut pas être utilisé actuellement, car SerPa ne contient aucune redirection vers un site externe. Bien que cette fonctionnalité ne soit pas complexe à implémenter, elle n’est pas encore en place.*

## Partie 2 : La Création

Dès les premières étapes de la conception du programme, nous avons choisi d’utiliser le framework Streamlit. Ce framework nous a permis d’augmenter l’interactivité entre l’utilisateur et le programme sans avoir à recourir au terminal, en hébergeant l’application sur un site et en intégrant divers éléments d'interface tels que la dropzone, le titre du programme, ainsi que des textes explicatifs.

De plus, en conformité avec les consignes, nous avons utilisé la bibliothèque suivante :

- **OpenCV** : Cette bibliothèque nous a permis d'exploiter plusieurs algorithmes, notamment SIFT et ORB, afin de réaliser un traitement avancé et complet des images (*Conversion des images en teintes de gris, Lire les images, Mettre en place un système de match, etc.*).

Ainsi que quelques bibliothèques suplémentaires :

- **NumPy** : Elle a facilité la représentation des images sous forme de tableaux numériques, ce qui a simplifié leur manipulation, l’extraction des pixels et la délimitation de la Region of Interest (*ROI*) afin de permettre à l’utilisateur de restreindre la zone de recherche du motif. Cette approche, bien qu’imparfaite, est la plus efficace et rapide dans le contexte présent.

- **PIL** : Cette bibliothèque nous a permis de lire directement, au sein du programme, les images traitées par la bibliothèque **Streamlit**.

Concernant les algorithmes utilisés, nous nous sommes appuyés principalement sur SIFT. Bien que nous ayons initialement testé ORB, les résultats obtenus étaient décevants, notamment en raison de la sensibilité d’ORB aux déformations géométriques et aux variations complexes de perspective, ce qui a entraîné une baisse significative du taux de réussite.

Une tentative de combinaison de SIFT et ORB a été réalisée dans l’optique de tirer parti de leurs avantages respectifs :

- ORB est rapide, peu gourmand en ressources et robuste face aux variations d’éclairage.

- SIFT, bien que plus coûteux en termes de calculs, se distingue par sa capacité à gérer les transformations complexes, telles que les rotations, les changements d’échelle et les déformations.

Cependant, cette combinaison n’a pas permis d’améliorer significativement les résultats. C'est pour cela que nous avons décidé de rester sur SIFT. 

## Partie 3 : Les Réussites et Les Echecs

Afin de bien couvrir l'intégralité de cette partie, nous allons nous permettre de la diviser en trois sous parties.

### L'Analyse des performances actuelles :

De manière générale, et sur la base des images testées, notre application atteint un taux de réussite de **23,52%**.

D'une part, bien que ce résultat ne puisse être qualifié ni d'extraordinaire ni de pleinement satisfaisant, il reste néanmoins convenable dans certains cas spécifiques. En effet, notre algorithme excelle particulièrement dans les situations où :

- Le motif recherché se trouve sur un fond blanc uni, permettant une reconnaissance visuelle claire et sans ambiguïté.
- Le motif n'est pas sujet à des distorsions majeures. Il est capable de tolérer certaines déformations mineures sans altérer la détection (*comme observé avec l'image MEA-5-4G*).

Vous retrouverez, ci-dessous, la liste des images où SerPa a reussi à détecter une pattern

|Nom de l'Image|Avec Recadrage|Sans Recadrage|
|:-|:--:|:--:|
|3-3|X| |
|4-3| |X|
|1-3||X|
|2-3||X|
|MEA-6-3G||X|
|MEA-14-4G||X|
|MEA-11-4G|X||
|MEA-5-4G||X|
|B-2-autre||X|
|Patern2_MiseEnAbime||X|
|Produit-1|X||

Cela montre que notre solution est fonctionnelle dans un cadre relativement contrôlé, mais ses performances diminuent rapidement lorsque ces conditions idéales ne sont pas respectées.

D'autre part, les chiffres révèlent également une faiblesse notable : dans **76,48%** des cas, l'algorithme échoue à identifier le motif au sein des images. Ce taux d'échec est beaucoup trop élevé pour considérer l'application comme pleinement opérationnelle ou efficace dans des scénarios variés ou en conditions réelles.

Il est aussi important de noté qu'une grande majorité des erreurs est une mauvaise reconnaissance du pattern (*Retourné, Negatif, etc.*) et non une non-reconnaissance dudit pattern.

### Points encourageants malgré tout :

Cependant, un point positif mérite d'être souligné : l'application fait preuve d'une grande fiabilité dans la gestion des images qui ne contiennent pas le motif recherché. En effet, elle parvient à éviter les correspondances erronées ou les "faux positifs" dans la majorité des cas, ce qui est un atout majeur pour garantir l'intégrité des résultats. Cela montre que, même si la reconnaissance des motifs reste un défi dans de nombreuses configurations, le système est capable de filtrer efficacement les cas invalides.

## Partie 4 : Les Améliorations Possibles

Pour améliorer les performances globales de SerPa, plusieurs axes d’amélioration méritent d’être explorés :

- **Optimisation des paramètres algorithmiques** : L’ajustement des paramètres de l’algorithme actuel pourrait permettre une meilleure gestion des motifs déformés, des arrière-plans complexes ou des variations d’éclairage, qui restent des défis majeurs pour l’efficacité de SerPa.
- **Intégration de techniques de machine learning** : L’intégration de modèles avancés tels que l’algorithme YOLO, entraînés à reconnaître des motifs spécifiques avec précision, pourrait améliorer les performances de l’application. Cette approche offrirait une robustesse accrue et une reconnaissance plus rapide, même dans des conditions variées.
- **Amélioration des motifs existants** : Les motifs actuels présentent certaines limites, notamment les ronds, qui facilitent la correspondance mais sont également une source fréquente d’erreurs. Une optimisation du design des motifs pourrait réduire ces ambiguïtés et améliorer la fiabilité des détections.
- **Augmentation de la bibliothèque de motifs** : Actuellement limitée à 16 motifs, la bibliothèque restreinte explique en partie les difficultés rencontrées dans certaines situations. L’élargissement de cette bibliothèque, avec des motifs mieux adaptés et diversifiés, offrirait une plus grande flexibilité et des résultats plus convaincants.
- **Élargissement de la base de tests** : Tester l’algorithme sur un éventail plus large de situations permettrait de mieux identifier ses failles et d’y remédier. En affinant l’algorithme à partir d’images variées et complexes, nous pourrions améliorer sa robustesse face à des conditions moins idéales.

En somme, bien que les performances actuelles de SerPa soient encore en deçà des attentes dans des situations variées, les résultats encourageants obtenus dans des configurations spécifiques, ainsi que l’absence de faux positifs, constituent une base solide. Grâce à ces pistes d’amélioration, l’application pourrait évoluer significativement et répondre à des besoins plus larges avec une efficacité accrue.