
<div align="center" id="main">
	<h1 align="center">Signale.py</h1>
	<p align="center">Elegant Console Logger For Python Command-Line Apps</p>
	<br>
	<br>
	<img src="./imgs/main.png" alt="example" align="center">
</div>

<hr>



## Installation
**Signale.py** can be installed using pip.

````bash

    [sudo] pip install signalepy

````



## Usage
Package consists of a class `Signale`, it is the main constructor class. The object created has all the logger functions in it.


### Using Loggers
Each logger function takes in three arguments:-
- `text`
- `prefix` ( Optional )
- `suffix` ( Optional )

They all are available in the logger object. To create one do this:-
````python

    from signalepy import Signale

    logger = Signale()

````

Now you can use the default loggers using this object like:-
````python

    ...

	logger.success("Started Successfully", prefix="Debugger")
	logger.warning("`a` function is deprecated", suffix="main.py")
	logger.complete("Run Complete")

    ...

````


This will produce the following result:-

<div align="center">
	<img align="center" src="./imgs/result.png">
</div>

<br><br>

<details>
	<summary>View All Available Loggers</summary>

- `simple`
- `success`
- `error`
- `warning`
- `start`
- `stop`
- `watch`
- `important`
- `pending`
- `complete`
- `debug`
- `pause`
- `info`
- `like`
- `center`

</details>



----------------------------------------------------------------------------------------------------------



## Scoped Loggers
To create scoped loggers, define the `scope` field in the `options` argument of constructor like:-

````python

	from signalepy import Signale

    logger = Signale({
    	"scope": "global scope"
    })
    logger.success("Scoped Logger Works!")

````

This will produce the following result:-

<div align="center">
	<img src="./imgs/scope_str.png" align="center">
</div>

<br><br>

You also create multiple scopes by setting the `scope` field to a list of strings like:-

````python

	from signalepy import Signale

    logger = Signale({
    	"scope": ["global scope", "inner scope"]
    })
    logger.success("Scoped Logger Works!")

````

This will produce the following result:-

<div align="center">
	<img src="./imgs/scope_list.png" align="center">
</div>


----------------------------------------------------------------------------------------------------------



## API

1. logger = `Signale(<options>)`

	<br>

	`Signale`

	- Type: `class`

	Signale class imported from `signalepy` module

	<br>

	`options`

	- Type: `dict`

	Options Dictionary for logger.

	<br><br>

2. logger.`<logger>(message="", prefix="", suffix="")`

	<br>

	`logger`

	- Type: `function`

	Can be any default logger

	<br>

	`message`

	- Type: `str`

	Message to be displayed

	<br>

	`prefix`

	- Type: `str`
	- Required: False

	Prefix text

	<br>

	`suffix`

	- Type: `str`
	- Required: False

	Suffix text



----------------------------------------------------------------------------------------------------------



**Licensed Under [MIT License](https://github.com/ShardulNalegave/signale.py/blob/master/LICENSE)**
**A Project By [Shardul Nalegave](https://shardul.netlify.com)**