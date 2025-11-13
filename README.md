# Un assistant pour créer des courbes paramétriques en TeX

Le programme de l'assistant nécessite plusieurs modules
 - tkinter (Tcl)
 - pillow
 - matplotlib (pas encore utilisé)
 - numpy (idem)

Le programme nécessite deux modules TeX
 - tikz
 - pgfplots
 
## Utilisation de l'assistant
Dans la zone principale, vous pouvez paramétrer des courbes.
Utilisation:
1. [x] Ajouter une nouvelle courbe (bouton Ajouter dans la barre de menu).
2. [x] Dans la liste, définissez les fonctions:
  - composante sur x
  - composante sur y
  - Couleur (parmis la liste, en anglais)
  - Domaine (dans lequel le paramètre se déplace)
  - style (parmis la liste, par défaut thick)
  - légende, le titre de la courbe
  - -- le style de ligne
3. [x] Paramétrer la grille en bas à gauche
4. [x] Regarder si les axes doivent avoir la même échelle (axes égaux)
5. [x] Définissez les limites du graphe
6. [x] Rentrer le nom de la figure (facultatif)
7. [x] Rentrer le titre de la légende (facultatif)
8. [x] Vous pouvez afficher la légende si besoin.
9. [ ] Paramétrage des axes : ne pas mettre de graduations

Pour retirer une ligne en erreur, séléctionnez la et cliquez sur Retirer.
Pour enregistrer la configuration, cliquez sur Enregistrer.
Pour voir la sortie TeX, cliquez sur Exporter.
Pour créer un point, laissez la colonne domaine vide, et entrez les coordonées dans l'abscisse et l'ordonnée.

Vous pouvez ouvrir un paramétrage déjà effectué.

## Conseils utilisation sur TeX
Nous conseillons le paragraphe suivant en entête pour améliorer le tracé

```tex
\pgfplotsset{every axis/.append style={
		axis x line=middle,    % put the x axis in the middle
		axis y line=middle,    % put the y axis in the middle
		axis line style={->,color=black}, % arrows on the axis
		xlabel={$x$},          % default put x on x-axis
		ylabel={$y$},          % default put y on y-axis
}}
```

## Compilation
Pour compiler, nous utilisons PyInstaller.
