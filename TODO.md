# TODO - Correctif "Stock faible"

- [ ] Comprendre le comportement actuel : 
  - [ ] Page React « Stock.jsx » filtre « Stock faible » côté client.
  - [ ] Page React « AlertStock.jsx » charge /products/api/medicaments/ puis filtre < minQty.
- [ ] Corriger la logique demandée : 
  - [ ] Quand on clique sur « Stock faible » (dans la page Stock), afficher uniquement les produits avec quantité inférieure au seuil.
  - [ ] Vérifier que l’état (onlyLowStock / minQty) et l’API renvoient les bons champs (quantite_stock).
- [ ] Tester : 
  - [ ] Vérifier manuellement que le tableau affiche uniquement les produits « stock faible » après clic.
  - [ ] Vérifier aussi la page /alert.

