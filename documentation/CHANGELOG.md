# Changelog

# Version History
- `0.0.x` Waffle-Bot POC
- `0.1.x` Multiple Spaces
- `0.2.x` Data Maturity
- `0.3.x` Scroll Command
- `0.4.x` Player Extension 
- `0.5.x` Presentation
- `0.6.x` Reactions
- `1.0.x` App Distribution

# Releases
<!-- @LatestFirst -->

## [0.4.0]
[Player Extension](https://github.com/jrsmth/waffle-bot/milestone/9) (future)
- `#39` Generate Player Average Score [![user](https://img.shields.io/badge/adamj335-181717.svg?style=flat&logo=github)](https://github.com/adamj335)
- `#42` Give User Unique ID on redis[![user](https://img.shields.io/badge/adamj335-181717.svg?style=flat&logo=github)](https://github.com/adamj335)
- `#43` Store King with ID [![user](https://img.shields.io/badge/adamj335-181717.svg?style=flat&logo=github)](https://github.com/adamj335)

## [0.3.1] [![user](https://img.shields.io/badge/adamj335-181717.svg?style=flat&logo=github)](https://github.com/adamj335) [![user](https://img.shields.io/badge/jrsmth-181717.svg?style=flat&logo=github)](https://github.com/jrsmth)
[Scroll Command](https://github.com/jrsmth/waffle-bot/milestone/4) (11/04/2024)
- `#44` Prevent duplicate records for the same streak
- `#46` Add README Badges (Code Coverage, Workflow, Deployment)
- `#48` Newline (`\n`) characters are now rendered properly
- `#50` Implement configurable vars to scroll functionality

## [0.3.0] [![user](https://img.shields.io/badge/adamj335-181717.svg?style=flat&logo=github)](https://github.com/adamj335)
[Scroll Command](https://github.com/jrsmth/waffle-bot/milestone/4) (18/03/2024)
- `#12` Add a slack /command to access scroll information
- `#24` Issues with update_scroll (conflicting data types Record vs Munch dict)

## [0.2.0] [![user](https://img.shields.io/badge/jrsmth-181717.svg?style=flat&logo=github)](https://github.com/jrsmth) [![user](https://img.shields.io/badge/adamj335-181717.svg?style=flat&logo=github)](https://github.com/adamj335)
[Data Maturity](https://github.com/jrsmth/waffle-bot/milestone/8) (08/03/2024)
- `#30` Formalise the conversion of objects into dictionaries (and vice versa) when moving to and from redis
- `#35` Player not getting updated (score & streak)

## [0.1.1] [![user](https://img.shields.io/badge/haydende-181717.svg?style=flat&logo=github)](https://github.com/haydende) [![user](https://img.shields.io/badge/jrsmth-181717.svg?style=flat&logo=github)](https://github.com/jrsmth)
[Multiple Spaces](https://github.com/jrsmth/waffle-bot/milestone/2) (22/02/2024)
- `#29` Added OS check in Makefile to support differences between Windows and Unix-based OS workflows
- `#31` Add workflow step to merge main back into develop after incremental snapshot bump

## [0.1.0] [![user](https://img.shields.io/badge/jrsmth-181717.svg?style=flat&logo=github)](https://github.com/jrsmth)
[Multiple Spaces](https://github.com/jrsmth/waffle-bot/milestone/2) (16/02/2024)
- `#10` Expand project to handle multiple Slack instances
- `#15` Replace python_sdk with bolt
- `#23` Create separate DEV and PROD waffle-bot instances

## [0.0.0] [![user](https://img.shields.io/badge/jrsmth-181717.svg?style=flat&logo=github)](https://github.com/jrsmth) [![user](https://img.shields.io/badge/adamj335-181717.svg?style=flat&logo=github)](https://github.com/adamj335) [![user](https://img.shields.io/badge/haydende-181717.svg?style=flat&logo=github)](https://github.com/haydende)
[Waffle-Bot POC](https://github.com/jrsmth/waffle-bot/milestone/1) (09/02/2024)
- `#4` Define Workflow: versioning, release, CICD, Change Log
- `#5` Establish test base
- `#7` Generate Streak History object

[0.0.0]: https://github.com/jrsmth/waffle-bot/releases/tag/0.0.0
[0.1.0]: https://github.com/jrsmth/waffle-bot/compare/0.0.0...0.1.0
[0.1.1]: https://github.com/jrsmth/waffle-bot/compare/0.1.0...0.1.1
[0.2.0]: https://github.com/jrsmth/waffle-bot/compare/0.1.1...0.2.0
[0.3.0]: https://github.com/jrsmth/waffle-bot/compare/0.2.0...0.3.0
[0.3.1]: https://github.com/jrsmth/waffle-bot/compare/0.3.0...0.3.1
[0.4.0]: https://github.com/jrsmth/waffle-bot/compare/0.3.1...0.4.0