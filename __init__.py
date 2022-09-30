import socket
from unittest import result

from .shell_run import async_shell_command
import platform
import asyncio


class Netscan:
    def __init__(self) -> None:
        self.base_ip = get_base_ip()  # get the base ip of the network
        self.devices = []

        self.try_count = 2
        asyncio.run(self._get_devices(self.base_ip))

    async def _get_devices(self, base_ip):
        commands = []
        # if no network is connected to the device
        if "127.0.0" in base_ip:
            self.devices.append('127.0.0.1')
            return
        else:
            # generate commands to be run
            for i in range(2, 255):
                # if the script is running on linux
                if platform == 'linux' or 'linux2':
                    command = f"ping -c {self.try_count} {base_ip}.{i}"
                    commands.append([command, base_ip + "." + str(i)])

                # if the script is running on Windows
                if platform == 'win32':
                    command = f"ping -n {self.try_count} {base_ip}.{i}"
                    commands.append([command, base_ip + "." + str(i)])

                # if the script is running on OS X
                if platform == 'darwin':
                    pass

        # run commands
        commands_to_run = []
        for command in commands:
            commands_to_run.append(async_shell_command(command[0], self._device_found, self._errcallback, command[1]))
        await asyncio.gather(*commands_to_run)

    def _device_found(self, _, ip):
        self.devices.append(ip)

    def _errcallback(self, out):
        pass


def get_base_ip():
    return socket.gethostbyname(socket.gethostname()).rsplit('.', 1)[0]
