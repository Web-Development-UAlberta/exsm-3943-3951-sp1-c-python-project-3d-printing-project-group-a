/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { apiGet, apiPost } from "../../lib/api";
import Image from "next/image";

export default function ConfiguratorPage() {
  const params = useParams();
  const id = params.id as string;

  const [scale, setScale] = useState(100);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [addedToCart, setAddedToCart] = useState(false);
  const [cartError, setCartError] = useState("");
  const [model, setModel] = useState<any>(null);
  const [selectedFilament, setSelectedFilament] = useState<any>(null);
  const [infill, setInfill] = useState(50);
  const [material, setMaterial] = useState("PLA");
  const [color, setColor] = useState("Black");
  const [multiColor, setMultiColor] = useState(false);
  const [selectedColors, setSelectedColors] = useState<string[]>([]);
  const [dimensions, setDimensions] = useState({
    length: 120,
    width: 80,
    height: 95,
  });

  useEffect(() => {
    const loadModel = async () => {
      try {
        const data = await apiGet(`/models/${id}`);
        setModel(data);
        if (data.filaments && data.filaments.length > 0) {
          setSelectedFilament(data.filaments[0]);
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    loadModel();
  }, [id]);

  const materials = ["PLA", "PETG", "ABS", "TPU"];
  const colors = ["Black", "White", "Blue", "Red", "Grey", "Green"];

  const toggleColor = (c: string) => {
    setSelectedColors((prev) => {
      if (prev.includes(c)) return prev.filter((x) => x !== c);
      if (prev.length >= 6) return prev;
      return [...prev, c];
    });
  };

  const baseGrams = 45;
  const scaledGrams = baseGrams * Math.pow(scale / 100, 3);
  const withWaste = scaledGrams * 1.2;

  const pricePerKg =
    material === "PLA"
      ? 25
      : material === "PETG"
        ? 32
        : material === "ABS"
          ? 28
          : 38;

  const materialCost = (withWaste / 1000) * pricePerKg;
  const printTimeHrs = 0.5;
  const machineCost = printTimeHrs * 10;
  const overhead = machineCost * 0.15;
  const subtotal = materialCost + machineCost + overhead;

  const surcharge =
    multiColor && selectedColors.length > 4 ? subtotal * 0.05 : 0;
  const total = (subtotal + surcharge) * 1.25;
  const shipping = 10.0;

  const dimWarning =
    dimensions.length > 500 ||
    dimensions.width > 500 ||
    dimensions.height > 500;

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-gray-300 border-t-gray-900 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-500">Loading model...</p>
        </div>
      </div>
    );
  }
  return (
    <div className="min-h-screen bg-linear-to-b from-slate-50 to-white text-slate-900">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="mb-8">
          <p className="mb-2 text-sm uppercase tracking-[0.2em] text-slate-500">
            PrintShop
          </p>
          <h1 className="text-4xl font-medium tracking-tight text-slate-950">
            Configurator
          </h1>
          <p className="mt-2 text-sm text-slate-500">
            Adjust the model and see pricing update instantly.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
          {addedToCart && (
            <div className="mb-6 rounded-xl bg-green-50 border border-green-200 p-4 flex justify-between items-center">
              <p className="text-sm text-green-700 font-medium">
                ✓ Added to cart!
              </p>
              <Link href="/cart" className="text-sm text-green-700 underline">
                View cart →
              </Link>
            </div>
          )}

          {cartError && (
            <div className="mb-6 rounded-xl bg-red-50 border border-red-200 p-3">
              <p className="text-sm text-red-600">{cartError}</p>
            </div>
          )}
          <div className="space-y-6">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="mb-4 h-56 rounded-2xl border border-slate-200 bg-gradient-to-br from-slate-100 to-slate-50 overflow-hidden flex items-center justify-center">
                {model?.model_image ? (
                  <img
                    src={`http://127.0.0.1:5000/api/models/images/${model.model_image.split("/").pop()}`}
                    alt={model.model_name}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <span className="text-sm text-slate-400">
                    [ 3D model preview ]
                  </span>
                )}
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.18em] text-slate-500">
                  Selected model
                </p>
                <h2 className="mt-2 text-2xl font-medium text-slate-950">
                  {model?.model_name || "Loading model"}
                </h2>
              </div>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-sm font-medium uppercase tracking-[0.16em] text-slate-500">
                Custom dimensions
              </h3>
              <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3">
                {[
                  { label: "Length", key: "length" as const },
                  { label: "Width", key: "width" as const },
                  { label: "Height", key: "height" as const },
                ].map((d) => (
                  <div
                    key={d.key}
                    className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3"
                  >
                    <p className="text-xs text-slate-500">{d.label}</p>
                    <input
                      type="number"
                      value={dimensions[d.key]}
                      onChange={(e) =>
                        setDimensions({
                          ...dimensions,
                          [d.key]: Number(e.target.value),
                        })
                      }
                      className="mt-2 w-full bg-transparent text-sm font-medium text-slate-900 outline-none"
                    />
                    <p className="mt-1 text-xs text-slate-400">mm</p>
                  </div>
                ))}
              </div>

              {dimWarning && (
                <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3">
                  <p className="text-sm text-amber-900">
                    Warning: keep each side at 500mm or less.
                  </p>
                </div>
              )}
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-sm font-medium uppercase tracking-[0.16em] text-slate-500">
                Scale
              </h3>
              <div className="mt-4">
                <input
                  type="number"
                  value={scale}
                  onChange={(e) => setScale(Number(e.target.value))}
                  className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none transition focus:border-slate-900 focus:ring-4 focus:ring-slate-900/5"
                  placeholder="e.g. 100"
                />
              </div>
              <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3">
                <p className="text-sm text-amber-900">150% = 3.375x material</p>
                <p className="mt-1 text-xs text-amber-700">
                  Scales cubically, so cost rises fast.
                </p>
              </div>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-sm font-medium uppercase tracking-[0.16em] text-slate-500">
                Infill
              </h3>
              <div className="mt-4 grid grid-cols-3 gap-3">
                {[
                  { value: 20, label: "Light" },
                  { value: 50, label: "Medium" },
                  { value: 100, label: "Solid" },
                ].map((opt) => (
                  <button
                    key={opt.value}
                    onClick={() => setInfill(opt.value)}
                    className={`rounded-xl border px-4 py-4 text-center transition cursor-pointer ${
                      infill === opt.value
                        ? "border-slate-950 bg-slate-950 text-white shadow-md"
                        : "border-slate-200 bg-white text-slate-800 hover:border-slate-300 hover:bg-slate-50"
                    }`}
                  >
                    <p className="text-lg font-medium">{opt.value}%</p>
                    <p className="mt-1 text-xs">{opt.label}</p>
                  </button>
                ))}
              </div>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-sm font-medium uppercase tracking-[0.16em] text-slate-500">
                Material
              </h3>
              <select
                value={material}
                onChange={(e) => setMaterial(e.target.value)}
                className="mt-4 w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none transition focus:border-slate-900 focus:ring-4 focus:ring-slate-900/5"
              >
                {materials.map((mat) => (
                  <option key={mat} value={mat}>
                    {mat}
                  </option>
                ))}
              </select>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-sm font-medium uppercase tracking-[0.16em] text-slate-500">
                Color
              </h3>
              <select
                value={color}
                onChange={(e) => setColor(e.target.value)}
                className="mt-4 w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none transition focus:border-slate-900 focus:ring-4 focus:ring-slate-900/5"
              >
                {colors.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <h3 className="text-sm font-medium uppercase tracking-[0.16em] text-slate-500">
                    Multi-color print
                  </h3>
                  <p className="mt-1 text-sm text-slate-500">
                    Up to 4 colors has no extra charge. More than 4 colors adds
                    5%.
                  </p>
                </div>
                <button
                  onClick={() => setMultiColor(!multiColor)}
                  className={`relative h-7 w-14 rounded-full transition cursor-pointer ${
                    multiColor ? "bg-slate-950" : "bg-slate-300"
                  }`}
                >
                  <span
                    className={`absolute top-1 h-5 w-5 rounded-full bg-white shadow transition ${
                      multiColor ? "left-8" : "left-1"
                    }`}
                  />
                </button>
              </div>

              {multiColor && (
                <div className="mt-5">
                  <p className="text-xs uppercase tracking-[0.16em] text-slate-500">
                    Choose colors
                  </p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {colors.map((c) => {
                      const active = selectedColors.includes(c);
                      return (
                        <button
                          key={c}
                          onClick={() => toggleColor(c)}
                          className={`cursor-pointer rounded-full px-4 py-2 text-sm transition ${
                            active
                              ? "bg-slate-950 text-white"
                              : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                          }`}
                        >
                          {c}
                        </button>
                      );
                    })}
                  </div>

                  <p className="mt-3 text-xs text-slate-500">
                    Selected: {selectedColors.length} / 6
                  </p>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {selectedColors.map((c) => (
                      <span
                        key={c}
                        className="rounded-full bg-blue-50 px-3 py-1 text-xs text-blue-700"
                      >
                        {c}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <p className="mt-3 text-xs text-slate-500">
                {multiColor
                  ? selectedColors.length > 4
                    ? "ON — 5% surcharge applied"
                    : "ON — no extra charge for 4 colors or less"
                  : "OFF — click to enable"}
              </p>
            </div>

            <button
              onClick={async () => {
                setCartError("");
                try {
                  await apiPost("/cart", {
                    model_id: Number(id),
                    filament_id: 1,
                    scale: scale,
                    infill_percent: infill,
                    color_count: multiColor ? selectedColors.length : 1,
                    quantity: 1,
                  });
                  setAddedToCart(true);
                  setTimeout(() => setAddedToCart(false), 3000);
                } catch (err: any) {
                  setCartError(err.message);
                }
              }}
              className="block w-full rounded-2xl bg-slate-950 px-6 py-4 text-center text-sm font-medium text-white shadow-lg shadow-slate-950/10 transition hover:bg-slate-800 cursor-pointer"
            >
              Add to Cart →
            </button>
          </div>

          <div>
            <div className="sticky top-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="mb-6">
                <p className="text-xs uppercase tracking-[0.18em] text-slate-500">
                  Live price breakdown
                </p>
                <h3 className="mt-2 text-2xl font-medium text-slate-950">
                  Summary
                </h3>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between border-b border-slate-100 pb-3">
                  <span className="text-sm text-slate-500">Dimensions</span>
                  <span className="text-sm text-slate-900">
                    {dimensions.length} x {dimensions.width} x{" "}
                    {dimensions.height} mm
                  </span>
                </div>
                <div className="flex justify-between border-b border-slate-100 pb-3">
                  <span className="text-sm text-slate-500">Scale</span>
                  <span className="text-sm text-slate-900">{scale}%</span>
                </div>
                <div className="flex justify-between border-b border-slate-100 pb-3">
                  <span className="text-sm text-slate-500">Infill</span>
                  <span className="text-sm text-slate-900">{infill}%</span>
                </div>
                <div className="flex justify-between border-b border-slate-100 pb-3">
                  <span className="text-sm text-slate-500">Material</span>
                  <span className="text-sm text-slate-900">{material}</span>
                </div>
                <div className="flex justify-between border-b border-slate-100 pb-3">
                  <span className="text-sm text-slate-500">Color</span>
                  <span className="text-sm text-slate-900">{color}</span>
                </div>
                <div className="flex justify-between border-b border-slate-100 pb-3">
                  <span className="text-sm text-slate-500">Multi-color</span>
                  <span className="text-sm text-slate-900">
                    {selectedColors.length
                      ? `${selectedColors.length} selected`
                      : "None"}
                  </span>
                </div>
              </div>

              <div className="mt-6 rounded-2xl bg-slate-50 p-4">
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-slate-500">
                      Material required
                    </span>
                    <span className="text-sm text-slate-900">
                      {withWaste.toFixed(1)} g
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-slate-500">
                      Material cost
                    </span>
                    <span className="text-sm text-slate-900">
                      ${materialCost.toFixed(2)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-slate-500">Print time</span>
                    <span className="text-sm text-slate-900">
                      {printTimeHrs} hrs
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-slate-500">Machine cost</span>
                    <span className="text-sm text-slate-900">
                      ${machineCost.toFixed(2)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-slate-500">Overhead</span>
                    <span className="text-sm text-slate-900">
                      ${overhead.toFixed(2)}
                    </span>
                  </div>
                  {multiColor && selectedColors.length > 4 && (
                    <div className="flex justify-between">
                      <span className="text-sm text-slate-500">
                        Multi-color surcharge
                      </span>
                      <span className="text-sm text-slate-900">
                        ${surcharge.toFixed(2)}
                      </span>
                    </div>
                  )}
                </div>
              </div>

              <div className="mt-6 border-t border-slate-200 pt-5">
                <div className="flex items-end justify-between">
                  <span className="text-sm uppercase tracking-[0.18em] text-slate-500">
                    Total
                  </span>
                  <span className="text-3xl font-medium text-slate-950">
                    ${total.toFixed(2)}
                  </span>
                </div>
                <p className="mt-1 text-xs text-slate-400">
                  All costs included in total.
                </p>
              </div>

              <div className="mt-5 rounded-2xl border border-blue-100 bg-blue-50 p-4">
                <div className="flex justify-between gap-4">
                  <span className="text-sm font-medium text-blue-700">
                    Shipping (Canada Post)
                  </span>
                  <span className="text-sm font-medium text-blue-700">
                    ${shipping.toFixed(2)} flat
                  </span>
                </div>
                <p className="mt-1 text-xs text-blue-600">Anywhere in Canada</p>
              </div>

              <div className="mt-5 rounded-2xl border border-slate-200 bg-white p-4 space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-slate-500">
                    Est. completion date
                  </span>
                  <span className="text-sm text-slate-900">--</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-slate-500">Est. ship date</span>
                  <span className="text-sm text-slate-900">--</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-amber-600">
                    Delay (orders ahead)
                  </span>
                  <span className="text-sm text-amber-600">None currently</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
