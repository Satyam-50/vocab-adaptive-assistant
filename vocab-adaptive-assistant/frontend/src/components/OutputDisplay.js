import React from "react";

import LevelIndicator from "./LevelIndicator";
import WordTooltip from "./WordTooltip";

export default function OutputDisplay({ data }) {
	if (!data) {
		return (
			<section className="card">
				<h2>Analysis Output</h2>
				<p>Run analysis to see simplified text and difficult words.</p>
			</section>
		);
	}

	return (
		<div className="stack">
			<LevelIndicator level={data.level} />

			<section className="card">
				<h3>Simplified Text</h3>
				<p className="simplified">{data.simplified_text}</p>
			</section>

			<section className="card">
				<h3>Difficult Words</h3>
				<div className="word-list">
					{data.difficult_words.length === 0 ? (
						<p>No difficult words detected.</p>
					) : (
						data.difficult_words.map((item) => <WordTooltip key={item.word} item={item} />)
					)}
				</div>
			</section>
		</div>
	);
}

