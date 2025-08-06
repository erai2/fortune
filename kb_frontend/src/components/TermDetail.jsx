import React from "react";
export default function TermDetail({ item, onClose }) {
  if (!item) return null;
  return (
    <div
      style={{
        background: "#fff",
        padding: 18,
        marginLeft: 18,
        borderRadius: 8,
        boxShadow: "0 2px 12px #0002",
        minWidth: 280
      }}
    >
      <button onClick={onClose} style={{ float: "right" }}>
        닫기
      </button>
      <div>
        <b>{item.term}</b>
      </div>
      <div style={{ color: '#888' }}>{item.category}</div>
      <div>{item.definition}</div>
      <div style={{ marginTop: 8 }}>{item.example}</div>
      {item.related_terms && (
        <div style={{ marginTop: 8 }}>
          <b>관련:</b> {item.related_terms.join(", ")}
        </div>
      )}
    </div>
  );
}
