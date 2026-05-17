import "./globals.css";
import Navbar from "./components/Navbar";

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
        <Navbar />
        <main className="max-w-7xl mx-auto px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
