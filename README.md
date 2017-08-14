# Incompatibility between `django-audit-log` and `django-modeltranslation`

_I found [a solution](#the-solution) to this problem. This original problem description is kept here, allowing others with the same issue to find the description and the solution._

This is a small Django project that utilises both `django-audit-log` and `django-modeltranslation`. It contains the Django app `app` with the model `MyModel`. Also included is a simple test for the model.

The project is set up with a SQLite database running in memory.

When running the tests via `./manage.py test`, the following unexpected exception is raised:

```
TypeError: 'text_es' is an invalid keyword argument for this function
```

The complete output is here:

```
$ ./manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
E
======================================================================
ERROR: test_my_model (app.tests.MyModelTestCase)
Test the model.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/path/to/django-auditlog-modeltranslation-testcase/app/tests.py", line 12, in setUp
    text='Text of Instance 1'
  File "/path/to/django-auditlog-modeltranslation-testcase/.env/lib/python3.5/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/path/to/django-auditlog-modeltranslation-testcase/.env/lib/python3.5/site-packages/modeltranslation/manager.py", line 381, in create
    return super(MultilingualQuerySet, self).create(**kwargs)
  File "/path/to/django-auditlog-modeltranslation-testcase/.env/lib/python3.5/site-packages/django/db/models/query.py", line 394, in create
    obj.save(force_insert=True, using=self.db)
  File "/path/to/django-auditlog-modeltranslation-testcase/.env/lib/python3.5/site-packages/django/db/models/base.py", line 807, in save
    force_update=force_update, update_fields=update_fields)
  File "/path/to/django-auditlog-modeltranslation-testcase/.env/lib/python3.5/site-packages/django/db/models/base.py", line 847, in save_base
    update_fields=update_fields, raw=raw, using=using,
  File "/path/to/django-auditlog-modeltranslation-testcase/.env/lib/python3.5/site-packages/django/dispatch/dispatcher.py", line 193, in send
    for receiver in self._live_receivers(sender)
  File "/path/to/django-auditlog-modeltranslation-testcase/.env/lib/python3.5/site-packages/django/dispatch/dispatcher.py", line 193, in <listcomp>
    for receiver in self._live_receivers(sender)
  File "/path/to/django-auditlog-modeltranslation-testcase/.env/lib/python3.5/site-packages/audit_log/models/managers.py", line 107, in post_save
    self.create_log_entry(instance, created and 'I' or 'U')
  File "/path/to/django-auditlog-modeltranslation-testcase/.env/lib/python3.5/site-packages/audit_log/models/managers.py", line 102, in create_log_entry
    manager.create(action_type = action_type, **attrs)
  File "/path/to/django-auditlog-modeltranslation-testcase/.env/lib/python3.5/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/path/to/django-auditlog-modeltranslation-testcase/.env/lib/python3.5/site-packages/django/db/models/query.py", line 392, in create
    obj = self.model(**kwargs)
  File "/path/to/django-auditlog-modeltranslation-testcase/.env/lib/python3.5/site-packages/django/db/models/base.py", line 572, in __init__
    raise TypeError("'%s' is an invalid keyword argument for this function" % list(kwargs)[0])
TypeError: 'text_es' is an invalid keyword argument for this function

----------------------------------------------------------------------
Ran 1 test in 0.003s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

If the audit log for the model is disabled (e.g. by removing or commenting out [this line](https://github.com/decibyte/django-auditlog-modeltranslation-testcase/blob/master/app/models.py#L11)), tests pass as expected.

Similarly, if translation of the model is disabled  (e.g. by removing or commenting out [this line](https://github.com/decibyte/django-auditlog-modeltranslation-testcase/blob/master/app/translation.py#L6)), tests also pass as expected.

But when both features are enabled, the above problem occurs.

This issue has been reported for [`django-audit-log`](https://github.com/Atomidata/django-audit-log/issues/48) and [`django-modeltranslation`](https://github.com/deschler/django-modeltranslation/issues/420).


## <a name="the-solution"></a>The Solution

After a while, and after going through the sources of both packages (yay, open source!) it suddenly struck me what the problem was and how to solve it: You simply need to register the auto generated audit log models for translation as well as the regular models, [as seen in this branch comparison](https://github.com/decibyte/django-auditlog-modeltranslation-testcase/compare/fix?expand=1#diff-f5e2c57158f98362114fabca111c67dfR7).