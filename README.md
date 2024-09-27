# TaskChecker application
Damir Nurtdinov
## Task description:
Implement an extensible application.

Code requirements: minimum 3 classes, use lambda functions and decorators at least once.

Extending the application functionality should not require the user to interfere with the code (aka plugin system).

## App description
Application supposed to check Python code on test-data with corresponding output. I did it for my online programming school.
Application allows to add extra-verifications to check student's code for malliscious elements.

# Execution
## How to run
Run file ```task_checker.py``` with your Python interpreter. 
## Extending app with plugins
Add your plugins in folder ```/plugins``` with ```.py``` extension. Your plugin should inherit form ```PluginInterface``` and override method ```run```. 
