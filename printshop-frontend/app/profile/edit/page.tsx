/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiGet, apiPut } from "@/app/lib/api";

export default function EditProfilePage() {
  const [form, setForm] = useState({
    username: "",
    full_name: "",
    email: "",
    phone_number: "",
    city: "",
    street_address: "",
    province: "",
    postal_code: "",
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const loadUser = async () => {
      try {
        const data = await apiGet("/users/me");
        setForm({
          username: data.username || "",
          full_name: data.full_name || "",
          email: data.email || "",
          phone_number: data.phone_number || "",
          city: data.city || "",
          street_address: data.street_address || "",
          province: data.province || "",
          postal_code: data.postal_code || "",
        });
      } catch (err: any) {
        console.log("Could not load user");
      } finally {
        setLoading(false);
      }
    };
    loadUser();
  }, []);
  const [passwords, setPasswords] = useState({
    current: "",
    newPass: "",
    confirm: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPasswords({ ...passwords, [e.target.name]: e.target.value });
  };

  const handleSave = async () => {
    setError("");
    setSuccess("");
    setSaving(true);
    try {
      await apiPut("/users/me", form);
      if (passwords.newPass) {
        if (passwords.newPass !== passwords.confirm) {
          setError("New passwords do not match");
          setSaving(false);
          return;
        }
        await apiPut("/users/me/password", {
          current_password: passwords.current,
          new_password: passwords.newPass,
        });
      }
      setSuccess("Profile updated successfully!");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-gray-300 border-t-gray-900 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-500">Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <Link
        href="/profile"
        className="text-sm text-gray-600 hover:text-gray-900 underline"
      >
        ← Profile
      </Link>
      <h1 className="text-2xl font-bold mt-2 mb-6 text-black">
        Edit your profile
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left — Personal Details */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-lg text-black font-semibold mb-4">
            Personal details
          </h2>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Username
            </label>
            <input
              name="username"
              value={form.username}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Full name
            </label>
            <input
              name="full_name"
              value={form.full_name}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email address
            </label>
            <input
              name="email"
              value={form.email}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Phone number
            </label>
            <input
              name="phone_number"
              value={form.phone_number}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
            />
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                City
              </label>
              <input
                name="city"
                value={form.city}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Street address
              </label>
              <input
                name="street_address"
                value={form.street_address}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Province
              </label>
              <input
                name="province"
                value={form.province}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Postal code
              </label>
              <input
                name="postal_code"
                value={form.postal_code}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
              />
            </div>
          </div>

          {/* Change Password */}
          <h2 className="text-lg font-semibold mt-6 text-black mb-4">
            Change password
          </h2>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Current password
            </label>
            <input
              name="current"
              type="password"
              placeholder="Enter current password"
              value={passwords.current}
              onChange={handlePasswordChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              New password
            </label>
            <input
              name="newPass"
              type="password"
              placeholder="Min 8 chars"
              value={passwords.newPass}
              onChange={handlePasswordChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Confirm new password
            </label>
            <input
              name="confirm"
              type="password"
              placeholder="Re-enter new password"
              value={passwords.confirm}
              onChange={handlePasswordChange}
              className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
            />
          </div>
        </div>

        {/* Right — Payment Details */}
        <div>
          <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
            <h2 className="text-lg font-semibold text-black mb-4">
              Saved payment details
            </h2>
            <p className="text-sm text-gray-500 mb-4">
              Secured by Stripe. Card details are stored securely by Stripe.
            </p>

            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4">
              <p className="text-sm font-medium text-black">
                VISA **** **** **** 4242
              </p>
              <p className="text-sm text-gray-500">Expires 04/28</p>
            </div>

            <button className=" bg-gray-800 w-full border border-gray-300 rounded-lg py-2 text-sm font-medium hover:bg-blue-500 hover:text-white">
              Update saved card
            </button>
            <p className="text-xs text-gray-400 mt-2">
              You will be redirected to Stripe to update
            </p>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-lg font-semibold mb-4 text-black">
              Billing address
            </h2>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Street
              </label>
              <input
                value="123 Main St"
                className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
                readOnly
              />
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  City
                </label>
                <input
                  value="Fox Creek"
                  className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
                  readOnly
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Province
                </label>
                <input
                  value="AB"
                  className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
                  readOnly
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Postal code
                </label>
                <input
                  value="T5A 0A1"
                  className="w-full border border-gray-300 rounded-lg px-4 py-2 text-sm"
                  readOnly
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom buttons */}
      {/* Messages */}
      {success && (
        <div className="mt-6 bg-green-50 border border-green-200 rounded-lg p-3">
          <p className="text-sm text-green-700">{success}</p>
        </div>
      )}
      {error && (
        <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-3">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      {/* Bottom buttons */}
      <div className="flex gap-4 mt-6">
        <button
          onClick={handleSave}
          disabled={saving}
          className={`px-6 py-2.5 rounded-lg text-sm font-medium ${
            saving
              ? "bg-gray-400 text-white cursor-not-allowed"
              : "bg-gray-900 text-white hover:bg-gray-800"
          }`}
        >
          {saving ? "Saving..." : "Save changes"}
        </button>
        <Link
          href="/profile"
          className="border border-gray-300 px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-red-500"
        >
          Cancel
        </Link>
      </div>
    </div>
  );
}
