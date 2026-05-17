import { BrowserRouter, Routes, Route, Link } from "react-router-dom"

import Dashboard from "./pages/Dashboard"
import Stock from "./pages/Stock"
import AddMedicament from "./pages/AddMedicament"
import Vente from "./pages/Vente"
import AlertStock from "./pages/AlertStock"

function App() {
  return (
    <BrowserRouter>

      {/* 🔵 NAVBAR ICI */}
      <nav className="flex gap-6 p-4 bg-blue-600 text-white">
        <Link to="/">Dashboard</Link>
        <Link to="/stock">Stock</Link>
        <Link to="/add">Ajout médicament</Link>
        <Link to="/vente">Vente</Link>
        <Link to="/alert">Alerte stock</Link>
      </nav>

      {/* 📄 PAGES */}
      <div className="p-6">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/stock" element={<Stock />} />
          <Route path="/add" element={<AddMedicament />} />
          <Route path="/vente" element={<Vente />} />
          <Route path="/alert" element={<AlertStock />} />
        </Routes>
      </div>

    </BrowserRouter>
  )
}

export default App