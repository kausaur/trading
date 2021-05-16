import django_tables2 as tables

class Company_DTO(tables.Table):
    name = tables.Column()
    close = tables.Column()
    min_close = tables.Column()
    max_close = tables.Column()
    min_percent = tables.Column()
    max_percent = tables.Column()
    valid = tables.Column()