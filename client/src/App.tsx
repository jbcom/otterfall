import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { RivermarshGame } from "./components/RivermarshGame";
import { theme } from './theme';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <RivermarshGame />
    </ThemeProvider>
  );
}

export default App;
