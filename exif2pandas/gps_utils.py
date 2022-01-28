# based on: https://gist.github.com/snakeye/fdc372dbf11370fe29eb
def convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    try:
        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)
    except (ZeroDivisionError, IndexError):
        d = m = s = 0

    return d + (m / 60.0) + (s / 3600.0)


def get_exif_location(exif_data):
    """
    Returns the latitude and longitude, if available, from the provided exif_data
    (obtained through get_exif_data above)
    """
    lat = None
    lon = None

    gps_latitude = exif_data.get('GPS GPSLatitude')
    gps_latitude_ref = exif_data.get('GPS GPSLatitudeRef')
    gps_longitude = exif_data.get('GPS GPSLongitude')
    gps_longitude_ref = exif_data.get('GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = convert_to_degress(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = round(0 - lat, 6)

        lon = convert_to_degress(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = round(0 - lon, 6)
        return lat, lon

    return None, None
