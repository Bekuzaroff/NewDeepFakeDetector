import { useState } from "react"
import LoginPage from "./LoginPage";
import SignUpPage from "./SignupPage";

function AuthPage(){

    const [has_account, setHasAccount] = useState<boolean>(false)

    return (<div className="auth-container">

        {has_account ? (<LoginPage></LoginPage>) : (<SignUpPage></SignUpPage>)}

        <span className="small-text" style={{ cursor: "pointer" }} onClick={() => {
            setHasAccount(!has_account)
        }}> {has_account ? ("нет аккаунта?") : ("уже есть аккаунт?")} </span>
    </div>);
}

export default AuthPage