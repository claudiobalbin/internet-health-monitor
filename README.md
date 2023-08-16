# internet-speedtest-rpi
Simple docker stack for raspberrypi logging internet speed with dashboards.

# Stack

1. Logger
    - Internet speed testing using cli;
    - Simple NixOS based on Debian that will trigger the speedtest-cli tool to log the output as json for further use.
    - Should be able to store test results in a shared volume or database;
2. Database
    - Efficient store of logged data;
    - Could be a simple database like SQLite or a more complex one;
3. UI
    - Simple UI to query and output logged data in a simple dashboard;
    - Python (Flask / Django) or dotnet;
