# ruff: noqa: E402
from opentelemetry.instrumentation import auto_instrumentation

auto_instrumentation.initialize()

import argparse
import asyncio
import logging

import grpc
from tripsphere.itinerary import metadata_pb2_grpc

from itinerary.services.metadata import MetadataServiceServicer

logger = logging.getLogger(__name__)


async def serve(port: int) -> None:
    server = grpc.aio.server()
    metadata_pb2_grpc.add_MetadataServiceServicer_to_server(
        MetadataServiceServicer(), server
    )
    server.add_insecure_port(f"[::]:{port}")
    logger.info(f"Start gRPC server on port {port}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log_level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    parser.add_argument(
        "--port",
        type=int,
        default=50051,
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    asyncio.run(serve(args.port))
