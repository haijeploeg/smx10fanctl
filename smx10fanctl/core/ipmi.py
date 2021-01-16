from cement import shell
from .exc import InvalidIPMISettings, UnknownZoneSpecified


class IPMI:
    def __init__(self, host='localhost', username=None, password=None):
        self._host = host
        self._username = username
        self._password = password

        self.ipmi_cmd_base = self._build_base_cmd(
            self._host,
            self._username,
            self._password)

    def _build_base_cmd(self, host, username, password):
        cmd_name = 'ipmitool'

        if host == 'localhost':
            return cmd_name
        elif host and username and password:
            return '{base} -H {host} -U {username} -P {password}'.format(
                base=cmd_name,
                host=host,
                username=username,
                password=password)
        else:
            raise InvalidIPMISettings('Missing IPMI username and/or password settings')

    def _build_full_cmd(self, cmd, redirect_stdout=False):
        if redirect_stdout:
            return '{} {} >/dev/null'.format(self.ipmi_cmd_base, cmd)

        return '{} {}'.format(self.ipmi_cmd_base, cmd)

    def _percentage_to_hex(self, percentage):
        # Ensure the percentage is always between 0 and 100
        # to prevent the execution of a wrong command
        percentage = max(0, min(100, percentage))
        hex_percentage = (64/100)*float(percentage)

        return '0x{}'.format(int(hex_percentage))

    def get_current_fan_profile(self):
        cmd_args = 'raw 0x30 0x45 0x00'
        cmd = self._build_full_cmd(cmd_args)

        out, err, exit_code = shell.cmd(cmd)

        if exit_code != 0:
            return err
        
        return out

    def set_fan_speed(self, zone, percentage):
        if zone == 'system':
            hex_zone = '0x00'
        elif zone == 'peripheral':
            hex_zone = '0x01'
        else:
            raise UnknownZoneSpecified('Unknown zone: {}'.format(zone))

        hex_percentage = self._percentage_to_hex(percentage)
        cmd_args = 'raw 0x30 0x70 0x66 0x01 {} {}'.format(hex_zone, hex_percentage)
        cmd = self._build_full_cmd(cmd_args, redirect_stdout=True)

        exit_code = shell.cmd(cmd, capture=False)

        if exit_code != 0:
            return False
        
        return True
