import { useEffect, useState } from "react";

const STORAGE_KEY = "vaa_progress";

export default function useUserProgress() {
	const [progress, setProgress] = useState(() => {
		const saved = localStorage.getItem(STORAGE_KEY);
		if (saved) return JSON.parse(saved);
		return {
			history: [],
			stats: {
				textsProcessed: 0,
				wordsLearned: 0,
				lastLevel: "B1",
			},
		};
	});

	useEffect(() => {
		localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
	}, [progress]);

	const addSession = (analysisResult) => {
		setProgress((prev) => {
			const session = {
				date: new Date().toISOString(),
				level: analysisResult.level,
				difficultWordCount: analysisResult.difficult_words.length,
			};
			const textsProcessed = prev.stats.textsProcessed + 1;
			const wordsLearned = prev.stats.wordsLearned + analysisResult.difficult_words.length;
			return {
				history: [session, ...prev.history].slice(0, 30),
				stats: {
					textsProcessed,
					wordsLearned,
					lastLevel: analysisResult.level,
				},
			};
		});
	};

	return { progress, addSession };
}

