import { Routes, Route } from "react-router-dom";
import RegisterPage from "./pages/RegisterPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/register" element={<RegisterPage />} />
    </Routes>
  );
}

function HomePage() {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold">Welcome</h1>
      <p className="mt-2">Your frontend is installed correctly 🎉</p>

      <div className="mt-4 space-x-4">
        <a href="/register" className="text-blue-500 underline">
          Register
        </a>
      </div>
    </div>
  );
}
