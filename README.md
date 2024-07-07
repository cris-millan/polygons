# polygons
fast-api, clean architecture, postgresql

1. run ``` docker-compose build  ```
2. run ``` docker-compose up ```
3. Go to the following route
3. you can use the following url to check doc ``` http://127.0.0.1:8000/docs```
![img.png](img.png)
4. i added a file example.xlsx that can be used to call api/v1/polygons/uploadfile

Notes: 
The process could be heavy for an endpoint, so it would be beneficial to add a job to process the file in the background.
Currently, there are limitations regarding file size, so I suggest avoiding uploading very large files

Missing: implement library de Jupyter