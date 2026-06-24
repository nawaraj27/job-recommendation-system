import { useCmsGroup } from "../api/cms";

export default function About() {
  const { data: cms } = useCmsGroup("about");
  const t = (k) => cms?.[k]?.text || "";
  return (
    <div className="max-w-3xl mx-auto px-6 py-16 space-y-8">
      <Block title="Mission" body={t("about.mission")} />
      <Block title="Vision" body={t("about.vision")} />
      <Block title="Platform" body={t("about.platform")} />
    </div>
  );
}
function Block({ title, body }) {
  return (
    <div>
      <h2 className="text-2xl font-bold">{title}</h2>
      <p className="mt-2 text-gray-600">{body}</p>
    </div>
  );
}
