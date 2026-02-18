import { DashboardBuilder } from "@/builder/DashboardBuilder";

export default function DashboardPage() {
  return (
    <main style={{ maxWidth: 1200, margin: "2rem auto", padding: "0 1rem" }}>
      <h1>Organization Dashboard</h1>
      <DashboardBuilder />
    </main>
  );
}
