# Cartouche

Une police pixel à chasse fixe, dérivée de [Mono10](https://jdjimenez.itch.io/) de Jesse D. Jimenez, écrite pour des interfaces en pixel art sur écran de téléphone. Des apps Android l'embarquent, et ce dépôt est la source de leurs fichiers de police : F-Droid doit pouvoir remonter d'un TTF embarqué jusqu'à ce qui l'a produit.

Deux familles, deux graisses chacune, dans `ttf/` :

- `Cartouche` Regular et Thin : le texte. Tout Windows-1252 (les langues d'Europe de l'Ouest), les flèches, les signes de comparaison, quelques signes de l'alphabet phonétique, et dans la zone privée d'Unicode des pièces de cadre et des symboles d'interface.
- `Cartouche Big` Regular et Thin : les symboles d'interface à la seconde taille, dans une boîte de 22 × 22.

Un glyphe occupe 11 colonnes sur 14 rangées de pixels ; une ligne de texte se pose à un pas de 15.

## La source

La source n'est pas le TTF mais des cartes de pixels en texte, une par graisse, dans `glyphs/`. Les scripts de `src/` les compilent :

```
./run build     # compile les quatre TTF dans ttf/, puis les contrôle
./run plank     # planche PNG des deux graisses dans tmp/
./run           # menu de toutes les tâches
```

Il faut Python 3 avec `fontTools` et `Pillow` (`questionary` pour le menu). Deux compilations des mêmes cartes donnent les mêmes octets.

La doc complète — la boîte, les étapes de dessin, la répartition de la zone privée — est dans [`docs/reference.md`](docs/reference.md).

## Licences

- La police est sous **SIL Open Font License 1.1**, comme Mono10 dont elle dérive : voir [`OFL.txt`](OFL.txt). Les TTF d'origine de Mono10 sont dans `upstream/mono10/`.
- Les scripts sont sous **GPL-3.0-or-later** : voir [`LICENSE`](LICENSE).
