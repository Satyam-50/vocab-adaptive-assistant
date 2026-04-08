import React from "react";
import { Link } from "react-router-dom";

export default function Home() {
	return (
		<section className="hero">
			<div>
				<h1>Vocabulary Level Adaptive Reading Assistant</h1>
				<p>
					Analyze any English passage, estimate CEFR difficulty, simplify wording,
					and learn tough vocabulary with contextual hints.
				</p>
				<div className="actions">
					<Link to="/reading" className="primary-btn link-btn">
						Open Reading Lab
					</Link>
					<Link to="/dashboard" className="ghost-btn link-btn">
						View Dashboard
					</Link>
				</div>
			</div>
		</section>
	);
}

