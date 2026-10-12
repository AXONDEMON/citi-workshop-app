import json
from store import store

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

    if method == "OPTIONS":
        return response(200, {})

    try:
        if method == "GET" and path == "/notes":
            return response(200, store.list())

        if method == "POST" and path == "/notes":
            try:
                data = json.loads(event.get("body") or "{}")
            except json.JSONDecodeError:
                return response(400, {"error": "Invalid JSON"})
            if not data.get("title"):
                return response(400, {"error": "title is required"})
            note = store.create(data["title"], data.get("content", ""))
            return response(201, note)

        if method == "DELETE" and path.startswith("/notes/"):
            note_id = path.split("/")[-1]
            if not store.delete(note_id):
                return response(404, {"error": "Note not found"})
            return response(200, {"deleted": note_id})

        return response(404, {"error": "Route not found"})

    except Exception as e:
        print("ERROR:", e)   # shows up in CloudWatch logs on AWS
        return response(500, {"error": "Internal server error"})