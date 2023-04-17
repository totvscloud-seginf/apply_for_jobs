import React from 'react';
import useConfig from "./useConfig";
import logo from "../logo.svg";

export default function header() : React.ReactElement {
  const config = useConfig();
  return (
    <header className="App-header flex items-center gap-10">
      <a href='/' className="flex justify-start items-center w-1/2">
        <img src={logo} className="h-12" alt="logo" />
        <h1 className="font-semibold text-slate-900 text-white text-xl">{config.app.TITLE}</h1>
      </a>
      <div className="flex justify-end w-1/2">
        <div className="text-white text-sm">v1.0.0</div>
      </div>
    </header>
  );
}