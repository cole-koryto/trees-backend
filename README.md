# trees-backend
Developed using Python 3.11.2 and Postgres 16.4

# Backend Setup
1. Ensure you have postgres installed 
2. Make the trees database on your postgres account (or change default database in config.py)
3. Update config.py with any information specific to the machine (e.g. password)
   1. LOCAL_DB_PORT is important to check since it can vary between machines and is predetermined by postgres
4. Execute `pip install -r requirements.txt`
5. Run `db_creation.py` to import data into database
6. Run `app.py` to start server

# Backup Service Setup
1. Create service file in `/etc/systemd/system/`
   1. e.g. `/etc/systemd/system/db_backup.service`
2. Get path to python executable using `python -c "import os; print(os.environ['_'])`
   1. e.g. `/usr/bin/python3`
3. Get path to server directory
   1. e.g. `/home/ubuntu/trees-backend`
4. Edit service file and enter the information you found

Example:
```
[Unit]
Description="Trees Database Backup"

[Service]
Restart=always
WorkingDirectory=/home/ubuntu/trees-backend
ExecStart=/usr/bin/python3 db_backup_service.py

[Install]
WantedBy=multi-user target
```
5. Now reload systemctl utility using `systemctl daemon-reload`
6. Start service `systemctl start /etc/systemd/system/db_backup.service`
7. Check status using `systemctl status /etc/systemd/system/db_backup.service`

Note: Backup service DOES NOT back up user table information. So this information can be lost.

Based on guide from: https://medium.com/@guemandeuhassler96/run-your-python-script-as-a-linux-daemon-9a82ed427c1a
