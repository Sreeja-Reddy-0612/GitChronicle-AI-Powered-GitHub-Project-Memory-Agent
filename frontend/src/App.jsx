import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Insights from "./pages/Insights";
import Phases from "./pages/Phases";
import Commits from "./pages/Commits";
import Navbar from "./components/Navbar";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/insights" element={<Insights />} />
        <Route path="/phases" element={<Phases />} />
        <Route path="/commits" element={<Commits />} />
      </Routes>
    </BrowserRouter>
  );
}