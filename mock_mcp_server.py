#!/usr/bin/env python3
import json
import sys

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            request = json.loads(line)
            if request.get("method") == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {"tools": [{"name": "echo_tool", "description": "Returns what you sent"}]}
                }
            elif request.get("method") == "tools/call":
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {"content": f"Echo: {request['params']['arguments'].get('msg')}"}
                }
            else:
                response = {"jsonrpc": "2.0", "id": request.get("id"), "error": "Unknown method"}
            
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
        except:
            break

if __name__ == "__main__":
    main()
