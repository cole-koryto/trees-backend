# Backend Troubleshooting Guide

This document outlines solutions to common issues that may arise with the backend of our website. Follow the steps in each section to resolve specific problems.

---

## Table of Contents
1. [Forgotten Admin Password](#1-forgotten-admin-password)
2. [Database Restoration](#2-database-restoration)
3. [Potential Issue #3](#3-potential-issue-3)
4. [Potential Issue #4](#4-potential-issue-4)

---

### 1. Forgotten Admin Password
**Problem**: All admin users have forgotten their passwords or account information.

**Solution Steps**:
1. **Configuration Requirements**
   - Locate the python file titled `admin_reset.py`. This script relies on the `config.py` file to specify default admin credentials. Check the `config.py` file to ensure it contains the proper default credentials.\
   They will look something like this:

     ```python
     # config.py

     # Default admin credentials
     ADMIN_USERNAME = "admin"
     ADMIN_EMAIL = "admin@example.com"
     ADMIN_NAME = "admin"
     ADMIN_PASSWORD = "examplepassword123"
     ```

   - **Note**: You do not need to change the information found here. It is purely intended as a default to reset to and should not contain any sensitive information.

2. **Running the Script**
   - Open a terminal and navigate to the directory containing `admin_reset.py`.
   - Run the script with:

     ```bash
     python admin_reset.py
     ```

   - This will either reset the existing default admin user with the name specified by `ADMIN_USERNAME` or add a new default admin user if no matching record exists.

3. **Expected Outcome**
   - After running the script, an admin user with the default username and password from `config.py` should have access restored.

#### Security Considerations

- **Password Security**: After using the default password to access the admin account, log in and update it immediately to a secure password.

---

### 2. Database Restoration
**Problem**: Database corruption requires resetting from a backup.

**Solution Steps**:

1. **Identify Latest Backup**
   - Locate the most recent verified backup in the `backup_csvs` folder.

2. **Disable Site Access**
   - Log into the AWS account containing the backend service.
   - Temporarily disable access to prevent data modification during restoration by running the following command in the temrinal.

   ```bash
   sudo systemctl stop trees-backend.service
   ```

3. **Replace Active CSVs**
   - Locate the `active_csvs` folder.
   - Remove the tree history and tree info csvs from this folder.
   - Place the most up-to-date history and info files from the `backup_csvs` into the `active_csvs` folder.
       - **Important**: Rename the files now located in the `active_csvs` folder to `tree_history.csv` and `tree_info.csv`.
            - *NOTE*: The restoration program CAN NOT run if the files do not follow the proper naming convention.

4. **Restore Database**
   - Locate and run `db_creation.py`.
      - **NOTE**: Running `db_creation.py` will also reset the admin user to the information stored in `config.py`.

5. **Re-enable Site Access**
   - Once confirmed, allow access to the site.
   - Verify the integrity of the restoration via the website (Ensure the information appears as expected).

---

_Last updated: 2024-11-15_
