import pulumi
from pulumi_command import local

from ..template import TemplateBase


class Template(TemplateBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.copy_command()
    
    def copy_command(self) -> local.Command:
        return local.Command(
            resource_name=self.resource_name,
            create=pulumi.Output.concat('echo "', self.template, f'" > {self.path_out}'),
            delete=f"rm {self.path_out}"
        )
