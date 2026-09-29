# cartouche-font

La police pixel **Cartouche**, partagée par plusieurs apps (Saylune, l'assistant). Deux familles, deux graisses chacune : `Cartouche` (Regular, Thin) pour le texte, `Cartouche Big` pour les symboles à la seconde taille.

Le nom : la cartouche de jeu des consoles, et en typographie le cadre qui entoure une inscription — cette police porte ses propres pièces de cadre.

Source de vérité : les **cartes de pixels** de `glyphs/`, une par graisse et par famille. Le TTF est un produit, pas une source : `./run build` le refait, et il se commite dans `ttf/` pour qu'une app l'embarque sans appeler aucun outil hors de son dépôt (exigence F-Droid). Deux compilations des mêmes cartes donnent les mêmes octets : la date inscrite dans le fichier est fixe.

La boîte fait **11 colonnes sur 14 rangées**, de y=11 à y=-2 : les capitales tiennent les rangées 0 à 9, les accents 10 et 11, les descendantes -1 et -2. La colonne 10 est l'interlettre et reste vide. Une ligne de texte se pose donc à un pas de 15, que le thème de l'app déclare — jamais le défaut de la police, qui vaut 14.

Un pixel de dessin vaut 64 unités, le cadratin 1024, l'avance 704.

## Les apps et leur copie

Chaque app copie depuis `ttf/` les fichiers qu'elle veut, les commite chez elle, et **vérifie elle-même** que sa copie est identique octet à octet à celle d'ici (norme `pixel-ui`, section Police). Ce projet ne connaît pas ses utilisatrices : il ne copie rien et ne vérifie rien chez elles. Après une recompilation qui change un TTF, c'est la vérification de l'app qui le signale.

Le repli pour un caractère absent est aussi l'affaire de l'app : un carré vide pour un texte fermé, une police système pour un texte ouvert.

## Les commandes

`./run` ouvre le menu ; `./run <tâche>` lance directement.

- `build` — compile les quatre TTF dans `ttf/`, puis lance `check`.
- `check` — prouve que chaque glyphe qu'on n'a pas retouché rend au pixel près comme Mono10. Les cinq descendantes redessinées sont nommées dans le script ; tout autre écart est une faute.
- `plank [texte]` — planches PNG des deux graisses dans `tmp/`, pour juger en regardant ; sans texte, un échantillon (alphabet, chiffres, accents, symboles).
- `draw <étape>` — relance une étape de dessin sur les cartes. L'étape tourne d'abord sur une copie, les glyphes ajoutés, redessinés ou retirés s'affichent, et rien n'est écrit sans confirmation.

`src/extract.py` repart de Mono10 et **écrase les cartes** : il ne sert qu'à tout recommencer, et n'est pas une tâche du menu.

## Les scripts

Dans `src/`, autour de `pixelfont.py` (la boîte, la lecture et l'écriture des cartes).

- `build.py` — compile les cartes en TTF, et refuse un glyphe qui déborde de la boîte.
- `check.py` — le contrôle contre Mono10.
- `plank.py` — la planche PNG. Ses couleurs sont celles du registre de Saylune, recopiées en nombres.
- `draw.py` — l'aperçu puis l'écriture d'une étape de dessin.
- `extract.py` — lit les TTF de Mono10 et écrit les cartes.

Les étapes de dessin, que `draw` relance :

- `descenders.py` — redessine `g j p q y` avec leur queue sous la ligne de base.
- `accents.py` — compose les 62 lettres accentuées et les accents seuls, dérive les deux tirets du trait d'union, et pose les glyphes de `drawn.py` (ligatures, fractions, signes). Le rond en chef n'a que deux rangées : c'est une arche, que le haut de la lettre ferme.
- `western.py` — le reste de Windows-1252, les flèches de texte et les signes de comparaison. Ce qui est un autre glyphe déplacé ou coupé en est tiré (les guillemets bas, le moins, le point médian, les flèches de la zone privée) ; le reste est dessiné.
- `frames.py` — découpe les seize pièces de cadre depuis la formule du banc de Saylune.
- `furniture.py` — les vingt-cinq symboles d'interface de la zone privée. Ce qui est un symbole plein — le disque, le triangle, la jauge, le cœur, le micro, la loupe, l'œil, le cadenas, l'histogramme, les points — est identique dans les deux graisses ; ce qui est un trait — les flèches, la coche, la croix, les curseurs, le retour, la flèche circulaire — s'amincit avec le reste.
- `big.py` — **les symboles une seconde fois, dans une boîte de 22 × 22**, pour la seconde taille. Chaque glyphe y est écrit comme les formes dont il est fait — disque, segment, anneau, polygone — avec l'épaisseur de trait en paramètre : 4 pixels en Regular, 2 en Thin. Ils portent **les mêmes codets** que les symboles ordinaires, dans la famille `Cartouche Big` : l'app demande le même caractère et choisit la famille selon ce qu'elle dessine, un bouton ou une ligne de texte.
- `phonemes.py` — les phonèmes que l'analyse de Saylune affiche (alphabet phonétique, hors zone privée). Trois sont une lettre tournée ou en miroir, sept une lettre plus une barre ou un crochet, quatre sont dessinés par graisse.
- `scramble.py` — couvre chaque lettre de carrés, pour le tour de l'IA que Saylune montre sans le laisser lire.

Ajouter un caractère : écrire son bloc `@nom U+XXXX` dans les deux cartes de la famille, puis `./run build`.

## La zone privée

Une app qui a besoin de codets privés les réserve ici avant de les dessiner, pour que deux apps ne s'en disputent aucun.

| Codets | Contenu | Utilisé par |
| --- | --- | --- |
| `U+E000`–`U+E00F` | les cadres : huit pièces en couche claire, les mêmes en couche sombre | Saylune, l'assistant |
| `U+E010`–`U+E028` | les symboles d'interface : triangle, disque d'enregistrement, quatre blocs de jauge, quatre flèches, coche, croix, cœur, pause, arrêt, micro, loupe, œil, curseurs, retour, flèche circulaire, cadenas, histogramme, point plein, point creux ; les mêmes codets dans `Cartouche Big` | Saylune |
| `U+E029`–`U+E0FF` | libre | — |
| `U+E100`–`U+E27F` | `U+E100` + le codet d'une lettre : sa version brouillée ; `U+E100` nu est la jumelle générique, sur laquelle tombe une lettre qui n'a pas la sienne | Saylune |
| `U+E280`– | libre | — |

## Licence et publication

Dérivée de **Mono10**, de Jesse D. Jimenez (Community Pack, 2020), sous SIL OFL 1.1 — voir `OFL.txt`. La police dérivée porte un autre nom, `Cartouche`, et reste sous la même licence. Les TTF d'origine sont dans `upstream/mono10/`, avec leur licence : `check` et `extract.py` les lisent.

Le dépôt est destiné à être public sur GitHub, pour que F-Droid puisse remonter des TTF embarqués dans une app jusqu'à leur source.
