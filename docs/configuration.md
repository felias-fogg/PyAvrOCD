# Configuration

You do not have to set up any configuration file before you can use PyAvrOCD. However, sometimes it may be convenient to store some options in a file so that you do not have to type them every time you invoke PyAvrOCD. Or, you may want to override options that are set in an IDE. For this purpose, the `@` notation is very helpful. If you place the string `@file.ext` on the command line, then arguments are read from `file.ext` and spliced into the command line. These arguments are read line by line.

Let us assume, `file.ext` contains the following lines:

```bash
--manage
eesave
--prog=3000
--to
atmelice
--veri=e
```

When you now invoke PyAvrOCD with `pyavrocd -d attiny13 -t dwlink @file.ext`, then this is expanded into

```bash
pyavrocd -d attiny13 -t dwlink --manage eesave --prog=3000 --to atmelice --veri=e
```

With the usual abbreviation rules, the fact that the equal sign can simply be substituted by space,  and the rule that later arguments override earlier ones, this is equivalent to

```text
pyavrocd --device attiny13 --manage eesave --prog-clock 3000 --tool atmelice --verify enable
```

Note that implicitly `@pyavrocd.options` is added to the end of the command line. This means that even if you cannot change the command line that invokes PyAvrOCD, because, e.g., PyAvrOCD is invoked by an IDE, you still can specify arguments that have precedence by using the configuration file `pyavrocd.options`.
