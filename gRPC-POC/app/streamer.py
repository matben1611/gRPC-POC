import grpc
import location_pb2
import location_pb2_grpc
import time

def run_location_client():
    channel = grpc.insecure_channel('localhost:50051')
    stub = location_pb2_grpc.LocationStreamerStub(channel)
    try:
        while(True):
            responses = stub.StreamLocationInfo(iter([location_pb2.LocationInfo()]))
            for response in responses:
                print(f"Aktuelles Datum und Uhrzeit: {response.current_datetime}")
                print(f"Zeitzone: {response.timezone}")
                print(f"Ort: {response.location}")
                print("-" * 20)
                time.sleep(3)
    except grpc.RpcError as e:
        print(f"Fehler beim Streamen von Ort- und Zeitinformationen: {e}")

if __name__ == '__main__':
    run_location_client()
