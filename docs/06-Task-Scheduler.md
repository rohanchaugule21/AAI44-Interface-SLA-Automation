# AAI-44 Interface SLA Automation — Windows Task Scheduler

## 1. Purpose

Windows Task Scheduler is used to automatically execute the Python automation on the local Windows machine.

The scheduler removes the need to manually start the Python script after the AAI-44 report has been received and synchronized to the local machine.

---

## 2. Task

The configured Windows Task Scheduler task is:

```text
AAI44 Interface SLA Automation
```

## 3. Execution Flow
The local execution flow is:
```
OneDrive
   |
   | CSV synchronized
   v
AAI44Input
   |
   v
Windows Task Scheduler
   |
   v
Python
   |
   v
Automation.py
   |
   +----> AAI44Output
   |
   +----> AAI44Processed
```

## 4. Task Action
The Task Scheduler Action is configured to launch Python.
Program / Script
The Python executable used by the current environment is:
```
C:\Users\<USERNAME>\AppData\Local\Microsoft\WindowsApps\python.exe
```

The actual path may differ between Windows environments.
Add Arguments
```
"C:\Users\<USERNAME>\OneDrive - SITA\AI Initiatives 2026\Agentic PlayBook\Automation.py"
```

Start In
```
C:\Users\<USERNAME>\OneDrive - SITA\AI Initiatives 2026\Agentic PlayBook
```

The Start In value points to the directory containing Automation.py.

## 5. Trigger Configuration
The current task is configured with a daily schedule.
The task starts during the expected AAI-44 report processing window.
The current configuration uses:
```
Start time: 12:45 PM
Frequency: Daily
Repeat interval: Every 5 minutes
Duration: 15 minutes
```

This provides multiple opportunities for the local automation to execute during the processing window.
The Python script itself determines whether a CSV is available and selects the latest CSV.


## 6. Why the Task Repeats
The report is expected to arrive around the daily reporting window.
There can be a short delay between:
```
Email received
      |
      v
Power Automate processing
      |
      v
OneDrive cloud file creation
      |
      v
OneDrive local synchronization
```

The repeated Task Scheduler execution provides additional opportunities for the CSV to become available before the processing window ends.

## 7. Python File Selection
Task Scheduler does not specify which CSV should be processed.
Instead, Python determines the input file.
The Python script searches:
```
AAI44Input
```
and selects the most recently modified CSV.
Therefore:
```
Task Scheduler
     |
     +-- Starts Python
              |
              +-- Finds latest CSV
              |
              +-- Processes CSV
```
This keeps scheduling logic separate from file-selection logic.


## 8. Task Settings
The current task is configured to:
- Allow the task to be run on demand.
- Prevent a new instance from starting if the task is already running.
- Stop the task if it runs for an unusually long duration.
- Force stop the task if required.
The task is configured to run under the user's Windows account.


## 9. Conditions
The task should not depend on the laptop being connected to AC power.
The following power restrictions should therefore be disabled for the intended unattended execution:
```
Start the task only if the computer is on AC power
Stop if the computer switches to battery power
```
Network availability is not configured as a separate Task Scheduler condition because OneDrive synchronization is responsible for making the file available locally.


## 10. Laptop Availability
The current implementation uses local Windows execution.
Therefore, the Windows machine is an operational dependency.
The machine needs to be available for:
- OneDrive synchronization.
- Task Scheduler execution.
- Python execution.
If the machine is completely powered off, Windows Task Scheduler cannot execute the Python script.


## 11. Sleep / Wake Considerations
Windows Task Scheduler can be configured to wake the computer for a scheduled task.
If this capability is required, the task can use:
```
Conditions
    |
    └── Wake the computer to run this task
```
The task can also be configured to run as soon as possible after a scheduled start is missed.
These settings should be validated against the organization's laptop and power-management policies before being relied upon for production operation.


## 12. Important Operational Limitation
There are three different machine states:
Machine is powered on
```
Power Automate
      |
      v
OneDrive Sync
      |
      v
Task Scheduler
      |
      v
Python
```

The automation can execute normally.

Machine is sleeping:
Depending on the Task Scheduler and Windows power configuration, the task may be able to wake the machine and execute.
This should be validated on the target machine.

Machine is completely powered off:
The local Task Scheduler cannot execute while Windows is powered off.
Therefore, the current architecture is not fully independent of the local machine.


## 13. Manual Execution
The Task Scheduler task can also be started manually.
In Task Scheduler:
```
Task Scheduler
   |
   v
AAI44 Interface SLA Automation
   |
   v
Run
```
This is useful for:
- Testing.
- Troubleshooting.
- Reprocessing a file.
- Validating changes.


## 14. Task Result
Windows Task Scheduler provides a task execution result.
A successful execution returns:
```
0x0
```
The task history can be used to investigate scheduling or execution problems.
For example:
```
Last Run Time
Last Run Result
Next Run Time
```
can be checked from the Task Scheduler interface.

## 15. Troubleshooting
Python did not run
Check:
1. Task Scheduler task is enabled.
2. The trigger is configured correctly.
3. The task is allowed to run on demand.
4. The Python executable path is valid.
5. The Automation.py path is valid.
6. The Windows machine was available at the scheduled time.
Python ran but no output was created
Check:
```
AAI44Input
```
for a CSV file.
If there is no CSV, check:
1. Power Automate run history.
2. OneDrive cloud folder.
3. OneDrive synchronization status.
CSV exists but was not processed
Check:
```
AAI44Input
```
and manually run the Task Scheduler task.
Then check the Python console output.

Excel was created but CSV remains in Input
This indicates that the Python transformation may have succeeded but the CSV move operation failed.
Check:
```
AAI44Output
```
for the generated Excel file.
Then investigate whether the CSV is locked or otherwise unavailable for moving.


## 16. Task Scheduler Dependency
The Task Scheduler component depends on:
- Windows operating system.
- Python installation.
- Correct Python executable path.
- Correct Automation.py path.
- OneDrive synchronization.
- Local filesystem access.

  
## 17. Architecture Position
Task Scheduler is the execution bridge between the synchronized cloud file and the Python transformation.
```
                CLOUD
                  |
                  v
             OneDrive
                  |
             File Sync
                  |
                  v
                LOCAL
                  |
                  v
          Windows Task Scheduler
                  |
                  v
             Python Script
                  |
                  v
          Structured Excel
```

## 18. Current Design Rationale
Windows Task Scheduler was selected because the current Python transformation already runs successfully on the local Windows environment.
This approach:
- Reuses the existing Python implementation.
- Avoids introducing Azure Functions.
- Avoids requiring a separate cloud-hosted Python service.
- Requires minimal additional infrastructure.
- Provides scheduled unattended execution while the machine is available.


## 19. Future Improvement
If the automation needs to operate independently of a user's laptop, the Python execution could be moved to a managed cloud environment.
Potential future architecture:
```
Power Automate
      |
      v
Cloud Storage
      |
      v
Cloud Python Runtime
      |
      v
Output
```
This is not part of the current implementation.
The current solution remains:
```
Power Automate
      |
      v
OneDrive
      |
      v
Windows Task Scheduler
      |
      v
Python
```


## 20. Summary
Windows Task Scheduler provides the automated local execution layer for the AAI-44 automation.
It launches the tested Python script at the configured processing interval, while Python remains responsible for identifying and processing the latest available CSV.
