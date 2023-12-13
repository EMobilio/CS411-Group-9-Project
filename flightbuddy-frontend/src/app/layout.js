import { Inter } from 'next/font/google'
import './globals.css'

import Header from './components/Header'
import Providers from './components/Providers'


const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'FlightBuddy',
  description: 'Create playlists for flights',
}

export default function RootLayout({ children }) {

  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
            <Header />
            <div className="line"></div>
          {children}
        </Providers>
      </body>
    </html>
  )
}
