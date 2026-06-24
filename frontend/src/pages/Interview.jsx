import { useState } from "react";
import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import api from "../api/client";

export default function Interview() {
  const { id } = useParams();
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);

  const { data: session } = useQuery({
    queryKey: ["interview", id],
    queryFn: async () => (await api.get(`/ai/interviews/${id}/`)).data,
  });

  if (!session) return <div className="p-12 text-gray-400">Loading…</div>;

  const submit = async () => {
    const payload = {
      answers: session.questions.map((q) => ({
        question: q.question, answer: answers[q.question] || "",
      })),
    };
    const { data } = await api.post(`/ai/interviews/${id}/submit/`, payload);
    setResult(data);
  };

  if (result) {
    return (
      <div className="max-w-3xl mx-auto px-6 py-12">
        <h1 className="text-2xl font-bold">Results</h1>
        <div className="text-4xl font-bold text-indigo-600 my-4">{result.overall_score}/100</div>
        {result.answers.map((a, i) => (
          <div key={i} className="border rounded p-4 mb-3">
            <p className="font-medium">{a.question}</p>
            <p className="text-sm text-gray-500 mt-1">Score: {a.score}</p>
            <p className="text-sm mt-1">{a.feedback}</p>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-12">
      <h1 className="text-2xl font-bold mb-6">Interview Simulation</h1>
      {session.questions.map((q, i) => (
        <div key={i} className="mb-5">
          <p className="font-medium">{q.type}: {q.question}</p>
          <textarea rows={3} className="border rounded w-full px-3 py-2 mt-2"
            value={answers[q.question] || ""}
            onChange={(e) => setAnswers({ ...answers, [q.question]: e.target.value })} />
        </div>
      ))}
      <button onClick={submit} className="px-6 py-3 bg-indigo-600 text-white rounded">Submit Answers</button>
    </div>
  );
}
