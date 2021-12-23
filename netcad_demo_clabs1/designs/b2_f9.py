from netcad.design_services import Design

from .std_design import create_std_design


def create_design(design: Design) -> Design:
    design = create_std_design(design)
    return design
