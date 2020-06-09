import json
import math


def get_distance_by_coords(llat1, llong1, llat2, llong2):
    # pi - число pi, rad - радиус сферы (Земли)
    rad = 6372795
    # координаты в радианах
    lat1 = llat1 * math.pi / 180.
    lat2 = llat2 * math.pi / 180.
    long1 = llong1 * math.pi / 180.
    long2 = llong2 * math.pi / 180.

    # косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    # вычисления длины большого круга
    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    dist = ad * rad
    return round(dist, 2)


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as datafile:
        data = json.load(datafile)
    return data


def get_biggest_bar(data):
    arr = []
    bar_name: str = ''
    bar_address: str = ''
    bar_seatscount: int = 0
    for i in data['features']:
        bar_name = i['properties']['Attributes']['Name']
        bar_address = i['properties']['Attributes']['Address']
        bar_seatscount = i['properties']['Attributes']['SeatsCount']
        arr.append([bar_name, bar_address, bar_seatscount])
    return sorted(arr, key=lambda x: (x[2], x[0]), reverse=True)[0]


def get_smallest_bar(data):
    arr = []
    bar_name: str = ''
    bar_address: str = ''
    bar_seatscount: int = 0
    for i in data['features']:
        bar_name = i['properties']['Attributes']['Name']
        bar_address = i['properties']['Attributes']['Address']
        bar_seatscount = i['properties']['Attributes']['SeatsCount']
        arr.append([bar_name, bar_address, bar_seatscount])
    return sorted(arr, key=lambda x: (x[2], x[0]))[0]


def get_closest_bar(data, latitude, longitude):
    # в jsone перепутаны местами координаты по сравнению с гуглом
    arr = []
    bar_long: float = 0.0
    bar_lat: float = 0.0
    far_from_user: float = 0.0
    for i in data['features']:
        bar_name = i['properties']['Attributes']['Name']
        bar_address = i['properties']['Attributes']['Address']
        bar_long = i['geometry']['coordinates'][0]
        bar_lat = i['geometry']['coordinates'][1]
        far_from_user = get_distance_by_coords(latitude, longitude, bar_lat, bar_long)
        arr.append([bar_name, bar_address, far_from_user])
    return sorted(arr, key=lambda x: (x[2], x[0]))[0]


if __name__ == '__main__':
    file = '1796.json'
    data = load_data(file)
    print(f"Самый большой бар {get_biggest_bar(data)[0]} по адресу "
          f"{get_biggest_bar(data)[1]} имеет {get_biggest_bar(data)[2]} мест")
    print(f"Самый маленький бар {get_smallest_bar(data)[0]} по адресу "
          f"{get_smallest_bar(data)[1]} имеет {get_smallest_bar(data)[2]} мест")
    # test_coords=[55.754109,37.620490]#широта, долгота точки на Красной площади
    user_latitude = input("Введите широту (latitude) вашей точки в градусах, например 55.754109: ")
    user_longitude = input("Введите долготу (longitude) вашей точки в градусах, например 37.620490: ")
    test_coords = list(map(float, [user_latitude, user_longitude]))
    print(f"Ближайший бар {get_closest_bar(data, test_coords[0], test_coords[1])[0]} находится по адресу "
          f"{get_closest_bar(data, test_coords[0], test_coords[1])[1]} в "
          f"{get_closest_bar(data, test_coords[0], test_coords[1])[2]} метрах от вас.")