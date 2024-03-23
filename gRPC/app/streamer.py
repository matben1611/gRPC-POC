import grpc
import location_pb2
import location_pb2_grpc
import time
import network_pb2
import network_pb2_grpc

def run_network_client():
    channel = grpc.insecure_channel('localhost:50051')
    stub = network_pb2_grpc.NetworkTrafficStub(channel)
    try:
        responses = stub.StreamNetworkInfo(iter([network_pb2.NetworkRequest()]))
        for response in responses:
            print(f"Aktueller Netzwerkverkehr: {response.current_traffic} bytes")
            print(f"Bandbreite: {response.bandwidth} bytes")
            print("-" * 20)
    except grpc.RpcError as e:
        print(f"Fehler beim Streamen von Netzwerkinformationen: {e}")

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
    #run_location_client()
    run_network_client()
