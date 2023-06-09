import {
  Routes,
  Route,
} from "react-router-dom";

import Header from "./components/Header";

import Home from "./routes/Home";
import Upload from "./routes/Upload"
import Delete from "./routes/Delete";
import About from "./routes/About";

function App() {
  return (
    <div>
      <Header />
      <div className="app--container">
        <Routes>
          <Route path="/" element={<Home /> } ></Route>
          <Route path="/upload" element={<Upload /> } ></Route>
          <Route path="/delete" element={<Delete /> } ></Route>
          <Route path="/about" element={<About /> } ></Route>
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
