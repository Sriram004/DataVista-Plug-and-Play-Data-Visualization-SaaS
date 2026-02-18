import Link from "next/link";

export default function HomePage() {
  return (
    <main style={{ maxWidth: 900, margin: "4rem auto", padding: "0 1rem" }}>
      <h1>DataVista</h1>
      <p>Plug-and-play multi-tenant analytics platform for instant dashboards.</p>
      <ul>
        <li>JWT auth + RBAC</li>
        <li>CSV/Excel ingestion and schema inference</li>
        <li>Interactive dashboard builder</li>
      </ul>
      <Link href="/dashboard">Open dashboard builder</Link>
    </main>
  );
}
