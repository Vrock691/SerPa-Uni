# Introduction

Ce rapport a pour objectif de présenter les finalités de l'algorithme, d’en détailler le fonctionnement et d’en analyser les éventuelles faiblesses.

Nous aborderons ensuite les principales difficultés rencontrées lors du développement, en mettant en lumière :
- Les améliorations envisageables.
- Les fonctionnalités que nous n'avons pas pu implémenter.

**Important :** Il était strictement interdit d'utiliser les différentes techniques de *machine learning* ou de réseau de neurones convolutifs.

## Partie 1 : Les Applications et Usages

Le programme SerPa, également connu sous le nom de Searchin Pattern, est conçu pour exceller dans la reconnaissance de motifs spécifiques au sein d'images variées. Dans sa version actuelle, SerPa est capable d'identifier jusqu'à 16 motifs différents sur divers supports visuels, tels que des panneaux publicitaires, des affiches, des gobelets, et bien d'autres encore.

L'intérêt principal de ce programme réside dans ses applications variées et innovantes :

- Reconnaissance de patterns pour un accès VIP : SerPa peut être utilisé dans des environnements événementiels pour détecter des motifs exclusifs. Par exemple, des motifs spécifiques pourraient servir de clé d'entrée pour des espaces réservés aux VIP, simplifiant ainsi l'accès tout en renforçant la sécurité.

- Communication codée grâce à un système binaire : Le programme est également capable de lire un code à 16 chiffres, construit à partir d'un format binaire (chaque case pouvant être noire ou blanche). Cette fonctionnalité permet d'utiliser SerPa comme outil pour échanger des messages cryptés ou sécurisés dans des environnements nécessitant une confidentialité élevée.

- Événements et jeux immersifs : Dans le cadre de chasses au trésor ou d'escape games, SerPa peut être utilisé pour scanner des motifs sur des objets ou des indices disséminés dans l'environnement. Cela ajoute une couche de technologie interactive au jeu, permettant aux participants de progresser en décodant des motifs spécifiques.

*Remarque : Le dernier exemple ne peut pas être utilisé actuellement, car SerPa ne contient aucune redirection vers un site externe. Bien que cette fonctionnalité ne soit pas complexe à implémenter, elle n’est pas encore en place.*

## Partie 2 : La Création

Voici une version révisée de votre texte avec un ton plus froid, académique et professionnel. J’ai également apporté quelques améliorations pour en clarifier la lecture et la compréhension :
Introduction

Ce rapport a pour objectif de présenter les finalités de l'algorithme, de détailler son fonctionnement et d'analyser ses éventuelles faiblesses.

Nous aborderons ensuite les principales difficultés rencontrées lors du développement, en mettant en lumière :

    Les améliorations envisageables ;
    Les fonctionnalités non implémentées.

Remarque importante : L’utilisation de techniques de machine learning ou de réseaux de neurones convolutifs a été strictement interdite.
Partie 1 : Applications et Usages

Le programme SerPa, également connu sous le nom de Searchin Pattern, est conçu pour exceller dans la reconnaissance de motifs spécifiques au sein d’images variées. Dans sa version actuelle, SerPa est capable d’identifier jusqu’à 16 motifs différents sur des supports visuels divers, tels que des panneaux publicitaires, des affiches, des gobelets, etc.

L’intérêt principal de ce programme réside dans ses applications variées et innovantes :

    Reconnaissance de motifs pour un accès VIP : SerPa peut être utilisé dans des environnements événementiels pour détecter des motifs exclusifs. Par exemple, des motifs spécifiques pourraient servir de clé d’entrée pour des espaces réservés aux VIP, simplifiant l’accès tout en garantissant une confidentialité élevée.

    Événements et jeux immersifs : Dans le cadre de chasses au trésor ou d’escape games, SerPa peut être utilisé pour scanner des motifs sur des objets ou des indices disséminés dans l’environnement. Cela ajoute une dimension interactive au jeu, permettant aux participants de progresser en décodant des motifs spécifiques.

Remarque : Le dernier exemple ne peut pas être utilisé actuellement, car SerPa ne contient aucune redirection vers un site externe. Bien que cette fonctionnalité ne soit pas complexe à implémenter, elle n’est pas encore en place.
Partie 2 : La Création

Dès les premières étapes de la conception du programme, nous avons choisi d’utiliser le framework Streamlit. Ce framework nous a permis d’augmenter l’interactivité entre l’utilisateur et le programme sans avoir à recourir au terminal, en hébergeant l’application sur un site et en intégrant divers éléments d'interface tels que la dropzone, le titre du programme, ainsi que des textes explicatifs.

De plus, en conformité avec les consignes, nous avons utilisé les bibliothèques suivantes :

- **OpenCV** : Cette bibliothèque nous a permis d'exploiter plusieurs algorithmes, notamment SIFT et ORB, afin de réaliser un traitement avancé et complet des images (*Conversion des images en teintes de gris, Lire les images, Mettre en place un système de match, etc.*).

- **NumPy** : Elle a facilité la représentation des images sous forme de tableaux numériques, ce qui a simplifié leur manipulation, l’extraction des pixels et la délimitation de la Region of Interest (ROI). Cette approche, bien qu’imparfaite, est la plus efficace et rapide dans le contexte présent.

- **PIL** : Bien que cette bibliothèque ne soit pas obligatoire, elle a permis de lire directement les images provenant de la bibliothèque **Streamlit**.

Nous avons également implémenté un système de ROI afin de permettre à l’utilisateur de restreindre la zone de recherche du motif. Bien que cette méthode ne soit pas la plus optimale, elle s’avère la plus rapide et efficace dans ce cas précis.

Concernant les algorithmes utilisés, nous nous sommes appuyés principalement sur SIFT. Bien que nous ayons initialement testé ORB, les résultats obtenus étaient décevants, notamment en raison de la sensibilité d’ORB aux déformations géométriques et aux variations complexes de perspective, ce qui a entraîné une baisse significative du taux de réussite.

Une tentative de combinaison de SIFT et ORB a été réalisée dans l’optique de tirer parti de leurs avantages respectifs :

- ORB est rapide, peu gourmand en ressources et robuste face aux variations d’éclairage.

- SIFT, bien que plus coûteux en termes de calculs, se distingue par sa capacité à gérer les transformations complexes, telles que les rotations, les changements d’échelle et les déformations.

Cependant, cette combinaison n’a pas permis d’améliorer significativement les résultats. En raison des limitations d’ORB, SIFT reste notre choix principal pour garantir une meilleure robustesse et précision dans la reconnaissance des motifs.





[A FINIR]

## Partie 3 : Les Réussites et Les Echecs

Sur 

MEA-5-4G fonctionne avec légère déformation !!!!

De manière plus générale, et avec les données que nous avons, notre application arrive à un taux de reussite de : **24,24%**

## Partie 4 : Les Améliorations Possibles

Pour ce qui en est des améliorations, la plus importante serait l'intégration de techniques de machine learning, comme l'algorithme YOLO, en le formant à reconnaître des motifs spécifiques avec précision.

Augmenter la bibliothèque de reconnaissance : nous n'avons que 16 patternes, ce qui peut expliquer la faiblesse de SerPa dans certaines situations.

Améliore les patternes : Les ronds des patternes permettent la bonne correspondance mais ils sont aussi source d'erreurs importante.