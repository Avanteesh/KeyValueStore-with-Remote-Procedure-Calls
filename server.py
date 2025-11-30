import grpc, logging
from concurrent import futures
from proto import schema_pb2, schema_pb2_grpc

db_store = {}

class KeyStoreService(schema_pb2_grpc.KeyStore):
    def Set(self, keyvalue: schema_pb2.KeyValue, context):
        db_store[keyvalue.key.key_name] = keyvalue.value.value_name
        return schema_pb2.Status(result=f"OK")

    def Get(self, key: schema_pb2.Key, context):
        if key.key_name not in db_store:
            return schema_pb2.ResponseVal(noval=False)
        return schema_pb2.ResponseVal(value=schema_pb2.Value(value_name=db_store[key.key_name]))

    def Delete(self, key: schema_pb2.Key, context):
        keyname = key.key_name
        if keyname not in db_store:
            return schema_pb2.Status(result=f"integer (0)")
        del db_store[keyname]
        return schema_pb2.Status(result=f"integer (1)")

    def LPush(self, keyval: schema_pb2.KeyValue, context):
        """
        push into the deque!
        """
        keyname, value = keyval.key.key_name, keyval.value.value_name
        if keyname not in db_store:
            db_store[keyname] = []
        db_store[keyname].append(value)
        return schema_pb2.Status(result=f"integer (1)")

    def LRange(self, rangeobj: schema_pb2.ListRange, context):
        keyname, start, stop = rangeobj.key.key_name, rangeobj.start, rangeobj.stop
        if keyname not in db_store:
            return schema_pb2.Deque(key_name=schema_pb2.Key(key_name="null"),data=[])
        lis = db_store[keyname]
        if stop < 0:
            lis = lis[start:len(lis)-stop]
        return schema_pb2.Deque(
          key_name=schema_pb2.Key(key_name=keyname),data=lis
        )

    def LPop(self, key: schema_pb2.Key, context):
        keyname = key.key_name
        if keyname not in db_store:
            return schema_pb2.ResponseVal(noval=False)
        return schema_pb2.ResponseVal(
          value=schema_pb2.Value(value_name=db_store[keyname].pop())
        )

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    schema_pb2_grpc.add_KeyStoreServicer_to_server(KeyStoreService(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server started in port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()



