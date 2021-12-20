from netcad.vlan import VlanProfile

vlan_native = VlanProfile(
    vlan_id=411, name="not_vlan_1", description="using different native vlan in demo"
)


vlan_phone = VlanProfile(vlan_id=10, name="PHONE", description="Voip Phone ports")

vlan_printer = VlanProfile(vlan_id=20, name="PRINTERS", description="Printer ports")
