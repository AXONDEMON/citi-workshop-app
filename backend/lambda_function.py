import json
import uuid

# In-memory store for now. We'll swap this for MongoDB in Phase 4.
NOTES = {}

HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS",
}


def response(status, body):
    return {"statusCode": status, "headers": HEADERS, "body": json.dumps(body)}


def lambda_handler(event, context):
    method = event.get("httpMethod")
    path = event.get("path", "")

    # CORS preflight: browsers send this before POST/DELETE
    if method == "OPTIONS":
        return response(200, {})

    # GET /notes
    if method == "GET" and path == "/notes":
        return response(200, list(NOTES.values()))

    # POST /notes
    if method == "POST" and path == "/notes":
        try:
            data = json.loads(event.get("body") or "{}")
        except json.JSONDecodeError:
            return response(400, {"error": "Invalid JSON"})
        if not data.get("title"):
            return response(400, {"error": "title is required"})
        note = {
            "id": str(uuid.uuid4()),
            "title": data["title"],
            "content": data.get("content", ""),
        }
        NOTES[note["id"]] = note
        return response(201, note)

    # DELETE /notes/<id>
    if method == "DELETE" and path.startswith("/notes/"):
        note_id = path.split("/")[-1]
        if note_id not in NOTES:
            return response(404, {"error": "Note not found"})
        del NOTES[note_id]
        return response(200, {"deleted": note_id})

    return response(404, {"error": "Route not found"})