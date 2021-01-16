import psutil


def get_current_cpu_temp(label_prefix=None):
    temp_sensors = psutil.sensors_temperatures()
    coretemp = temp_sensors['coretemp']

    if label_prefix:
        current_temp = [int(x.current) for x in coretemp if label_prefix in x.label]
    else:
        current_temp = [int(x.current) for x in coretemp]

    return max(current_temp)
