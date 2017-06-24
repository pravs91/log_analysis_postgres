# Serving log analysis using PostgreSQL
This project analyses the data from a news website's server requests log to get meaningful insights.
It uses Python psycopg2 with PostgreSQL.

## Setup and run
To run the script, do:
```python log_analysis.py```

## Database Tables
- The ```authors``` table includes information about the authors of articles.
- The ```articles``` table includes the articles themselves.
- The ```log``` table includes one entry for each time a user has accessed the site.

## Questions answered
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## VIEWS created to answer these questions

The view ```articleViews``` is created joining the tables ```articles``` and ```log``` to get the title, author and view count for each article. This is helpful to answer questions 1 and 2.

The views ```requests``` and ```errors``` are created as the total number of requests per date on the log and total errors per day (status NOT 200 OK)

```
CREATE VIEW articleViews as select title,author,count(path) as views 
        from articles join log 
        on (substring(path from '[^/]+$') = slug and status = '200 OK') 
        group by title, author, path 
        order by views desc;


CREATE VIEW requests as select time::date, count(time::date) as requests 
        from log group by time::date order by time::date;

CREATE VIEW errors as select time::date, count(time::date) as errors 
        from log where status != '200 OK'  group by time::date order by time::date;
