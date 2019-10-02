# SnowStorm

SnowStorm is an audio streaming tool built to make running internet radio stations easy

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python 3.6+
* pip

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
_optionally install using setup.py file_
```
python setup.py install
```

Run SnowStorm
```
python run.py
```

## Deployment

### Configuration

Configuration is performed through environment veriables, or easy containerization.

It is recommended that SnowStorm is run under a systemd service/init script, with a dedicated user.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Chance Nelson** - [chance-nelson](https://github.com/chance-nelson)

See also the list of [contributors](https://github.com/chance-nelson/SnowStorm/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* **Quod Libet Team** - mutagen - [quodlibet](https://github.com/quodlibet)
