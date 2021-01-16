import psutil


def get_current_cpu_temp(package_id='Package id 0'):
    temp_dict = psutil.sensors_temperatures()

    return temp_dict
