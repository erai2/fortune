import React from "react";
export default function TermCardList({ items, onClick }) {
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 14 }}>
      {items.map(item => (
        <div
          key={item.id}
          onClick={() => onClick(item)}
          style={{
            background: "#f5f7fa",
            borderRadius: 8,
            padding: 16,
            width: 250,
            cursor: "pointer",
            boxShadow: "0 2px 8px #0001",
            marginBottom: 10
          }}
        >
          <b>{item.term}</b>
          <br />
          <span style={{ fontSize: 12, color: '#888' }}>{item.category}</span>
          <div style={{ marginTop: 6 }}>{item.definition}</div>
        </div>
      ))}
    </div>
  );
}
