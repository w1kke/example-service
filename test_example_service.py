import sys
import grpc

from grpc_health.v1 import health_pb2 as heartb_pb2
from grpc_health.v1 import health_pb2_grpc as  heartb_pb2_grpc

# import the generated classes
import service.service_spec.example_service_pb2_grpc as grpc_ex_grpc
import service.service_spec.example_service_pb2 as grpc_ex_pb2

from service import registry

if __name__ == "__main__":
    
    try:
        test_flag = False
        if len(sys.argv) == 2:
            if sys.argv[1] == "auto":
                test_flag = True
        
        # Example Service - Arithmetic
        endpoint = input("Endpoint (localhost:{}): ".format(
            registry["example_service"]["grpc"])) if not test_flag else ""
        if endpoint == "":
            endpoint = "localhost:{}".format(
                registry["example_service"]["grpc"])
        
        grpc_method = input(
            "Method (add|sub|mul|div|hc): ") if not test_flag else "mul"

        # Open a gRPC channel
        channel = grpc.insecure_channel("{}".format(endpoint))

        if grpc_method == "hc":
            stub = heartb_pb2_grpc.HealthStub(channel)
            request = heartb_pb2.HealthCheckRequest(service="MyService")
            response = stub.Check(request, timeout=10)
            print(response)
        else:
            a = float(input("Number 1: ") if not test_flag else "12")
            b = float(input("Number 2: ") if not test_flag else "7")
            stub = grpc_ex_grpc.CalculatorStub(channel)
            number = grpc_ex_pb2.Numbers(a=a, b=b)
            
            if grpc_method == "add":
                response = stub.add(number)
                print(response.value)
            elif grpc_method == "sub":
                response = stub.sub(number)
                print(response.value)
            elif grpc_method == "mul":
                response = stub.mul(number)
                print(response.value)
            elif grpc_method == "div":
                response = stub.div(number)
                print(response.value)
            else:
                print("Invalid method!")
                exit(1)
    
    except Exception as e:
        print(e)
        exit(1)
