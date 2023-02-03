## Python script to migrate files from MongoDB Gridfs to filesystem

## Steps to run the script

Scripts requires python version 3 or above to run.

1. Install the pip dependencies and devDependencies and start the server.

    ```sh
    pip install -r requirements.txt
    ```

2. Replace connection_string and folder_location, database_name in script line number 34, 36 and 38

3. Run python script 
   3.1 To migrate all files from <database_name>
    ```sh
    python3 migrate_gridfs.py migrate_files
    ```
    3.2 To migrate files with limit of 10 from <database_name>
    ```sh
    python3 migrate_gridfs.py migrate_files 10
    ```
    3.3 To insert data to gridfs
    ```sh
    python3 migrate_gridfs.py insert_grid_fs
    ```
    This will create gridfs collection in MongoDB in database name mentioned in line number 36

4. Migration log activity saved in migration.log file in the same folder


5. If Migration fails for some file, log contains the file_id and file_name for the files which are not migrated as described below
```diff
+ INFO 2023-02-02 17:16:17,823-File with _id  : 63d37b9075165ba5cb33aada and name 90060cfe-622a-4869-8272-512101bb93ce.txt migrated to path
+ INFO 2023-02-02 17:16:18,202-File with _id  : 63d37b8f75165ba5cb33aad8 and name 78814913-5823-4781-9420-fbbb3bd8b8e3.txt migrated to path
+ INFO 2023-02-02 17:16:18,581-File with _id  : 63d37b8e75165ba5cb33aad6 and name 66422d37-52b1-419f-ae9e-79ebb94403ad.txt migrated to path

- ERROR 2023-02-03 11:35:05,872-63dca4035f3a94b4361aa1bb :: 9428b088-2986-4525-b268-373c56201891.txt :: name 'destinations' is not defined
- ERROR 2023-02-03 11:35:05,872-63dca40326f8ddb807394e81 :: 0358f16b-f8fb-4ba3-aa0a-830cdfeb9996.txt :: name 'destinations' is not defined
- ERROR 2023-02-03 11:35:05,872-63dca40317de685692b31eba :: 60865ed9-60d8-443f-b0d4-82145d84cf73.txt :: name 'destinations' is not defined
``` 

#### Improvements
- [ ] Adding mongodb connection string, folder name, database name dynamically to system arguments 
- [ ] Use bulk write
- [ ] Add more logging
 


