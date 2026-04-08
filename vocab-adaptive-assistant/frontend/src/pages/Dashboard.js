import React from "react";

import ProgressChart from "../components/ProgressChart";
import useUserProgress from "../hooks/useUserProgress";

export default function Dashboard() {
	const { progress } = useUserProgress();

	return (
		<div className="stack">
			<section className="card stats-grid">
				<div>
					<div className="stat-label">Texts Processed</div>
					<div className="stat-value">{progress.stats.textsProcessed}</div>
				</div>
				<div>
					<div className="stat-label">Words Learned</div>
					<div className="stat-value">{progress.stats.wordsLearned}</div>
				</div>
				<div>
					<div className="stat-label">Last Level</div>
					<div className="stat-value">{progress.stats.lastLevel}</div>
				</div>
			</section>

			<ProgressChart history={progress.history} />

			<section className="card">
				<h3>Recent Sessions</h3>
				<ul className="session-list">
					{progress.history.length === 0 ? (
						<li>No sessions yet.</li>
					) : (
						progress.history.slice(0, 8).map((entry, idx) => (
							<li key={idx}>
								<span>{new Date(entry.date).toLocaleString()}</span>
								<span>{entry.level}</span>
								<span>{entry.difficultWordCount} difficult words</span>
							</li>
						))
					)}
				</ul>
			</section>
		</div>
	);
}

