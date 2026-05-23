/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useState, useEffect } from "react";
import { apiGet } from "../lib/api";
import { useRouter } from "next/navigation";

export default function CustomUploadPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  // Settings to pass to configurator
  const [scale, setScale] = useState(100);
  const [infill, setInfill] = useState(50);
  const [selectedFilament, setSelectedFilament] = useState<any>(null);
  const [multiColorEnabled, setMultiColorEnabled] = useState(false);
  const [colorCount, setColorCount] = useState(1);
  const [selectedColors, setSelectedColors] = useState<string[]>([]);

  const multiColorOptions = [
    { name: "Black", hex: "#000000" },
    { name: "White", hex: "#FFFFFF" },
    { name: "Blue", hex: "#0000FF" },
    { name: "Red", hex: "#FF0000" },
    { name: "Green", hex: "#00FF00" },
    { name: "Grey", hex: "#808080" },
  ];

  const toggleMultiColor = (hex: string) => {
    setSelectedColors((prev) => {
      if (prev.includes(hex)) return prev.filter((c) => c !== hex);
      return [...prev, hex];
    });
    setColorCount(
      selectedColors.includes(hex)
        ? selectedColors.length - 1
        : selectedColors.length + 1,
    );
  };

  // Real filaments from backend
  const [filaments, setFilaments] = useState<any[]>([]);
  const [loadingFilaments, setLoadingFilaments] = useState(true);

  // Group filaments by material type
  const [selectedMaterial, setSelectedMaterial] = useState<string>("");

  useEffect(() => {
    const loadFilaments = async () => {
      try {
        const data = await apiGet("/filaments");
        setFilaments(data);
        if (data.length > 0) {
          setSelectedFilament(data[0]);
          setSelectedMaterial(data[0].material_name);
        }
      } catch (err: any) {
        console.log("Could not load filaments");
      } finally {
        setLoadingFilaments(false);
      }
    };
    loadFilaments();
  }, []);

  // Get unique materials
  const materials = [...new Set(filaments.map((f: any) => f.material_name))];

  // Get filaments for selected material
  const filteredFilaments = filaments.filter(
    (f: any) => f.material_name === selectedMaterial,
  );

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    const validFile =
      file.name.toLowerCase().endsWith(".stl") ||
      file.name.toLowerCase().endsWith(".3mf");
    if (!validFile) {
      alert("Only STL and 3MF files are supported.");
      return;
    }
    setSelectedFile(file);
  }

  async function handleUpload() {
    if (!selectedFile) return;
    setIsUploading(true);
    setError("");
    try {
      const token = localStorage.getItem("token");

      // Build form data with file + pre-configured values
      const formData = new FormData();
      formData.append("file", selectedFile);
      formData.append("scale", scale.toString());
      formData.append("infill_percent", infill.toString());
      formData.append(
        "color_count",
        (multiColorEnabled
          ? selectedColors.length || colorCount
          : 1
        ).toString(),
      );
      if (selectedFilament) {
        formData.append("filament_id", selectedFilament.filament_id.toString());
      }

      const res = await fetch("http://127.0.0.1:5000/api/models/upload/", {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Upload failed");

      // Redirect to configurator with real model_id and pre-configured values
      const params = new URLSearchParams({
        filament_id: selectedFilament?.filament_id?.toString() || "",
        scale: scale.toString(),
        infill: infill.toString(),
        multicolor: multiColorEnabled.toString(),
        color_count: (multiColorEnabled
          ? selectedColors.length || colorCount
          : 1
        ).toString(),
      });

      router.push(`/product/${data.model_id}?${params.toString()}`);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsUploading(false);
    }
  }

  function handleClear() {
    setSelectedFile(null);
    setScale(100);
    setInfill(50);
    setMultiColorEnabled(false);
    setColorCount(1);
    if (filaments.length > 0) {
      setSelectedFilament(filaments[0]);
      setSelectedMaterial(filaments[0].material_name);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-6xl px-4 py-5 sm:px-6 lg:px-8">
        {/* Breadcrumb */}
        <div className="mb-5 rounded-xl border border-blue-100 bg-blue-50 px-4 py-2 text-center text-sm text-blue-800">
          Home → Custom Upload → Configurator → Cart → Checkout
        </div>

        {/* Progress */}
        <div className="mb-7 grid grid-cols-5 gap-2 text-center text-xs font-medium sm:text-sm">
          <div className="rounded-lg bg-blue-700 px-2 py-3 text-white">
            ✓ Browse
          </div>
          <div className="rounded-lg bg-slate-900 px-2 py-3 text-white">
            Upload
          </div>
          <div className="rounded-lg bg-slate-200 px-2 py-3 text-slate-600">
            Configure
          </div>
          <div className="rounded-lg bg-slate-200 px-2 py-3 text-slate-600">
            Cart
          </div>
          <div className="rounded-lg bg-slate-200 px-2 py-3 text-slate-600">
            Checkout
          </div>
        </div>

        {/* Header */}
        <div className="mb-7 rounded-2xl border border-slate-200 bg-white px-6 py-6 text-center shadow-sm">
          <h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">
            Upload Your Custom 3D Model
          </h2>
          <div className="mt-3 flex flex-wrap items-center justify-center gap-3 text-sm text-slate-600">
            <p>
              Accepted: <b>.stl</b> and <b>.3mf</b>
            </p>
            <span className="hidden sm:inline">•</span>
            <p>
              Max per dimension: <b>500 mm</b>
            </p>
          </div>
          <p className="mt-3 text-sm text-amber-700">
            Material failures are your responsibility.
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-[1fr_1.2fr]">
          {/* LEFT — Upload */}
          <div>
            <h2 className="mb-4 text-lg font-semibold text-slate-900">
              Step 1 — Upload
            </h2>

            <label className="flex min-h-[240px] cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-slate-300 bg-white px-5 text-center shadow-sm transition hover:border-blue-300 hover:bg-blue-50/30">
              <h3 className="text-xl font-semibold text-slate-900">
                Drag & drop here
              </h3>
              <p className="mt-1 text-sm text-slate-500">or click to browse</p>
              <div className="mt-6 text-4xl text-blue-500">↑</div>
              <p className="mt-6 text-sm font-medium text-slate-600">
                .stl or .3mf
              </p>
              <input
                type="file"
                accept=".stl,.3mf"
                onChange={handleFileChange}
                className="hidden"
              />
            </label>

            {selectedFile && (
              <div className="mt-4 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="font-medium text-slate-900">
                      {selectedFile.name}
                    </p>
                    <p className="text-sm text-slate-500">
                      {(selectedFile.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                  <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700">
                    Ready
                  </span>
                </div>
              </div>
            )}

            {error && (
              <div className="mt-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-center text-sm text-red-700">
                {error}
              </div>
            )}

            {isUploading && (
              <div className="mt-3 rounded-xl border border-blue-100 bg-blue-50 px-4 py-3 text-center text-sm text-blue-700">
                Uploading and processing model...
              </div>
            )}

            {/* Buttons */}
            <div className="mt-4 flex gap-3">
              <button
                onClick={handleUpload}
                disabled={!selectedFile || isUploading}
                className={`flex-1 rounded-xl px-4 py-3 text-sm font-semibold transition ${
                  selectedFile && !isUploading
                    ? "bg-slate-900 text-white hover:bg-slate-800"
                    : "cursor-not-allowed bg-slate-200 text-slate-500"
                }`}
              >
                {isUploading ? "Uploading..." : "Upload & Continue →"}
              </button>
              <button
                onClick={handleClear}
                className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
              >
                Clear
              </button>
            </div>

            <div className="mt-5 rounded-xl border border-green-100 bg-green-50 p-4">
              <h3 className="text-sm font-semibold text-green-900">
                After upload
              </h3>
              <p className="mt-1 text-sm text-green-800">
                Your settings below will be pre-loaded in the configurator.
              </p>
            </div>
          </div>

          {/* RIGHT — Settings */}
          <div>
            <h2 className="mb-4 text-lg font-semibold text-slate-900">
              Step 2 — Pre-configure
            </h2>
            <p className="mb-5 text-sm text-slate-600">
              These settings will carry over to the configurator.
            </p>

            <div className="space-y-4">
              {/* Scale */}
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-purple-700">
                  Scale (%)
                </div>
                <input
                  type="text"
                  value={scale}
                  onFocus={(e) => e.target.select()}
                  onChange={(e) => {
                    const val = e.target.value.replace(/[^0-9]/g, "");
                    if (val === "") setScale(0);
                    else setScale(Math.min(Number(val), 200));
                  }}
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none focus:border-slate-900"
                  placeholder="e.g. 100"
                />
                <p className="mt-2 text-xs text-amber-700">
                  150% = 3.375x material — cost rises fast!
                </p>
              </div>

              {/* Infill */}
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-green-700">
                  Infill
                </div>
                <div className="grid grid-cols-3 gap-2 text-center">
                  {[
                    { value: 20, label: "Light" },
                    { value: 50, label: "Medium" },
                    { value: 100, label: "Solid" },
                  ].map((opt) => (
                    <button
                      key={opt.value}
                      onClick={() => setInfill(opt.value)}
                      className={`rounded-xl border py-3 text-sm font-medium transition ${
                        infill === opt.value
                          ? "border-slate-900 bg-slate-900 text-white"
                          : "border-slate-200 bg-slate-50 hover:bg-slate-100"
                      }`}
                    >
                      <p className="text-base font-bold">{opt.value}%</p>
                      <p className="text-xs">{opt.label}</p>
                    </button>
                  ))}
                </div>
              </div>

              {/* Material */}
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-amber-700">
                  Material
                </div>
                {loadingFilaments ? (
                  <p className="text-sm text-slate-500">Loading materials...</p>
                ) : (
                  <div className="flex flex-wrap gap-2">
                    {materials.map((mat) => (
                      <button
                        key={mat}
                        onClick={() => {
                          setSelectedMaterial(mat);
                          const firstFilament = filaments.find(
                            (f: any) => f.material_name === mat,
                          );
                          if (firstFilament) setSelectedFilament(firstFilament);
                        }}
                        className={`rounded-full px-4 py-2 text-sm font-medium transition ${
                          selectedMaterial === mat
                            ? "bg-slate-900 text-white"
                            : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                        }`}
                      >
                        {mat}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Multi-color */}
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-slate-700">Color</p>
                    <p className="text-xs text-slate-500">
                      5+ colors adds 5% surcharge
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => {
                      setMultiColorEnabled(!multiColorEnabled);
                      setSelectedColors([]);
                      setColorCount(1);
                    }}
                    className={`relative h-7 w-12 rounded-full transition ${
                      multiColorEnabled ? "bg-blue-600" : "bg-slate-300"
                    }`}
                  >
                    <span
                      className={`absolute top-1 h-5 w-5 rounded-full bg-white shadow transition ${
                        multiColorEnabled ? "left-6" : "left-1"
                      }`}
                    />
                  </button>
                </div>

                {multiColorEnabled && (
                  <div className="mt-4 bg-blue-50 border border-blue-200 rounded-xl p-3">
                    <label className="text-xs text-blue-700 font-medium block mb-3">
                      Pick your colors (select multiple):
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {multiColorOptions.map((c) => (
                        <button
                          key={c.hex}
                          onClick={() => toggleMultiColor(c.hex)}
                          className={`flex items-center gap-2 rounded-full border px-3 py-2 text-sm transition ${
                            selectedColors.includes(c.hex)
                              ? "border-blue-600 bg-blue-600 text-white"
                              : "border-slate-200 bg-white text-slate-700 hover:bg-slate-50"
                          }`}
                        >
                          <span
                            className="h-4 w-4 rounded-full border border-slate-300"
                            style={{ backgroundColor: c.hex }}
                          />
                          {c.name}
                        </button>
                      ))}
                    </div>

                    {selectedColors.length > 0 && (
                      <div className="mt-3">
                        <p className="text-xs text-blue-700 font-medium mb-2">
                          Selected: {selectedColors.length} color
                          {selectedColors.length > 1 ? "s" : ""}
                          {selectedColors.length >= 5 &&
                            " — 5% surcharge applies"}
                        </p>
                        <div className="flex gap-1">
                          {selectedColors.map((hex) => (
                            <span
                              key={hex}
                              className="h-6 w-6 rounded-full border-2 border-white shadow"
                              style={{ backgroundColor: hex }}
                            />
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Pricing info */}
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="mb-4 text-xs font-semibold uppercase tracking-wide text-slate-900">
                  How pricing works
                </div>
                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                  {[
                    { label: "Material", desc: "Base grams × scale³" },
                    { label: "Machine", desc: "Print hours × rate" },
                    { label: "Overhead", desc: "Power & maintenance" },
                    { label: "Total", desc: "Subtotal + margin" },
                  ].map((item) => (
                    <div
                      key={item.label}
                      className="rounded-xl bg-slate-50 p-4 text-sm"
                    >
                      <p className="font-semibold text-slate-900">
                        {item.label}
                      </p>
                      <p className="mt-1 text-slate-600">{item.desc}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
