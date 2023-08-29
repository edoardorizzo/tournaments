import HomePage from "./pages/HomePage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TournamentNamePage from "./pages/TournamentNamePage";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<HomePage></HomePage>} />
          <Route path="/tournament" element={<TournamentNamePage></TournamentNamePage>} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
