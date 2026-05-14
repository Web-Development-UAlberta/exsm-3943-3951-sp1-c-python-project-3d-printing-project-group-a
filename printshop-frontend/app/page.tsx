"use client";

import { useState } from "react";
import Link from "next/link";

export default function Home() {
  const [search, setSearch] = useState("");
  const [activeCategory, setActiveCategory] = useState("All");
  const [activeMaterial, setActiveMaterial] = useState("All");

  const categories = [
    "All",
    "Utilities",
    "Gaming",
    "Collectibles",
    "Props",
    "Decorations",
    "Education",
  ];

  const materials = ["All", "PLA", "PETG", "ABS", "TPU"];

  const models = [
    { id: 1, name: "Desk Vase", price: 75.16, category: "Decorations" },
    { id: 2, name: "D20 Dice", price: 42.0, category: "Gaming" },
    { id: 3, name: "Iron Man Bust", price: 124.5, category: "Collectibles" },
    { id: 4, name: "Cable Clip", price: 18.75, category: "Utilities" },
    { id: 5, name: "Helmet Prop", price: 89.0, category: "Props" },
    { id: 6, name: "DNA Model", price: 68.2, category: "Education" },
  ];

  const filtered = models.filter((m) => {
    if (activeCategory !== "All" && m.category !== activeCategory) return false;
    if (activeMaterial !== "All" && activeMaterial !== "All") return true;
    if (search && !m.name.toLowerCase().includes(search.toLowerCase()))
      return false;
    return true;
  });

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-slate-50 text-slate-900">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="mb-8">
          <p className="text-xs uppercase tracking-[0.24em] text-slate-500">
            PrintShop
          </p>
          <h1 className="mt-2 text-4xl font-medium tracking-tight text-slate-950">
            Browse models
          </h1>
          <p className="mt-2 text-sm text-slate-500">
            Discover ready-to-print designs or upload your own.
          </p>
        </div>

        <div className="mb-6 flex flex-col gap-3 sm:flex-row">
          <input
            type="text"
            placeholder="Search models..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 rounded-2xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none transition focus:border-slate-900 focus:ring-4 focus:ring-slate-900/5"
          />
          <button className="rounded-2xl bg-slate-950 px-6 py-3 text-sm font-medium text-white shadow-lg shadow-slate-950/10 transition hover:bg-slate-800">
            Search
          </button>
        </div>

        <div className="mb-5">
          <h2 className="mb-3 text-sm font-medium uppercase tracking-[0.16em] text-slate-500">
            Browse by category
          </h2>
          <div className="flex flex-wrap gap-2">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`rounded-full px-4 py-2 text-sm transition ${
                  activeCategory === cat
                    ? "bg-slate-950 text-white shadow-md"
                    : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        <div className="mb-8 flex flex-wrap items-center gap-2">
          <span className="text-sm font-medium uppercase tracking-[0.16em] text-slate-500">
            Material
          </span>
          {materials.map((mat) => (
            <button
              key={mat}
              onClick={() => setActiveMaterial(mat)}
              className={`rounded-full px-4 py-2 text-sm transition ${
                activeMaterial === mat
                  ? "bg-slate-950 text-white shadow-md"
                  : "bg-slate-100 text-slate-700 hover:bg-slate-200"
              }`}
            >
              {mat}
            </button>
          ))}
        </div>

        <div className="mb-4 flex items-end justify-between">
          <h2 className="text-2xl font-medium tracking-tight text-slate-950">
            Model library
          </h2>
          <p className="text-sm text-slate-500">
            {filtered.length} models found
          </p>
        </div>

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {filtered.map((model) => (
            <Link
              key={model.id}
              href={`/product/${model.id}`}
              className="group overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:-translate-y-0.5 hover:shadow-lg"
            >
              <div className="flex h-44 items-center justify-center bg-gradient-to-br from-slate-100 to-slate-50">
                <span className="text-sm text-slate-400">[ preview ]</span>
              </div>

              <div className="p-5">
                <div className="mb-3 flex items-start justify-between gap-4">
                  <h3 className="text-lg font-medium text-slate-950">
                    {model.name}
                  </h3>
                  <span className="text-lg font-medium text-slate-950">
                    ${model.price.toFixed(2)}
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="inline-flex rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-700">
                    {model.category}
                  </span>
                  <span className="text-xs text-blue-700 transition group-hover:underline">
                    View details →
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>

        <div className="mt-10 rounded-2xl border border-blue-100 bg-gradient-to-r from-blue-50 to-indigo-50 p-6 text-center shadow-sm">
          <p className="text-sm text-slate-700">
            Looking to print your own design?
          </p>
          <p className="mt-3 text-xs text-slate-500">
            Supported files: .stl .3mf .jpg .png
          </p>

          <Link
            href="/custom"
            className="mt-4 inline-flex items-center justify-center rounded-2xl bg-blue-600 px-6 py-3 text-sm font-medium text-white shadow-lg shadow-blue-600/20 transition hover:bg-blue-700"
          >
            Upload Custom Model
          </Link>
        </div>
      </div>
    </div>
  );
}
