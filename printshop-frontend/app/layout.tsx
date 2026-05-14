import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "PrintShop 3D",
  description: "3D Printing Online Store",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        <nav className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <Link href="/" className="text-xl font-bold text-gray-900">
              PrintShop
            </Link>
            <div className="flex gap-6">
              <Link href="/" className="text-gray-600 hover:text-gray-900">
                Models
              </Link>
              <Link href="/cart" className="text-gray-600 hover:text-gray-900">
                Cart
              </Link>
              <Link
                href="/orders"
                className="text-gray-600 hover:text-gray-900"
              >
                Orders
              </Link>
              <Link
                href="/profile"
                className="text-gray-600 hover:text-gray-900"
              >
                Profile
              </Link>
            </div>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
