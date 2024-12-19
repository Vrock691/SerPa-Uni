# Introduction

Ce rapport a pour objectif de présenter les finalités de l'algorithme, d’en détailler le fonctionnement et d’en analyser les éventuelles faiblesses.

Nous aborderons ensuite les principales difficultés rencontrées lors du développement, en mettant en lumière :
- Les améliorations envisageables.
- Les fonctionnalités que nous n'avons pas pu implémenter.

**Important :** Il était strictement interdit d'utiliser les différentes techniques de *machine learning* ou de réseau de neurones convolutifs.

## Partie 1 : Les Applications et Usages

Le programme SerPa, également appelé Searchin Pattern, est principalement dédié à la reconnaissance de motifs spécifiques. Dans sa version actuelle, SerPa est capable d'identifier 16 motifs différents au sein de divers types d'images, notamment des panneaux publicitaires, des affiches, des gobelets, et bien d'autres supports visuels.

L'intéret de ce programme est ...

## Partie 2 : La Création

Dès les prémices de la conception du programme, nous avons tout de suite pensés à utiliser le Framework [Streamlit](https://streamlit.io/). Ledit framework nous a permis d'augmenter l'interactivité entre l'utilisateur et le programme, sans avoir à passé par le terminal, en "*hébèrgent*" le programme sur un site et en impémentant quelques éléments d'interface, tels que la dropzone, le titre du programme ou encore un peu de texte.

De plus, et comme les consignes nous le recommandaient, nous avons utilisé les bibliothèques suivantes :
- OpenCV : Cette bibliothèque nous a permis d'exploiter divers algorithmes tels que SIFT et ORB, chacun ayant des applications spécifiques, pour effectuer un traitement avancé des images.
- Pandas :
- Numpy :
- Pil :

Quant aux algorithmes utilisés, ...

Et en fin, n

## Partie 3 : Les Forces et Faiblesses



## Partie 4 : Les Améliorations Possibles

Pour ce qui en est des améliorations, la plus importante serait l'intégration de techniques de machine learning, comme l'algorithme YOLO, en le formant à reconnaître des motifs spécifiques avec précision.