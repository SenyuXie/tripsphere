from concurrent import futures
from importlib.metadata import PackageNotFoundError, version

import grpc

from itinerary.protos import itinerary_pb2, itinerary_pb2_grpc


class ItineraryServicer(itinerary_pb2_grpc.ItineraryServiceServicer):
    def GetVersion(self, request, context):
        try:
            ver = version("itinerary")
        except PackageNotFoundError:
            ver = "unknown"
        return itinerary_pb2.GetVersionResponse(version=ver)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    itinerary_pb2_grpc.add_ItineraryServiceServicer_to_server(
        ItineraryServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
