# news-image-20261125 — acct1 entrypoint.
# Writes the day's newspaper image to /output/entry.png. Deterministic, no network.
import os

from build import build


def main():
    os.makedirs("/output", exist_ok=True)
    build("/output/entry.png")


if __name__ == "__main__":
    main()
