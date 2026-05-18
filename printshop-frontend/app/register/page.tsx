/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { apiPost } from "../lib/api";

export default function RegisterPage() {
  const [form, setForm] = useState({
    username: "",
    password: "",
    full_name: "",
    email: "",
    phone_number: "",
    city: "",
    street_address: "",
    province: "",
    postal_code: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRegister = async () => {
    setError("");
    setLoading(true);

    try {
      await apiPost("/auth/register", form);
      router.push("/login");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center">
      <div className="bg-white border border-gray-200 rounded-lg p-8 w-full max-w-lg">
        <h1 className="text-2xl font-bold text-center mb-6">
          Create your account
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
            name="username"
            placeholder="e.g. Robel_M"
            value={form.username}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Password
          </label>
          <input
            name="password"
            type="password"
            placeholder="min 8 chars -- include a number and symbol"
            value={form.password}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Full name
          </label>
          <input
            name="full_name"
            placeholder="e.g. Robel Measho"
            value={form.full_name}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Email address
          </label>
          <input
            name="email"
            type="email"
            placeholder="e.g. R@email.com"
            value={form.email}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Phone number
          </label>
          <input
            name="phone_number"
            placeholder="e.g. 780-555-0101"
            value={form.phone_number}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
          />
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              City
            </label>
            <input
              name="city"
              placeholder="e.g. Fox Creek"
              value={form.city}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Street address
            </label>
            <input
              name="street_address"
              placeholder="e.g. 123 Main St"
              value={form.street_address}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Province
            </label>
            <input
              name="province"
              placeholder="e.g. AB"
              value={form.province}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Postal code
            </label>
            <input
              name="postal_code"
              placeholder="e.g. T5A 0A1"
              value={form.postal_code}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
            />
          </div>
        </div>

        <button
          onClick={handleRegister}
          disabled={loading}
          className={`w-full py-2.5 rounded-lg font-medium text-sm ${
            loading
              ? "bg-gray-400 text-white cursor-not-allowed"
              : "bg-gray-900 text-white hover:bg-gray-800"
          }`}
        >
          {loading ? "Creating account..." : "Create my account"}
        </button>

        <p className="text-sm text-center text-gray-500 mt-4">
          Already have an account?{" "}
          <Link href="/login" className="text-gray-900 font-medium underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
