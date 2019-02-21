# SnowStorm

SnowStorm is an audio streaming tool built to make running internet radio stations through [Icecast](https://icecast.org) easy.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* [Icecast](https://icecast.org)
* [shouty](https://github.com/edne/shouty)

### Installing

Clone the repo
```
git clone https://github.com/chance-nelson/SnowStorm.git
cd SnowStorm 
```

Install dependencies
```
pip install -r requirements.txt
```

Run SnowStorm
```
snowstorm.py path/to/config.ini
```

## Deployment

### Configuration

All needed credentials and audio information are stored in an ini file
```
[SERVER]
host=localhost
port=8000
source_password=AGoodPassword
mount=/stream
admin_password=ABetterPassword

[MUSIC]
playlist=playlist.m3u
```

It is recommended that SnowStorm is run under a systemd service/init script, with a dedicated user.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Chance Nelson** - [chance-nelson](https://github.com/chance-nelson)

See also the list of [contributors](https://github.com/chance-nelson/SnowStorm/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* **Eduardo N** - shouty library - [edne](https://github.com/edne)
* **Icecast Team** - Icecast
