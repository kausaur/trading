import django_tables2 as tables
import itertools

def get_valid(**kwargs):
    record = kwargs.get("record", None)
    if record and record['valid']:
        return "success"
    else:
        return "danger"

class Company_DTO(tables.Table):
    row_number = tables.Column(empty_values=())
    name = tables.Column(attrs={
        "td": {
            "class": get_valid
        }
    })
    close = tables.Column()
    min_close = tables.Column()
    max_close = tables.Column()
    min_percent = tables.Column()
    max_percent = tables.Column()
    valid = tables.Column(visible=False, empty_values=())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return next(self.counter)

    class Meta:
        attrs = {'class': 'table table-striped table-hover'}