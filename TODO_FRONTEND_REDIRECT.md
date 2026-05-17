# TODO - Rediriger vers le frontend (Production SPA)

- [x] Build le frontend React avec Vite pour générer `Pharmacie/frontend/dist/`

- [x] Ajouter une vue Django qui sert `dist/index.html` (SPA fallback)

- [ ] Mettre à jour `backend/urls.py` pour que `/` et toutes les routes inconnues renvoient vers l’index SPA
- [ ] Ajouter/ajuster le middleware/paramètres de `settings.py` si nécessaire pour servir les assets statiques de React
- [ ] Tester : naviguer dans React via `/stock`, `/add`, `/vente`, `/alert` puis rafraîchir la page

