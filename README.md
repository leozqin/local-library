# Local Library
Local Library is a simple read-only ebook library that indexes your `epub` ebooks against a read-only file system and provides a nice UI to browse and download them.

# Running
## Dev
To start the API server, in the repository root, create a fresh Python 3.12 virtual environment. Then, install the `requirements.txt` in that venv. Then, run `fastapi dev` to start the API server.

To start the web interface, first install nodejs 22. Then, in a different terminal session, navigate to `web` and run `npm install`. Finally, run `npm run dev` to start the web interface on port 4321.

If you're using nix, you can install pre-reqs by doing `nix-shell nodejs_22 python312`.

## Docker
Modify [the Compose stack](docker-compose.yml) to your heart's content, and then run `docker compose up` to start the app.
