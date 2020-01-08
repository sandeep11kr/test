Setup-Instructions
====================
1. Install JDK from https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
2. Update your environment variable and set JAVA_HOME to point to the folder where JDK is installed
3. Update your environment PATH variable and add %JAVA_HOME%\bin
4. Download Ngrok tool from https://ngrok.com/download
5. Checkout the code from git into PROJECT_HOME
6. Open command prompt and go to the PROJECT_HOME
7. Run the command <b>run.bat</b>
8. If this command is run for the first time then all the dependency jars will be downloaded and 
    the test server will start. 

Execution - Instructions
=========================
1. Open command prompt and run command <b>ngrok http 6160</b>
2. If you would like to setup the test server to run on some other port then you can modify the property <i>server.port</i> 
in application.properties file under src/main/resources folder
3. Make note of the proxy path displayed in "Forwarding". <i>Example http://31c1b148.ngrok.io</i>
4. Before starting your test, make sure you copy the test scripts of your interest directly under </i>target/classes/conversations</i>
folder. All the dictionary and scripts to be included should also be copied. These files will have extension <i>.txt</i>.
The target folder may not be available when you get a fresh copy of the code from git. This folder structure will appear 
once you run tests
5. Once the test scripts are copied to the target folder as described above, run the test suite using command run.bat or start.sh, depending
on your OS
6. The browser will be launched automatically with <b>http://localhost:6160</b> opened
7. To run a new test, click on "Run New" button
8. In the form enter the proxy path noted in point 3 above. This needs to be done once in a session
9. Number of concurrent calls represent the number of threads you would want to run
10. Call Duration in Minutes represent the total duration for which calls should be run in each thread
11. Number of calls to be made represents the number of calls that each thread should make in a session. 
If both call duration and number of calls are specified then the call duration value will take precedence


<b>Adding new test scripts</b>

To add a new test script 
1. create a text file or copy the file under <i>testscripts</i> folder
2. Rename the file and copy it in the same directory
3. Make necessary modifications
4. All test files should end with the extension <i>.test</i>
5. Restart the test

<b>Specifying keywords in test script</b>

The test script is made of multiple stages. Each stage is to be separated using the delimiter =======

Each stage supports multiple statements. Every statement has to be separated using the delimiter -- OR --

Each statement supports the structure as described in the example below

```
[] 1. Specify the timeout for this statement
[Like, Order, Favorite] 2. List out the hints that you would like to supply the ASR
[What can i get you today] 3. Sample text of the text that you are expecting from CN server
	[Keywords:: {get & you, get & today, like & order &! favorite, what & like & you , can & get & you, good & today}] 4. The list of keywords that you expect in the statement from CN
	[Resp:: I would like to order a pizza] 5. The response that you would like to send back to CN server
```
Please note the brackets of the form <i>[,],{,}</i> above. They are part of the syntax and mandatory

<b>Keyword Syntax</b>

The keywords in the statement support various conjunctions like <i>and, or, and not</i>

Keywords should be listed within the brackets {}. Comma separated terms mean the server statement will match if any one of the keywords matches.
```
Eg. {hello, greeting}, will match either of "Hello World", "Greeting world", "Hello CN" or "Greetings". 
```
The keywords are case insensitive and support partial matches like <i>greeting</i> matches <i>greetings</i>

To specify presence of more than one words in a statement, you can use <i>&</i> operator
```
Eg. {hello & world} will match "Hello World" and not "Hello CN"
```

You can also combine <i>OR and AND</i> using operators <i> | and & </i>
```$xslt
Eg. {(hello | greeting) & world} will match either of "Hello world" and "greetings world"
```

To match statements that should have certain words and not include certain words, you can use the <i>&!</i> operator

```$xslt
Eg. {(hello | greeting) & world &! How} will match "Hello world" but not "Hello world, how are you"
```
<b>Include external scripts</b>

Your scripts can include snippets from external scripts. This is useful when similar statements are repeated across test scripts.
You can create a snippet file with an extension </i>.txt</i> and add your snippets in it. The snippet can have single or multiple 
statements.
```$xslt
Eg. start.txt
[]
[test]
[This is test snippet]
	[Keywords:: {test, snippet}]
	[Resp:: OK]
```
The snippet can be included in any <i>test</i> script through the syntax <i>#include</i>

```$xslt
Eg. 1.test
#include start.txt
```
The inclusion can be done at any point in the script. Make sure the overall syntax is not disturbed due to the inclusion.

<b>Response Macros</b>

You might need to send back the same response across test scripts. To avoid repeating the text across scripts you can make use 
of <i>macros</i>.
<p>Macros are stored in a text file called <i>dictionary.txt</i> which is available in the root of the <i>testscripts</i> folder</p>

The dictionary file stores data in key value form
```$xslt
RESP_ON_NO_MATCH=Could you please repeat that
CONFIRM=yes | OK | Got It | Understood
```
The key represents the name of the macro and can be specified in your test script
```$xslt
Eg. 
[]
[test]
[This is test snippet]
	[Keywords:: {test, snippet}]
	[Resp:: {CONFIRM}]
```
In the above case, any one of the responses <i>yes, Ok, Got It or Understood</i> will be sent back.
