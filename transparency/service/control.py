def service_check(service, service1, service2):
    if service1 not in service:
        print("Error - Service1 is wrong! Not available service, possible services:")
        print(list(service.keys()))
        return False

    else:
        if service2 not in service[service1]:
            print("Error - Service2 is wrong! Not available service, possible services:")
            print(list(service[service1].keys()))
            return False
        else:
            return True
