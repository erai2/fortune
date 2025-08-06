export async function addTermAPI(text, related_terms = []) {
  const res = await fetch("http://localhost:8000/api/terms", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, related_terms })
  });
  return await res.json();
}

export async function getTermsAPI() {
  const res = await fetch("http://localhost:8000/api/terms");
  return await res.json();
}

export async function searchTermsAPI(query) {
  const res = await fetch("http://localhost:8000/api/terms/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  });
  return await res.json();
}
