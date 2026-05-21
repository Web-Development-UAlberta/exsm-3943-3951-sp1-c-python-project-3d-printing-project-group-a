/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { apiGet, apiPost } from "../../lib/api";

export default function ConfiguratorPage() {
  const params = useParams();
  const id = params.id as string;

  const searchParams =
    typeof window !== "undefined"
      ? new URLSearchParams(window.location.search)
      : new URLSearchParams();
  const preFilamentId = searchParams.get("filament_id");
  const preScale = searchParams.get("scale");
  const preInfill = searchParams.get("infill");
  const preMulticolor = searchParams.get("multicolor");
  const preColorCount = searchParams.get("color_count");

  const [scale, setScale] = useState(100);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [addedToCart, setAddedToCart] = useState(false);
  const [cartError, setCartError] = useState("");
  const [model, setModel] = useState<any>(null);
  const [selectedFilament, setSelectedFilament] = useState<any>(null);
  const [infill, setInfill] = useState(50);

  const [selectedColors, setSelectedColors] = useState<string[]>([]);
  const [multiColor, setMultiColor] = useState(false);
  const [colorCount, setColorCount] = useState(1);

  useEffect(() => {
    const loadModel = async () => {
      try {
        const data = await apiGet(`/models/${id}`);
        setModel(data);

        if (data.filaments && data.filaments.length > 0) {
          // Check if pre-selected filament from custom page
          if (preFilamentId) {
            const pre = data.filaments.find(
              (f: any) => f.filament_id === Number(preFilamentId),
            );
            setSelectedFilament(pre || data.filaments[0]);
          } else {
            setSelectedFilament(data.filaments[0]);
          }
        }
        // Apply other pre-selected settings from custom page
        if (preScale) setScale(Number(preScale));
        if (preInfill) setInfill(Number(preInfill));
        if (preMulticolor === "true") setMultiColor(true);
        if (preColorCount) setColorCount(Number(preColorCount));
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    loadModel();
  }, [id]);

  const toggleColor = (c: string) => {
    setSelectedColors((prev) => {
      if (prev.includes(c)) return prev.filter((x) => x !== c);
      if (prev.length >= 6) return prev;
      return [...prev, c];
    });
  };

  const [quote, setQuote] = useState<any>(null);
  const [quoteLoading, setQuoteLoading] = useState(false);
  const shipping = 10.0;

  useEffect(() => {
    if (!model || !selectedFilament) return;
    const getQuote = async () => {
      setQuoteLoading(true);
      try {
        const data = await apiPost("/models/quote", {
          model_id: model.model_id,
          filament_id: selectedFilament.filament_id,
          scale: scale,
          infill_percent: infill,
          color_count: multiColor ? Math.max(selectedColors.length, 1) : 1,
        });
        setQuote(data);
      } catch (err: any) {
        console.log("Quote error:", err.message);
      } finally {
        setQuoteLoading(false);
      }
    };
    const timer = setTimeout(getQuote, 300);
    return () => clearTimeout(timer);
  }, [
    model,
    selectedFilament,
    scale,
    infill,
    multiColor,
    selectedColors.length,
  ]);

  const dimWarning =
    (model?.model_length || 0) > 500 ||
    (model?.model_width || 0) > 500 ||
    (model?.model_height || 0) > 500;

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
            <div className="fixed bottom-6 right-6 z-50 rounded-xl bg-green-600 text-white px-4 py-3 shadow-lg flex items-center gap-3">
              <p className="text-sm font-medium">✓ Added to cart!</p>
              <Link href="/cart" className="text-sm underline">
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
                Model dimensions
              </h3>
              <p className="text-xs text-slate-400 mt-1 mb-3">
                Read from model file
              </p>
              <div className="mt-2 grid grid-cols-1 gap-3 sm:grid-cols-3">
                {[
                  { label: "Length", value: model?.model_length },
                  { label: "Width", value: model?.model_width },
                  { label: "Height", value: model?.model_height },
                ].map((d) => (
                  <div
                    key={d.label}
                    className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3"
                  >
                    <p className="text-xs text-slate-500">{d.label}</p>
                    <p className="mt-2 text-sm font-medium text-slate-900">
                      {d.value}
                    </p>
                    <p className="mt-1 text-xs text-slate-400">mm</p>
                  </div>
                ))}
              </div>
              {dimWarning && (
                <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3">
                  <p className="text-sm text-amber-900">
                    Warning: dimensions exceed 500mm per side.
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
                  type="text"
                  value={scale}
                  onChange={(e) => {
                    const val = e.target.value.replace(/[^0-9]/g, "");
                    if (val === "") setScale(0);
                    else setScale(Math.min(Number(val), 200));
                  }}
                  onFocus={(e) => e.target.select()}
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
                Material & Color
              </h3>
              {model?.filaments && model.filaments.length > 0 ? (
                <div className="mt-4 space-y-2">
                  {model.filaments.map((f: any) => (
                    <button
                      key={f.filament_id}
                      onClick={() => f.in_stock && setSelectedFilament(f)}
                      disabled={!f.in_stock}
                      className={`w-full text-left px-4 py-3 rounded-xl border-2 transition flex items-center justify-between ${
                        !f.in_stock
                          ? "border-slate-100 bg-slate-50 opacity-50 cursor-not-allowed"
                          : selectedFilament?.filament_id === f.filament_id
                            ? "border-slate-900 bg-slate-50 shadow-sm"
                            : "border-slate-200 hover:border-slate-300"
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div
                          className="w-6 h-6 rounded-full border border-slate-300"
                          style={{ backgroundColor: f.color_hex }}
                        />
                        <div>
                          <p className="text-sm font-medium">
                            {f.material_name}
                          </p>
                          <p className="text-xs text-slate-500">
                            {f.color_hex} — ${f.filament_price}/kg
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        {selectedFilament?.filament_id === f.filament_id && (
                          <span className="text-xs bg-slate-900 text-white px-2 py-0.5 rounded-full">
                            Selected
                          </span>
                        )}
                        {f.in_stock ? (
                          <span className="text-xs text-green-600">
                            In stock
                          </span>
                        ) : (
                          <span className="text-xs text-red-600">
                            Out of stock
                          </span>
                        )}
                      </div>
                    </button>
                  ))}
                </div>
              ) : (
                <p className="mt-4 text-sm text-slate-500">
                  No filaments available
                </p>
              )}
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <h3 className="text-sm font-medium uppercase tracking-[0.16em] text-slate-500">
                    Multi-color print
                  </h3>
                  <p className="mt-1 text-sm text-slate-500">
                    5 or more colors adds 5% surcharge.
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
                    {model?.filaments?.map((f: any) => {
                      const active = selectedColors.includes(f.color_hex);
                      return (
                        <button
                          key={f.filament_id}
                          onClick={() => toggleColor(f.color_hex)}
                          className={`cursor-pointer flex items-center gap-2 rounded-full px-3 py-2 text-sm transition ${
                            active
                              ? "bg-slate-950 text-white"
                              : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                          }`}
                        >
                          <div
                            className="w-4 h-4 rounded-full border border-slate-300"
                            style={{ backgroundColor: f.color_hex }}
                          />
                          {f.material_name}
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
                  ? selectedColors.length >= 2
                    ? "ON — 5% surcharge applied"
                    : "ON — no extra charge for under 2 colors"
                  : "OFF — click to enable"}
              </p>
            </div>

            <button
              onClick={async () => {
                setCartError("");
                try {
                  await apiPost("/cart", {
                    model_id: Number(id),
                    filament_id: selectedFilament?.filament_id || 1,
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
                    {model?.model_length} x {model?.model_width} x{" "}
                    {model?.model_height} mm
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
                  <span className="text-sm text-slate-900">
                    {selectedFilament?.material_name || "--"}
                  </span>
                </div>
                <div className="flex justify-between border-b border-slate-100 pb-3">
                  <span className="text-sm text-slate-500">
                    Material & Color
                  </span>
                  <div className="flex items-center gap-2">
                    {selectedFilament?.color_hex && (
                      <div
                        className="w-4 h-4 rounded-full border border-slate-300"
                        style={{ backgroundColor: selectedFilament.color_hex }}
                      />
                    )}
                    <span className="text-sm text-slate-900">
                      {selectedFilament
                        ? `${selectedFilament.material_name} — ${selectedFilament.color_hex}`
                        : "--"}
                    </span>
                  </div>
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
              {quoteLoading ? (
                <div className="mt-6 rounded-2xl bg-slate-50 p-6 text-center">
                  <div className="w-5 h-5 border-2 border-slate-300 border-t-slate-900 rounded-full animate-spin mx-auto mb-2"></div>
                  <p className="text-xs text-slate-500">Calculating price...</p>
                </div>
              ) : quote ? (
                <>
                  <div className="mt-6 rounded-2xl bg-slate-50 p-4">
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm text-slate-500">
                          Material required
                        </span>
                        <span className="text-sm text-slate-900">
                          {quote.material_grams} g
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-slate-500">
                          Material cost
                        </span>
                        <span className="text-sm text-slate-900">
                          ${quote.material_cost}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-slate-500">
                          Print time
                        </span>
                        <span className="text-sm text-slate-900">
                          {quote.print_hours} hrs
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-slate-500">
                          Machine cost
                        </span>
                        <span className="text-sm text-slate-900">
                          ${quote.machine_cost}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-slate-500">Overhead</span>
                        <span className="text-sm text-slate-900">
                          ${quote.overhead}
                        </span>
                      </div>
                      {quote.multicolor_surcharge > 0 && (
                        <div className="flex justify-between">
                          <span className="text-sm text-slate-500">
                            Multi-color surcharge
                          </span>
                          <span className="text-sm text-slate-900">
                            ${quote.multicolor_surcharge}
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
                        ${quote.total}
                      </span>
                    </div>
                    <p className="mt-1 text-xs text-slate-400">
                      All costs included in total.
                    </p>
                  </div>
                </>
              ) : (
                <div className="mt-6 rounded-2xl bg-slate-50 p-6 text-center">
                  <p className="text-sm text-slate-500">
                    Select options to see pricing
                  </p>
                </div>
              )}

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
5