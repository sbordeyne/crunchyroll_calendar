"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Crunchyroll Calendar."""


if __name__ == "__main__":
    main(prog_name="crunchyroll-calendar")  # pragma: no cover
