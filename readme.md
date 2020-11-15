# Certificate Generator

Certificate generator is a utility that helps you to generate a bulk of certificates with the same format but different data. It is helpful to anyone who wants to generate the same type of certificate with some changes in the content only. 

## Installation

From the root of the project run the following command

```bash
pip install -r requirements.txt
```

## Testing

To test the project run the following commands from the root of the project.

```python
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Then goto 127.0.0.1:8000 to view the project.

## Contributing
See for the issue present and try to solve it.
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Flow of project
<ol>
<li>First upload csv.
<li>Upload template. 
<li>Select point on image and map the coordinate with values such as column name, font size and color.
<li>After the user selects all the points, generate a preview to show.
<li>User verifies the preview and click on the generate all.
<li>All the data is sent to the backend and certificates will be generated.
<li>We will provide an option to either mail the certificate or download the files. 
</ol>



## License
[MIT](https://choosealicense.com/licenses/mit/)
