import "./App.css";
import * as React from "react";
import Header from "./components/Header";
import PassForm from "./components/PasswordForm";
import Password from "./components/Password";

/**
 * Our Web Application
 */
export default function App( {passID}: {passID?: string | null} ) {
  return (
    <div className="App">
      <Header />
      <p className="App-intro mt-10 px-20">
        {!passID 
        ? ( <PassForm /> ) 
        : (
            <div className="w-3/4 m-auto">
              <Password id={passID} />
            </div>
          )
        }
      </p>
    </div>
  );
}
