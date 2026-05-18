/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { apiGet, apiPost } from "../lib/api";

export default function CheckoutPage() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [placing, setPlacing] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  useEffect(() => {
    const loadCart = async () => {
      try {
        const data = await apiGet("/cart");
        setItems(data.items || data);
      } catch (err: any) {
        console.log("Could not load cart");
      } finally {
        setLoading(false);
      }
    };
    loadCart();
  }, []);

  const subtotal = items.reduce((sum, item) => sum + (item.price || 0), 0);
  const shipping = 10;
  const total = subtotal + shipping;

  const handlePlaceOrder = async () => {
    setError("");
    setPlacing(true);
    try {
      await apiPost("/checkout", {});
      router.push("/orders");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setPlacing(false);
    }
  };
  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-gray-300 border-t-gray-900 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-500">Loading checkout...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="mx-auto max-w-7xl px-6 py-10">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">
            Checkout
          </h1>

          <p className="mt-1 text-sm text-gray-500">
            Secure payment powered by Stripe
          </p>
        </div>

        {/* Progress */}
        <div className="mb-8 overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
          {/* Top Text */}
          <div className="border-b border-gray-200 px-6 py-3 text-center text-sm font-medium">
            <span className="text-green-700">✓ STEP 1: Configure</span>

            <span className="mx-3 text-gray-400">→</span>

            <span className="text-green-700">✓ STEP 2: Cart</span>

            <span className="mx-3 text-gray-400">→</span>

            <span className="text-blue-700 font-semibold">
              STEP 3: Checkout
            </span>

            <span className="mx-3 text-gray-400">→</span>

            <span className="text-gray-400">Done</span>
          </div>

          {/* Status Buttons */}
          <div className="grid grid-cols-4 gap-4 p-4">
            <div className="rounded-xl bg-green-100 py-3 text-center text-sm font-semibold text-green-800 border border-green-200">
              ✓ Configure
            </div>

            <div className="rounded-xl bg-green-100 py-3 text-center text-sm font-semibold text-green-800 border border-green-200">
              ✓ Cart
            </div>

            <div className="rounded-xl bg-black py-3 text-center text-sm font-semibold text-white">
              Checkout
            </div>

            <div className="rounded-xl bg-gray-100 py-3 text-center text-sm font-semibold text-gray-500 border border-gray-200">
              Done
            </div>
          </div>
        </div>

        {/* Main Layout */}
        <div className="grid gap-8 lg:grid-cols-2">
          {/* Left Side */}
          <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
            <div className="mb-6">
              <h2 className="text-xl font-semibold text-gray-900">
                Payment Details
              </h2>

              <p className="mt-1 text-sm text-gray-500">
                Card details are securely handled by Stripe
              </p>
            </div>

            {/* Stripe Mock */}
            <div className="mb-6 rounded-2xl border border-gray-200 bg-gray-50 p-5">
              <p className="mb-4 text-sm text-gray-400">
                Stripe.js secure card element
              </p>

              <div className="space-y-4">
                <div className="rounded-xl border border-gray-300 bg-white px-4 py-3">
                  <p className="text-xs text-gray-400">Card Number</p>

                  <p className="mt-1 text-sm text-gray-300">
                    4242 4242 4242 4242
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="rounded-xl border border-gray-300 bg-white px-4 py-3">
                    <p className="text-xs text-gray-400">Expiry</p>

                    <p className="mt-1 text-sm text-gray-300">MM / YY</p>
                  </div>

                  <div className="rounded-xl border border-gray-300 bg-white px-4 py-3">
                    <p className="text-xs text-gray-400">CVV</p>

                    <p className="mt-1 text-sm text-gray-300">123</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Name */}
            <div className="mb-8">
              <label className="mb-2 block text-sm font-medium text-gray-700">
                Name on Card
              </label>

              <input
                type="text"
                placeholder="John Smith"
                className="w-full rounded-xl border border-gray-300 px-4 py-3 text-sm outline-none transition focus:border-black"
              />
            </div>

            {/* Error */}
            {error && (
              <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-3">
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}

            {/* Buttons */}
            <div className="flex gap-4">
              <button
                onClick={handlePlaceOrder}
                disabled={placing}
                className={`flex-1 rounded-xl py-3 text-sm font-semibold transition ${
                  placing
                    ? "bg-gray-400 text-white cursor-not-allowed"
                    : "bg-black text-white hover:bg-gray-900"
                }`}
              >
                {placing ? "Placing order..." : "Place Order"}
              </button>

              <Link
                href="/cart"
                className="flex-1 rounded-xl border border-gray-300 bg-white py-3 text-center text-sm font-semibold text-gray-700 transition hover:bg-gray-100"
              >
                Back to Cart
              </Link>
            </div>

            <div className="mt-4 flex justify-between text-xs text-gray-400">
              <p>Payments secured by Stripe</p>

              <p>SSL encrypted checkout</p>
            </div>
          </div>

          {/* Right Side */}
          <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
            <div className="mb-6">
              <h2 className="text-xl font-semibold text-gray-900">
                Order Summary
              </h2>

              <p className="mt-1 text-sm text-gray-500">
                Review your items before placing the order
              </p>
            </div>

            {/* Items */}
            <div className="space-y-5">
              {items.map((item, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between border-b border-gray-100 pb-5"
                >
                  <div className="flex items-center gap-4">
                    <div className="flex h-16 w-16 items-center justify-center rounded-xl bg-gray-100 text-xs text-gray-400">
                      IMG
                    </div>

                    <div>
                      <p className="font-medium text-gray-900">{item.name}</p>

                      <p className="mt-1 text-sm text-gray-500">
                        {item.material} / {item.color}
                      </p>
                    </div>
                  </div>

                  <p className="font-semibold text-gray-900">
                    ${item.price.toFixed(2)}
                  </p>
                </div>
              ))}
            </div>

            {/* Totals */}
            <div className="mt-6 border-t border-gray-200 pt-6">
              <div className="mb-3 flex justify-between text-sm">
                <span className="text-gray-500">Subtotal</span>

                <span className="font-medium text-gray-900">
                  ${subtotal.toFixed(2)}
                </span>
              </div>

              <div className="mb-5 flex justify-between text-sm">
                <span className="text-gray-500">Shipping (Canada Post)</span>

                <span className="font-medium text-gray-900">
                  ${shipping.toFixed(2)}
                </span>
              </div>

              <div className="flex justify-between border-t border-gray-200 pt-5">
                <span className="text-lg font-semibold text-gray-900">
                  Total
                </span>

                <span className="text-lg font-bold text-gray-900">
                  ${total.toFixed(2)}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
