"use client"
import { useRouter } from "next/navigation"
import { ChangeEvent, useState } from "react"
import axios from "axios"

const PlaylistForm = () => {
    const router = useRouter()

    const [flightNumber, setFlightNumber] = useState('')
    const [isValidFlightNumber, setIsValidFlightNumber] = useState(true) 

    const handleSubmit = async (e) => {
        e.preventDefault()

        await axios.get('http://127.0.0.1:8000/api/get_flight_info/', {
                params: {
                    flight_number: flightNumber
                }
            })
            .then((res) => {
                console.log(res.data)
                if (res.status === 200) {
                    if (res.data["error"] === "Flight not found") {
                        setIsValidFlightNumber(false)
                    } else {
                        router.push('/profile')
                    }
                }
                
            })
            .catch((error) => {
                console.log(error)
            })
        }

    return (
        <form className='flight-form' onSubmit={handleSubmit}>
            <h2>Enter Your Flight Number:</h2>
            <input 
                required 
                className='flight-input' 
                name="flightNumber"
                id="flightNumber"
                type="text"
                value={flightNumber}
                onChange={(e) => {setFlightNumber(e.target.value); setIsValidFlightNumber(true)}} 
            />
            <button className='generate-button'>Generate Playlist</button>
            <div>{!isValidFlightNumber && <h3>Flight Not Found</h3>}</div>
        </form>
    )
}

export default PlaylistForm