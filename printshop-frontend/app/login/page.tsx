"use client";

import { useState } from "react";
import Link from "next/link";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    // later this will connect to Rami's backend
    console.log("Login:", username, password);
  };

  return (
    <div className="flex justify-center items-center min-h-[80vh]">
      <div className="bg-white border border-gray-200 rounded-lg p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold text-center mb-6">Welcome back</h1>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Username
          </label>
          <input
            type="text"
            placeholder="Enter your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
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
            className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
          />
        </div>

        <button
          onClick={handleLogin}
          className="w-full bg-gray-900 text-white py-2.5 rounded-lg font-medium text-sm hover:bg-gray-800"
        >
          Sign in
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
