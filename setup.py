from setuptools import setup


setup(
    name="MAC Uploader",
    version="1.0",
    install_requires=[
        'flask',
        'flask-bootstrap',
        'flask-uploads',
        'flask-wtf',
        'werkzeug',
        'requests',
        'urllib3',
        'boto3'
    ]
)
