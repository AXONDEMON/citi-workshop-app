import json
from lambda_function import lambda_handler

def call(method, path, body=None):
    event = {"httpMethod": method, "path": path,
             "body": json.dumps(body) if body else None}
    res = lambda_handler(event, None)
    print(method, path, "->", res["statusCode"], res["body"])
    return json.loads(res["body"])

created = call("POST", "/notes", {"title": "First", "content": "Hello"})
call("POST", "/notes", {"content": "no title"})   # expect 400
call("GET", "/notes")
call("DELETE", f"/notes/{created['id']}")
call("GET", "/notes")                              # expect empty list
call("DELETE", "/notes/does-not-exist")            # expect 404

n = call("POST", "/notes", {"title": "Old", "content": "x"})
call("PUT", f"/notes/{n['id']}", {"title": "New", "content": "y"})   # expect 200
call("PUT", f"/notes/{n['id']}", {"content": "no title"})            # expect 400
call("PUT", "/notes/missing", {"title": "t"})                        # expect 404
call("GET", "/notes")                                                # shows "New"