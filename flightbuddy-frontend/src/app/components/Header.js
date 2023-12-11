import { LoginButton } from "./LoginButton"
import Navbar from "./Navbar"
import Title from "./Title"

const Header = () => {
    return (
        <div className="header">
            <Title />
            <Navbar />
            <LoginButton />
        </div>
    )
}

export default Header