import asyncio
from importlib.metadata import PackageNotFoundError, version

import grpc
from tripsphere.itinerary import metadata_pb2, metadata_pb2_grpc


class MetadataServicer(metadata_pb2_grpc.MetadataServiceServicer):
    def GetVersion(self, request, context):
        try:
            _version = version("itinerary")
        except PackageNotFoundError:
            _version = "unknown"
        return metadata_pb2.GetVersionResponse(version=_version)


async def serve():
    server = grpc.aio.server()
    metadata_pb2_grpc.add_MetadataServiceServicer_to_server(MetadataServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
