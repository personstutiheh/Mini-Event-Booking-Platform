import {useState} from "react";

function Login({onLoginSuccess}){
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    async function handleSubmit(e){
        e.preventDefault();
        setError("");

        const response = await fetch("http://localhost:8000/login",{
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({email, password}),
        });
        
        if(!response.ok){
            setError("Invalid email or password");
            return;
        }
        const data = await response.json();
        onLoginSuccess(data.access_token, email);
    }
    return(
        <form onSubmit={handleSubmit}>
            <h2>Login</h2>
            {error && <p style={{color: "red"}}>{error}</p>}
            <input placeholder="Email" value={email} onChange={e =>setEmail(e.target.value)}/>
            <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
            <button type="submit">Login</button>
        </form>
    );
}
export default Login;