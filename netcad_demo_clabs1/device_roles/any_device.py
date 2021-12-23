from netcad.device import Device


class AnyDevice(Device):
    sort_key = tuple()
    product_model = "cEOSLab"
    device_type = "cEOS-8"
    os_name = "eos"

    def __init__(self, bld_id: int, fl_id: int, name: str, **kwargs):
        name = f"{name}.{bld_id}{fl_id}"
        super().__init__(name=name, **kwargs)
        self.bld_id = bld_id
        self.flr_id = fl_id

    def __lt__(self, other: "AnyDevice"):
        return self.sort_key < other.sort_key
