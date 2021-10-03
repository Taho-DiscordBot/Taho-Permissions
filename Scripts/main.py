import requests
import toml
import json

config = toml.load(f"./config.toml")

url = f"https://discord.com/api/{config['other']['api_version']}/applications/{config['bot']['id']}/"
guild_id = config['optional']['guild']
if guild_id == 0:
    url += "commands"
else:
    url += f"guilds/{guild_id}/commands"

headers = {
    "Authorization": f"Bot {config['bot']['token']}"
}

response = requests.get(url = url, headers = headers)
response_list = json.loads(response.text)

def write_options(options:list, spaces: int, file, command, recursive = False):

    def write_spaces(spaces:int):
        for _i in range(spaces):
            file.write(' ')

    if recursive is False:
        file.write('\n')

    for option in options:

        option_name = option['name']
        write_spaces(spaces)
        file.write(f'[{command}.{option_name}]\n\n')

        option_type = option['type']
        write_spaces(spaces)
        file.write(f'type = {option_type}\n')

        write_spaces(spaces)
        file.write(f'name = "{option_name}"\n')

        option_description = option['description']
        write_spaces(spaces)
        file.write(f'description = "{option_description}"\n')

        if 'required' in option:
            required = option['required']
            if required is True:
                write_spaces(spaces)
                file.write(f'required = true\n')
            else:
                write_spaces(spaces)
                file.write(f'required = false\n')
        
        if 'choices' in option:
            file.write('\n')
            choices = option['choices']
            for choice in choices:
                choice_name = choice['name']
                write_spaces(spaces + 4)
                file.write(f'[{option_name}.{choice_name}]\n\n')
                write_spaces(spaces + 4)
                file.write(f'name = "{choice_name}"\n')

                choice_value = choice['value']
                write_spaces(spaces + 4)
                if isinstance(choice_value, str):
                    file.write(f'value = "{choice_value}"\n')
                else:
                    file.write(f'value = {choice_value}\n')

                if choice != choices[-1]:
                    file.write('\n')

        elif option_type in (1, 2):
            file.write('\n')
            recursive_options = option['options']
            write_options(recursive_options, spaces + 4, file, option_name, recursive = True)
        
        elif 'channel_types' in option:
            channel_types = option['channel_types']
            file.write(f'channel_types = {channel_types}\n')

        if option != options[-1]:   
            file.write('\n')
    if recursive is False:
        file.write('\n')

with open(f"./{config['other']['name']}.toml", 'w', encoding = 'utf-8') as file:
    for command in response_list:
        name = command['name']
        file.write(f'[{name}]\n\n')

        command_id = command['id']
        file.write(f'id = {command_id}\n')

        command_type = command['type']
        file.write(f'type = {command_type}\n')

        application_id = command['application_id']
        file.write(f'application_id = {application_id}\n')

        if 'guild_id' in command:
            guild_id = command['guild_id']
            file.write(f'guild_id = {guild_id}\n')

        file.write(f'name = "{name}"\n')

        description = command['description']
        file.write(f'description = "{description}"\n')

        if 'options' in command:
            options = command['options']
            write_options(options, 4, file, name)
        
        permission = command['default_permission']
        if permission is True:
            file.write(f'permission = true\n')
        else:
            file.write(f'permission = false\n')
        
        version = command['version']
        file.write(f'version = {version}\n')

        file.write(f'\n\n')
