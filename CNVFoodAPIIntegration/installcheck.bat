echo off
where java >nul 2>nul
if %errorlevel%==1 (
    @echo Java not found in path. Please install JDK and configure JAVA_HOME
)
if %errorlevel%==0 (
    @echo Java installation detected
)

where groovy >nul 2>nul
if %errorlevel%==1 (
    @echo Groovy not found in path. Please install groovy sdk and configure it in the path
)
if %errorlevel%==0 (
    @echo groovy installation detected
)
