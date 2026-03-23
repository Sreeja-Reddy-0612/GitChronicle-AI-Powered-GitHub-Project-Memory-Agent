import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Insights from "./pages/Insights";
import Phases from "./pages/Phases";
import Commits from "./pages/Commits";
import Navbar from "./components/Navbar";
import TypeDistribution from "./pages/TypeDistribution";
import CommitExplanation from "./pages/CommitExplanation";

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/insights" element={<Insights />} />
        <Route path="/phases" element={<Phases />} />
        <Route path="/commits" element={<Commits />} />
        <Route path="/type-distribution" element={<TypeDistribution />} />
        <Route path="/commit-explanation" element={<CommitExplanation />} />
      </Routes>
    </BrowserRouter>
  );
}