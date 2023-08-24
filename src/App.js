import HomePage from "./pages/HomePage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TournamentNamePage from "./pages/TournamentNamePage";
import PlayerNamePage from "./pages/PlayerNamePage";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<HomePage></HomePage>} />
          <Route path="/tournament" element={<TournamentNamePage></TournamentNamePage>} />
          <Route path="/player" element={<PlayerNamePage></PlayerNamePage>} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
