import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

const client = axios.create({
	baseURL: BASE_URL,
	timeout: 20000,
	headers: {
		"Content-Type": "application/json",
	},
});

export async function healthCheck() {
	const response = await client.get("/health");
	return response.data;
}

export async function analyzeText(text) {
	const response = await client.post("/analyze", { text });
	return response.data;
}

export default client;

