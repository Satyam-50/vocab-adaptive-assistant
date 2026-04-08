import React from "react";

const LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"];

export default function LevelIndicator({ level = "B1" }) {
	const index = Math.max(0, LEVELS.indexOf(level));
	const progress = ((index + 1) / LEVELS.length) * 100;

	return (
		<section className="card">
			<h3>Predicted CEFR Level</h3>
			<div className="level-row">
				<div className="level-chip">{level}</div>
				<div className="level-bar">
					<div className="level-fill" style={{ width: `${progress}%` }} />
				</div>
			</div>
			<div className="level-labels">
				{LEVELS.map((l) => (
					<span key={l}>{l}</span>
				))}
			</div>
		</section>
	);
}

