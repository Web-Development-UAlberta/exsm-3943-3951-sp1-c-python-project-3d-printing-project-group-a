"use client";

import Link from "next/link";

export default function ProfilePage() {
  // hardcoded user data — later comes from backend
  const user = {
    username: "Robel_M",
    fullName: "Robel Measho",
    email: "R@email.com",
    phone: "780-555-0101",
    city: "Fox Creek, AB",
    postalCode: "T5A 0A1",
  };

  // hardcoded orders — later comes from backend
  const orders = [
    { id: "ORD-001", item: "Desk Vase", status: "Printing", date: "Apr 28" },
    { id: "ORD-002", item: "D20 Dice x2", status: "Shipped", date: "Apr 22" },
    { id: "ORD-003", item: "Cable Clip", status: "Pending", date: "Apr 30" },
    {
      id: "ORD-004",
      item: "Iron Man Bust",
      status: "Completed",
      date: "Apr 15",
    },
    { id: "ORD-005", item: "DNA Model", status: "Completed", date: "Apr 10" },
  ];

  const statusColor: Record<string, string> = {
    Pending: "bg-yellow-100 text-yellow-800",
    Printing: "bg-blue-100 text-blue-800",
    Shipped: "bg-purple-100 text-purple-800",
    Completed: "bg-green-100 text-green-800",
  };

  return (
    <div>
      {/* Profile Info */}
      <h1 className="text-2xl text-black font-bold mb-6">My profile</h1>
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-8">
        <div className="flex items-center gap-6 mb-6">
          <div className="w-16 h-16 bg-gray-300 rounded-full flex items-center justify-center">
            <span className="text-xl font-bold text-gray-600">RM</span>
          </div>
          <div>
            <h2 className="text-lg text-black font-semibold">
              {user.fullName}
            </h2>
            <p className="text-sm text-gray-500">@{user.username}</p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-black">Email</p>
            <p className="text-sm text-gray-500  font-medium">{user.email}</p>
          </div>
          <div>
            <p className="text-sm text-black">Phone</p>
            <p className="text-sm text-gray-500  font-medium">{user.phone}</p>
          </div>
          <div>
            <p className="text-sm text-black">City</p>
            <p className="text-sm text-gray-500  font-medium">{user.city}</p>
          </div>
          <div>
            <p className="text-sm text-black">Postal code</p>
            <p className="text-sm. text-gray-500  font-medium">
              {user.postalCode}
            </p>
          </div>
        </div>

        <Link
          href="/profile/edit"
          className="mt-4 inline-block bg-gray-900 text-white px-6 py-2 rounded-lg text-sm font-medium hover:bg-gray-800"
        >
          Edit profile
        </Link>
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
                Ship date
              </th>
              <th className="text-left px-4 py-3 text-sm font-semibold text-gray-700"></th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id} className="border-t border-gray-100">
                <td className="px-4 py-3 text-sm text-gray-500 font-medium">
                  {order.id}
                </td>
                <td className="px-4 py-3 text-gray-500 text-sm">
                  {order.item}
                </td>
                <td className="px-4 py-3">
                  <span
                    className={`text-xs px-2 py-1 rounded-full font-medium ${statusColor[order.status]}`}
                  >
                    {order.status}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm text-gray-500">
                  {order.date}
                </td>
                <td className="px-4 py-3">
                  {order.status === "Pending" && (
                    <button className="text-xs text-red-600 font-medium hover:text-red-800">
                      Cancel
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
