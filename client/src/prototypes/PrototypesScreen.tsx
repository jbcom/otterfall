import { useState, Suspense } from 'react';
import {
  Box,
  Container,
  Typography,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Paper,
  CircularProgress,
  Button,
} from '@mui/material';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
  useSortable,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { PROTOTYPES, PrototypeManifest } from './shared';

interface SortablePrototypeItemProps {
  prototype: PrototypeManifest;
  onSelect: (id: string) => void;
  isSelected: boolean;
}

function SortablePrototypeItem({ prototype, onSelect, isSelected }: SortablePrototypeItemProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: prototype.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <ListItem
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      disablePadding
      sx={{ mb: 1 }}
    >
      <Paper
        elevation={isSelected ? 8 : 2}
        sx={{
          width: '100%',
          bgcolor: isSelected ? 'primary.dark' : 'background.paper',
        }}
      >
        <ListItemButton onClick={() => onSelect(prototype.id)}>
          <ListItemText
            primary={prototype.title}
            secondary={prototype.description}
            primaryTypographyProps={{
              color: isSelected ? 'primary.contrastText' : 'text.primary',
              fontWeight: isSelected ? 'bold' : 'normal',
            }}
            secondaryTypographyProps={{
              color: isSelected ? 'primary.contrastText' : 'text.secondary',
            }}
          />
        </ListItemButton>
      </Paper>
    </ListItem>
  );
}

export function PrototypesScreen() {
  const [prototypes, setPrototypes] = useState(PROTOTYPES.slice().sort((a, b) => a.order - b.order));
  const [selectedPrototype, setSelectedPrototype] = useState<string | null>(null);
  const [PrototypeComponent, setPrototypeComponent] = useState<React.ComponentType<{ onExit: () => void }> | null>(null);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      setPrototypes((items) => {
        const oldIndex = items.findIndex((item) => item.id === active.id);
        const newIndex = items.findIndex((item) => item.id === over.id);
        return arrayMove(items, oldIndex, newIndex);
      });
    }
  };

  const handleSelectPrototype = async (id: string) => {
    const prototype = prototypes.find((p) => p.id === id);
    if (!prototype) return;

    setSelectedPrototype(id);
    const module = await prototype.load();
    setPrototypeComponent(() => module.default);
  };

  const handleExitPrototype = () => {
    setSelectedPrototype(null);
    setPrototypeComponent(null);
  };

  if (selectedPrototype && PrototypeComponent) {
    return (
      <Suspense fallback={
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
          <CircularProgress />
        </Box>
      }>
        <PrototypeComponent onExit={handleExitPrototype} />
      </Suspense>
    );
  }

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
        Rivermarsh Prototypes
      </Typography>

      <Typography variant="body1" paragraph align="center" sx={{ mb: 4, color: 'text.secondary' }}>
        Select a prototype to test. Drag to reorder.
      </Typography>

      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragEnd={handleDragEnd}
      >
        <SortableContext
          items={prototypes.map((p) => p.id)}
          strategy={verticalListSortingStrategy}
        >
          <List>
            {prototypes.map((prototype) => (
              <SortablePrototypeItem
                key={prototype.id}
                prototype={prototype}
                onSelect={handleSelectPrototype}
                isSelected={selectedPrototype === prototype.id}
              />
            ))}
          </List>
        </SortableContext>
      </DndContext>
    </Container>
  );
}
