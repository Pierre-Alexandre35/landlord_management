import { Paper, Typography, Stack, Link } from "@mui/material";
import LoginForm from "../components/LoginForm";
import { Link as RouterLink } from "react-router-dom";

export default function LoginPage() {
  return (
    <Paper elevation={3} sx={{ p: 4 }}>
      <Stack spacing={2}>
        <Typography variant="h5" align="center">
          Login
        </Typography>

        <LoginForm />

        <Typography variant="body2" align="center">
          Don’t have an account?{" "}
          <Link component={RouterLink} to="/register">
            Register
          </Link>
        </Typography>
      </Stack>
    </Paper>
  );
}
