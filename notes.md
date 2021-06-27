### Querysets

```python
# returns all the data sets from the sales database
qs = Sale.objects.all()

# return data for the given primary key
qs = Sale.objects.get(id=1)

# filter data with the column
# __date operator is appended to created as its a DateTimeField to match the value
qs = Sale.objects.filter(created__date=date_from)

# return dataset in a list of dictionary
qs.values()

# return dataset in a list of tuples
qs.values_list()
```

### Related names / Reverse relationship

### Class Bases Vs Function Based Views
