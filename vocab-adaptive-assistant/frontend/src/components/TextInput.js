import React, { useState } from "react";

export default function TextInput({ onAnalyze, loading }) {
	const [text, setText] = useState("");

	return (
		<section className="card">
			<h2>Input Text</h2>
			<textarea
				className="text-area"
				rows={9}
				placeholder="Paste any English paragraph to analyze readability and vocabulary difficulty..."
				value={text}
				onChange={(e) => setText(e.target.value)}
			/>
			<div className="actions">
				<button
					className="primary-btn"
					disabled={loading || !text.trim()}
					onClick={() => onAnalyze(text)}
				>
					{loading ? "Analyzing..." : "Analyze Text"}
				</button>
			</div>
		</section>
	);
}

