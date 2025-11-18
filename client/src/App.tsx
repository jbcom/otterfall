import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { PrototypesScreen } from "./prototypes/PrototypesScreen";
import { theme } from './theme';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <PrototypesScreen />
    </ThemeProvider>
  );
}

export default App;
