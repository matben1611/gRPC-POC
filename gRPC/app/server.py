import grpc
from concurrent import futures
import time
import datetime
import pytz
import calculator_pb2 
import calculator_pb2_grpc 
import location_pb2
import location_pb2_grpc
import network_pb2
import network_pb2_grpc
import psutil

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class LocationStreamerServicer(location_pb2_grpc.LocationStreamerServicer):
    def StreamLocationInfo(self, request_iterator, context):
        for _ in request_iterator:
            current_time = datetime.datetime.now(pytz.utc)
            location_info = location_pb2.LocationInfo(
                current_datetime=current_time.strftime("%Y-%m-%d %H:%M:%S"),
                timezone=current_time.strftime("%Z"),
                location="Your_Location_Here"
            )
            yield location_info

class NetworkTrafficServicer(network_pb2_grpc.NetworkTrafficServicer):
    def StreamNetworkInfo(self, request_iterator, context):
        while True:
            network_traffic = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            bandwidth = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            network_info = network_pb2.NetworkResponse(
                current_traffic=network_traffic,
                bandwidth=bandwidth
            )
            yield network_info
            time.sleep(3)  # Stream alle 3 Sekunden aktualisieren


class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def AddNumbers(self, request, context):
        result = request.x + request.y
        return calculator_pb2.AddResponse(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    location_pb2_grpc.add_LocationStreamerServicer_to_server(LocationStreamerServicer(), server)
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    network_pb2_grpc.add_NetworkTrafficServicer_to_server(NetworkTrafficServicer(), server)  # Fügen Sie den Netzwerk-Traffic-Dienst hinzu
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started. Listening on port 50051.")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
