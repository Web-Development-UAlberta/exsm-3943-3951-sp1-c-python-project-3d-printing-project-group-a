/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */
"use client";

import { useState, useEffect } from "react";
import { apiGet, apiPost, apiDelete, apiPut } from "../lib/api";
export default function AdminPage() {
  const [filaments, setFilaments] = useState<any[]>([]);
  const [printers, setPrinters] = useState<any[]>([]);
  const [orders, setOrders] = useState<any[]>([]);
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddFilament, setShowAddFilament] = useState(false);
  const [newFilament, setNewFilament] = useState({
    name: "",
    color: "",
    stock: "",
    price: "",
    wear: false,
    manufacturer: "",
  });

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const [filamentsData, printersData, ordersData, usersData] =
          await Promise.all([
            apiGet("/admin/filaments"),
            apiGet("/admin/printers"),
            apiGet("/admin/orders"),
            apiGet("/admin/users"),
          ]);
        setFilaments(filamentsData);
        setPrinters(printersData);
        setOrders(ordersData);
        setUsers(usersData);
      } catch (err: any) {
        console.log("Could not load dashboard");
      } finally {
        setLoading(false);
      }
    };
    loadDashboard();
  }, []);

  const statusColor: Record<string, string> = {
    Pending: "bg-amber-50 text-amber-700 ring-1 ring-amber-200",
    Printing: "bg-blue-50 text-blue-700 ring-1 ring-blue-200",
    Shipped: "bg-violet-50 text-violet-700 ring-1 ring-violet-200",
    Completed: "bg-emerald-50 text-emerald-700 ring-1 ring-emerald-200",
  };

  const handleAddFilament = async () => {
    try {
      const data = await apiPost("/admin/filaments", {
        material_name: newFilament.name,
        color_hex: newFilament.color,
        quantity_in_stock: Number(newFilament.stock),
        filament_price: Number(newFilament.price),
        more_wear_and_tear: newFilament.wear,
        manufacturer: newFilament.manufacturer,
      });
      setFilaments([...filaments, data]);
    } catch (err: any) {
      console.log("Could not add filament");
    }
    setNewFilament({
      name: "",
      color: "",
      stock: "",
      price: "",
      wear: false,
      lead: "",
    });
    setShowAddFilament(false);
  };

  const addPrinter = async () => {
    try {
      const data = await apiPost("/admin/printers", { printer_type_id: 1 });
      setPrinters([...printers, data]);
    } catch (err: any) {
      console.log("Could not add printer");
    }
  };

  const removePrinter = async (id: number) => {
    try {
      await apiDelete(`/admin/printers/${id}`);
    } catch (err: any) {
      console.log("Could not remove printer");
    }
    setPrinters(printers.filter((p) => p.printer_id !== id));
  };

  const toggleAdmin = async (id: number) => {
    const user = users.find((u) => u.user_id === id);
    const isAdmin = user?.is_admin;
    try {
      if (isAdmin) {
        await apiPut(`/admin/users/${id}/remove-admin`, {});
      } else {
        await apiPut(`/admin/users/${id}/make-admin`, {});
      }
      setUsers(
        users.map((u) =>
          (u.id || u.user_id) === id
            ? { ...u, is_admin: !isAdmin, isAdmin: !isAdmin }
            : u,
        ),
      );
    } catch (err: any) {
      console.log("Could not toggle admin");
    }
  };

  const activeOrders = orders.filter(
    (o) => o.order_status === "Printing" || o.order_status === "Pending",
  ).length;
  const lowStock = filaments.filter(
    (f) => (f.quantity_in_stock || f.stock || 0) < 300,
  ).length;
  const totalOrders = orders.length;
  const freePrinters = printers.filter((p) => p.status === "Available").length;

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-gray-300 border-t-gray-900 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-500">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-7xl px-6 py-8">
        <div className="mb-8">
          <p className="text-xs uppercase tracking-[0.22em] text-slate-500">
            PrintShop Admin
          </p>
          <h1 className="mt-2 text-4xl font-medium tracking-tight text-slate-950">
            Admin Dashboard
          </h1>
          <p className="mt-2 text-sm text-slate-500">
            Monitor inventory, printers, users, and order status.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-8 lg:grid-cols-4">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-3xl font-medium text-blue-700">{activeOrders}</p>
            <p className="mt-1 text-sm text-slate-500">Active orders</p>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-3xl font-medium text-rose-600">{lowStock}</p>
            <p className="mt-1 text-sm text-slate-500">Low stock</p>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-3xl font-medium text-emerald-600">
              {totalOrders}
            </p>
            <p className="mt-1 text-sm text-slate-500">Total orders</p>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-3xl font-medium text-violet-600">
              {freePrinters}/{printers.length}
            </p>
            <p className="mt-1 text-sm text-slate-500">Printers free</p>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-2">
          <div className="space-y-8">
            <div>
              <div className="mb-4 flex items-center justify-between">
                <h2 className="text-xl font-medium text-slate-950">
                  Filament inventory
                </h2>
                <button
                  onClick={() => setShowAddFilament(!showAddFilament)}
                  className="cursor-pointer text-sm font-medium text-blue-700 hover:text-blue-800"
                >
                  + Add filament
                </button>
              </div>

              <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
                <table className="w-full">
                  <thead className="bg-slate-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                        Name
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                        Color
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                        Stock
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                        $/kg
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                        Wear
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wide text-slate-500">
                        Lead
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {filaments.map((f) => (
                      <tr
                        key={f.filament_id}
                        className={
                          f.quantity_in_stock < 300 ? "bg-rose-50/50" : ""
                        }
                      >
                        <td className="px-4 py-3 text-sm text-slate-900">
                          {f.material_name}
                        </td>
                        <span className="flex items-center gap-2">
                          {f.color_hex && (
                            <div
                              className="w-4 h-4 rounded-full border border-slate-300"
                              style={{ backgroundColor: f.color_hex }}
                            />
                          )}
                          {f.color_hex || "--"}
                        </span>
                        <td className="px-4 py-3 text-sm">
                          <span
                            className={
                              f.quantity_in_stock < 300
                                ? "font-medium text-rose-700"
                                : "text-slate-700"
                            }
                          >
                            {f.quantity_in_stock}g
                          </span>
                          {f.quantity_in_stock < 300 && (
                            <span className="ml-2 rounded-full bg-rose-100 px-2 py-0.5 text-xs font-medium text-rose-700">
                              LOW
                            </span>
                          )}
                        </td>
                        <td className="px-4 py-3 text-sm text-slate-700">
                          ${f.filament_price}/kg
                        </td>
                        <td className="px-4 py-3 text-sm text-slate-700">
                          {f.more_wear_and_tear ? "Yes" : "No"}
                        </td>
                        <td className="px-4 py-3 text-sm text-slate-500">
                          {f.manufacturer || "--"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="mt-3 rounded-xl border border-rose-100 bg-rose-50 px-4 py-3 text-center">
                <p className="text-xs text-rose-700">
                  Alert when stock falls below 30%
                </p>
              </div>

              {showAddFilament && (
                <div className="mt-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                  <div className="mb-4">
                    <h3 className="text-sm font-medium text-slate-950">
                      New filament
                    </h3>
                    <p className="mt-1 text-xs text-slate-500">
                      Add a new material to inventory.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
                    <input
                      placeholder="Material: [PLA]"
                      value={newFilament.name}
                      onChange={(e) =>
                        setNewFilament({ ...newFilament, name: e.target.value })
                      }
                      className="rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-900 focus:ring-4 focus:ring-slate-900/5"
                    />
                    <input
                      placeholder="Color: [#000000]"
                      value={newFilament.color}
                      onChange={(e) =>
                        setNewFilament({
                          ...newFilament,
                          color: e.target.value,
                        })
                      }
                      className="rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-900 focus:ring-4 focus:ring-slate-900/5"
                    />
                    <input
                      placeholder="Quantity [1000]"
                      value={newFilament.stock}
                      onChange={(e) =>
                        setNewFilament({
                          ...newFilament,
                          stock: e.target.value,
                        })
                      }
                      className="rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-900 focus:ring-4 focus:ring-slate-900/5"
                    />
                    <input
                      placeholder="Price [25]"
                      value={newFilament.price}
                      onChange={(e) =>
                        setNewFilament({
                          ...newFilament,
                          price: e.target.value,
                        })
                      }
                      className="rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-900 focus:ring-4 focus:ring-slate-900/5"
                    />
                    <button
                      onClick={() =>
                        setNewFilament({
                          ...newFilament,
                          wear: !newFilament.wear,
                        })
                      }
                      className={`cursor-pointer rounded-xl border px-3 py-2 text-sm transition ${
                        newFilament.wear
                          ? "border-slate-950 bg-slate-950 text-white"
                          : "border-slate-300 bg-white text-slate-700 hover:bg-slate-50"
                      }`}
                    >
                      {newFilament.wear ? "Wear: Yes" : "Wear: No"}
                    </button>
                    <input
                      placeholder="e.g. Manufacturer"
                      value={newFilament.manufacturer}
                      onChange={(e) =>
                        setNewFilament({
                          ...newFilament,
                          manufacturer: e.target.value,
                        })
                      }
                      className="rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none focus:border-slate-900 focus:ring-4 focus:ring-slate-900/5"
                    />
                  </div>

                  <button
                    onClick={handleAddFilament}
                    className="mt-4 w-full rounded-xl bg-slate-950 px-4 py-3 text-sm font-medium text-white shadow-lg shadow-slate-950/10 cursor-pointer hover:bg-slate-800"
                  >
                    Save new filament
                  </button>
                </div>
              )}
            </div>

            <div>
              <h2 className="mb-4 text-xl font-medium text-slate-950">
                User management
              </h2>
              <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
                <table className="w-full">
                  <thead className="bg-slate-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-500">
                        Username
                      </th>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-500">
                        Full name
                      </th>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-500">
                        Role
                      </th>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-500">
                        Action
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {users.map((user) => (
                      <tr key={user.user_id}>
                        <td className="px-4 py-3 text-sm text-slate-900">
                          {user.username}
                        </td>
                        <td className="px-4 py-3 text-sm text-slate-700">
                          {user.full_name || user.fullName}
                        </td>
                        <td className="px-4 py-3">
                          <span
                            className={`rounded-full px-2.5 py-1 text-xs font-medium ${
                              user.is_admin
                                ? "bg-violet-50 text-violet-700 ring-1 ring-violet-200"
                                : "bg-slate-100 text-slate-600"
                            }`}
                          >
                            {user.is_admin ? "Admin" : "Customer"}
                          </span>
                        </td>
                        <td className="px-4 py-3">
                          <button
                            onClick={() => toggleAdmin(user.user_id || user.id)}
                            className={`cursor-pointer rounded-lg px-3 py-1.5 text-xs font-medium transition ${
                              user.is_admin
                                ? "bg-rose-50 text-rose-700 hover:bg-rose-100"
                                : "bg-blue-50 text-blue-700 hover:bg-blue-100"
                            }`}
                          >
                            {user.is_admin ? "Remove admin" : "Make admin"}
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div className="space-y-8">
            <div>
              <div className="mb-4 flex items-center justify-between">
                <h2 className="text-xl font-medium text-slate-950">
                  Printers ({printers.length}x Prusa MK4)
                </h2>
                <button
                  onClick={addPrinter}
                  className="cursor-pointer rounded-xl bg-slate-950 px-4 py-2 text-sm font-medium text-white shadow-lg shadow-slate-950/10 hover:bg-slate-800"
                >
                  + Add printer
                </button>
              </div>

              <div className="space-y-4">
                {printers.map((printer) => (
                  <div
                    key={printer.printer_id}
                    className={`overflow-hidden rounded-2xl border bg-white shadow-sm ${
                      printer.status === "Printing"
                        ? "border-blue-200"
                        : "border-emerald-200"
                    }`}
                  >
                    <div
                      className={`flex items-center justify-between px-4 py-3 text-white ${
                        printer.status === "Printing"
                          ? "bg-blue-600"
                          : "bg-emerald-600"
                      }`}
                    >
                      <span className="text-sm font-medium">
                        {printer.printer_name} #{printer.printer_id}
                      </span>
                      <span className="text-sm font-medium">
                        {printer.status}
                      </span>
                    </div>
                    <div className="flex items-center justify-between gap-4 px-4 py-4">
                      {printer.current_order ? (
                        <p className="text-sm text-slate-700">
                          <span className="font-medium text-slate-900">
                            Current order:{" "}
                          </span>
                          #{printer.current_order} — {printer.filament}
                        </p>
                      ) : (
                        <p className="text-sm font-medium text-emerald-700">
                          Ready for next job
                        </p>
                      )}
                      <button
                        onClick={() => removePrinter(printer.printer_id)}
                        className="cursor-pointer rounded-lg border border-rose-200 bg-rose-50 px-3 py-1.5 text-xs font-medium text-rose-700 hover:bg-rose-100"
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h2 className="mb-4 text-xl font-medium text-slate-950">
                All orders
              </h2>
              <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
                <table className="w-full">
                  <thead className="bg-slate-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-500">
                        Order
                      </th>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-500">
                        Status
                      </th>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-500">
                        Total
                      </th>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-500">
                        Printer
                      </th>
                      <th className="px-4 py-3 text-left text-sm font-medium text-slate-500">
                        Action
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {orders.map((order) => (
                      <tr key={order.order_id}>
                        <td className="px-4 py-3 text-sm text-slate-900">
                          #{order.order_id} — {order.username}
                        </td>
                        <td className="px-4 py-3">
                          <span
                            className={`rounded-full px-2.5 py-1 text-xs font-medium ${statusColor[order.order_status] || "bg-gray-100 text-gray-600"}`}
                          >
                            {order.order_status}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-sm text-slate-700">
                          ${(order.total_price || 0).toFixed(2)}
                        </td>
                        <td className="px-4 py-3 text-sm text-slate-500">
                          {order.items?.[0]?.model || "--"}
                        </td>
                        <td className="px-4 py-3">
                          <select
                            defaultValue={order.order_status}
                            onChange={async (e) => {
                              try {
                                await apiPut(
                                  `/admin/orders/${order.order_id}`,
                                  {
                                    order_status: e.target.value,
                                  },
                                );
                                setOrders(
                                  orders.map((o) =>
                                    o.order_id === order.order_id
                                      ? { ...o, order_status: e.target.value }
                                      : o,
                                  ),
                                );
                              } catch (err: any) {
                                console.log("Could not update order");
                              }
                            }}
                            className="cursor-pointer rounded-lg bg-slate-100 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-200"
                          >
                            <option value="Pending">Pending</option>
                            <option value="Printing">Printing</option>
                            <option value="Shipped">Shipped</option>
                            <option value="Completed">Completed</option>
                            <option value="Cancelled">Cancelled</option>
                          </select>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
