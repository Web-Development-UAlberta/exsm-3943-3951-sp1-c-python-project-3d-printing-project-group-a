/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import Link from "next/link";
import { useState, useEffect } from "react";
import { apiGet, apiDelete } from "../lib/api";

export default function ProfilePage() {
  const [user, setUser] = useState<any>(null);
  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const [userData, ordersData] = await Promise.all([
          apiGet("/users/me"),
          apiGet("/orders"),
        ]);
        setUser(userData);
        setOrders(ordersData.slice(0, 5));
      } catch (err: any) {
        console.log("Could not load profile");
      } finally {
        setLoading(false);
      }
    };
    loadProfile();
  }, []);

  const statusColor: Record<string, string> = {
    Pending: "bg-yellow-100 text-yellow-800",
    Printing: "bg-blue-100 text-blue-800",
    Shipped: "bg-purple-100 text-purple-800",
    Completed: "bg-green-100 text-green-800",
  };
  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-gray-300 border-t-gray-900 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-500">Loading profile...</p>
        </div>
      </div>
    );
  }

  if (!user) return null;

  const deleteAccount = async () => {
    if (
      !confirm(
        "Are you sure you want to permanently delete your account? This cannot be undone.",
      )
    )
      return;
    try {
      await apiDelete(`/users/me`);
      localStorage.clear();
      alert("Your account has been deleted. Thank you for using PrintShop!");
      window.location.href = "/";
    } catch (err: any) {
      alert("Could not delete account. Please try again.");
    }
  };
  const hasOrders = orders.length > 0;

  return (
    <div>
      {/* Profile Info */}
      <h1 className="text-2xl text-black font-bold mb-6">My profile</h1>
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-8">
        <div className="flex items-center gap-6 mb-6">
          <div className="w-16 h-16 bg-gray-300 rounded-full flex items-center justify-center">
            <span className="text-xl font-bold text-gray-600">
              {user.full_name
                ?.split(" ")
                .map((n: string) => n[0])
                .join("")
                .toUpperCase()}
            </span>
          </div>
          <div>
            <h2 className="text-lg text-black font-semibold">
              {user.full_name}
            </h2>
            <p className="text-sm text-gray-500">@{user.username}</p>
          </div>
        </div>

        <div>
          <p className="text-sm text-black">Email</p>
          <p className="text-sm text-gray-500 font-medium">{user.email}</p>
        </div>
        <div>
          <p className="text-sm text-black">Phone</p>
          <p className="text-sm text-gray-500 font-medium">
            {user.phone_number}
          </p>
        </div>
        <div>
          <p className="text-sm text-black">City</p>
          <p className="text-sm text-gray-500 font-medium">{user.city}</p>
        </div>
        <div>
          <p className="text-sm text-black">Postal code</p>
          <p className="text-sm text-gray-500 font-medium">
            {user.postal_code}
          </p>
        </div>

        <div className="mt-4 flex gap-3">
          <Link
            href="/profile/edit"
            className="inline-block bg-gray-900 text-white px-6 py-2 rounded-lg text-sm font-medium hover:bg-gray-800"
          >
            Edit profile
          </Link>
          <button
            onClick={deleteAccount}
            className="inline-block bg-red-600 text-white px-6 py-2 rounded-lg text-sm font-medium hover:bg-red-700"
          >
            Delete account
          </button>
        </div>
      </div>

      {/* Order History */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-black">My orders</h2>
        <Link
          href="/orders"
          className="text-sm text-gray-600 hover:text-gray-900 underline"
        >
          View all orders
        </Link>
      </div>

      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="text-left px-4 py-3 text-sm font-semibold text-gray-700">
                Order ID
              </th>
              <th className="text-left px-4 py-3 text-sm font-semibold text-gray-700">
                Item
              </th>
              <th className="text-left px-4 py-3 text-sm font-semibold text-gray-700">
                Status
              </th>
              <th className="text-left px-4 py-3 text-sm font-semibold text-gray-700">
                Date
              </th>
              <th className="text-left px-4 py-3 text-sm font-semibold text-gray-700">
                Total
              </th>
              <th className="text-left px-4 py-3 text-sm font-semibold text-gray-700"></th>
            </tr>
          </thead>
          <tbody>
            {!hasOrders ? (
              <tr>
                <td
                  colSpan={5}
                  className="px-4 py-8 text-center text-sm text-gray-500"
                >
                  No orders yet
                </td>
              </tr>
            ) : (
              orders.map((order) => (
                <tr
                  key={order.order_header_id || order.id}
                  className="border-t border-gray-100"
                >
                  <td className="px-4 py-3 text-sm text-gray-500 font-medium">
                    #{order.order_id || order.order_header_id || order.id}
                  </td>
                  <td className="px-4 py-3 text-gray-500 text-sm">
                    {order.items?.[0]?.model || order.item || "--"}
                  </td>
                  <td className="px-4 py-3">
                    <span
                      className={`text-xs px-2 py-1 rounded-full font-medium ${statusColor[order.order_status || order.status] || "bg-gray-100 text-gray-600"}`}
                    >
                      {order.order_status || order.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500">
                    {order.order_date || "--"}
                  </td>
                  <td className="px-4 py-3 text-sm font-medium text-gray-900">
                    ${(order.total_price || 0).toFixed(2)}
                  </td>
                  <td className="px-4 py-3">
                    {order.order_status === "Pending" && (
                      <button className="text-xs text-red-600 font-medium hover:text-red-800">
                        Cancel
                      </button>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
