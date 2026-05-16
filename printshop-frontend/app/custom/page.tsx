"use client";

import { useState } from "react";
import Link from "next/link";

const colorOptions = [
  { name: "Red", value: "red", className: "bg-red-500" },
  { name: "Blue", value: "blue", className: "bg-blue-500" },
  { name: "Green", value: "green", className: "bg-green-500" },
  { name: "Black", value: "black", className: "bg-slate-900" },
  {
    name: "White",
    value: "white",
    className: "bg-slate-100 border border-slate-300",
  },
  { name: "Yellow", value: "yellow", className: "bg-yellow-400" },
];

export default function CustomUploadPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [selectedColor, setSelectedColor] = useState("red");
  const [multiColorEnabled, setMultiColorEnabled] = useState(false);

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

  function handleUpload() {
    if (!selectedFile) return;

    setIsUploading(true);

    setTimeout(() => {
      console.log("Uploaded:", selectedFile.name);
      setIsUploading(false);
    }, 2000);
  }

  const currentColor =
    colorOptions.find((c) => c.value === selectedColor) ?? colorOptions[0];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-6xl px-4 py-5 sm:px-6 lg:px-8">
        <div className="mb-5 rounded-xl border border-blue-100 bg-blue-50 px-4 py-2 text-center text-sm text-blue-800">
          Home → Custom Tile → Upload → Configurator → Cart → Checkout
        </div>

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

            <button
              onClick={handleUpload}
              disabled={!selectedFile || isUploading}
              className={`mt-4 w-full rounded-xl px-4 py-3 text-sm font-semibold transition ${
                selectedFile && !isUploading
                  ? "bg-slate-900 text-white hover:bg-slate-800"
                  : "cursor-not-allowed bg-slate-200 text-slate-500"
              }`}
            >
              {isUploading ? "Uploading..." : "Upload file"}
            </button>

            {isUploading && (
              <div className="mt-3 rounded-xl border border-blue-100 bg-blue-50 px-4 py-3 text-center text-sm text-blue-700">
                Upload in progress...
              </div>
            )}

            <div className="mt-5 rounded-xl border border-green-100 bg-green-50 p-4">
              <h3 className="text-sm font-semibold text-green-900">
                After upload
              </h3>
              <p className="mt-1 text-sm text-green-800">
                You’ll be taken to the configurator with your model pre-loaded.
              </p>
            </div>
          </div>

          <div>
            <h2 className="mb-4 text-lg font-semibold text-slate-900">
              Step 2 — What you can customize
            </h2>

            <p className="mb-5 text-sm text-slate-600">
              These settings will appear on the configurator page after upload.
            </p>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-blue-700">
                  Dimensions
                </div>
                <div className="grid grid-cols-3 gap-2 text-center">
                  <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
                    <p className="text-xs text-slate-500">L</p>
                    <p className="mt-1 text-base font-semibold">120 mm</p>
                  </div>
                  <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
                    <p className="text-xs text-slate-500">W</p>
                    <p className="mt-1 text-base font-semibold">80 mm</p>
                  </div>
                  <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
                    <p className="text-xs text-slate-500">H</p>
                    <p className="mt-1 text-base font-semibold">95 mm</p>
                  </div>
                </div>
                <p className="mt-3 text-xs text-amber-700">
                  Max 500 mm per side
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-purple-700">
                  Scale
                </div>
                <div className="rounded-lg border border-slate-200 bg-slate-50 p-4 text-center text-base font-semibold">
                  100% default
                </div>
                <p className="mt-3 text-sm text-slate-600">
                  Larger scale uses more material and increases print time.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-green-700">
                  Infill
                </div>
                <div className="grid grid-cols-3 gap-2 text-center">
                  <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
                    <p className="text-base font-semibold">20%</p>
                    <p className="text-xs text-slate-500">Light</p>
                  </div>
                  <div className="rounded-lg border border-green-200 bg-green-50 p-3">
                    <p className="text-base font-semibold text-green-700">
                      50%
                    </p>
                    <p className="text-xs text-slate-500">Medium</p>
                  </div>
                  <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
                    <p className="text-base font-semibold">100%</p>
                    <p className="text-xs text-slate-500">Solid</p>
                  </div>
                </div>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-amber-700">
                  Material
                </div>
                <div className="space-y-2 text-sm text-slate-700">
                  <p>
                    <span className="font-semibold">PLA</span> — Popular
                  </p>
                  <p>
                    <span className="font-semibold">PETG</span> — Strong
                  </p>
                  <p>
                    <span className="font-semibold">ABS</span> — Durable
                  </p>
                  <p>
                    <span className="font-semibold">TPU</span> — Flexible
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="mb-4 text-xs font-semibold uppercase tracking-wide text-rose-700">
                Color and multi-color
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <p className="mb-3 text-sm font-medium text-slate-700">
                    Select your color
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {colorOptions.map((color) => (
                      <button
                        key={color.value}
                        type="button"
                        onClick={() => setSelectedColor(color.value)}
                        className={`flex items-center gap-2 rounded-full border px-3 py-2 text-sm transition ${
                          selectedColor === color.value
                            ? "border-slate-900 bg-slate-900 text-white"
                            : "border-slate-200 bg-white text-slate-700 hover:bg-slate-50"
                        }`}
                      >
                        <span
                          className={`h-4 w-4 rounded-full ${color.className}`}
                        />
                        {color.name}
                      </button>
                    ))}
                  </div>
                  <p className="mt-3 text-sm text-slate-600">
                    Selected color:{" "}
                    <span className="font-medium">{currentColor.name}</span>
                  </p>
                </div>

                <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-slate-700">
                        Multi-color printing
                      </p>
                      <p className="text-xs text-slate-500">
                        Up to 4 colors without surcharge
                      </p>
                    </div>

                    <button
                      type="button"
                      onClick={() => setMultiColorEnabled(!multiColorEnabled)}
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

                  <div className="mt-4 rounded-lg bg-white p-3 text-sm">
                    {multiColorEnabled ? (
                      <p className="text-blue-700">Multi-color enabled.</p>
                    ) : (
                      <p className="text-slate-600">Single color mode.</p>
                    )}
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="mb-4 text-xs font-semibold uppercase tracking-wide text-slate-900">
                How pricing works
              </div>
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                <div className="rounded-xl bg-slate-50 p-4 text-sm">
                  <p className="font-semibold text-slate-900">Material</p>
                  <p className="mt-1 text-slate-600">Base grams × scale³</p>
                </div>
                <div className="rounded-xl bg-slate-50 p-4 text-sm">
                  <p className="font-semibold text-slate-900">Machine</p>
                  <p className="mt-1 text-slate-600">Print hours × rate</p>
                </div>
                <div className="rounded-xl bg-slate-50 p-4 text-sm">
                  <p className="font-semibold text-slate-900">Overhead</p>
                  <p className="mt-1 text-slate-600">Power and maintenance</p>
                </div>
                <div className="rounded-xl bg-slate-50 p-4 text-sm">
                  <p className="font-semibold text-slate-900">Total</p>
                  <p className="mt-1 text-slate-600">Subtotal + margin</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
