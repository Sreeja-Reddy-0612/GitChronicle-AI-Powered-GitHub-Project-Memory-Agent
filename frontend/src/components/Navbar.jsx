import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <div style={styles.nav}>
      <Link to="/" style={{ textDecoration: 'none', color: 'white' }}>
        <h2>🚀 GitChronicle</h2>
      </Link>

      <div style={styles.links}>
        <Link to="/" style={styles.link}>Dashboard</Link>
        <Link to="/insights" style={styles.link}>Insights</Link>
        <Link to="/phases" style={styles.link}>Phases</Link>
        <Link to="/commits" style={styles.link}>Commits</Link>
      </div>
    </div>
  );
}

const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "15px 30px",
    background: "#020617",
    borderBottom: "1px solid #334155",
  },
  links: {
    display: "flex",
    gap: "20px",
  },
  link: {
    color: "#cbd5e1",
    textDecoration: "none",
    fontSize: "16px",
    fontWeight: "500",
    transition: "color 0.2s",
  }
};