# 📦 KeyValueStore-with-Remote-Procedure-Calls

A minimal distributed **Key–Value Store** implemented using **gRPC**.  
Supports basic Redis-like operations — `SET`, `GET`, `DELETE`, list operations (`LPUSH`, `LRANGE`, `LPOP`) — exposed as **RPC methods**.

> This project is designed for learning RPC concepts, Protobuf schemas, and gRPC networking.

---

## ⭐ Features

- 🚀 Remote command execution using **gRPC**
- 📦 In-memory key–value database
- 🧠 Redis-like list operations
- 🔐 Strongly typed protobuf interfaces
- 🧱 Extensible service design
- 🧪 Includes multi-client test scripts

---

## 🗂 Project Structure

```
KeyValueStore-with-Remote-Procedure-Calls/
├── server/          # gRPC server implementation
├── client/          # gRPC client interface
├── proto/           # .proto schema
├── tests/           # multithread + integration tests
├── README.md
└── pyproject.toml / requirements.txt
```

---

# 🧬 RPC Schema (Protobuf)

The core service definition:

```proto
service KeyStore {
  rpc Set(KeyValue) returns (Status);
  rpc Get(Key) returns (Value);
  rpc Delete(Key) returns (Status);

  rpc LPush(ListInsert) returns (Status);
  rpc LRange(ListRange) returns (ListValues);
  rpc LPop(Key) returns (Value);
}
```

This means the client sends structured messages — not raw strings or JSON — with strict, type-safe fields.

---

# 🚀 Getting Started

## 📥 Clone the Repository

```bash
git clone https://github.com/<your-user>/KeyValueStore-with-Remote-Procedure-Calls.git
cd KeyValueStore-with-Remote-Procedure-Calls
```

---

# 🐍 Python Setup

> You mentioned using **uv** — so here is the recommended workflow.

### 1️⃣ Create and activate environment

```bash
uv venv
source .venv/bin/activate
```

### 2️⃣ Install dependencies

If using `requirements.txt`:

```bash
uv pip install -r requirements.txt
```

If using `pyproject.toml`:

```bash
uv pip install .
```

---

# 🛠️ Generate Protobuf Code

> Only required if modifying `.proto` files.

```bash
python -m grpc_tools.protoc \
  -I proto \
  --python_out=. \
  --grpc_python_out=. \
  proto/mini_redis.proto
```

This produces:

- `mini_redis_pb2.py` (message types)
- `mini_redis_pb2_grpc.py` (service stubs)

---

# ▶️ Running The Server

```bash
python server/main.py
```

Output example:

```
Server started on port 50051
```

---

# 💻 Running the Client

```bash
python client/main.py
```

You’ll be prompted for input or you can call operations through API-style scripts.

---

# 🧪 Tests

This project includes **multi-client tests** for concurrency and correctness.

Run:

```bash
python tests/test_remote.py
```

Tests include scenarios such as:

✔ concurrent SET on same keys  
✔ list push/pop on shared keys  
✔ server reboot safety  
✔ invalid key handling

Outputs assert final state consistency.

---

# 📡 Example Commands

### Set a key

```
SET foo 123
```

### Get a key

```
GET foo
→ 123
```

### Delete a key

```
DELETE foo
→ OK
```

---

## 📚 List Operations

### Push

```
LPUSH scores 1 2 3
```

List stored as:
```
["3", "2", "1"]
```

### Range

```
LRANGE scores 0 2
→ ["3","2","1"]
```

### Pop

```
LPOP scores
→ "3"
```

---

# 🧠 Design Philosophy

This project is intentionally simple:

- No JSON, no REST
- No object serialization magic
- Protobuf → AST → typed remote calls
- Simpler than Redis, but illustrates the core concepts

gRPC gives:

✔ type safety  
✔ streaming RPC methods  
✔ language-agnostic API  
✔ scalability to microservices

---

# 🛤️ Roadmap

Suggested future improvements:

- [ ] Persistent RDB-style snapshotting
- [ ] TTL / expiry support
- [ ] Authentication
- [ ] Streaming list iteration
- [ ] Multiple databases (DB index)
- [ ] Load balancing across nodes
- [ ] Real benchmarks (Locust)

---

# 🤝 Contributing

Contributions are welcome!

1. Fork repo  
2. Create feature branch  
3. Submit pull request

---

# 📄 License

MIT — free to use, learn, and modify.
