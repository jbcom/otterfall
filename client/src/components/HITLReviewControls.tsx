import { useState } from 'react';
import {
  Box,
  Slider,
  TextField,
  Button,
  Typography,
  Paper,
} from '@mui/material';

export interface HITLReviewData {
  rating: number;
  notes: string;
  decision: 'REJECT' | 'SAVE' | null;
  timestamp: string;
}

interface HITLReviewControlsProps {
  onSubmit: (data: HITLReviewData) => void;
  defaultRating?: number;
  defaultNotes?: string;
}

export function HITLReviewControls({
  onSubmit,
  defaultRating = 5,
  defaultNotes = '',
}: HITLReviewControlsProps) {
  const [rating, setRating] = useState(defaultRating);
  const [notes, setNotes] = useState(defaultNotes);

  const handleSubmit = (decision: 'REJECT' | 'SAVE') => {
    const reviewData: HITLReviewData = {
      rating,
      notes,
      decision,
      timestamp: new Date().toISOString(),
    };
    onSubmit(reviewData);
  };

  return (
    <Paper
      elevation={3}
      sx={{
        p: 3,
        mt: 2,
        backgroundColor: 'background.paper',
        borderTop: '2px solid',
        borderColor: 'divider',
      }}
    >
      <Typography variant="h6" gutterBottom>
        Human-in-the-Loop Review
      </Typography>

      <Box sx={{ mb: 3 }}>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Rating (1-10)
        </Typography>
        <Slider
          value={rating}
          onChange={(_, value) => setRating(value as number)}
          min={1}
          max={10}
          step={1}
          marks
          valueLabelDisplay="on"
          sx={{
            '& .MuiSlider-markLabel': {
              fontSize: '0.75rem',
            },
          }}
        />
      </Box>

      <Box sx={{ mb: 3 }}>
        <TextField
          fullWidth
          multiline
          rows={4}
          label="Notes"
          placeholder="Provide feedback, observations, or specific issues..."
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          variant="outlined"
        />
      </Box>

      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
        <Button
          variant="outlined"
          color="error"
          size="large"
          onClick={() => handleSubmit('REJECT')}
          sx={{ minWidth: 120 }}
        >
          REJECT
        </Button>
        <Button
          variant="contained"
          color="success"
          size="large"
          onClick={() => handleSubmit('SAVE')}
          sx={{ minWidth: 120 }}
        >
          SAVE
        </Button>
      </Box>
    </Paper>
  );
}

export default HITLReviewControls;
