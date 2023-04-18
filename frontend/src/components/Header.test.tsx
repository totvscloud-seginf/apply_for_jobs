import * as React from "react";
import ReactDOM from "react-dom";
import Header from "./Header";

jest.mock("./ConfigContext");

it("Renders Header without crashing", () => {
  const div = document.createElement("div");
  ReactDOM.render(<Header/>, div);
  ReactDOM.unmountComponentAtNode(div);
});
