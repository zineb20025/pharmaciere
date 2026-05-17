const fieldClasses = "block w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-indigo-300 focus:ring-4 focus:ring-indigo-100"

export default function AddMedicament() {
  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-extrabold tracking-tight text-slate-900">Ajout médicament</h1>
      <p className="mt-2 text-sm text-slate-600">Formulaire de création côté frontend (POST classique vers Django).</p>

      <form
        method="post"
        action="/products/ajouter-medicament/"
        className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
      >
        {/* CSRF: Django exige un token valide pour les POST.
            On récupère le token depuis le cookie 'csrftoken' (si présent) via document.cookie.
            Sinon, Django risque de rejeter la requête. */}
        <input
          type="hidden"
          name="csrfmiddlewaretoken"
          value={(() => {
            const m = document.cookie.match(/(^|;\\s*)csrftoken=([^;]+)/)
            return m ? decodeURIComponent(m[2]) : ''
          })()}
        />


        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="md:col-span-2">
            <label htmlFor="nom" className="block text-sm font-semibold text-slate-700">
              Nom du médicament
            </label>
            <input id="nom" name="nom" type="text" required className={fieldClasses} />
          </div>

          <div>
            <label htmlFor="categorie" className="block text-sm font-semibold text-slate-700">
              Catégorie
            </label>
            <input id="categorie" name="categorie" type="text" required className={fieldClasses} />
          </div>

          <div>
            <label htmlFor="quantite_stock" className="block text-sm font-semibold text-slate-700">
              Quantité en stock
            </label>
            <input
              id="quantite_stock"
              name="quantite_stock"
              type="number"
              min="0"
              required
              className={fieldClasses}
            />
          </div>

          <div className="md:col-span-2">
            <label htmlFor="description" className="block text-sm font-semibold text-slate-700">
              Description
            </label>
            <textarea id="description" name="description" rows={3} className={fieldClasses} />
          </div>

          <div>
            <label htmlFor="prix_achat" className="block text-sm font-semibold text-slate-700">
              Prix d'achat (DH)
            </label>
            <input
              id="prix_achat"
              name="prix_achat"
              type="number"
              step="0.01"
              min="0.01"
              required
              className={fieldClasses}
            />
          </div>

          <div>
            <label htmlFor="prix_vente" className="block text-sm font-semibold text-slate-700">
              Prix de vente (DH)
            </label>
            <input
              id="prix_vente"
              name="prix_vente"
              type="number"
              step="0.01"
              min="0.01"
              required
              className={fieldClasses}
            />
          </div>

          <div className="md:col-span-2">
            <label htmlFor="date_expiration" className="block text-sm font-semibold text-slate-700">
              Date d'expiration
            </label>
            <input id="date_expiration" name="date_expiration" type="date" className={fieldClasses} />
          </div>
        </div>

        <div className="mt-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <a href="/" className="text-sm font-semibold text-slate-600 hover:text-slate-900">
            ← Retour
          </a>
          <button
            type="submit"
            className="rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-extrabold text-white shadow-sm hover:bg-indigo-700 transition"
          >
            + Ajouter le médicament
          </button>
        </div>

        <div className="mt-4 text-xs text-rose-600">
          Note : si Django bloque le POST à cause du CSRF, il faudra remplacer le champ csrfmiddlewaretoken par un token réel.
        </div>
      </form>
    </div>
  )
}

