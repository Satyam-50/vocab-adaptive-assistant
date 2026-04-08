import React from "react";

const CEFR_SCORE = { A1: 1, A2: 2, B1: 3, B2: 4, C1: 5, C2: 6 };

export default function ProgressChart({ history }) {
	const data = [...history].slice(0, 10).reverse();
	const width = 520;
	const height = 220;
	const padding = 30;

	if (!data.length) {
		return (
			<section className="card">
				<h3>Progress Trend</h3>
				<p>No sessions yet. Analyze text to generate trend data.</p>
			</section>
		);
	}

	const points = data.map((item, i) => {
		const x = padding + (i * (width - padding * 2)) / Math.max(data.length - 1, 1);
		const score = CEFR_SCORE[item.level] || 3;
		const y = height - padding - ((score - 1) / 5) * (height - padding * 2);
		return { x, y, item };
	});

	const path = points.map((p, i) => `${i === 0 ? "M" : "L"}${p.x} ${p.y}`).join(" ");

	return (
		<section className="card">
			<h3>Progress Trend</h3>
			<svg viewBox={`0 0 ${width} ${height}`} className="chart-svg">
				<line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} stroke="#486581" />
				<line x1={padding} y1={padding} x2={padding} y2={height - padding} stroke="#486581" />
				<path d={path} fill="none" stroke="#f0b429" strokeWidth="3" />
				{points.map((p, idx) => (
					<circle key={idx} cx={p.x} cy={p.y} r="4" fill="#102a43" />
				))}
			</svg>
		</section>
	);
}

