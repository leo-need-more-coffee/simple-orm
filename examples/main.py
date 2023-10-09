from models import Box, Circle

Box.objects.add(Box('BOX 1', 1, 1))

Circle.objects.add(Circle(Box.objects.get(width=1, height=1), "CIRCLE 1", 5, {'data':5}))

print(Box.objects.filter(width=1, height=1).json())
print(Circle.objects.get(name="CIRCLE 1").json())
Box.objects.delete(name="BOX 1")
print(Box.objects.all().json())