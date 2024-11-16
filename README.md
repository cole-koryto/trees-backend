# trees-backend
Developed using Python 3.11.2 and Postgres 16.4

# Backend Setup
1. Clone trees-backend repo
2. Ensure you have postgres installed 
3. Make the trees database on your postgres account (or change default database in config.py)
4. Update config.py with any information specific to the machine (e.g. postgres password, postgres user, etc)
   1. LOCAL_DB_PORT is important to check since it can vary between machines and is predetermined by postgres
5. Execute `pip install -r requirements.txt`
6. Run `db_creation.py` to import data into database from `active_csvs` folder
7. Run `app.py` to start server

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

Based on guide from: https://medium.com/@guemandeuhassler96/run-your-python-script-as-a-linux-daemon-

# Resetting Database from CSV
1. Move the most recent .csv backup from `backup_csvs` to `active_csvs` 
2. Replace existing tree_history.csv and/or tree_info.csv in the active_csvs folder with the csvs from `backup_csvs`
   1. Program cannot run without those EXACT files existing in that EXACT location
3. **Optional** If you want to restore the users table, Move the most recent .csv backup from `backup_csvs` to `active_csvs`
   1. Note: You can restore treeinfo and treehistroy without restoring users
4. Run db_creation.py
   1. **PLEASE NOTE:** Running db_creation.py will also reset the admin user to the information stored in config.py

# Server Setup
The server setup was based on the "Setting up FastAPI Server Medium Guide.pdf" article which provides a very comprehensive guide on how to set up FastAPI application on nginx server. I would highly recommend you read it for further details
1. Create server and set up a static IP that referees to it
2. Follow steps in **Backend Setup** and **Backup Service Setup**
3. Create a systemd file based on trees-backend.service
   1. e.g. `sudo nano /etc/systemd/system/trees-backend.service`
4. Restart the systemctl daemon : sudo systemctl daemon-reload 
5. Restart the web-hosting service: sudo systemctl start trees-backend.service 
6. See the status of your service : sudo systemctl status trees-backend.service
7. Run sudo apt install nginx
8. Run sudo nano /etc/nginx/sites-available/trees-backend
   1. Create file based on nginx-trees file in references    
9. sudo ln -s /etc/nginx/sites-available/trees-backend /etc/nginx/sitesenabled/
   1. A symbolic link is created in the /etc/nginx/sitesenabled/ directory. This allows the files to be the same without having to modify both whenever you make a change
10. Run sudo nginx -t
11. Run sudo systemctl reload nginx
 
