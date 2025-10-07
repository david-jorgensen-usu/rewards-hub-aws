# rewards-hub-aws
Rewards Hub Django Backend through AWS EC2

# Note on Static Files
For Nginx, when you update any static file, you need to run the command:

```python3 manage.py collectstatic```

This recollects all static files that Gunicorn serves.
