import { useMemo, useState } from 'react'

import {
  Bell,
  Boxes,
  ClipboardList,
  CreditCard,
  FileText,
  Package,
  Search,
  Settings,
  Store,
  Users,
  UserCog,
  LayoutDashboard,
  Activity,
  Stethoscope,
  TrendingUp,
} from 'lucide-react'
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from 'recharts'

function cn(...classes) {
  return classes.filter(Boolean).join(' ')
}

const menuItems = [
  { label: 'Tableau de bord', icon: LayoutDashboard, key: 'dashboard' },
  { label: 'Médicaments', icon: Stethoscope, key: 'medicaments' },
  { label: 'Stock', icon: Package, key: 'stock' },
  { label: 'Ventes', icon: ClipboardList, key: 'ventes' },
  { label: 'Achats', icon: CreditCard, key: 'achats' },
  { label: 'Fournisseurs', icon: Store, key: 'fournisseurs' },
  { label: 'Clients', icon: Users, key: 'clients' },
  { label: 'Utilisateurs', icon: UserCog, key: 'utilisateurs' },
  { label: 'Paramètres', icon: Settings, key: 'parametres' },
  { label: 'Rapports', icon: FileText, key: 'rapports' },
]

export default function Dashboard() {
  const [activeKey, setActiveKey] = useState('dashboard')
  const [query, setQuery] = useState('')

  // Données statiques fictives
  const stats = useMemo(
    () => [
      {
        title: 'Nombre total de médicaments',
        value: 1284,
        icon: Boxes,
        iconBg: 'bg-indigo-50 text-indigo-600',
        iconFg: 'text-indigo-600',
        trend: '+4.2% vs hier',
      },
      {
        title: 'Stock faible',
        value: 37,
        icon: Activity,
        iconBg: 'bg-rose-50 text-rose-600',
        iconFg: 'text-rose-600',
        trend: 'Seuil atteint',
      },
      {
        title: 'Ventes du jour',
        value: 84,
        icon: ClipboardList,
        iconBg: 'bg-sky-50 text-sky-600',
        iconFg: 'text-sky-600',
        trend: '+12 commandes',
      },
      {
        title: 'Chiffre d’affaires',
        value: '24 680 DH',
        icon: TrendingUp,
        iconBg: 'bg-emerald-50 text-emerald-600',
        iconFg: 'text-emerald-600',
        trend: '+8.1% cette semaine',
      },
      {
        title: 'Achats récents',
        value: 19,
        icon: Package,
        iconBg: 'bg-purple-50 text-purple-600',
        iconFg: 'text-purple-600',
        trend: 'Dernières 48h',
      },
    ],
    []
  )

  const sales7Days = useMemo(
    () => [
      { day: 'Lun', ventes: 28 },
      { day: 'Mar', ventes: 34 },
      { day: 'Mer', ventes: 29 },
      { day: 'Jeu', ventes: 41 },
      { day: 'Ven', ventes: 52 },
      { day: 'Sam', ventes: 44 },
      { day: 'Dim', ventes: 36 },
    ],
    []
  )

  const soonExpiring = useMemo(
    () => [
      { name: 'Amoxicilline 500mg', batch: 'B-2194', exp: '2026-06-02', qty: 6 },
      { name: 'Vitamine C 1g', batch: 'C-7711', exp: '2026-06-11', qty: 12 },
      { name: 'Ibuprofène 400mg', batch: 'I-3302', exp: '2026-06-18', qty: 9 },
      { name: 'Oméprazole 20mg', batch: 'O-1088', exp: '2026-07-01', qty: 14 },
      { name: 'Loratadine 10mg', batch: 'L-5520', exp: '2026-07-08', qty: 8 },
    ],
    []
  )

  const topSold = useMemo(
    () => [
      { name: 'Paracétamol 500mg', sold: 126, revenue: '2 340 DH' },
      { name: 'Azithromycine 250mg', sold: 98, revenue: '3 120 DH' },
      { name: 'Metformine 500mg', sold: 86, revenue: '2 650 DH' },
      { name: 'Losartan 50mg', sold: 77, revenue: '1 980 DH' },
      { name: 'Ciprofloxacine 500mg', sold: 69, revenue: '1 740 DH' },
    ],
    []
  )

  const recentActivities = useMemo(
    () => [
      {
        title: 'Réapprovisionnement effectué',
        detail: 'Lot: B-2194 • Quantité: 24',
        time: 'il y a 18 min',
        tone: 'emerald',
      },
      {
        title: 'Nouvelle vente enregistrée',
        detail: 'Client: FARAH K. • Total: 420 DH',
        time: 'il y a 45 min',
        tone: 'indigo',
      },
      {
        title: 'Stock mis à jour',
        detail: 'Ibuprofène 400mg • -3 unités',
        time: 'aujourd’hui 10:12',
        tone: 'amber',
      },
      {
        title: 'Commande fournisseur créée',
        detail: 'Fournisseur: MedSupply • 2 articles',
        time: 'aujourd’hui 09:05',
        tone: 'sky',
      },
    ],
    []
  )

  const filteredSoonExpiring = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return soonExpiring
    return soonExpiring.filter((m) =>
      m.name.toLowerCase().includes(q) || m.batch.toLowerCase().includes(q)
    )
  }, [query, soonExpiring])

  const activeIdx = useMemo(() => menuItems.findIndex((i) => i.key === activeKey), [activeKey])

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="flex min-h-screen">
        {/* Sidebar */}
        <aside className="fixed inset-y-0 left-0 z-20 w-72 border-r border-slate-200 bg-white">
          <div className="flex h-full flex-col">
            <div className="flex items-center justify-between px-6 py-5">
              <div className="flex items-center gap-3">
                <div className="relative grid h-10 w-10 place-items-center rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-500 shadow-soft">
                  <div className="absolute -inset-2 rounded-3xl bg-indigo-400/20 blur" />
                  <span className="relative text-white font-black text-lg">💊</span>
                </div>
                <div className="leading-tight">
                  <div className="text-[15px] font-extrabold tracking-tight text-slate-900">Pharma KAZM</div>
                  <div className="text-xs text-slate-500">Gestion de pharmacie</div>
                </div>
              </div>
            </div>

            <div className="px-4 pb-4">
              <div className="rounded-2xl bg-slate-50 p-3 border border-slate-200">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-2xl bg-gradient-to-br from-indigo-50 to-violet-50 grid place-items-center text-indigo-600">
                    <Stethoscope className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-slate-800">Pharmacien</div>
                    <div className="text-xs text-slate-500">Admin SaaS</div>
                  </div>
                </div>
              </div>
            </div>

            <nav className="flex-1 overflow-y-auto px-2 pb-5">
              <div className="space-y-1">
                {menuItems.map((item, idx) => {
                  const Icon = item.icon
                  const isActive = item.key === activeKey
                  return (
                    <button
                      key={item.key}
                      type="button"
                      onClick={() => setActiveKey(item.key)}
                      className={cn(
                        'group flex w-full items-center gap-3 rounded-2xl px-4 py-3 text-left transition-all',
                        isActive
                          ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-soft'
                          : 'text-slate-700 hover:bg-slate-100'
                      )}
                    >
                      <span
                        className={cn(
                          'grid h-10 w-10 place-items-center rounded-xl transition-all',
                          isActive ? 'bg-white/15' : 'bg-slate-100 group-hover:bg-white'
                        )}
                      >
                        <Icon
                          className={cn('h-5 w-5 transition-all', isActive ? 'text-white' : 'text-indigo-600')}
                        />
                      </span>
                      <span className="text-sm font-semibold">{item.label}</span>
                      {isActive ? (
                        <span className="ml-auto inline-flex items-center rounded-full bg-white/15 px-2 py-1 text-xs font-medium">
                          Actif
                        </span>
                      ) : idx === activeIdx ? (
                        <span className="ml-auto inline-flex items-center rounded-full bg-slate-100 px-2 py-1 text-xs font-medium text-slate-600">
                          •
                        </span>
                      ) : (
                        <span className="ml-auto opacity-0 transition-opacity group-hover:opacity-100 text-slate-400">
                          →
                        </span>
                      )}
                    </button>
                  )
                })}
              </div>
            </nav>

            <div className="px-6 pb-6">
              <div className="rounded-2xl border border-slate-200 bg-white p-4">
                <div className="flex items-start gap-3">
                  <div className="rounded-xl bg-indigo-50 text-indigo-600 grid place-items-center h-10 w-10">
                    <Bell className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-slate-800">Centre de notifications</div>
                    <div className="text-xs text-slate-500">Suivi stock & ventes</div>
                    <div className="mt-3 flex items-center gap-2">
                      <span className="inline-flex items-center rounded-full bg-indigo-50 px-2 py-1 text-xs font-semibold text-indigo-600">
                        3 alertes
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </aside>

        {/* Main */}
        <main className="ml-72 w-full">
          {/* Topbar */}
          <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/70 backdrop-blur">
            <div className="flex items-center justify-between gap-4 px-6 py-4">
              {/* Search */}
              <div className="flex-1">
                <div className="relative max-w-xl">
                  <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                  <input
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Rechercher un médicament, lot, ou un batch..."
                    className="w-full rounded-2xl border border-slate-200 bg-white/90 py-3 pl-11 pr-4 text-sm outline-none transition-all focus:border-indigo-300 focus:ring-4 focus:ring-indigo-100"
                  />
                </div>
              </div>

              {/* Right side */}
              <div className="flex items-center gap-3">
                <button
                  type="button"
                  className="relative rounded-2xl border border-slate-200 bg-white/90 p-2 text-slate-600 shadow-sm transition hover:-translate-y-0.5 hover:shadow"
                  aria-label="Notifications"
                >
                  <Bell className="h-5 w-5" />
                  <span className="absolute right-2 top-1 h-2 w-2 rounded-full bg-indigo-500" />
                </button>

                <div className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-white/90 px-3 py-2">
                  <div className="grid h-10 w-10 place-items-center rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-500 text-white shadow-soft">
                    <UserCog className="h-5 w-5" />
                  </div>
                  <div className="leading-tight">
                    <div className="text-sm font-semibold text-slate-900">Admin</div>
                    <div className="text-xs text-slate-500">Pharmacien</div>
                  </div>
                </div>
              </div>
            </div>
          </header>

          {/* Content */}
          <div className="px-6 py-6">
            <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
              <div>
                <div className="text-2xl font-extrabold tracking-tight text-slate-900">Tableau de bord</div>
                <div className="mt-1 text-sm text-slate-600">Vue claire, minimaliste et temps réel (fictif)</div>
              </div>
              <div className="flex items-center gap-2">
                <span className="inline-flex items-center rounded-full bg-indigo-50 px-3 py-2 text-xs font-semibold text-indigo-700">
                  SaaS • PharmaPro
                </span>
                <span className="inline-flex items-center rounded-full bg-slate-100 px-3 py-2 text-xs font-semibold text-slate-600">
                  {new Date().toLocaleDateString('fr-FR')}
                </span>
              </div>
            </div>

            {/* Stat cards */}
            <section className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3">
              {stats.map((s) => {
                const Icon = s.icon
                return (
                  <div
                    key={s.title}
                    className="group relative rounded-2xl bg-white p-5 shadow-md ring-1 ring-slate-100/60 transition hover:-translate-y-1 hover:shadow-soft"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <div className="text-sm font-semibold text-slate-700">{s.title}</div>
                        <div className="mt-2 text-3xl font-extrabold tracking-tight text-slate-900">
                          {typeof s.value === 'number' ? s.value.toLocaleString('fr-FR') : s.value}
                        </div>
                        <div className="mt-2 text-xs font-semibold text-slate-500">{s.trend}</div>
                      </div>
                      <div
                        className={cn(
                          'grid h-12 w-12 place-items-center rounded-2xl',
                          s.iconBg
                        )}
                      >
                        <Icon className={cn('h-6 w-6', s.iconFg)} />
                      </div>
                    </div>

                    <div className="pointer-events-none absolute -right-10 -top-10 h-32 w-32 rounded-full bg-gradient-to-br from-indigo-500/15 to-violet-500/10 blur" />
                    <div className="mt-4 flex items-center gap-2">
                      <span className="inline-flex items-center rounded-full bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-600">
                        Détails
                      </span>
                      <span className="text-xs font-semibold text-indigo-600 opacity-0 transition-opacity group-hover:opacity-100">
                        Voir
                      </span>
                    </div>
                  </div>
                )
              })}
            </section>

            {/* Charts & lists */}
            <section className="mt-6 grid grid-cols-1 gap-4 xl:grid-cols-3">
              {/* Sales chart */}
              <div className="xl:col-span-2 rounded-2xl bg-white p-5 shadow-md ring-1 ring-slate-100/60">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <div className="text-sm font-semibold text-slate-700">Ventes sur 7 jours</div>
                    <div className="mt-1 text-xs text-slate-500">Tendance fictive (par jour)</div>
                  </div>
                  <span className="inline-flex items-center rounded-full bg-indigo-50 px-3 py-2 text-xs font-semibold text-indigo-700">
                    Derniers 7 jours
                  </span>
                </div>

                <div className="mt-4 h-72 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={sales7Days} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                      <defs>
                        <linearGradient id="salesGradient" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#6366F1" stopOpacity={0.35} />
                          <stop offset="95%" stopColor="#6366F1" stopOpacity={0.05} />
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
                      <XAxis dataKey="day" tick={{ fill: '#64748b', fontSize: 12 }} />
                      <YAxis tick={{ fill: '#64748b', fontSize: 12 }} width={38} />
                      <Tooltip
                        cursor={{ fill: 'rgba(99,102,241,0.08)' }}
                        contentStyle={{ borderRadius: 14, border: '1px solid #E5E7EB' }}
                        formatter={(value) => [String(value), 'Ventes']}
                      />
                      <Area
                        type="monotone"
                        dataKey="ventes"
                        stroke="#6366F1"
                        fill="url(#salesGradient)"
                        strokeWidth={3}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>

                <div className="mt-4 flex flex-wrap items-center gap-3">
                  <div className="flex items-center gap-2">
                    <span className="h-2.5 w-2.5 rounded-full bg-indigo-500" />
                    <span className="text-xs font-semibold text-slate-600">Ventes</span>
                  </div>
                  <span className="text-xs text-slate-500">Objectif : +10%</span>
                </div>
              </div>

              {/* Soon expiring */}
              <div className="rounded-2xl bg-white p-5 shadow-md ring-1 ring-slate-100/60">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <div className="text-sm font-semibold text-slate-700">Médicaments bientôt périmés</div>
                    <div className="mt-1 text-xs text-slate-500">Filtré via la recherche</div>
                  </div>
                  <span className="inline-flex items-center rounded-full bg-rose-50 px-3 py-2 text-xs font-semibold text-rose-700">
                    Expirations
                  </span>
                </div>

                <div className="mt-4 space-y-3">
                  {filteredSoonExpiring.map((m) => (
                    <div
                      key={m.batch}
                      className="rounded-2xl border border-slate-200/70 bg-slate-50 p-3 transition hover:bg-white"
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <div className="text-sm font-bold text-slate-900">{m.name}</div>
                          <div className="mt-1 text-xs text-slate-500">Batch: {m.batch}</div>
                        </div>
                        <div className="text-right">
                          <div className="text-xs font-semibold text-rose-700">{m.exp}</div>
                          <div className="mt-1 text-xs font-semibold text-slate-600">{m.qty} unités</div>
                        </div>
                      </div>
                      <div className="mt-3 h-2.5 rounded-full bg-slate-200">
                        <div
                          className="h-2.5 rounded-full bg-gradient-to-r from-rose-500 to-indigo-500"
                          style={{ width: `${Math.min(100, Math.max(10, (m.qty / 20) * 100))}%` }}
                        />
                      </div>
                    </div>
                  ))}

                  {filteredSoonExpiring.length === 0 ? (
                    <div className="rounded-2xl border border-dashed border-slate-300 p-4 text-sm text-slate-500 text-center">
                      Aucun résultat.
                    </div>
                  ) : null}
                </div>
              </div>
            </section>

            {/* Top sold + activities */}
            <section className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-3">
              <div className="xl:col-span-1 rounded-2xl bg-white p-5 shadow-md ring-1 ring-slate-100/60">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <div className="text-sm font-semibold text-slate-700">Top médicaments vendus</div>
                    <div className="mt-1 text-xs text-slate-500">Classement fictif</div>
                  </div>
                  <span className="inline-flex items-center rounded-full bg-indigo-50 px-3 py-2 text-xs font-semibold text-indigo-700">
                    Top 5
                  </span>
                </div>

                <div className="mt-4 space-y-3">
                  {topSold.map((t, i) => (
                    <div
                      key={t.name}
                      className="flex items-center justify-between gap-3 rounded-2xl border border-slate-200/70 bg-white p-3 transition hover:-translate-y-0.5 hover:shadow"
                    >
                      <div className="flex items-center gap-3">
                        <div
                          className={cn(
                            'grid h-10 w-10 place-items-center rounded-2xl text-sm font-bold',
                            i === 0
                              ? 'bg-gradient-to-br from-indigo-500 to-violet-500 text-white'
                              : 'bg-slate-100 text-slate-700'
                          )}
                        >
                          {i + 1}
                        </div>
                        <div>
                          <div className="text-sm font-bold text-slate-900">{t.name}</div>
                          <div className="mt-1 text-xs text-slate-500">Vendus: {t.sold}</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-xs font-semibold text-slate-500">CA</div>
                        <div className="text-sm font-extrabold text-slate-900">{t.revenue}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="xl:col-span-2 rounded-2xl bg-white p-5 shadow-md ring-1 ring-slate-100/60">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <div className="text-sm font-semibold text-slate-700">Activités récentes</div>
                    <div className="mt-1 text-xs text-slate-500">Journal fictif</div>
                  </div>
                  <span className="inline-flex items-center rounded-full bg-slate-100 px-3 py-2 text-xs font-semibold text-slate-600">
                    Live
                  </span>
                </div>

                <div className="mt-4 space-y-3">
                  {recentActivities.map((a, idx) => {
                    const toneMap = {
                      emerald: 'bg-emerald-50 text-emerald-700',
                      indigo: 'bg-indigo-50 text-indigo-700',
                      amber: 'bg-amber-50 text-amber-700',
                      sky: 'bg-sky-50 text-sky-700',
                    }
                    return (
                      <div
                        key={idx}
                        className="rounded-2xl border border-slate-200/70 bg-slate-50 p-4 transition hover:bg-white"
                      >
                        <div className="flex items-start justify-between gap-4">
                          <div className="flex items-start gap-3">
                            <div
                              className={cn(
                                'grid h-11 w-11 place-items-center rounded-2xl font-bold',
                                toneMap[a.tone] || 'bg-indigo-50 text-indigo-700'
                              )}
                            >
                              <Activity className="h-5 w-5" />
                            </div>
                            <div>
                              <div className="text-sm font-extrabold text-slate-900">{a.title}</div>
                              <div className="mt-1 text-xs text-slate-600">{a.detail}</div>
                            </div>
                          </div>
                          <div className="text-right">
                            <div className="text-xs font-semibold text-slate-500">{a.time}</div>
                            <div className="mt-2 inline-flex items-center rounded-full bg-white border border-slate-200 px-3 py-1 text-xs font-semibold text-slate-600">
                              Détails
                            </div>
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            </section>

            {/* Footer spacing */}
            <div className="h-8" />
          </div>
        </main>
      </div>

      {/* Mobile sidebar overlay - simple UX */}
      <style>{`
        /* small-screen tweak: keep sidebar visible via scroll; can be extended to collapse */
        @media (max-width: 1024px) {
          aside.fixed { width: 18rem; }
          main { margin-left: 18rem; }
        }
        @media (max-width: 768px) {
          aside.fixed { width: 16rem; }
          main { margin-left: 16rem; }
        }
      `}</style>
    </div>
  )
}

