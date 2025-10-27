import { API_BASE_URL } from "./config";

export async function registerUser(user) {
  const res = await fetch(`${API_BASE_URL}/api/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(user),
  });

  let data = {};
  try {
    data = await res.json();
  } catch (err) {
    console.error("Error parsing response:", err);
  }

  if (!res.ok) {
    throw { response: { data } };
  }

  return data;
}
