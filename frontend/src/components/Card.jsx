export default function Card({ title, onClick }) {
  return (
    <div onClick={onClick} style={styles.card}>
      <h3>{title}</h3>
    </div>
  );
}

const styles = {
  card: {
    padding: "20px",
    background: "#f3f3f3",
    borderRadius: "10px",
    cursor: "pointer",
    textAlign: "center",
  },
};