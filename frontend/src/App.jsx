import { useState } from "react";

const COPY = {
  ru: {
    eyebrow: "Prompt → Poem",
    title: "Стихотворение из твоего промпта",
    subhead:
      "Отправь несколько образов или слов — и получи короткий свободный стих.",
    label: "Твой промпт",
    placeholder: "Например: город после дождя, теплый свет, диалог у окна",
    submit: "Сочинить",
    submitting: "Собираю строки...",
    example: "Пример",
    errorEmpty: "Введите промпт — даже одно предложение подойдет.",
    errorGeneric: "Что-то пошло не так.",
    errorFetch: "Не удалось получить стихотворение.",
    resultTitle: "Готовое стихотворение",
    usedWords: "Ключевые слова:",
    examples: [
      "Город после дождя, кофе и неон, разговор на кухне",
      "Путешествие к морю, старый фотоаппарат, теплый ветер",
      "Тишина библиотеки, запах бумаги, зимний вечер"
    ],
    langLabel: "Язык",
    langRu: "Русский",
    langEn: "English"
  },
  en: {
    eyebrow: "Prompt → Poem",
    title: "A Poem from Your Prompt",
    subhead: "Send a few images or words — get a short free‑verse poem.",
    label: "Your prompt",
    placeholder: "For example: city after rain, warm light, a window dialogue",
    submit: "Compose",
    submitting: "Weaving lines...",
    example: "Example",
    errorEmpty: "Please enter a prompt — even one sentence works.",
    errorGeneric: "Something went wrong.",
    errorFetch: "Could not fetch the poem.",
    resultTitle: "Your poem",
    usedWords: "Keywords:",
    examples: [
      "City after rain, coffee and neon, a kitchen conversation",
      "A journey to the sea, an old camera, a warm wind",
      "Library silence, paper scent, a winter evening"
    ],
    langLabel: "Language",
    langRu: "Русский",
    langEn: "English"
  }
};

export default function App() {
  const [lang, setLang] = useState("ru");
  const [prompt, setPrompt] = useState("");
  const [poem, setPoem] = useState("");
  const [usedWords, setUsedWords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const copy = COPY[lang];

  const submitPrompt = async (event) => {
    event.preventDefault();
    setError("");
    setPoem("");
    setUsedWords([]);

    if (!prompt.trim()) {
      setError(copy.errorEmpty);
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("/api/poem", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
      });

      if (!response.ok) {
        throw new Error(copy.errorFetch);
      }

      const data = await response.json();
      setPoem(data.poem);
      setUsedWords(data.used_words || []);
    } catch (err) {
      setError(err.message || copy.errorGeneric);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <main className="panel">
        <header className="header">
          <div className="header-top">
            <p className="eyebrow">{copy.eyebrow}</p>
            <div className="lang">
              <span>{copy.langLabel}</span>
              <button
                type="button"
                className={lang === "ru" ? "lang-btn active" : "lang-btn"}
                onClick={() => setLang("ru")}
              >
                {copy.langRu}
              </button>
              <button
                type="button"
                className={lang === "en" ? "lang-btn active" : "lang-btn"}
                onClick={() => setLang("en")}
              >
                {copy.langEn}
              </button>
            </div>
          </div>
          <h1>{copy.title}</h1>
          <p className="subhead">{copy.subhead}</p>
        </header>

        <form className="form" onSubmit={submitPrompt}>
          <label className="label" htmlFor="prompt">
            {copy.label}
          </label>
          <textarea
            id="prompt"
            rows="5"
            value={prompt}
            onChange={(event) => setPrompt(event.target.value)}
            placeholder={copy.placeholder}
          />
          <div className="actions">
            <button type="submit" disabled={loading}>
              {loading ? copy.submitting : copy.submit}
            </button>
            <button
              type="button"
              className="ghost"
              onClick={() =>
                setPrompt(
                  copy.examples[Math.floor(Math.random() * copy.examples.length)]
                )
              }
            >
              {copy.example}
            </button>
          </div>
        </form>

        {error && <p className="error">{error}</p>}

        {poem && (
          <section className="result">
            <h2>{copy.resultTitle}</h2>
            <pre>{poem}</pre>
            {usedWords.length > 0 && (
              <p className="used">
                {copy.usedWords} <span>{usedWords.join(", ")}</span>
              </p>
            )}
          </section>
        )}
      </main>
    </div>
  );
}
