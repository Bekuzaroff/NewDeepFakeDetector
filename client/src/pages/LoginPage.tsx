import type { AxiosError } from "axios";
import { useState, type ChangeEvent, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

interface AuthResponse {
  access_token: string;
  status: string;
  message: string;
}

interface ErrorResponse {
  status?: string;
  message?: string;
}


function LoginPage(){
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      setError("");
      setLoading(true);

      if (username.length < 3) {
        setError("Имя пользователя должно быть минимум 3 символа");
        setLoading(false);
        return;
      }

      if (password.length < 6) {
        setError("Пароль должен быть минимум 6 символов");
        setLoading(false);
        return;
      }

      try {
        const response = await api.post<AuthResponse>(
          `auth/user/`,
          {
            username,
            pswrd: password
          }
        );

        if (response.data.access_token) {
          localStorage.setItem("token", response.data.access_token);
          localStorage.setItem("username", username);
          navigate("/home", { replace: true });
        } else {
          setError("Не удалось получить токен");
        }
      } catch (err) {
        const error = err as AxiosError<ErrorResponse>;
        console.log(error)
        setError(error.response?.data?.message || "Ошибка логина");
      } finally {
        setLoading(false);
      }
    };

  return <form className="auth-card" onSubmit={handleSubmit}>
  <h2>Логин</h2>

  <input
    type="text"
    placeholder="Имя пользователя"
    value={username}
    onChange={(e: ChangeEvent<HTMLInputElement>) =>
                setUsername(e.target.value)
              }
    required
  />

  <input
    type="password"
    placeholder="Пароль"
    value={password}
    onChange={(e: ChangeEvent<HTMLInputElement>) =>
            setPassword(e.target.value)
          }
    required
  />

  {error && (
          <div
            style={{
              color: "#ff6b6b",
              fontSize: 14,
              textAlign: "center",
              padding: "8px",
              background: "rgba(255,0,0,0.1)",
              borderRadius: "8px",
            }}
          >
            {error}
          </div>
        )}

        <button
          type="submit"
          className="gradient-btn"
          disabled={loading}
          style={{
            width: "100%",
            padding: "14px",
          }}
        >
          {loading ? "Загрузка..." : "Войти"}
        </button>
</form>
}


export default LoginPage