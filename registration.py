import os
import json
import socket
import http.client

CONSUL_HOST = "consul"
CONSUL_PORT = 8500

AGENT_NAME = "student_agent"
SERVICE_PORT = 5001
AGENT_HOSTNAME = os.environ.get('AGENT_HOSTNAME', socket.gethostname())  # e.g., 'student_agent'

def register_service():
    service = {
        "ID": AGENT_NAME,
        "Name": AGENT_NAME,
        "Address": AGENT_HOSTNAME,
        "Port": SERVICE_PORT,
        "Tags": ["flask", "student", "agent"],
        "Check": {
            "HTTP": f"http://{AGENT_HOSTNAME}:{SERVICE_PORT}/health",
            "Interval": "10s"
        }
    }

    conn = http.client.HTTPConnection(CONSUL_HOST, CONSUL_PORT)
    conn.request("PUT", "/v1/agent/service/register", body=json.dumps(service),
                 headers={"Content-Type": "application/json"})
    res = conn.getresponse()
    print(f"Registered with Consul. Status: {res.status} {res.reason}")
    conn.close()

if __name__ == "__main__":
    import time
    while True:
        register_service()
        time.sleep(60)
