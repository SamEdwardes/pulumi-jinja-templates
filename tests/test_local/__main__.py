import pulumi
import pulumi_command
from pulumi_jinja_templates import local
from rich import print, inspect

import sys

home_directory = pulumi_command.local.Command(
    resource_name='get home directory',
    create="echo $HOME"
)
username = pulumi_command.local.Command(
    resource_name='get user name',
    create="echo $USER"
)
pulumi.export('user-name', username.stdout)


# inspect(home_directory, title="home_directory")
# inspect(home_directory.stdout, title="home_directory.stdout")

template = local.Template(
    resource_name="copy template",
    path_in="./templates/in.yaml",
    path_out="./templates/out.yaml",
    home_dir=home_directory.stdout,
    user=username.stdout
)
