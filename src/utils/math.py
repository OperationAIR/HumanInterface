
def pressure_to_pa(press_in):
    """Convert pressure in [cm H2O] to [pa]
    Returns a rounded integer"""
    conversion_factor = 98.0665
    return int(round(press_in * conversion_factor))

def pressure_to_cm_h2o(press_in):
    """Convert pressure in [pa] to [cm H2O]
    Returns a rounded integer"""
    conversion_factor = 98.0665
    return int(round(press_in / conversion_factor))
