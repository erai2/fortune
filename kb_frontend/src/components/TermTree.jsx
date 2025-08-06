import React from "react";
export default function TermTree({ items, onSelect }) {
  const cats = {};
  items.forEach(t => {
    cats[t.category] = cats[t.category] || [];
    cats[t.category].push(t);
  });
  return (
    <div
      style={{
        background: '#f9fafb',
        padding: 16,
        borderRadius: 8,
        minWidth: 350,
        maxHeight: 400,
        overflow: 'auto'
      }}
    >
      {Object.keys(cats).map(cat => (
        <div key={cat}>
          <b>{cat}</b>
          <ul>
            {cats[cat].map(t => (
              <li key={t.id} style={{ cursor: 'pointer' }} onClick={() => onSelect(t)}>
                {t.term}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
