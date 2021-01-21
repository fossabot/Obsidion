"""Logging management."""
import logging


def setup_logging():
    handler = logging.FileHandler(filename="obsidion.log", encoding="utf-8", mode="w")
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )

    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.INFO)
    discord_logger.addHandler(handler)

    obsidion_logger = logging.getLogger("obsidion")
    obsidion_logger.setLevel(logging.INFO)
    obsidion_logger.addHandler(handler)
