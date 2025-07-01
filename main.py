from ursina import *

app = Ursina()

window.title = 'Sonic 3D Clone'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# Cenário (plano de chão)
ground = Entity(model='plane', texture='white_cube', collider='box', scale=(100,1,100), texture_scale=(100,100), color=color.green)

# Rampas
ramp = Entity(model='cube', color=color.orange, collider='box', position=(5,0.5,10), scale=(10,1,5), rotation=(30,0,0))
ramp2 = duplicate(ramp, position=(-5,0.5,20), rotation=(45,0,0), color=color.red)

# Jogador (Sonic fake)
player = Entity(model='cube', color=color.azure, scale=(1, 2, 1), position=(0,2,0), collider='box')

# Câmera em terceira pessoa
camera.parent = player
camera.position = (0, 3, -12)
camera.rotation = (10, 0, 0)
camera.fov = 90

# Variáveis de movimento
speed = 10
jump_force = 0.4
gravity = 0.015
velocity_y = 0
is_jumping = False

def update():
    global velocity_y, is_jumping

    # Movimento lateral
    if held_keys['a']:
        player.x -= speed * time.dt
    if held_keys['d']:
        player.x += speed * time.dt

    # Movimento para frente e trás
    if held_keys['w']:
        player.z += speed * time.dt
    if held_keys['s']:
        player.z -= speed * time.dt

    # Pulo
    if held_keys['space'] and not is_jumping:
        velocity_y = jump_force
        is_jumping = True

    # Gravidade
    velocity_y -= gravity
    player.y += velocity_y

    # Colisão com o chão
    if player.y <= 2:
        player.y = 2
        velocity_y = 0
        is_jumping = False

    # Boost de velocidade (simples)
    if held_keys['left shift']:
        player.z += speed * 2 * time.dt

app.run()
