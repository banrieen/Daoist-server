import numpy as np
import plotly.graph_objects as go

def cylinder(r:float, h:float, a:float=0, nt:int=100, nv:int=50)->tuple:
    """
    parametrize the cylinder of radius r, height h, base point a
    """
    theta = np.linspace(0, 2*np.pi, nt)
    v = np.linspace(a, a+h, nv )
    theta, v = np.meshgrid(theta, v)
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    z = v
    return x, y, z

def boundary_circle(r:float, h:float, nt:int=100)->tuple:
    """
    r - boundary circle radius
    h - height above xOy-plane where the circle is included
    returns the circle parameterization
    """
    theta = np.linspace(0, 2*np.pi, nt)
    x= r*np.cos(theta)
    y = r*np.sin(theta)
    z = h*np.ones(theta.shape)
    return x, y, z
r1 = 2
a1 = 0
h1 = 5

r2 = 1.35
a2 = 1
h2 = 3

x1, y1, z1 = cylinder(r1, h1, a=a1)
x2, y2, z2 = cylinder(r2, h2, a=a2)

colorscale = [[0, 'blue'],
        [1, 'blue']]

cyl1 = go.Surface(x=x1, y=y1, z=z1,
            colorscale = colorscale,
            showscale=False,
            opacity=0.5)
xb_low, yb_low, zb_low = boundary_circle(r1, h=a1)
xb_up, yb_up, zb_up = boundary_circle(r1, h=a1+h1)

bcircles1 =go.Scatter3d(x = xb_low.tolist()+[None]+xb_up.tolist(),
                        y = yb_low.tolist()+[None]+yb_up.tolist(),
                        z = zb_low.tolist()+[None]+zb_up.tolist(),
                        mode ='lines',
                        line = dict(color='blue', width=2),
                        opacity =0.55, showlegend=False)

cyl2 = go.Surface(x=x2, y=y2, z=z2,
    colorscale = colorscale,
    showscale=False,
    opacity=0.7)

xb_low, yb_low, zb_low = boundary_circle(r2, h=a2)
xb_up, yb_up, zb_up = boundary_circle(r2, h=a2+h2)

bcircles2 =go.Scatter3d(x = xb_low.tolist()+[None]+xb_up.tolist(),
            y = yb_low.tolist()+[None]+yb_up.tolist(),
            z = zb_low.tolist()+[None]+zb_up.tolist(),
            mode ='lines',
            line = dict(color='blue', width=2),
            opacity =0.75, showlegend=False)

layout = go.Layout(scene_xaxis_visible=False, scene_yaxis_visible=False, scene_zaxis_visible=False)
fig =  go.Figure(data=[cyl2, bcircles2, cyl1, bcircles1], layout=layout)

fig.update_layout(scene_camera_eye_z= 0.55)
fig.layout.scene.camera.projection.type = "orthographic" #commenting this line you get a fig with perspective proj

fig.show()