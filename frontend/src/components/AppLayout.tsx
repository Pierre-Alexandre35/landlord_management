import { Container, Box } from "@mui/material";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "background.default", py: 8 }}>
      <Container maxWidth="sm">{children}</Container>
    </Box>
  );
}
