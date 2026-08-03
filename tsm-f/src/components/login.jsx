import { Component } from 'react'
import '../App.css'


class SignIn extends Component{
    render() {
       <div className='container'>
            <div className='bo'>
                <h2>Login</h2>
                <div className="fi">
                    <div>
                        <label htmlFor="">Username</label>
                        <input type="text" name="" id="" className="h1" />
                    </div>
                    <div>
                        <label htmlFor="">passwored</label>
                        <input type="password" name="" id="" className="h1"/>
                    </div>
                    <input type="submit" value="Login" id="but" />
                </div>
            </div>
        </div>
    }
}

export default SignIn;