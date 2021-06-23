import click


@click.group()
def main():
    pass


@main.command()
@click.option("--a", prompt=" Enter the first number", type=int)
@click.option("--b", prompt="Enter the second number", type=int)
def add(a, b):
    value = a + b
    click.echo(f"The added value is {value}")


@main.command()
@click.option("--a", prompt="Enter the first number", type=int)
@click.option("--b", prompt="Enter the second number", type=int)
def sub(a, b):
    value = a - b
    click.echo(f"The difference is {value}")


@main.command()
@click.option("--a", prompt="Enter first number", type=int)
@click.option("--b", prompt="Enter the second number", type=int)
def mul(a, b):
    value = a * b
    click.echo(f"The multiplied value {value}")


@main.command()
@click.option("--a", prompt="Enter first number", type=int)
@click.option("--b", prompt="Enter second number", type=int)
def div(a, b):
    value = a / b
    click.echo(f"The divided value {value}")


if __name__ == "__main__":
    main()
