import typer

from ldns import server as dns_server

app = typer.Typer()


@app.command()
def server():
    dns_server.bind_and_receive()

if __name__ == "__main__":
    app()
