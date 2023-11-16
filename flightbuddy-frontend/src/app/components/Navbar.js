import Link from "next/link";

const Navbar = () => {
    return (
        <nav className="navbar">
            <Link className="link" href='/'>Home</Link>
            <Link className="link" href='/profile'>Profile</Link>
        </nav>
    );
}

export default Navbar;