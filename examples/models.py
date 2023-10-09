import simple_orm.models as models
from simple_orm.models import IntegerField, TextField, ForeignKey, JsonField
from simple_orm.models import simple_orm
from pathlib import Path
import sys

PATH = Path(__file__).absolute().parent.parent
sys.path.append(str(PATH))


@simple_orm
class Box(models.Model):
    name = TextField()
    width = IntegerField()
    height = IntegerField()


@simple_orm
class Circle(models.Model):
    box = ForeignKey(object_class=Box, foreign_field='name')
    name = TextField()
    radius = IntegerField()
    data = JsonField()