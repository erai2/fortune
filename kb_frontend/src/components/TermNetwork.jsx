import React, { useRef, useEffect } from "react";
import { Network, DataSet } from "vis-network/peer";
export default function TermNetwork({ items, onSelect }) {
  const ref = useRef(null);
  useEffect(() => {
    if (!ref.current || !items.length) return;
    const nodes = items.map(t => ({ id: t.id, label: t.term, group: t.category, title: t.definition }));
    const edges = [];
    items.forEach(t => {
      if (Array.isArray(t.related_terms)) {
        t.related_terms.forEach(rt => {
          const target = items.find(tt => tt.term === rt);
          if (target) edges.push({ from: t.id, to: target.id });
        });
      }
    });
    const network = new Network(
      ref.current,
      { nodes: new DataSet(nodes), edges: new DataSet(edges) },
      { nodes: { shape: "dot", size: 20 }, physics: { stabilization: true } }
    );
    network.on("click", params => {
      if (params.nodes.length > 0) {
        const sel = items.find(t => t.id === params.nodes[0]);
        onSelect(sel);
      }
    });
    return () => network.destroy();
  }, [items, onSelect]);
  return <div ref={ref} style={{ width: 500, height: 400, border: "1px solid #bbb", borderRadius: 8 }} />;
}
