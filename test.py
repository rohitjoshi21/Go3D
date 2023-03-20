from ursina import *
from ursina.shaders import lit_with_shadows_shader # you have to apply this shader to enties for them to receive shadows.

app = Ursina()

EditorCamera()
Entity(model='plane', scale=10, color=color.gray, shader=lit_with_shadows_shader)
Entity(model='cube', y=1, shader=lit_with_shadows_shader)
pivot = Entity()
SpotLight(parent=pivot, x=2,y=2, z=3, shadows=True)
app.run()