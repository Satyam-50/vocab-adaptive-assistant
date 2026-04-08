import React from "react";
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";
import Dashboard from "./pages/Dashboard";
import Home from "./pages/Home";
import ReadingPage from "./pages/ReadingPage";

export default function App() {
	return (
		<AuthProvider>
			<BrowserRouter>
				<div className="app-shell">
					<header className="top-nav">
						<div className="brand">Vocab Adaptive Assistant</div>
						<nav>
							<Link to="/">Home</Link>
							<Link to="/reading">Reading Lab</Link>
							<Link to="/dashboard">Dashboard</Link>
						</nav>
					</header>
					<main className="page-wrap">
						<Routes>
							<Route path="/" element={<Home />} />
							<Route path="/reading" element={<ReadingPage />} />
							<Route path="/dashboard" element={<Dashboard />} />
						</Routes>
					</main>
				</div>
			</BrowserRouter>
		</AuthProvider>
	);
}

