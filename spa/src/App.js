import {
  Routes,
  Route,
} from "react-router-dom";

import Header from "./components/Header";

import Home from "./routes/Home";

function App() {
  return (
    <div>
      <Header />
      <div className="app--container">
        <Routes>
          <Route path="/" element={<Home /> } ></Route>
          <Route
          path="*"
          element={
            <main style={{ padding: "1rem" }}>
              <h1>Why are you here? Go Back!</h1>
            </main>
          }
          />
        </Routes>
      </div>
    </div>
  );
}

export default App;
