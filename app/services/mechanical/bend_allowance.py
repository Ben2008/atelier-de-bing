import math

def bend_allowance(angle_deg, radius, thickness, k_factor):
    return math.radians(angle_deg) * (radius + k_factor * thickness)
