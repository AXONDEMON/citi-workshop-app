import { Card, CardContent, CardActions, Typography, Button } from "@mui/material";

export default function NoteCard({ note, onDelete }) {
    return (
        <Card>
            <CardContent>
                <Typography variant="h6">{note.title}</Typography>
                <Typography color="text.secondary">{note.content}</Typography>
            </CardContent>
            <CardActions>
                <Button size="small" color="error" onClick={() => onDelete(note.id)}>
                    Delete
                </Button>
            </CardActions>
        </Card>
    );
}