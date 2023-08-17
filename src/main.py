import numpy as np
import math
import matplotlib.pyplot as plt

def normalize(vec3):
    return vec3/np.linalg.norm(vec3)

def ray_trace(objects, origin, direction):
    s = origin
    v = objects["center"]-s
    d = normalize(direction)
    D = np.dot(v, d)**2-(v**2-objects["radius"]**2)

    color = np.ones((3))
    if np.min(D)>0:
        ta = -np.dot(v, d)+np.sqrt(D)
        tb = -np.dot(v, d)-np.sqrt(D)
        xa = s+ta*d
        xb = s+tb*d
        
        nearest_point = None
        min_distance = np.inf
        if np.sqrt(np.sum((xa-origin)**2))<=min_distance: nearest_point = xa
        if np.sqrt(np.sum((xb-origin)**2))<=min_distance: nearest_point = xb

        N = normalize(nearest_point-objects["center"])
        L = normalize(nearest_point-light["center"])
        V = normalize(nearest_point-origin)
        H = normalize(L+V)

        color -= (light["ambient"]*objects["ambient"])
        color -= (light["diffuse"]*objects["diffuse"]*np.dot(L, N))
        color -= (light["specular"]*objects["specular"]*(np.dot(N, H)**objects["shininess"]))

    return color
    
if __name__=="__main__":
    T = np.array([0, 0, 1])
    E = np.array([0, 0, 0])

    t = T-E
    v = np.array([0, 1, 0])
    b = np.cross(t, v)

    t_norm = normalize(t)
    b_norm = normalize(b)
    v_norm = np.cross(t_norm, b_norm)

    m = 250
    k = 250
    d = 125

    theta = 2*math.atan(k/(2*d))
    ratio = (m-1)/(k-1)

    g_x = d*math.tan(theta/2)
    g_y = g_x*ratio

    q_x = (2*g_x)/(k-1)*b_norm
    q_y = (2*g_y)/(m-1)*v_norm
    p_1m = t_norm*d-g_x*b_norm-g_y*v_norm

    viewport = np.zeros((m, k, 3))

    light = {"center": np.array([-40, -40, -200]), "ambient": np.array([1, 1, 1]), "diffuse": np.array([1, 1, 1]), "specular": np.array([1, 1, 1])}
    objects = {"center": np.array([0, 0, 120]), "radius" : 50, "ambient": np.array([0, 1, 1]), "diffuse": np.array([0, 1, 1]), "specular": np.array([0, 1, 1]), "shininess": 80}

    for i in range(1, m+1):
        for j in range(1, k+1):
            x, y, z = p_1m+q_x*(i-1)+q_y*(j-1)
            viewport[i-1][j-1] = np.clip(ray_trace(objects, np.zeros((3)), np.array([x, y, z])), 0, 1)

    plt.imshow(viewport)
    plt.show()