// frontend/app/layout.tsx

import "./globals.css";

export const metadata = {
  title: "Risk-Aware ML System",
  description: "Product UI",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
