import React from "react";

export default function WordTooltip({ item }) {
	return (
		<div className="word-item">
			<div className="word-main">{item.word}</div>
			<div className="word-meaning">{item.meaning}</div>
			<div className="word-synonyms">Synonyms: {item.synonyms.join(", ")}</div>
		</div>
	);
}

