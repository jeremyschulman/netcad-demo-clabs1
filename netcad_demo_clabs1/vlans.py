from netcad.vlan import VlanProfile

vlan_native = VlanProfile(
    vlan_id=411, name="not_vlan_1", description="using different native vlan in demo"
)


vlan_phones = VlanProfile(vlan_id=10, name="Phones", description="Voip Phone ports")

vlan_printers = VlanProfile(vlan_id=20, name="Printers", description="Printer ports")

vlan_media_iptvs = VlanProfile(
    vlan_id=20, name="IPTV", description="IPTV set-top-boxes"
)

vlan_inband_mgmt = VlanProfile(
    vlan_id=911, name="Inband_MGMT", description="SVI used for inband management"
)
