"use client"

import { signIn, signOut, useSession } from "next-auth/react"

export const LoginButton = () => {
    const { session } = useSession()
    
    if (session && session.user) {
        return (
            <a className="login" onClick={() => signOut()}>Sign Out</a>
        )
    }

    return (
        <a 
            className="login" 
            onClick={() => signIn("spotify")}
        >
            Sign In
        </a>
    )
}