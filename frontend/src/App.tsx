import React from "react";
import { Route, Switch } from "react-router-dom";
import moment from "moment";

// styles & assetes
import "./App.scss";

// components
import TheNavigation from "./components/TheNavigation";

// views
import Dashboard from "./view/Dashboard";
// import About from "./view/About";

function App() {
  moment.locale("cs")
  return (
    <div className="App">
      <header>
        <TheNavigation />
      </header>

      <main className="content" >
        <Switch>
          <Route path="/" component={Dashboard} exact />
          {/* <Route path="/about" component={About} /> */}
        </Switch>
      </main>

      <footer>
      </footer>
    </div>
  );
}

export default App;
