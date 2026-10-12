const API_URL = import.meta.env.VITE_API_URL; // empty for now -> mock mode

let mockNotes = [
    { id: "1", title: "Welcome", content: "This is a mock note." },
];

export async function getNotes() {
    if (!API_URL) return [...mockNotes];
    const res = await fetch(`${API_URL}/notes`);
    if (!res.ok) throw new Error("Failed to load notes");
    return res.json();
}

export async function createNote(note) {
    if (!API_URL) {
        const created = { ...note, id: String(Date.now()) };
        mockNotes = [created, ...mockNotes];
        return created;
    }
    const res = await fetch(`${API_URL}/notes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(note),
    });
    if (!res.ok) throw new Error("Failed to create note");
    return res.json();
}

export async function deleteNote(id) {
    if (!API_URL) {
        mockNotes = mockNotes.filter((n) => n.id !== id);
        return;
    }
    const res = await fetch(`${API_URL}/notes/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Failed to delete note");
}