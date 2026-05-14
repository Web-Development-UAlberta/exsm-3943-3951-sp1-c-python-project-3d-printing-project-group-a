"use client";

import { useState } from "react";
import Link from "next/link";

export default function CartPage() {
  const [items, setItems] = useState([
    {
      id: 1,
      name: "Desk Vase",
      material: "PLA",
      color: "Black",
      price: 75.16,
      qty: 1,
    },
    {
      id: 2,
      name: "D20 Dice",
      material: "PETG",
      color: "Blue",
      price: 42.0,
      qty: 2,
    },
    {
      id: 3,
      name: "Cable Clip",
      material: "PLA",
      color: "White",
      price: 18.75,
      qty: 1,
    },
  ]);

  const shipping = 10;

  const updateQty = (id: number, change: number) => {
    setItems(
      items.map((item) => {
        if (item.id === id) {
          const newQty = item.qty + change;

          if (newQty < 1) return item;

          return {
            ...item,
            qty: newQty,
          };
        }

        return item;
      }),
    );
  };

  const removeItem = (id: number) => {
    setItems(items.filter((item) => item.id !== id));
  };

  const cancelCart = () => {
    setItems([]);
  };

  const subtotal = items.reduce((sum, item) => sum + item.price * item.qty, 0);

  const total = subtotal + shipping;

  // Replace the JSX return from your component with the following:
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
                    key={item.id}
                    className="bg-white border rounded-lg shadow-sm p-4 flex gap-4 items-center"
                  >
                    <div className="flex-shrink-0 h-24 w-24 rounded-md bg-gray-100 border flex items-center justify-center text-sm text-gray-500">
                      [img]
                    </div>

                    <div className="flex-1">
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="text-xl text-black font-medium">
                            {item.name}
                          </h3>
                          <p className="text-sm text-blue-600 font-medium mt-1">
                            {item.material} / {item.color}
                          </p>
                        </div>

                        <div className="text-right">
                          <div className="text-lg text-gray-800 font-medium">
                            ${(item.price * item.qty).toFixed(2)}
                          </div>
                          <button
                            onClick={() => removeItem(item.id)}
                            className="mt-2 text-sm text-red-600 hover:underline"
                          >
                            Remove
                          </button>
                        </div>
                      </div>

                      <div className="mt-3 flex items-center gap-4">
                        <div className="inline-flex items-center rounded-md border bg-white">
                          <button
                            onClick={() => updateQty(item.id, -1)}
                            aria-label="decrease"
                            className="px-3 py-2 text-gray-700 hover:bg-gray-50"
                          >
                            −
                          </button>
                          <div className="px-4 py-2 text-sm text-gray-900">
                            {item.qty}
                          </div>
                          <button
                            onClick={() => updateQty(item.id, 1)}
                            aria-label="increase"
                            className="px-3 py-2 text-gray-700 hover:bg-gray-50"
                          >
                            +
                          </button>
                        </div>

                        <div className="text-sm text-gray-500">
                          Unit: ${item.price.toFixed(2)}
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
