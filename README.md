# Demo - NetCadCam using ContainerLab

---

**NOTE** - This is under repo is under active development and is meant for
examination purposes only at this time. More is coming soon, including a video
and the related repositories used by this demo.

---

This respository contains a "Hello, world!" example of using the
[NetCadCam](https://github.com/jeremyschulman/netcadcam) toolkit.

The  network testbed uses the
[containerlab](https://containerlab.srlinux.dev/) system, version 0.22.0.

The demonstration defines three designs, showing in the
[netcad.toml](netcad.toml) configuration file.  Each design is a "building-floor".
Each design has, by default, the following:

* one "core" device
* two "access" devices, each with 2 uplinks to the core
* one "access-point", that is connected to an access-device

The "access-point" does not exist in the containerlab demonstration.  It is
designed as a psuedo-device for the purpose of the design elements.

The primary purpose of this repo is to allow anyone interested in the NetCadCam
project to see a working example of design files and how they are used to
validate the operational state of the network.  Inclusively:

  * The ability to generate the network checks and validate the operational state of the network
  * The ability to generate the cEOS configuration files
  * The ability to generate the containerlabs topology file
  * See how NetCadCam can be extended to include containerlab CLI features
