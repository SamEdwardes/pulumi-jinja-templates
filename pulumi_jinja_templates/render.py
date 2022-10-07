from pathlib import Path
from typing import List
import jinja2
import pulumi

from pulumi_command import local

from rich import print, inspect
from rich.console import Console
import hashlib

console = Console()


class Template:

    def __init__(self, resource_name: str, path_in: str, path_out: str, **kwargs):
        self.resource_name = resource_name
        self.path_in = Path(path_in)
        self.path_out = Path(path_out)
        self.template = self.render(**kwargs)
        self.command = local.Command(
            resource_name=self.resource_name,
            create=pulumi.Output.concat('echo "', self.template, f'" > {self.path_out}')
        )

    def render(self, **kwargs) -> pulumi.Output:
        output = pulumi.Output.all(**kwargs) \
            .apply(lambda args: f"Rendered string: {', '.join([args[key] for key in kwargs.keys()])}")
        return output

    # def copy_template(self):
    #     command = local.Command(
    #         resource_name=self.resource_name,
    #         create=pulumi.Output.concat('echo "', self.template, f'" > {self.path_out}')
    #     )
    #     return command

    def hash_template(self) -> pulumi.Output:
        text = self.path_in.read_text()
        hash_str = hashlib.sha224(bytes(text, encoding='utf-8')).hexdigest()
        return pulumi.Output.concat(hash_str)


# =============================================================================

# def hash_file(path: str) -> pulumi.Output:
#     text = Path(path).read_text()
#     hash_str = hashlib.sha224(bytes(text, encoding='utf-8')).hexdigest()
#     return pulumi.Output.concat(hash_str)


# def _create_template(path: str) -> jinja2.Template:
#     return jinja2.Template(Path(path).read_text())


# def copy_template(
#     resource_name: str,
#     template: pulumi.Output,
#     path_out: str,
# ):
#     return local.Command(
#         resource_name=resource_name,
#         create=pulumi.Output.concat('echo "', template, f'" > {Path(path_out)}'),
#         triggers=[hash_file(f.file_in)]

#     )
#     return None


# def render_template(path: str, **kwargs) -> pulumi.Output:
#     print(f"{kwargs=}")
#     outputs = list(kwargs.values())
#     print(f"{outputs=}")
#     return (
#         pulumi.Output.all(**kwargs)
#         .apply(lambda x: f"Rendered string: {' '.join([x[key] for key, values in kwargs.items()])}")
#     )
    # return pulumi.Output.all(
    #     outputs
    # ).apply(
    #     lambda x: _create_template(
    #         path
    #     ).render(
    #         **kwargs
    #     )
    # )
    # return None

# def write_template(template: pulumi.Output, path_out: str):

        # Copy the server side files
# @dataclass
# class serverSideFile:
#     file_in: str
#     file_out: str
#     template_render_command: pulumi.Output

# server_side_files = [
#     serverSideFile(
#         "server-side-files/config/database.conf",
#         "~/database.conf",
#         pulumi.Output.all(db.address).apply(lambda x: create_template("server-side-files/config/database.conf").render(db_address=x[0]))
#     ),
#     serverSideFile(
#         "server-side-files/config/load-balancer",
#         "~/load-balancer",
#         pulumi.Output.all(server.public_ip).apply(lambda x: create_template("server-side-files/config/load-balancer").render(server_ip_address=x[0]))
#     ),
#     serverSideFile(
#         "server-side-files/config/rserver.conf",
#         "~/rserver.conf",
#         pulumi.Output.all().apply(lambda x: create_template("server-side-files/config/rserver.conf").render())

#     ),
# ]

# command_copy_config_files = []
# for f in server_side_files:
#     command_copy_config_files.append(
#         remote.Command(
#             f"copy {f.file_out} server {name}",
#             create=pulumi.Output.concat('echo "', f.template_render_command, f'" > {f.file_out}'),
#             connection=connection, 
#             opts=pulumi.ResourceOptions(depends_on=[server]),
#             triggers=[hash_file(f.file_in)]
#         )
#     )
