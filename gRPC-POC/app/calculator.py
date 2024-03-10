import grpc
import calculator_pb2
import calculator_pb2_grpc

def run_calculator_client():
    channel = grpc.insecure_channel('localhost:50051')
    stub = calculator_pb2_grpc.CalculatorStub(channel)
    try:
        response = stub.AddNumbers(calculator_pb2.AddRequest(x=5, y=3))
        print(f"Ergebnis der Addition: {response.result}")
    except grpc.RpcError as e:
        print(f"Fehler beim Aufruf des Taschenrechners: {e}")

if __name__ == '__main__':
    run_calculator_client()
