from pathlib import Path

import jinja2
import pulumi
from rich import inspect, print
from rich.console import Console

console = Console()

def create_template(path: Path) -> jinja2.Template:
    return jinja2.Template(path.read_text())

class TemplateBase:

    def __init__(self, resource_name: str, path_in: str, path_out: str, **kwargs):
        self.resource_name = resource_name
        self.path_in = Path(path_in)
        self.path_out = Path(path_out)
        self.template = self.render(**kwargs)
    
    def render(self, **kwargs) -> pulumi.Output:
        return pulumi.Output.all(**kwargs) \
            .apply(lambda args: create_template(self.path_in).render(
                **{ k: args[k] for k, v in kwargs.items()}
            ))
