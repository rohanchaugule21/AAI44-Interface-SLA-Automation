# AAI-44 Interface SLA Automation — OneDrive Integration

## 1. Purpose

OneDrive for Business is used as the file transfer and synchronization layer between the Power Automate cloud flow and the local Windows environment.

Power Automate saves the incoming AAI-44 CSV into a OneDrive folder.

The OneDrive client then synchronizes the file to the local Windows machine, where Windows Task Scheduler and Python can access it.

---

## 2. Integration Flow

The integration follows this path:

```text
Power Automate
      |
      | Create file
      v
OneDrive for Business
      |
      | OneDrive synchronization
      v
Local Windows Folder
      |
      v
Windows Task Scheduler
      |
      v
Python Automation