import React, { useState } from "react";
export default function TermForm({ onAdd }) {
  const [text, setText] = useState("");
  return (
    <div>
      <textarea
        value={text}
        onChange={e => setText(e.target.value)}
        rows={3}
        style={{ width: 500 }}
        placeholder="설명/용어/개념을 입력..."
      />
      <button
        onClick={() => {
          onAdd(text);
          setText("");
        }}
        disabled={!text}
      >
        AI 구조화+저장
      </button>
    </div>
  );
}
