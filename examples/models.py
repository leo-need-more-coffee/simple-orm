import simple_orm.models as models
from simple_orm.models import IntegerField, TextField
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
    name = TextField()
    radius = IntegerField()
