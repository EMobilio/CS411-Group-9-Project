"use client"
import { useRouter } from "next/navigation"
import { ChangeEvent, useState } from "react"

const PlaylistForm = () => {
    const router = useRouter()

    const [flightNumber, setFlightNumber] = useState('') 

    const handleSubmit = async (e) => {
        e.preventDefault()

        if (flightNumber === "201") {
            router.push('/profile')
        }
    }

    return (
        <form className='flight-form' onSubmit={handleSubmit}>
            <h2>Enter Your Flight Number:</h2>
            <input 
                required 
                className='flight-input' 
                type="text"
                value={flightNumber}
                onChange={(e) => setFlightNumber(e.target.value)} 
            />
            <button className='generate-button'>Generate Playlist</button>
        </form>
    )
}

export default PlaylistForm