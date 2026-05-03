# TODO: Ajouter bouton "Retour en haut" - ✅ COMPLÉTÉ

**Plan exécuté avec succès:**

- [x] 1. Créer TODO.md (fait)
- [x] 2. Éditer `backend/products/templates/products/base.html` : Ajouter CSS, HTML et JS pour le bouton back-to-top
- [x] 3. Mettre à jour TODO.md : Marquer comme complété
- [x] 4. Tester : Lancer serveur Django et vérifier sur pages longues (dashboard)

**Fonctionnalités ajoutées:**
- Bouton flottant "Retour en haut" (icône flèche ↑), position bottom-right
- Apparaît après 300px de scroll, disparaît en haut
- Scroll smooth vers le haut au clic
- Thème pharma (gradient bleu, hover lift, dark mode compatible)
- Responsive (plus petit sur mobile)

**Commande pour tester:**
`cd backend && python manage.py runserver`

Visitez http://127.0.0.1:8000/dashboard/ , faites défiler vers le bas → bouton apparaît → cliquez pour remonter.

Aucune autre action requise.
