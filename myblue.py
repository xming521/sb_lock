import bluetooth


def find_all():
    print()
    nearby_devices = bluetooth.discover_devices(
        duration=2, lookup_names=True, flush_cache=True, lookup_class=True)
    for addr in nearby_devices:
        print(addr)


def find_only(address):
    nearby_devices = bluetooth.discover_devices(
        duration=4, lookup_names=True, flush_cache=True)
    driver_list = [i[0] for i in nearby_devices]
    if address in driver_list:
        return True
    else:
        return False
