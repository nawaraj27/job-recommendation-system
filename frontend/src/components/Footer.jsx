import { useCmsGroup } from "../api/cms";

export default function Footer() {
  const { data: cms } = useCmsGroup("footer");
  const contact = cms?.["footer.contact"] || {};
  const social = cms?.["footer.social"] || {};
  return (
    <footer className="mt-16 border-t bg-gray-50 px-6 py-8 text-sm text-gray-600">
      <div className="flex flex-wrap justify-between gap-6">
        <div>
          <p>{contact.email}</p>
          <p>{contact.phone}</p>
        </div>
        <div className="flex gap-4">
          {Object.entries(social).map(([k, v]) => (
            <a key={k} href={v} className="capitalize hover:text-indigo-600">{k}</a>
          ))}
        </div>
        <div className="flex gap-4">
          <a href="/legal/terms">Terms</a>
          <a href="/legal/privacy">Privacy</a>
        </div>
      </div>
    </footer>
  );
}
