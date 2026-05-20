/* eslint-disable react-hooks/immutability */
/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { apiGet } from "./lib/api";

export default function Home() {
  const [search, setSearch] = useState("");
  const [activeCategory, setActiveCategory] = useState("All");
  const [activeMaterial, setActiveMaterial] = useState("All");
  const [models, setModels] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [tags, setTags] = useState<any[]>([]);
  const [allFilaments, setAllFilaments] = useState<any[]>([]);

  const tagColors: Record<string, { color: string; inactive: string }> = {
    Utilities: {
      color: "bg-blue-600 text-white",
      inactive: "bg-blue-50 text-blue-600 hover:bg-blue-100",
    },
    Gaming: {
      color: "bg-purple-600 text-white",
      inactive: "bg-purple-50 text-purple-600 hover:bg-purple-100",
    },
    Collectibles: {
      color: "bg-yellow-500 text-white",
      inactive: "bg-yellow-50 text-yellow-600 hover:bg-yellow-100",
    },
    Props: {
      color: "bg-teal-600 text-white",
      inactive: "bg-teal-50 text-teal-600 hover:bg--100",
    },
    Decorations: {
      color: "bg-pink-500 text-white",
      inactive: "bg-pink-50 text-pink-600 hover:bg-pink-100",
    },
    Education: {
      color: "bg-green-600 text-white",
      inactive: "bg-green-50 text-green-600 hover:bg-green-100",
    },
  };
  const materials = ["All", "PLA", "PETG", "ABS", "TPU"];

  useEffect(() => {
    loadModels();
  }, []);

  const loadModels = async () => {
    setLoading(true);
    try {
      const data = await apiGet("/models");
      setModels(data);
      // Extract unique tags from models
      const allTags: any[] = [];
      data.forEach((model: any) => {
        model.tags?.forEach((tag: any) => {
          if (!allTags.find((t) => t.tag_id === tag.tag_id)) {
            allTags.push(tag);
          }
        });
      });
      setTags(allTags);
      const filamentsData = await apiGet("/filaments");
      setAllFilaments(filamentsData);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchWithCategory = async (tagId: number) => {
    setLoading(true);
    try {
      let query = "/models?";
      if (search) query += `search=${search}&`;
      query += `tag_id=${tagId}&`;
      if (activeMaterial !== "All") {
        const filament = allFilaments.find(
          (f: any) => f.material_name === activeMaterial,
        );
        if (filament) query += `filament_id=${filament.filament_id}&`;
      }
      const data = await apiGet(query);
      setModels(data);
    } catch (err: any) {
      console.log("Could not filter");
    } finally {
      setLoading(false);
    }
  };
  const handleSearch = async () => {
    setLoading(true);
    try {
      let query = "/models?";
      if (search) query += `search=${search}&`;
      if (activeCategory !== "All") {
        const tag = tags.find((t) => t.tag_name === activeCategory);
        if (tag) query += `tag_id=${tag.tag_id}&`;
      }
      if (activeMaterial !== "All") query += `material=${activeMaterial}&`;
      const data = await apiGet(query);
      setModels(data);
    } catch (err: any) {
      console.log("Backend not available");
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Search */}
      <div className="flex gap-3 mb-6">
        <input
          type="text"
          placeholder="Search models..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 border border-gray-300 rounded-lg px-4 py-2 text-sm"
        />
        <button
          onClick={handleSearch}
          className="bg-gray-900 text-white px-6 py-2 rounded-lg text-sm font-medium"
        >
          Search
        </button>
      </div>

      {/* Categories */}
      <div className="mb-4">
        <h2 className="text-sm font-semibold text-teal-100-600 mb-2">
          Browse by category
        </h2>
        <div className="flex gap-2 flex-wrap">
          {/* All button */}
          <button
            onClick={() => {
              setActiveCategory("All");
              loadModels();
            }}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${
              activeCategory === "All"
                ? "bg-gray-900 text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            All
          </button>

          {/* Dynamic tags from backend */}
          {tags.map((tag) => {
            const colors = tagColors[tag.tag_name] || {
              color: "bg-gray-900 text-white",
              inactive: "bg-gray-100 text-gray-600 hover:bg-gray-200",
            };
            return (
              <button
                key={tag.tag_id}
                onClick={() => {
                  setActiveCategory(tag.tag_name);
                  handleSearchWithCategory(tag.tag_id);
                }}
                className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${
                  activeCategory === tag.tag_name
                    ? colors.color
                    : colors.inactive
                }`}
              >
                {tag.tag_name}
              </button>
            );
          })}
        </div>
      </div>

      {/* Material filter */}
      <div className="flex items-center gap-2 mb-6">
        <span className="text-sm font-semibold text-gray-200">Material:</span>
        {materials.map((mat) => (
          <button
            key={mat}
            onClick={() => {
              setActiveMaterial(mat);
              if (mat === "All") {
                loadModels();
              } else {
                const filament = allFilaments.find(
                  (f: any) => f.material_name === mat,
                );
                if (filament) {
                  setLoading(true);
                  apiGet(`/models?filament_id=${filament.filament_id}&`)
                    .then((data) => setModels(data))
                    .catch(() => {})
                    .finally(() => setLoading(false));
                }
              }
            }}
            className={`px-3 py-1 rounded-full text-sm ${
              activeMaterial === mat
                ? "bg-gray-900 text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            {mat}
          </button>
        ))}
        {(activeCategory !== "All" || activeMaterial !== "All" || search) && (
          <button
            onClick={() => {
              setActiveCategory("All");
              setActiveMaterial("All");
              setSearch("");
              loadModels();
            }}
            className="text-sm text-red-600 hover:underline"
          >
            Clear filters ✕
          </button>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-6">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="text-center py-12">
          <p className="text-gray-500">Loading models...</p>
        </div>
      )}

      {/* Model grid */}
      {!loading && (
        <>
          <h2 className="text-lg font-bold text-gray-900 mb-4">
            Model library
          </h2>
          {models.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500">No models found</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {models.map((model: any) => (
                <Link
                  key={model.model_id}
                  href={`/product/${model.model_id}`}
                  className="border border-gray-200 rounded-lg bg-white hover:shadow-md"
                >
                  <div className="h-40 bg-gray-100 rounded-t-lg overflow-hidden flex items-center justify-center">
                    {model.model_image ? (
                      <img
                        src={`http://127.0.0.1:5000/api/models/images/${model.model_image.split("/").pop()}`}
                        alt={model.model_name}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <span className="text-gray-400 text-sm">[ preview ]</span>
                    )}
                  </div>
                  <div className="p-4">
                    <div className="flex justify-between items-center mb-2">
                      <h3 className="font-semibold text-gray-900">
                        {model.model_name}
                      </h3>
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {model.tags?.map((tag: any) => {
                        const colors = tagColors[tag.tag_name] || {
                          inactive: "bg-gray-100 text-gray-600",
                        };
                        return (
                          <span
                            key={tag.tag_id}
                            className={`text-xs px-2 py-1 rounded-full ${colors.inactive}`}
                          >
                            {tag.tag_name}
                          </span>
                        );
                      })}
                      {Array.from(
                        new Map(
                          model.filaments?.map((f) => [f.material_name, f]),
                        ).values(),
                      ).map((f) => (
                        <span
                          key={f.filament_id}
                          className="text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded-full"
                        >
                          {f.material_name}
                        </span>
                      ))}
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </>
      )}

      {/* Custom model hint */}
      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
        <p className="text-sm text-blue-700 font-medium">
          Looking to print your own design?{" "}
          <Link href="/custom" className="underline">
            Upload a custom model
          </Link>
        </p>
      </div>
    </div>
  );
}
