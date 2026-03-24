export default function Home() {
  return (
    <div className="space-y-8">
      <section>
        <h2 className="mb-4 text-2xl font-bold">Dashboard</h2>
        <p className="text-gray-600">
          Track local government council hearing updates across BC municipalities.
          Opt-in to topics you care about and get alerts when new agendas, videos,
          or minutes are published.
        </p>
      </section>

      <section className="grid gap-4 sm:grid-cols-3">
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h3 className="text-sm font-medium text-gray-500">Municipalities</h3>
          <p className="mt-2 text-3xl font-bold">14</p>
          <p className="text-sm text-gray-400">CRD region</p>
        </div>
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h3 className="text-sm font-medium text-gray-500">Active Sources</h3>
          <p className="mt-2 text-3xl font-bold">--</p>
          <p className="text-sm text-gray-400">CivicWeb + YouTube</p>
        </div>
        <div className="rounded-lg border bg-white p-6 shadow-sm">
          <h3 className="text-sm font-medium text-gray-500">Your Tracks</h3>
          <p className="mt-2 text-3xl font-bold">0</p>
          <p className="text-sm text-gray-400">Create your first track</p>
        </div>
      </section>

      <section>
        <h3 className="mb-3 text-lg font-semibold">Quick Actions</h3>
        <div className="flex gap-3">
          <a
            href="/tracks/new"
            className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            Create Track
          </a>
          <a
            href="/municipalities"
            className="rounded-lg border px-4 py-2 text-sm font-medium hover:bg-gray-50"
          >
            Browse Municipalities
          </a>
        </div>
      </section>

      <footer className="mt-12 border-t pt-4 text-xs text-gray-400">
        <p>
          Public data only. Not official government communication. AI-generated
          summaries may contain errors — always verify with original sources.
        </p>
      </footer>
    </div>
  );
}
