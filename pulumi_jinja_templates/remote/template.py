import pulumi
from pulumi_command import remote

from ..template import TemplateBase


class Template(TemplateBase):
    def __init__(self, connection: remote.ConnectionArgs, **kwargs):
        super().__init__(**kwargs)
        self.connection = connection
        self.copy_command()
    
    def copy_command(self) -> remote.Command:
        return remote.Command(
            resource_name=self.resource_name,
            connection=self.connection,
            create=pulumi.Output.concat('echo "', self.template, f'" > {self.path_out}')
            delete=f"rm {self.path_out}"
        )