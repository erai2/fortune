import React, { useState, useEffect } from "react";
import { addTermAPI, getTermsAPI, searchTermsAPI } from "./api";
import TermForm from "./components/TermForm";
import SearchBox from "./components/SearchBox";
import TermCardList from "./components/TermCardList";
import TermNetwork from "./components/TermNetwork";
import TermTree from "./components/TermTree";
import TermDetail from "./components/TermDetail";

function App() {
  const [terms, setTerms] = useState([]);
  const [results, setResults] = useState([]);
  const [view, setView] = useState("card");
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    getTermsAPI().then(setTerms);
  }, []);

  async function handleAdd(text, related_terms = []) {
    const obj = await addTermAPI(text, related_terms);
    setTerms(ts => [...ts, obj]);
  }

  async function handleSearch(query) {
    setResults(await searchTermsAPI(query));
    setView("card");
  }

  const viewList = results.length ? results : terms;

  return (
    <div style={{ maxWidth: 1200, margin: "0 auto", padding: 24 }}>
      <h2>명리학 지식 네트워크 통합시각화 데모</h2>
      <TermForm onAdd={handleAdd} />
      <SearchBox onSearch={handleSearch} />
      <div style={{ margin: "18px 0" }}>
        <button onClick={() => setView("card")}>카드</button>
        <button onClick={() => setView("network")}>네트워크</button>
        <button onClick={() => setView("tree")}>트리</button>
      </div>
      <div style={{ display: 'flex', gap: 28 }}>
        {view === "card" && (
          <TermCardList items={viewList} onClick={setSelected} />
        )}
        {view === "network" && (
          <TermNetwork items={viewList} onSelect={setSelected} />
        )}
        {view === "tree" && (
          <TermTree items={viewList} onSelect={setSelected} />
        )}
        <TermDetail item={selected} onClose={() => setSelected(null)} />
      </div>
    </div>
  );
}

export default App;
