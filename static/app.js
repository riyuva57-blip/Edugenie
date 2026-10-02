const response = await fetch(endpoint, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(body)
});

const contentType = response.headers.get('content-type') || '';
let data;

if (contentType.includes('application/json')) {
  data = await response.json();
} else {
  const rawText = await response.text();
  throw new Error(
    `Server error (${response.status}): ${rawText.slice(0, 200)}`
  );
}

if (!response.ok) {
  throw new Error(data.detail || 'Request failed.');
}