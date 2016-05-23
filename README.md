Migrate Eclipse to Android Studio
========
This is a project targeting convert eclipse project to android studio project with easy.

## What's it offering?
Handle those file from eclipse project to traditional gradle-based android studio project:
* Asset file
* So file
* Aidl file
* Manifest file and progurad rules

## Prerequisite
### Tool
* Python installed <https://www.python.org/downloads/>
* Python IDE (optional)
### Knowledge
* Basic Python knowledge
* Basic Gradle knowledge

## How to use
Just to call this method:
```Python
start_migrate(eclipse_project_path, output_path)
```
The **output_path** will be created if not exist.

### My eclipse project only has a main project
* Create a hello world Project using Android Studio
* Move generated file in app folder
* modify build.gradle:
change this line **apply plugin: 'com.android.library'** to **apply plugin: 'com.android.application'**

### My eclipse project only has a main project and many library projects
* For main project, manage it like above
* For library project, Move generated Android Studio Project in root folder

### Post work
Your still need to configure your app info (minSdkVersion something like this) in your main module **build.gradle**:
something like those:
```groovy
defaultConfig {
    applicationId "your package name"
    minSdkVersion 15
    targetSdkVersion 23
    versionCode 1
    versionName "1.0"
}
```
and **signingConfigs** too.
For more information: check <http://tools.android.com/tech-docs/new-build-system/user-guide> this post.
This guide helps me a lot when I am learning gradle.

A lot more:
* adding all your projects in **settings.gradle**
* manage in your library dependency in libarary **build.gradle**
* You will still need a little effort to make your project compile in most cases

If your are a Chinese Reader, this article may help you <https://github.com/gengjiawen/gengjiawen.github.io/blob/master/_posts/2015-7-4-MigrateFromEclipseToAndroidStudio.md>.

## Notice
* This script is written in Python3
* Tested in Python 3.4 & 3.5

## License

    Copyright 2016 Daniel Geng

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

