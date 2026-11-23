import type { Metadata, Viewport } from "next";
import "./globals.css";
import RegisterSW from "./register-sw";
export const metadata: Metadata = {
  title: "Trading Intelligence | Pro Terminal",
  description: "Multi-asset trading intelligence and signal analytics platform.",
  applicationName: "Trading Intelligence",
  appleWebApp: { capable: true, statusBarStyle: "black-translucent", title: "Trading Intel" },
  manifest: "/manifest.webmanifest",
};
export const viewport: Viewport = { themeColor: "#070b12", width: "device-width", initialScale: 1, maximumScale: 1 };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body><RegisterSW />{children}</body></html>;
}
