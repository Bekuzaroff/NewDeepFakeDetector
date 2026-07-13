import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";


import "./styles/global.css";
import "./styles/auth.css";
import AuthPage from "./pages/AuthPage";
import HomePage from "./pages/HomePage";
import type { JSX } from "react/jsx-runtime";

const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/auth" replace />;
};

function App() {
  return <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/auth" replace />} />
        <Route path="/auth" element={<AuthPage></AuthPage>} />
        <Route
          path="/home"
          element={
            <ProtectedRoute>
              <HomePage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
}

export default App;