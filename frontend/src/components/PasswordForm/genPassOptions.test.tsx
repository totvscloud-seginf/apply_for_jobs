import * as React from "react";
import ReactDOM from "react-dom";
import GenPassOptions from "./genPassOptions";


it("Renders Password Component without crashing", () => {
  const div = document.createElement("div");
  ReactDOM.render(<GenPassOptions setValue={() => {}}/>, div);
  ReactDOM.unmountComponentAtNode(div);
});
