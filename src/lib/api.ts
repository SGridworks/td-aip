const API_BASE = 'http://localhost:8000/api/v1';

export async function fetchAssets() {
  const res = await fetch(`${API_BASE}/assets`);
  if (!res.ok) throw new Error('Failed to fetch assets');
  return res.json();
}

export async function fetchAsset(id: string) {
  const res = await fetch(`${API_BASE}/assets/${id}`);
  if (!res.ok) throw new Error('Failed to fetch asset');
  return res.json();
}

export async function fetchProjects() {
  const res = await fetch(`${API_BASE}/investment/projects`);
  if (!res.ok) throw new Error('Failed to fetch projects');
  return res.json();
}
