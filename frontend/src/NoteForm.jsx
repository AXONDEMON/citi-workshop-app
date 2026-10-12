import { useState } from "react";
import { Stack, TextField, Button } from "@mui/material";

export default function NoteForm({ onAdd }) {
    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");

    const handleSubmit = () => {
        if (!title.trim()) return;
        onAdd({ title, content });
        setTitle("");
        setContent("");
    };

    return (
        <Stack direction={{ xs: "column", sm: "row" }} spacing={2} sx={{ mb: 3 }}>
            <TextField label="Title" value={title}
                onChange={(e) => setTitle(e.target.value)} fullWidth />
            <TextField label="Content" value={content}
                onChange={(e) => setContent(e.target.value)} fullWidth />
            <Button variant="contained" onClick={handleSubmit}>Add</Button>
        </Stack>
    );
}