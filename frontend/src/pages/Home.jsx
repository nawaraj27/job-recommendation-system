import { Link } from "react-router-dom";
import { useCmsGroup } from "../api/cms";

export default function Home() {
  const { data: cms, isLoading } = useCmsGroup("home");
  if (isLoading) return <Center>Loading…</Center>;
  const t = (k) => cms?.[k]?.text || "";
  const features = cms?.["home.features"]?.items || [];

  return (
    <div>
      <section className="text-center px-6 py-20 bg-gradient-to-b from-indigo-50 to-white">
        <h1 className="text-4xl font-bold max-w-2xl mx-auto">{t("home.hero.title")}</h1>
        <p className="mt-4 text-gray-600 max-w-xl mx-auto">{t("home.hero.subtitle")}</p>
        <Link to="/analyze"
          className="inline-block mt-8 px-6 py-3 bg-indigo-600 text-white rounded-lg">
          {t("home.hero.cta")}
        </Link>
      </section>
      <section className="grid gap-6 px-6 py-16 max-w-5xl mx-auto md:grid-cols-4">
        {features.map((f, i) => (
          <div key={i} className="p-5 border rounded-lg">
            <h3 className="font-semibold">{f.title}</h3>
            <p className="text-sm text-gray-600 mt-2">{f.desc}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
function Center({ children }) {
  return <div className="p-20 text-center text-gray-400">{children}</div>;
}
