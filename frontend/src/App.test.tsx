import * as React from "react";
import ReactDOM from "react-dom";

import App from "./App";

jest.mock("./components/ConfigContext");
jest.mock("../app/api/setPassword", () => ({}));
jest.mock("../app/api/requestPassword", () => ({}));

it("renders without crashing", () => {
  const div = document.createElement("div");
  ReactDOM.render(<App />, div);
  ReactDOM.unmountComponentAtNode(div);
});
