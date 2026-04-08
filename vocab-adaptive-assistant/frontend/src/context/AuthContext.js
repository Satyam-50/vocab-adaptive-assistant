import React, { createContext, useContext, useMemo, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
	const [user, setUser] = useState(() => {
		const saved = localStorage.getItem("vaa_user");
		return saved ? JSON.parse(saved) : { id: "guest", name: "Guest Learner" };
	});

	const value = useMemo(
		() => ({
			user,
			login: (name) => {
				const next = { id: "guest", name: name || "Guest Learner" };
				setUser(next);
				localStorage.setItem("vaa_user", JSON.stringify(next));
			},
			logout: () => {
				const next = { id: "guest", name: "Guest Learner" };
				setUser(next);
				localStorage.setItem("vaa_user", JSON.stringify(next));
			},
		}),
		[user]
	);

	return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
	const value = useContext(AuthContext);
	if (!value) {
		throw new Error("useAuth must be used inside AuthProvider");
	}
	return value;
}

