import React, { useState } from "react";

import OutputDisplay from "../components/OutputDisplay";
import TextInput from "../components/TextInput";
import useUserProgress from "../hooks/useUserProgress";
import { analyzeText } from "../services/api";

export default function ReadingPage() {
	const [loading, setLoading] = useState(false);
	const [result, setResult] = useState(null);
	const [error, setError] = useState("");
	const { addSession } = useUserProgress();

	const handleAnalyze = async (text) => {
		setLoading(true);
		setError("");
		try {
			const data = await analyzeText(text);
			setResult(data);
			addSession(data);
		} catch (err) {
			setError(err?.response?.data?.detail || "Unable to analyze text.");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="grid-two">
			<div>
				<TextInput onAnalyze={handleAnalyze} loading={loading} />
				{error ? <div className="error-box">{error}</div> : null}
			</div>
			<OutputDisplay data={result} />
		</div>
	);
}

