/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import Link from "next/link";
import { useMemo, useState, useEffect } from "react";
import { apiGet, apiPut } from "../lib/api";

export default function OrdersPage() {
  const [selectedOrder, setSelectedOrder] = useState("");
  const [orders, setOrders] = useState<any[]>([]);
  const [orderDetails, setOrderDetails] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadOrders = async () => {
      try {
        const data = await apiGet("/orders");
        setOrders(data);
        if (data.length > 0) {
          setSelectedOrder(data[0].order_id);
        }
      } catch (err: any) {
        console.log("Could not load orders");
      } finally {
        setLoading(false);
      }
    };
    loadOrders();
  }, []);

  useEffect(() => {
    if (!selectedOrder) return;
    const loadDetail = async () => {
      try {
        const data = await apiGet(`/orders/${selectedOrder}`);
        setOrderDetails((prev) => ({ ...prev, [selectedOrder]: data }));
      } catch (err: any) {
        console.log("Could not load order detail");
      }
    };
    loadDetail();
  }, [selectedOrder]);

  const statusStyles: Record<string, string> = {
    Pending: "bg-yellow-100 text-yellow-800 border border-yellow-200",

    Printing: "bg-blue-100 text-blue-800 border border-blue-200",

    Shipped: "bg-purple-100 text-purple-800 border border-purple-200",

    Completed: "bg-green-100 text-green-800 border border-green-200",
  };

  const selected = orderDetails[selectedOrder] || null;

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-gray-300 border-t-gray-900 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-500">Loading orders...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="mx-auto max-w-7xl px-6 py-10">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-gray-900">
              My Orders
            </h1>

            <p className="mt-1 text-sm text-gray-500">
              Track and manage your 3D printing orders
            </p>
          </div>

          <Link
            href="/"
            className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-100"
          >
            ← Continue Shopping
          </Link>
        </div>

        {/* Status Guide */}
        <div className="mb-8 grid gap-4 md:grid-cols-4">
          <div className="rounded-xl border border-yellow-200 bg-yellow-50 p-4">
            <p className="text-sm font-semibold text-yellow-800">Pending</p>

            <p className="mt-1 text-xs text-yellow-700">
              Waiting to begin printing
            </p>
          </div>

          <div className="rounded-xl border border-blue-200 bg-blue-50 p-4">
            <p className="text-sm font-semibold text-blue-800">Printing</p>

            <p className="mt-1 text-xs text-blue-700">
              Currently printing on MK4
            </p>
          </div>

          <div className="rounded-xl border border-purple-200 bg-purple-50 p-4">
            <p className="text-sm font-semibold text-purple-800">Shipped</p>

            <p className="mt-1 text-xs text-purple-700">
              In transit with Canada Post
            </p>
          </div>

          <div className="rounded-xl border border-green-200 bg-green-50 p-4">
            <p className="text-sm font-semibold text-green-800">Completed</p>

            <p className="mt-1 text-xs text-green-700">
              Successfully delivered
            </p>
          </div>
        </div>

        {/* Orders Table */}
        <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
          <div className="border-b border-gray-200 px-6 py-4">
            <h2 className="text-lg font-semibold text-gray-900">
              Order History
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Select an order to view details
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                    Order ID
                  </th>

                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                    Item
                  </th>

                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                    Status
                  </th>

                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                    Total
                  </th>

                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">
                    Date
                  </th>

                  <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">
                    Action
                  </th>
                </tr>
              </thead>

              <tbody>
                {orders.length === 0 ? (
                  <tr>
                    <td
                      colSpan={6}
                      className="px-6 py-10 text-center text-sm text-gray-500"
                    >
                      No orders yet —{" "}
                      <Link href="/" className="text-blue-600 underline">
                        browse models
                      </Link>
                    </td>
                  </tr>
                ) : (
                  orders.map((order) => (
                    <tr
                      key={order.order_id}
                      onClick={() => setSelectedOrder(order.order_id)}
                      className={`cursor-pointer border-t border-gray-100 transition hover:bg-gray-50 ${
                        selectedOrder === order.order_id
                          ? "bg-blue-50"
                          : "bg-white"
                      }`}
                    >
                      <td className="px-6 py-5 text-sm font-semibold text-gray-900">
                        #{order.order_id}
                      </td>
                      <td className="px-6 py-5 text-sm text-gray-700">
                        {order.items?.[0]?.model || "--"}
                      </td>
                      <td className="px-6 py-5">
                        <span
                          className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${statusStyles[order.order_status || order.status] || "bg-gray-100 text-gray-600"}`}
                        >
                          {order.order_status || order.status}
                        </span>
                      </td>
                      <td className="px-6 py-5 text-sm font-medium text-gray-900">
                        ${(order.total_price || 0).toFixed(2)}
                      </td>
                      <td className="px-6 py-5 text-sm text-gray-500">
                        {order.order_date || "--"}
                      </td>

                      <td className="px-6 py-5 text-right">
                        <div className="flex items-center justify-end gap-3">
                          {selectedOrder === order.id && (
                            <span className="text-xs font-medium text-blue-600">
                              Viewing
                            </span>
                          )}
                          {order.order_status === "Pending" && (
                            <button
                              onClick={async (e) => {
                                e.stopPropagation();
                                try {
                                  await apiPut(
                                    `/orders/${order.order_id}/cancel`,
                                    {},
                                  );
                                  setOrders(
                                    orders.map((o) =>
                                      o.order_id === order.order_id
                                        ? { ...o, order_status: "Cancelled" }
                                        : o,
                                    ),
                                  );
                                } catch (err: any) {
                                  console.log("Could not cancel order");
                                }
                              }}
                              className="text-sm font-medium text-red-600 transition hover:text-red-800"
                            >
                              Cancel
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        <p className="mt-3 text-xs text-gray-500">
          Orders can only be cancelled while in Pending status.
        </p>

        {/* Detail Cards */}
        {selected && (
          <div className="mt-8 grid gap-6 lg:grid-cols-2">
            {/* Left */}
            <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
              <div className="mb-6 flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900">
                    Order Details
                  </h3>

                  <p className="mt-1 text-sm text-gray-500">{selectedOrder}</p>
                </div>

                <span
                  className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${
                    statusStyles[
                      orders.find((o) => o.order_id === selectedOrder)
                        ?.order_status || "Pending"
                    ] || "bg-gray-100 text-gray-600"
                  }`}
                >
                  {
                    orders.find((o) => o.order_id === selectedOrder)
                      ?.order_status
                  }
                </span>
              </div>

              <div className="space-y-4">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Order Date</span>

                  <span className="font-medium text-gray-900">
                    {selected.order_date || "--"}
                  </span>
                </div>

                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Completion Date</span>

                  <span className="font-medium text-gray-900">
                    {selected.completion || "--"}
                  </span>
                </div>

                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Ship Date</span>

                  <span className="font-medium text-gray-900">
                    {selected.tracking_number ? selected.order_date : "--"}
                  </span>
                </div>

                {selected.tracking_number && (
                  <div className="rounded-xl border border-gray-200 bg-gray-50 p-4">
                    <p className="text-sm font-medium text-gray-700">
                      Tracking Number
                    </p>

                    <p className="mt-1 text-sm text-gray-900">
                      {selected.tracking_number}
                    </p>

                    <Link
                      href="https://www.canadapost-postescanada.ca/track-reperage/en"
                      target="_blank"
                      className="mt-3 inline-block text-sm font-medium text-blue-600 hover:underline"
                    >
                      Track package →
                    </Link>
                  </div>
                )}

                <div className="border-t border-gray-200 pt-4">
                  <div className="mb-2 flex justify-between text-sm">
                    <span className="text-gray-500">Subtotal</span>

                    <span className="font-medium text-gray-900">
                      $
                      {(
                        (selected.total_price || 0) -
                        (selected.shipping_price || 10)
                      ).toFixed(2)}
                    </span>
                  </div>

                  <div className="mb-4 flex justify-between text-sm">
                    <span className="text-gray-500">Shipping</span>

                    <span className="font-medium text-gray-900">
                      $
                      {(
                        selected.shipping_price ||
                        selected.shipping ||
                        10
                      ).toFixed(2)}
                    </span>
                  </div>

                  <div className="flex justify-between text-lg font-semibold text-gray-900">
                    <span>Total</span>

                    <span>
                      $
                      {(selected.total_price || selected.total || 0).toFixed(2)}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Right */}
            <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
              <div className="mb-6">
                <h3 className="text-xl font-semibold text-gray-900">
                  Items in Order
                </h3>

                <p className="mt-1 text-sm text-gray-500">
                  Products included in this shipment
                </p>
              </div>

              <div className="space-y-4">
                {(selected.items || selected.order_details || []).map(
                  (item: any, i: number) => (
                    <div
                      key={i}
                      className="flex items-center justify-between rounded-xl border border-gray-200 p-4"
                    >
                      <div className="flex items-center gap-4">
                        <div className="flex h-16 w-16 items-center justify-center rounded-lg bg-gray-100 text-xs text-gray-400">
                          IMG
                        </div>

                        <div>
                          <h4 className="font-medium text-gray-900">
                            {item.model || "Model"}
                          </h4>
                          <p className="mt-1 text-sm text-gray-500">
                            {item.filament} — Scale: {item.scale || "--"}% —
                            Infill: {item.infill || "--"}%
                          </p>
                        </div>
                      </div>

                      <div className="text-right">
                        <p className="text-sm text-gray-500">
                          Qty: {item.quantity || 1}
                        </p>
                        <p className="mt-1 font-semibold text-gray-900">
                          ${(item.unit_price || 0).toFixed(2)}
                        </p>
                      </div>
                    </div>
                  ),
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
