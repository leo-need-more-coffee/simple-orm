from models import Box, Circle

Box.objects.add(Box("BOX 1", 1, 1))
Box.objects.add(Box("BOX 2", 1, 1))
Box.objects.add(Box("BOX 3", 2, 2))
Circle.objects.add(Circle("CIRCLE 1", 5))

print(Box.objects.filter(width=1, height=1).json())
print(Box.objects.get(name="BOX 1").json())
Box.objects.delete(name="BOX 2")
print(Box.objects.all().json())