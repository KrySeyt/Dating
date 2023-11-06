import type { Metadata } from "next"

import "./globals.css"

import { GeistMono, GeistSans } from "geist/font"

export const metadata: Metadata = {
    title: "Dating",

    description: "Find your like-minded people",
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body className={`${GeistSans.variable} ${GeistMono.variable}`}>
                {children}
            </body>
        </html>
    )
}
