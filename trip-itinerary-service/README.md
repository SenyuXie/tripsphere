First, generate the gRPC code:

```shell
uv run -m grpc_tools.protoc \
    -I../contracts/protobuf \
    --python_out=libs/tripsphere/src \
    --grpc_python_out=libs/tripsphere/src \
    --mypy_out=libs/tripsphere/src \
    --mypy_grpc_out=libs/tripsphere/src \
    ../contracts/protobuf/tripsphere/itinerary/metadata.proto
```

Then, start the server:

```shell
uv run -m itinerary.server
```