/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiGet, apiDelete, apiPut } from "../lib/api";

export default function CartPage() {
  const [items, setItems] = useState<any[]>([]);
  const [cartData, setCartData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadCart = async () => {
      try {
        const data = await apiGet("/cart");
        setItems(data.items || []);
        setCartData(data);
      } catch (err: any) {
        console.log("Could not load cart");
      } finally {
        setLoading(false);
      }
    };
    loadCart();
  }, []);

  const updateQty = async (id: number, change: number) => {
    const item = items.find((i) => i.order_detail_id === id);
    if (!item) return;
    const newQty = (item.order_quantity || 1) + change;
    if (newQty < 1) return;
    try {
      const data = await apiPut(`/cart/${id}`, { quantity: newQty });
      setItems(data.items || []);
      setCartData(data);
    } catch (err: any) {
      setItems(
        items.map((i) =>
          i.order_detail_id === id ? { ...i, order_quantity: newQty } : i,
        ),
      );
    }
  };

  const removeItem = async (id: number) => {
    try {
      await apiDelete(`/cart/${id}`);
      setItems(items.filter((item) => item.order_detail_id !== id));
    } catch (err: any) {
      console.log("Could not remove item from cart");
    }
  };

  const cancelCart = async () => {
    try {
      await apiDelete("/cart");
    } catch (err: any) {
      console.log("Backend not available, clearing locally");
    }
    setItems([]);
  };
  const shipping = cartData ? cartData.shipping_price : 10;
  const subtotal = items.reduce(
    (sum, item) => sum + (item.unit_price || 0) * (item.order_quantity || 1),
    0,
  );
  const total = subtotal + shipping;

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-gray-300 border-t-gray-900 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-500">Loading cart...</p>
        </div>
      </div>
    );
  }
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-4xl font-medium text-black tracking-tight">
            Cart{" "}
          </h1>
          <p className="text-gray-500 text-sm mt-1">
            Review items before checkout
          </p>
        </div>

        {/* Progress */}
        <div className="bg-white rounded-md shadow-sm mb-6 border">
          <div className="border-b px-6 py-3 text-sm text-center text-gray-700">
            <span className="text-blue-600 font-medium">STEP 1: Configure</span>
            <span className="mx-2 text-gray-400">→</span>
            <span className="text-blue-600 font-medium">STEP 2: Cart</span>
            <span className="mx-2 text-gray-400">→</span>
            <span className="text-blue-600 font-medium">STEP 3: Pay</span>
            <span className="mx-2 text-gray-400">→</span>
            <span className="text-green-600 font-medium">Done!</span>
          </div>

          <div className="grid grid-cols-5 gap-4 p-4">
            <div className="rounded-md bg-blue-700 py-2 text-center text-white text-sm font-medium">
              ✓ Browse
            </div>
            <div className="rounded-md bg-blue-700 py-2 text-center text-white text-sm font-medium">
              ✓ Configure
            </div>
            <div className="rounded-md bg-black py-2 text-center text-white text-sm font-medium">
              Cart
            </div>
            <div className="rounded-md bg-gray-100 py-2 text-center text-sm text-gray-700">
              Checkout
            </div>
            <div className="rounded-md bg-gray-100 py-2 text-center text-sm text-gray-700">
              Done
            </div>
          </div>
        </div>

        {/* Cart Label */}
        <div className="mb-5">
          <h2 className="inline-block border-b-2 border-gray-200 pb-1 text-2xl text-black font-medium">
            Your cart{" "}
            <span className="text-sm text-gray-500">
              ({items.length} items)
            </span>
          </h2>
        </div>

        {items.length === 0 ? (
          <div className="bg-white rounded-md shadow-sm border p-10 text-center">
            <p className="text-lg text-gray-600 mb-4">Your cart is empty</p>
            <Link
              href="/"
              className="inline-block rounded-md bg-black px-5 py-2 text-white text-sm font-medium hover:bg-gray-800"
            >
              Browse models
            </Link>
          </div>
        ) : (
          <div className="md:flex md:items-start md:gap-8">
            {/* Items column */}
            <div className="flex-1">
              <div className="space-y-4">
                {items.map((item) => (
                  <div
                    key={item.order_detail_id || item.id}
                    className="bg-white border rounded-lg shadow-sm p-4 flex gap-4 items-center"
                  >
                    <div className="shrink-0 h-24 w-24 rounded-md bg-gray-100 border overflow-hidden flex items-center justify-center">
                      {item.model_image ? (
                        <img
                          src={`http://127.0.0.1:5000/api/models/images/${item.model_image.split("/").pop()}`}
                          alt={item.model_name}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <span className="text-lg font-medium text-gray-500">
                          {item.model_name?.charAt(0) || "?"}
                        </span>
                      )}
                    </div>

                    <div className="flex-1">
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="text-xl text-black font-medium">
                            {item.model_name || item.name || "Model"}
                          </h3>
                          <p className="text-sm text-blue-600 font-medium mt-1">
                            {item.material_name || item.material || "--"} —
                            Scale: {item.scale || 100}% — Infill:{" "}
                            {item.infill_percent || 50}%
                          </p>
                        </div>

                        <div className="text-right">
                          <div className="text-lg text-gray-800 font-medium">
                            $
                            {(
                              (item.unit_price || item.price || 0) *
                              (item.order_quantity || item.qty || 1)
                            ).toFixed(2)}
                          </div>
                          <button
                            onClick={() =>
                              removeItem(item.order_detail_id || item.id)
                            }
                            className="mt-2 text-sm text-red-600 hover:underline"
                          >
                            Remove
                          </button>
                        </div>
                      </div>

                      <div className="mt-3 flex items-center gap-4">
                        <div className="inline-flex items-center rounded-md border bg-white">
                          <button
                            onClick={() =>
                              updateQty(item.order_detail_id || item.id, -1)
                            }
                            aria-label="decrease"
                            className="px-3 py-2 text-gray-700 hover:bg-gray-50"
                          >
                            −
                          </button>
                          <div className="px-4 py-2 text-sm text-gray-900">
                            {item.order_quantity || item.qty || 1}
                          </div>
                          <button
                            onClick={() =>
                              updateQty(item.order_detail_id || item.id, 1)
                            }
                            aria-label="increase"
                            className="px-3 py-2 text-gray-700 hover:bg-gray-50"
                          >
                            +
                          </button>
                        </div>

                        <div className="text-sm text-gray-500">
                          Unit: $
                          {(item.unit_price || item.price || 0).toFixed(2)}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Actions */}
              <div className="mt-6 flex gap-3">
                <button
                  onClick={cancelCart}
                  className="rounded-md bg-red-600 text-white px-4 py-2 text-sm font-medium hover:bg-red-700"
                >
                  Cancel cart
                </button>

                <Link
                  href="/"
                  className="rounded-md border px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  ← Keep shopping
                </Link>
              </div>
            </div>

            {/* Summary column */}
            <aside className="w-full md:w-96 mt-6 md:mt-0">
              <div className="sticky top-6 bg-white border rounded-lg shadow-sm p-5">
                <div className="flex justify-between text-sm text-gray-600">
                  <span>Subtotal</span>
                  <span className="text-gray-900 font-medium">
                    ${subtotal.toFixed(2)}
                  </span>
                </div>

                <div className="flex justify-between text-sm text-gray-600 mt-3">
                  <span>Shipping</span>
                  <span className="text-gray-900 font-medium">
                    ${shipping.toFixed(2)}
                  </span>
                </div>

                <div className="border-t mt-4 pt-4">
                  <div className="flex justify-between items-baseline">
                    <span className="text-lg text-gray-700">TOTAL</span>
                    <span className="text-2xl text-black font-medium">
                      ${total.toFixed(2)}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    incl. $10 Canada Post
                  </p>
                </div>

                <Link
                  href="/checkout"
                  className="mt-5 block w-full rounded-md bg-black text-white text-center py-3 text-sm font-medium hover:bg-gray-900"
                >
                  Proceed to Checkout →
                </Link>
              </div>
            </aside>
          </div>
        )}
      </div>
    </div>
  );
}
