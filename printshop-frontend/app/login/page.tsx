/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { apiPost } from "../lib/api";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async () => {
    setError("");
    setLoading(true);

    try {
      const data = await apiPost("/auth/login", { username, password });
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user_id", data.user_id);
      router.push("/");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-[80vh]">
      <div className="bg-white border border-gray-200 rounded-lg p-8 w-full max-w-md">
        <h1 className="text-black text-2xl font-bold text-center mb-6">
          Welcome back
        </h1>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Username
          </label>
          <input
            type="text"
            placeholder="Enter your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="text-black w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
          />
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Password
          </label>
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="text-black w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
          />
        </div>

        <button
          onClick={handleLogin}
          disabled={loading}
          className={`w-full py-2.5 rounded-lg font-medium text-sm ${
            loading
              ? "bg-gray-400 text-white cursor-not-allowed"
              : "bg-gray-900 text-white hover:bg-gray-800"
          }`}
        >
          {loading ? "Signing in..." : "Sign in"}
        </button>

        <p className="text-sm text-center text-gray-500 mt-4">
          No account yet?{" "}
          <Link
            href="/register"
            className="text-gray-900 font-medium underline"
          >
            Create one
          </Link>
        </p>
      </div>
    </div>
  );
}
