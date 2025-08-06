import React, { useState } from "react";
export default function SearchBox({ onSearch }) {
  const [query, setQuery] = useState("");
  return (
    <div style={{ margin: "16px 0" }}>
      <input
        type="text"
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="자연어/키워드로 검색"
        style={{ width: 340 }}
      />
      <button
        onClick={() => onSearch(query)}
        disabled={!query}
        style={{ marginLeft: 8 }}
      >
        AI 검색
      </button>
    </div>
  );
}
