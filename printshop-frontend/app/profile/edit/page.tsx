"use client";

import { useState } from "react";
import Link from "next/link";

export default function EditProfilePage() {
  const [form, setForm] = useState({
    username: "Robel_M",
    fullName: "Robel Measho",
    email: "R@email.com",
    phone: "780-555-0101",
    city: "Fox Creek",
    street: "123 Main St",
    province: "AB",
    postalCode: "T5A 0A1",
  });

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

  const handleSave = () => {
    // later this will connect to Rami's backend
    console.log("Save profile:", form);
    console.log("Password change:", passwords);
  };

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
              name="fullName"
              value={form.fullName}
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
              name="phone"
              value={form.phone}
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
                name="street"
                value={form.street}
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
                name="postalCode"
                value={form.postalCode}
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
      <div className="flex gap-4 mt-6">
        <button
          onClick={handleSave}
          className="bg-gray-900 text-white px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-gray-800"
        >
          Save changes
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
