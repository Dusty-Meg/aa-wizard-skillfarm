# Wizard Skillfarm

Skill farm plugin for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth)
(AA).

![License](https://img.shields.io/badge/license-GPLv3-green)
![python](https://img.shields.io/badge/python-3.10-informational)
![django](https://img.shields.io/badge/django-3.2-informational)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

______________________________________________________________________

Basic skill farming helper designed to piggyback off allianceauth-corptools.
Requires django-eveuniverse to also be installed.
Run `python manage.py eveuniverse_load_data types --types-enabled-sections market_groups` after installation to populate the skills list.
