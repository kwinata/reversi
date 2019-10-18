class Settings:
    # TODO: Make tile object to be its own class
    tile_1 = '#'
    tile_2 = '.'
    empty_tile = ' '
    tile_hint = '?'
    dimensions = [8, 8]


for dim in Settings.dimensions:
    if dim < 2:
        raise ValueError("Minimal dimension is 2, if not it is either not useful or does not make sense")
