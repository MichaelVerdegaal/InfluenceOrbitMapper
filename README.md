# Influence Orbit Mapper
![](https://img.shields.io/badge/python-v3.8-blue)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/d62746887a694002907b83828aa57c89)](https://www.codacy.com/gh/MichaelVerdegaal/InfluenceOrbitMapper/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MichaelVerdegaal/InfluenceOrbitMapper&amp;utm_campaign=Badge_Grade)

Orbit Mapper is a tool built for the Influence defi game, set in a whole new fictional space system. The tool is meant
to assist in visualizing asteroids orbit and their locations, and the ability to plan a route between them with
complicated criteria. The tool originated from the need to compare more than 2 asteroids at once, which is not possible
in the basegame. Upon this ideas starting building that 

![Thumbnail](https://cdn.discordapp.com/attachments/697855611643232394/903745762045870080/brave_mK8x5WQ404.png)

## Table of contents
- [Installation](#installation)
  + [Requirements](#requirements)
  + [Dependencies](#dependencies)
  + [Run](#run)
- [Contributing](#contributing)
- [References](#references)

## Installation
### Requirements

- Python 3.8+
- Latest .json data export copied to root directory. You can find
  the [direct download link here](https://www.dropbox.com/sh/5g3ww8wi9n0p4s6/AADcR0lgL8iKTQrpiWUC37Oxa?dl=0) or in
  the [influence-utils repo](https://github.com/Influenceth/influence-utils)
- [Poetry installation](https://python-poetry.org/docs/) for dependency management

### Dependencies

- Install packages via `poetry install`

### Run 

The application backend is [Quart](https://pgjones.gitlab.io/quart/), which is an async version 
of Flask. To run:
- Set the environment variable `QUART_APP=viewer.main:app`
- Execute `quart run` in terminal

Alternatively a run configuration is provided if you're using Pycharm. The steps to make your own run configuration are 
the same as above, but don't forget to set the root directory as the working directory.

## Contributing

Contributing is welcome! To do so:
- Read contributing.md 
- Pick an issue to work on, or submit a new one (preferably adhere to the issue templates)

## References

- [influence-utils](https://github.com/Influenceth/influence-utils). A repository with tools made by the main developers
  of Influence.
