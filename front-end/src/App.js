import React from "react";
import "./App.css";

import { Container } from "@material-ui/core";
import MenuAppBar from "./Navbar";

import Home from "./home/Home";

function App() {
  return (
    <div className="App">
      <MenuAppBar />
      <Container fixed>
        <Home />
      </Container>
    </div>
  );
}

export default App;
