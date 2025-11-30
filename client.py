import logging
import grpc
import schema_pb2
import schema_pb2_grpc


class RedisRPCClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.remote_store = None

    def delete(self, _key: str):
        self.check_connection()
        return self.remote_store.Delete(
          schema_pb2.Key(key_name=_key)
        ).result

    def get(self, _key: str):
        self.check_connection()
        response = self.remote_store.Get(
          schema_pb2.Key(key_name=_key)
        )
        match response.WhichOneof("res"):
            case "noval":
                return "(null)"
            case "value":
                return response.value.value_name

    def set(self, key: str, value: str):
        self.check_connection()
        return self.remote_store.Set(
          schema_pb2.KeyValue(
           key=schema_pb2.Key(key_name=key),
           value=schema_pb2.Value(value_name=value)
          )
        ).result

    def lpush(self, key: str, value: str):
        self.check_connection()
        return self.remote_store.LPush(
          schema_pb2.KeyValue(
           key=schema_pb2.Key(key_name=key),
           value=schema_pb2.Value(value_name=value)
          )
        ).result

    def lrange(self, key: str, start: int, stop: int):
        self.check_connection()
        return self.remote_store.LRange(
          schema_pb2.ListRange(
           key=schema_pb2.Key(key_name=key),
           start=start,stop=stop
          )
        )

    def lpop(self, key: str):
        self.check_connection()
        response = self.remote_store.LPop(schema_pb2.Key(key_name=key))
        match response.WhichOneof("res"):
            case "noval":
                return "(null)"
            case "value":
                return response.value.value_name

    def check_connection(self):
        if self.remote_store is None:
            raise OSError("server not found! please reconnect to the RPC Server")
    
    def connect(self):
        """Create reusable gRPC channel"""
        channel = grpc.insecure_channel(f"{self.host}:{self.port}")
        self.remote_store = schema_pb2_grpc.KeyStoreStub(channel)

