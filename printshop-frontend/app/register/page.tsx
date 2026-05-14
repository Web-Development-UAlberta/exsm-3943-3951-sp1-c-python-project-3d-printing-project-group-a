"use client";

import { useState } from "react";
import Link from "next/link";

export default function RegisterPage() {
  const [form, setForm] = useState({
    username: "",
    password: "",
    fullName: "",
    email: "",
    phone: "",
    city: "",
    street: "",
    province: "",
    postalCode: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };


  const handleRegister = () => {
    // later this will connect to Rami's backend
    console.log("Register:", form);
  };

  return (
    <div className="flex justify-center">
      <div className="bg-white border border-gray-200 rounded-lg p-8 w-full max-w-lg">
        <h1 className="text-2xl font-bold text-center text-black mb-6">
          Create your account
        </h1>

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
            name="fullName"
            placeholder="e.g. Robel Measho"
            value={form.fullName}
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
            name="phone"
            placeholder="e.g. 780-555-0101"
            value={form.phone}
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
              name="street"
              placeholder="e.g. 123 Main St"
              value={form.street}
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
              name="postalCode"
              placeholder="e.g. T5A 0A1"
              value={form.postalCode}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
            />
          </div>
        </div>

        <button
          onClick={handleRegister}
          className="w-full bg-gray-900 text-white py-2.5 rounded-lg font-medium text-sm hover:bg-gray-800"
        >
          Create my account
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
