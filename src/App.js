import HomePage from "./pages/HomePage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TournamentNamePage from "./pages/TournamentNamePage";
import MatchPage from "./pages/MatchPage";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<HomePage></HomePage>} />
          <Route path="/tournament" element={<TournamentNamePage></TournamentNamePage>} />
          <Route path="/matches" element={<MatchPage></MatchPage>} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
