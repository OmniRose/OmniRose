# For use in the rose_select template

regions_raw = [
    ['Baltic', 2, 12],
    ['Britain', -8, 0],
    ['Iceland', -18, -9],
    ['Mediterranean', -2, 6],
    ['Australia', -8, 18],
    ['New Zealand', 7, 27],
    ['US East Coast', -20, 5],
    ['US West Coast', 10, 22],
    ['Alaska', 6, 22],
]

regions = []
for name, start, end in regions_raw:
    regions.append({
        "name"  : name,
        "start" : start,
        "end"   : end,
    })
