/* eslint-disable react-hooks/set-state-in-effect */
"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function Navbar() {
  const [loggedIn, setLoggedIn] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    setLoggedIn(!!token);
  }, []);

  const handleSignOut = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user_id");
    setLoggedIn(false);
    router.push("/login");
  };

  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link href="/" className="text-xl font-bold text-gray-900">
          PrintShop
        </Link>
        <div className="flex items-center gap-6">
          <Link href="/" className="text-gray-600 hover:text-gray-900">
            Models
          </Link>
          <Link href="/cart" className="text-gray-600 hover:text-gray-900">
            Cart
          </Link>
          <Link href="/orders" className="text-gray-600 hover:text-gray-900">
            Orders
          </Link>
          <Link href="/profile" className="text-gray-600 hover:text-gray-900">
            Profile
          </Link>

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
