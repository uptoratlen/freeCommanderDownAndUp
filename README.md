# freeCommanderDownAndUp

# Table of contents

[freeCommanderDownAndUp](#freecommanderdownandup)
- [Table of contents](#table-of-contents)
  * [Overview](#overview)
    + [Limitations](#limitations)
  * [Technologies](#technologies)
  * [What it does](#what-it-does)
  * [Setup](#setup)
  * [Edit freeCommanderDownAndUp_credential.json](#edit-freecommanderdownandup-credentialjson)
  * [Edit freeCommanderDownAndUp.json](#edit-freecommanderdownandupjson)
  * [Run](#run)
    + [Log](#log)
  * [Remarks](#remarks)
  * [FAQ](#faq)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


```
INFO: Currently I review if this thing realy works. (April 4th 2022)
```

## Overview
Since a few years I'm a lifetime user of freeCommander.
A great tool BUT it lacks one feature. Some sort of "autoupdater".
You got the info that a new version is online, but it is a bit stressful to update (login, download, extract and 
install). I even skip some versions just because I'm lazy....
Recently I came across the forum post here:
[Auto Update request](https://freecommander.com/forum/viewtopic.php?p=33610&hilit=download#p25617)
and
[download new version](https://freecommander.com/forum/viewtopic.php?p=37879&hilit=update#p37879)

And by reading that it is not that easy, I though, wait.... and here we are

Here is the link to the FreeCommander forum: (tbd) 


### Limitations
* It works for me, maybe for others as well. I do not pretend to be perfect
* I the webpage changes, I need to adjust and find a better way (or someone else?)
  
## Technologies
The freeCommanderDownAndUp obviously was created in Python with Selenium and the chromedriver.
chromedriver was selected because the firefox profile was a bit (as said lazy...) more complex.

## What it does
For users with less experience, basically what it does:
Python opens a chrome (headless == invisible) browser with a new profile (so your real one does not get altered) by the 
webdriver. chromedriver is the link between chrome and selenium, and than it simulates browser actions like you 
would do, to download a new version. Login, select the download and install it optional or extract the portable version.
As I expect that the webpage may be altered by some time, I guess later the automation will fail. 
The program is to some extent configurable for this case. 

First use (env)
```
* The job ran successful with webpages on April 4th 2022.
* Python 3.7.3 
* Selenium was version 4.1.3
* ChromeDriver 98.0.4758.80 (7f0488e8ba0d8e019187c6325a16c29d9b7f4989-refs/branch-heads/4758@{#972})
* Chrome 99.0.4844.84 (Offizieller Build) (64-Bit)
* Hosting OS was Windows 11 (21H2)
```

## Setup
* Install obviously python (assuming default settings)
  
* install with pip selenium
```
pip install selenium
```
* Get freeCommanderDownAndUp.py, freeCommanderDownAndUp.json and freeCommanderDownAndUp_credential.json from this 
  repository  
Use one of the two options  
  - Go to "releases" and download the last release published as ZIP
  - Download from main   
```
Click on "Code" (green button on top), than select "Download ZIP"
Extract the Content to some writeable folder. Eg. c:\freeCommanderDownAndUp\ 
```
The difference is that main, may contain newer und not so tested code.

* Get chromedriver(.exe) as zip from 
https://chromedriver.chromium.org/downloads, extract the chromedriver.exe
and place it in the same folder as the freeCommanderDownAndUp.py
Use the matching version to the installed chrome browser (check the chromedriver page for more infos)
  ```
  Hint: The "pip install chromedriver" will install the driver also, but may not work, as I expect the driver in the 
  same folder as the .py file. and Pip places it somewhere in the system. I do it that way to keep my versions.
  ```

## Edit freeCommanderDownAndUp_credential.json
This is a not working sample! - You need of course a valid login.

```
[
  {
        "username":"<edit_your_username_here>",
        "password":"<edit_your_password_here>"
  }
]
```
| Name          | value allowed        | Remark                      | introduced |
|:---|:---:|:----------------------------|:----------:|
| username      | string | your donor user name/mail   |   v0.1.0   |
| password      | string   | your donor user password |   v0.1.0   |

```
INFO: in case your password contains a "\" you need to mask them with a "\\"; eg. your pass is "abc\def" json need 
to show "abc\\def"
```


## Edit freeCommanderDownAndUp.json
This is a sample! - You need to adjust to your needs.

```
[
    {
        "log_level": "INFO",
        "login_url": "http://freecommander.com/donors/login",
        "browser_display": "yes",
        "downloadfolder": "c:\\download\\fc\\downloaded",
        "portabletarget": "c:\\download\\fc\\portable",
        "download": "portable32,setup32,portable64,setup64",
        "execute": "64",
        "extract": "32",
        "close_browser": "yes"
    }
]
```
| Name          |              value allowed              | Remark                                                                                                                                                                                                                                 | introduced  |
|:---|:---------------------------------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------:|
| log_level      |   [debug/info/warning/error/critical]   | The log level just in case needed - info is default, debug is fallback                                                                                                                                                                 |   v0.1.0    |
| login_url |                 string                  | The login page of freecommander donor                                                                                                                                                                                                   |   v0.1.0    |
| browser_display |                [Yes/No]                 | In case you want to see the magic                                                                                                                                                                                                      |   v0.1.0    |
| downloadfolder |                 string                  | The location on the disk where all downloads will be copied to. Must exist prior.                                                                                                                                                      |   v0.1.0    |
| portabletarget |                 string                  | The folder where the portable will be extracted to. must <br/>exist prior; Will be overwritten with new files from the zip.                                                                                                            |   v0.1.0    |
| download | [portable32,setup32,portable64,setup64] | A comma separated list of types to be downloaded.                                                                                                                                                                                      |   v0.1.0    |
| execute |                 [32/64]                 | The type 32 or 64 that will be installed, leave blank to skip.                                                                                                                                                                         |      v0.1.0       |
| extract |                  [32/64]                  | The type 32 or 64 that will be extracted, leave blank to skip.                                                                                                                                                                         |   v0.1.0    |
| close_browser |                  [Yes/No]                | In case you want to keep the automated browser open, select "yes". |   v0.1.0    |


## Run 
```
usage: freeCommanderDownAndUp.py

```

### Log
The is a log (rolling) for each run named freeCommanderDownAndUp.log in the same folder as the .py.
Check for more info. And Check log_level just in case.

## Remarks
(TBD)

## FAQ
(TBD)
