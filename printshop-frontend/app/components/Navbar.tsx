/* eslint-disable react-hooks/set-state-in-effect */
"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { apiGet } from "../lib/api";

export default function Navbar() {
  const [loggedIn, setLoggedIn] = useState(false);
  const router = useRouter();

  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    setLoggedIn(!!token);
    if (token) {
      apiGet("/users/me")
        .then((data) => {
          setIsAdmin(data.is_admin || false);
        })
        .catch(() => {});
    }
  }, []);

  const handleSignOut = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user_id");
    setLoggedIn(false);
    router.push("/login");
  };

  return (
    <nav className="bg-slate-900 border-b border-slate-700 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link href="/" className="text-xl font-bold text-teal-400">
          PrintShop
        </Link>
        <div className="flex items-center gap-6">
          <Link href="/" className="text-gray-100 hover:text-gray-900">
            Models
          </Link>
          <Link href="/cart" className="text-gray-200 hover:text-gray-900">
            Cart
          </Link>
          <Link href="/orders" className="text-gray-200 hover:text-gray-900">
            Orders
          </Link>
          <Link href="/profile" className="text-gray-200 hover:text-gray-900">
            Profile
          </Link>
          {isAdmin && (
            <Link
              href="/admin"
              className="text-purple-600 hover:text-purple-900 font-medium"
            >
              Admin
            </Link>
          )}

          {loggedIn ? (
            <button
              onClick={handleSignOut}
              className="bg-red-600 text-white px-4 py-1.5 rounded-lg text-sm font-medium hover:bg-red-700"
            >
              Sign out
            </button>
          ) : (
            <Link
              href="/login"
              className="bg-gray-900 text-white px-4 py-1.5 rounded-lg text-sm font-medium hover:bg-gray-800"
            >
              Sign in
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
