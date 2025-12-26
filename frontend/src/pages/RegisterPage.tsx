import { Paper, Typography } from "@mui/material";
import RegisterForm from "../components/RegisterForm";

export default function RegisterPage() {
  return (
    <Paper elevation={3} sx={{ p: 4 }}>
      <Typography variant="h5" align="center" gutterBottom>
        Create your account
      </Typography>
      <RegisterForm />
    </Paper>
  );
}
