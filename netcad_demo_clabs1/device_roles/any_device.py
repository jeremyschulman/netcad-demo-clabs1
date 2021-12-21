from netcad.device import Device


class AnyDevice(Device):
    sort_key = tuple()
    product_model = "cEOS-8"
    os_name = "eos"

    def __lt__(self, other: "AnyDevice"):
        return self.sort_key < other.sort_key
