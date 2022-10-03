import asyncio
from concurrent.futures import process
from unittest import result


# run a single command
def shell_command(command: str, callback,errcallback,args=None):
    ''' 
    run a single shell script

    Parameters:
        command (str): the shell command to be run
        callback (function): a callback function if the command is executes successfully takes 1 args, the output of the shell command
        errcallback (function): a callback function if the command fails
    '''
    result = asyncio.run(async_shell_command(command, callback,errcallback,args))
    return result


# run mulltiple commands at the same time
def shell_commands(commands: list, callback, errcallback):
    '''
    run's multiple command in a list eg['echo hello', 'echo world']

    Parameters:
        commands (str): list of command to be ran eg:['echo hello', 'echo world']
        callback (function): callback function that runs on each command if it is successful 
        errcallback function: callback function that runs on each command when it failes
    '''
    result = asyncio.run(async_shell_commands(commands, callback,errcallback))
    return result


async def async_shell_command(command: str, callback, errcallback, args):
    
    # run a shell command as a subprosess
    Process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await Process.communicate()

    
    if Process.returncode == 0:
        # if the command exexutes without an error
        callback(stdout,args)
    else:
        # if the command exexutes with an error
        errcallback(stderr)

async def async_shell_commands(commands: list, callback, errcallback):
    commands_to_run = []
    for command in commands:
        commands_to_run.append(async_shell_command(command,callback,errcallback,args=None))
    result = await asyncio.gather(*commands_to_run)
