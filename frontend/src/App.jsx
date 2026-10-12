import { useState, useEffect } from "react";
import {
  AppBar, Toolbar, Typography, Container, Box, Alert, CircularProgress,
} from "@mui/material";
import NoteForm from "./NoteForm";
import NoteCard from "./NoteCard";
import { getNotes, createNote, deleteNote } from "./api";

export default function App() {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getNotes()
      .then(setNotes)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const handleAdd = async (note) => {
    try {
      const created = await createNote(note);
      setNotes((prev) => [created, ...prev]);
    } catch (e) {
      setError(e.message);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteNote(id);
      setNotes((prev) => prev.filter((n) => n.id !== id));
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar><Typography variant="h6">Notes App</Typography></Toolbar>
      </AppBar>

      <Container maxWidth="md" sx={{ py: 4 }}>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        <NoteForm onAdd={handleAdd} />

        {loading ? (
          <CircularProgress />
        ) : (
          <Box sx={{
            display: "grid", gap: 2,
            gridTemplateColumns: { xs: "1fr", md: "1fr 1fr" }
          }}>
            {notes.map((n) => <NoteCard key={n.id} note={n} onDelete={handleDelete} />)}
          </Box>
        )}
      </Container>
    </>
  );
}