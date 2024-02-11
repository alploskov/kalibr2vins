import yaml
import typer


kalibr2vins = typer.Typer()

@kalibr2vins.command()
def gen(input_dir: str = typer.Option(help="path to dirrectory with output from kalibr"),
        output_dir: str = typer.Option(help="path to dirrectory for vins configuration")):
    """
    translate kalibr config to vins-fusion
    """
    typer.echo(input_dir, output_dir)
