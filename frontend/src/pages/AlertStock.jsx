import { useEffect, useMemo, useState } from "react";

export default function AlertStock() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [minQty, setMinQty] = useState(10);
  const [query, setQuery] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        setLoading(true);
        setError("");

        const apiBase = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
        const endpoint = `${apiBase}/products/api/medicaments/`;

        const res = await fetch(endpoint);
        if (!res.ok) {
          const text = await res.text().catch(() => "");
          throw new Error(`HTTP ${res.status}. endpoint: ${endpoint}. Body: ${text.slice(0, 120)}`);
        }

        const data = await res.json();
        if (!cancelled) {
          setItems(Array.isArray(data.medicaments) ? data.medicaments : []);
        }
      } catch (e) {
        if (!cancelled) setError(`Impossible de charger les alertes. ${e?.message ?? ""}`);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return items.filter((m) => {
      const matchesQuery =
        !q ||
        String(m.nom ?? "").toLowerCase().includes(q) ||
        String(m.categorie ?? "").toLowerCase().includes(q) ||
        String(m.date_expiration ?? "").toLowerCase().includes(q);

      const matchesLow = Number(m.quantite_stock ?? 0) < Number(minQty ?? 10);
      return matchesQuery && matchesLow;
    });
  }, [items, query, minQty]);

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-900">Alerte stock faible</h1>
          <p className="mt-1 text-sm text-slate-600">
            Médicaments avec quantité <span className="font-bold">{minQty}</span>
          </p>
        </div>

        <div className="flex items-center gap-3">
          <label className="inline-flex items-center gap-2 text-sm font-semibold text-slate-700">
            Seuil
            <input
              type="number"
              min={0}
              className="w-28 rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm outline-none"
              value={minQty}
              onChange={(e) => setMinQty(Number(e.target.value))}
            />
          </label>
        </div>
      </div>

      <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Rechercher (nom, catégorie, expiration...)"
          className="flex-1 rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-indigo-300 focus:ring-4 focus:ring-indigo-100"
        />
        <div className="text-sm font-semibold text-slate-700">
          Résultats : <span className="text-rose-700">{filtered.length}</span>
        </div>
      </div>

      <div className="mt-5 rounded-2xl border border-slate-200 bg-white shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-6 text-slate-600">Chargement…</div>
        ) : error ? (
          <div className="p-6 text-rose-700 font-semibold">{error}</div>
        ) : filtered.length === 0 ? (
          <div className="p-6 text-slate-600">Aucune alerte.</div>
        ) : (
          <div className="overflow-auto">
            <table className="min-w-full text-left">
              <thead className="bg-slate-50 border-b">
                <tr>
                  <th className="p-3 text-sm font-bold text-slate-700">Nom</th>
                  <th className="p-3 text-sm font-bold text-slate-700">Catégorie</th>
                  <th className="p-3 text-sm font-bold text-slate-700">Quantité</th>
                  <th className="p-3 text-sm font-bold text-slate-700">Prix achat</th>
                  <th className="p-3 text-sm font-bold text-slate-700">Prix vente</th>
                  <th className="p-3 text-sm font-bold text-slate-700">Expiration</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((m) => (
                  <tr key={m.id} className="border-b last:border-b-0 hover:bg-slate-50/60">
                    <td className="p-3 text-sm font-semibold text-slate-900">{m.nom}</td>
                    <td className="p-3 text-sm text-slate-700">{m.categorie}</td>
                    <td className="p-3 text-sm font-semibold text-rose-700">{m.quantite_stock}</td>
                    <td className="p-3 text-sm text-slate-700">{m.prix_achat} DH</td>
                    <td className="p-3 text-sm text-slate-700">{m.prix_vente} DH</td>
                    <td className="p-3 text-sm text-slate-700">{m.date_expiration || "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

