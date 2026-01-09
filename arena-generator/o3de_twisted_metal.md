# O3DE Twisted Metal Arena - MVP Setup Guide

## Overview
This creates a randomized combat arena with drivable vehicles, AI opponents, and collectible power-ups in Open 3D Engine.

## Prerequisites
- O3DE installed (download from https://o3de.org/)
- Basic familiarity with O3DE Editor
- Python 3 (comes with O3DE)

## Project Setup

### 1. Create New Project
1. Open O3DE Project Manager
2. Create new project: `TwistedMetalArena`
3. Open project in O3DE Editor

### 2. File Structure
Create these folders in your project:

```
TwistedMetalArena/
├── Scripts/
│   ├── arena_generator.py
│   ├── vehicle_controller.py
│   ├── ai_vehicle.py
│   └── powerup_spawner.py
├── Levels/
│   └── arena_level.prefab
└── Assets/
    ├── Materials/
    │   ├── arena_floor.material
    │   ├── arena_wall.material
    │   ├── vehicle.material
    │   └── powerup.material
    └── Textures/
        ├── floor_grid.png
        ├── wall_concrete.png
        └── powerup_glow.png
```

## Script Files

### arena_generator.py
Place in: `TwistedMetalArena/Scripts/arena_generator.py`

```python
import azlmbr.bus as bus
import azlmbr.editor as editor
import azlmbr.entity as entity
import azlmbr.math as math
import azlmbr.components as components
import random

class ArenaGenerator:
    def __init__(self):
        self.arena_size = 100.0
        self.wall_height = 10.0
        self.wall_thickness = 2.0
        self.obstacle_count = 15
        
    def generate_arena(self):
        """Generate complete arena with floor, walls, and obstacles"""
        print("Generating Twisted Metal Arena...")
        
        # Create floor
        self.create_floor()
        
        # Create perimeter walls
        self.create_walls()
        
        # Create random obstacles
        self.create_obstacles()
        
        print("Arena generation complete!")
        
    def create_floor(self):
        """Create arena floor"""
        floor_entity = editor.ToolsApplicationRequestBus(bus.Broadcast, 'CreateNewEntity', entity.EntityId())
        editor.EditorEntityAPIBus(bus.Event, 'SetName', floor_entity, "Arena_Floor")
        
        # Add mesh component
        mesh_component = editor.EditorComponentAPIBus(bus.Broadcast, 'AddComponentsOfType', 
                                                       floor_entity, ['Mesh'])
        
        # Set as flat plane (you'll assign mesh asset in editor)
        transform = math.Transform_CreateIdentity()
        transform.scale = math.Vector3(self.arena_size, self.arena_size, 1.0)
        components.TransformBus(bus.Event, 'SetWorldTM', floor_entity, transform)
        
        # Add physics collider
        collider = editor.EditorComponentAPIBus(bus.Broadcast, 'AddComponentsOfType',
                                                floor_entity, ['PhysX Static Rigid Body', 'PhysX Collider'])
        
        return floor_entity
        
    def create_walls(self):
        """Create perimeter walls"""
        half_size = self.arena_size / 2.0
        
        # North wall
        self.create_wall(math.Vector3(0, half_size, self.wall_height/2), 
                        math.Vector3(self.arena_size, self.wall_thickness, self.wall_height))
        
        # South wall
        self.create_wall(math.Vector3(0, -half_size, self.wall_height/2), 
                        math.Vector3(self.arena_size, self.wall_thickness, self.wall_height))
        
        # East wall
        self.create_wall(math.Vector3(half_size, 0, self.wall_height/2), 
                        math.Vector3(self.wall_thickness, self.arena_size, self.wall_height))
        
        # West wall
        self.create_wall(math.Vector3(-half_size, 0, self.wall_height/2), 
                        math.Vector3(self.wall_thickness, self.arena_size, self.wall_height))
        
    def create_wall(self, position, scale):
        """Create individual wall segment"""
        wall_entity = editor.ToolsApplicationRequestBus(bus.Broadcast, 'CreateNewEntity', entity.EntityId())
        editor.EditorEntityAPIBus(bus.Event, 'SetName', wall_entity, "Arena_Wall")
        
        # Add mesh component (box)
        mesh_component = editor.EditorComponentAPIBus(bus.Broadcast, 'AddComponentsOfType',
                                                       wall_entity, ['Mesh'])
        
        # Set transform
        transform = math.Transform_CreateTranslation(position)
        transform.scale = scale
        components.TransformBus(bus.Event, 'SetWorldTM', wall_entity, transform)
        
        # Add physics
        editor.EditorComponentAPIBus(bus.Broadcast, 'AddComponentsOfType',
                                     wall_entity, ['PhysX Static Rigid Body', 'PhysX Collider'])
        
        return wall_entity
        
    def create_obstacles(self):
        """Create random obstacles throughout arena"""
        half_size = self.arena_size / 2.0 - 10.0  # Keep away from edges
        
        for i in range(self.obstacle_count):
            x = random.uniform(-half_size, half_size)
            y = random.uniform(-half_size, half_size)
            
            width = random.uniform(3.0, 8.0)
            height = random.uniform(2.0, 6.0)
            depth = random.uniform(3.0, 8.0)
            
            self.create_obstacle(math.Vector3(x, y, height/2), 
                               math.Vector3(width, depth, height))
            
    def create_obstacle(self, position, scale):
        """Create individual obstacle"""
        obstacle = editor.ToolsApplicationRequestBus(bus.Broadcast, 'CreateNewEntity', entity.EntityId())
        editor.EditorEntityAPIBus(bus.Event, 'SetName', obstacle, "Obstacle")
        
        # Add mesh
        editor.EditorComponentAPIBus(bus.Broadcast, 'AddComponentsOfType',
                                     obstacle, ['Mesh'])
        
        # Set transform
        transform = math.Transform_CreateTranslation(position)
        transform.scale = scale
        components.TransformBus(bus.Event, 'SetWorldTM', obstacle, transform)
        
        # Add physics
        editor.EditorComponentAPIBus(bus.Broadcast, 'AddComponentsOfType',
                                     obstacle, ['PhysX Static Rigid Body', 'PhysX Collider'])
        
        return obstacle

# Execute when script runs
if __name__ == "__main__":
    generator = ArenaGenerator()
    generator.generate_arena()
```

### vehicle_controller.py
Place in: `TwistedMetalArena/Scripts/vehicle_controller.py`

```python
import azlmbr.bus as bus
import azlmbr.entity as entity
import azlmbr.math as math
import azlmbr.legacy.general as general

class VehicleController:
    def __init__(self):
        self.entity_id = None
        self.speed = 20.0
        self.turn_speed = 2.0
        self.boost_multiplier = 2.0
        self.is_boosting = False
        
    def OnActivate(self, entity_id):
        """Called when entity activates"""
        self.entity_id = entity_id
        
        # Listen for input
        self.input_handler = bus.NotificationHandler('InputEventNotificationBus')
        self.input_handler.connect(self.entity_id)
        
        # Tick handler for movement
        self.tick_handler = bus.NotificationHandler('TickBus')
        self.tick_handler.connect()
        self.tick_handler.add_callback('OnTick', self.on_tick)
        
    def OnDeactivate(self):
        """Cleanup"""
        if self.input_handler:
            self.input_handler.disconnect()
        if self.tick_handler:
            self.tick_handler.disconnect()
            
    def on_tick(self, delta_time, time_point):
        """Update every frame"""
        if not self.entity_id or not self.entity_id.IsValid():
            return
            
        # Get current transform
        transform = bus.TransformBus(bus.Event, 'GetWorldTM', self.entity_id)
        
        # Get input
        forward = general.get_axis_value("vertical")  # W/S or Up/Down
        turn = general.get_axis_value("horizontal")  # A/D or Left/Right
        
        # Apply boost
        current_speed = self.speed
        if self.is_boosting:
            current_speed *= self.boost_multiplier
            
        # Move forward/backward
        if forward != 0:
            forward_dir = transform.GetColumn(1)  # Y-axis is forward in O3DE
            movement = forward_dir * (forward * current_speed * delta_time)
            
            position = transform.position + movement
            transform.position = position
            
        # Turn
        if turn != 0:
            rotation = transform.rotation
            angle = turn * self.turn_speed * delta_time
            turn_quat = math.Quaternion_CreateFromAxisAngle(math.Vector3(0, 0, 1), angle)
            rotation = rotation * turn_quat
            transform.rotation = rotation
            
        # Apply transform
        bus.TransformBus(bus.Event, 'SetWorldTM', self.entity_id, transform)
        
    def OnPressed(self, input_name):
        """Handle button presses"""
        if input_name == "boost":  # Space bar
            self.is_boosting = True
            
    def OnReleased(self, input_name):
        """Handle button releases"""
        if input_name == "boost":
            self.is_boosting = False
```

### ai_vehicle.py
Place in: `TwistedMetalArena/Scripts/ai_vehicle.py`

```python
import azlmbr.bus as bus
import azlmbr.math as math
import random

class AIVehicle:
    def __init__(self):
        self.entity_id = None
        self.speed = 15.0
        self.turn_speed = 1.5
        self.wander_timer = 0.0
        self.wander_direction = math.Vector3(1, 0, 0)
        self.change_direction_time = 3.0
        
    def OnActivate(self, entity_id):
        """Called when entity activates"""
        self.entity_id = entity_id
        
        # Tick handler
        self.tick_handler = bus.NotificationHandler('TickBus')
        self.tick_handler.connect()
        self.tick_handler.add_callback('OnTick', self.on_tick)
        
        # Random initial direction
        self.pick_new_direction()
        
    def OnDeactivate(self):
        """Cleanup"""
        if self.tick_handler:
            self.tick_handler.disconnect()
            
    def pick_new_direction(self):
        """Choose random direction to move"""
        angle = random.uniform(0, 2 * 3.14159)
        self.wander_direction = math.Vector3(
            math.Math_Cos(angle),
            math.Math_Sin(angle),
            0
        )
        
    def on_tick(self, delta_time, time_point):
        """AI behavior update"""
        if not self.entity_id or not self.entity_id.IsValid():
            return
            
        # Update wander timer
        self.wander_timer += delta_time
        if self.wander_timer >= self.change_direction_time:
            self.pick_new_direction()
            self.wander_timer = 0.0
            
        # Get transform
        transform = bus.TransformBus(bus.Event, 'GetWorldTM', self.entity_id)
        
        # Move in wander direction
        movement = self.wander_direction * (self.speed * delta_time)
        position = transform.position + movement
        transform.position = position
        
        # Rotate to face movement direction
        if self.wander_direction.GetLength() > 0.01:
            target_rotation = math.Quaternion_CreateFromVector3(self.wander_direction)
            current_rotation = transform.rotation
            
            # Smoothly interpolate rotation
            new_rotation = math.Quaternion_Slerp(current_rotation, target_rotation, 
                                                 self.turn_speed * delta_time)
            transform.rotation = new_rotation
            
        # Apply transform
        bus.TransformBus(bus.Event, 'SetWorldTM', self.entity_id, transform)
        
        # Simple boundary check (bounce off walls)
        if abs(position.x) > 45 or abs(position.y) > 45:
            self.wander_direction = self.wander_direction * -1
```

### powerup_spawner.py
Place in: `TwistedMetalArena/Scripts/powerup_spawner.py`

```python
import azlmbr.bus as bus
import azlmbr.editor as editor
import azlmbr.entity as entity
import azlmbr.math as math
import random

class PowerUpSpawner:
    def __init__(self):
        self.spawn_points = []
        self.powerup_count = 10
        self.arena_size = 40.0
        
    def spawn_powerups(self):
        """Create power-up spawn points throughout arena"""
        for i in range(self.powerup_count):
            x = random.uniform(-self.arena_size, self.arena_size)
            y = random.uniform(-self.arena_size, self.arena_size)
            z = 2.0  # Float above ground
            
            self.create_powerup(math.Vector3(x, y, z))
            
    def create_powerup(self, position):
        """Create individual power-up"""
        powerup = editor.ToolsApplicationRequestBus(bus.Broadcast, 'CreateNewEntity', entity.EntityId())
        editor.EditorEntityAPIBus(bus.Event, 'SetName', powerup, "PowerUp")
        
        # Add mesh (sphere or cube)
        editor.EditorComponentAPIBus(bus.Broadcast, 'AddComponentsOfType',
                                     powerup, ['Mesh'])
        
        # Set position and scale
        transform = math.Transform_CreateTranslation(position)
        transform.scale = math.Vector3(1.5, 1.5, 1.5)
        bus.TransformBus(bus.Event, 'SetWorldTM', powerup, transform)
        
        # Add rotation animation (optional)
        editor.EditorComponentAPIBus(bus.Broadcast, 'AddComponentsOfType',
                                     powerup, ['Script Canvas'])
        
        # Add trigger collider for pickup
        editor.EditorComponentAPIBus(bus.Broadcast, 'AddComponentsOfType',
                                     powerup, ['PhysX Trigger'])
        
        return powerup

# Execute
if __name__ == "__main__":
    spawner = PowerUpSpawner()
    spawner.spawn_powerups()
```

## Setup Instructions

### Step 1: Create Basic Entities

1. **Player Vehicle:**
   - Create Entity → Name: "Player_Vehicle"
   - Add components:
     - Mesh Component (assign cube mesh temporarily)
     - PhysX Dynamic Rigid Body
     - PhysX Collider (box shape)
     - Script Component (attach `vehicle_controller.py`)
   - Set scale: (3, 5, 2) for car-like proportions
   - Position: (0, 0, 2)

2. **AI Vehicles (create 3-5):**
   - Create Entity → Name: "AI_Vehicle_1"
   - Add components:
     - Mesh Component (cube mesh, different color material)
     - PhysX Dynamic Rigid Body
     - PhysX Collider (box shape)
     - Script Component (attach `ai_vehicle.py`)
   - Duplicate and spread around arena

3. **Camera:**
   - Create Entity → Name: "Chase_Camera"
   - Add Camera Component
   - Parent to Player_Vehicle
   - Position: (0, -15, 8) relative to player
   - Rotation: Look down at ~20 degrees

### Step 2: Create Materials

#### Floor Material
File: `Assets/Materials/arena_floor.material`

```json
{
    "materialType": "StandardPBR",
    "properties": {
        "baseColor": [0.3, 0.3, 0.35, 1.0],
        "metallic": 0.1,
        "roughness": 0.8
    }
}
```

#### Wall Material
File: `Assets/Materials/arena_wall.material`

```json
{
    "materialType": "StandardPBR",
    "properties": {
        "baseColor": [0.5, 0.5, 0.5, 1.0],
        "metallic": 0.0,
        "roughness": 0.9
    }
}
```

#### Vehicle Material
File: `Assets/Materials/vehicle.material`

```json
{
    "materialType": "StandardPBR",
    "properties": {
        "baseColor": [0.8, 0.1, 0.1, 1.0],
        "metallic": 0.7,
        "roughness": 0.3
    }
}
```

### Step 3: Create Simple Textures

For MVP, create simple colored textures in any image editor:

**floor_grid.png** (512x512):
- Dark gray background with lighter grid lines
- Save to: `Assets/Textures/floor_grid.png`

**wall_concrete.png** (512x512):
- Medium gray with slight noise/grain
- Save to: `Assets/Textures/wall_concrete.png`

**powerup_glow.png** (256x256):
- Bright yellow/orange with glow effect
- Save to: `Assets/Textures/powerup_glow.png`

### Step 4: Input Configuration

1. Open: Edit → Project Settings → Input Bindings
2. Add input events:
   - `vertical`: W/S keys and Up/Down arrows
   - `horizontal`: A/D keys and Left/Right arrows
   - `boost`: Space bar
   - `fire`: Left Mouse Button (for future weapons)

### Step 5: Run Arena Generator

1. Open Script Canvas or Python Console in O3DE
2. Run: `arena_generator.py`
3. Arena will generate with walls and obstacles
4. Run: `powerup_spawner.py` to add power-ups

### Step 6: Configure Physics

1. Open PhysX Configuration
2. Set gravity: (0, 0, -9.81)
3. Enable continuous collision detection
4. Set vehicle mass: 1000kg
5. Set friction: 0.8 for better control

## Testing the MVP

1. Press Ctrl+G to enter Game Mode
2. Use WASD or Arrow Keys to drive
3. Space bar for boost
4. AI vehicles should wander around
5. Collisions should work (vehicles bounce off walls/obstacles)

## Next Steps for Enhancement

Once this MVP is working, you can add:

- **Weapons System**: Projectile spawning and damage
- **Health System**: Vehicle damage and destruction
- **Power-up Effects**: Speed boost, shields, weapons
- **Better Vehicle Models**: Replace cubes with actual car meshes
- **Particle Effects**: Explosions, tire smoke, weapon fire
- **HUD**: Health bars, ammo counter, minimap
- **Sound Effects**: Engine sounds, collisions, weapons
- **Arena Variations**: Different arena layouts and themes

## Troubleshooting

**Vehicles fall through floor:**
- Ensure floor has PhysX Static Rigid Body and Collider
- Check that vehicle has PhysX Dynamic Rigid Body

**No movement:**
- Verify input bindings are set up
- Check Script Component is attached and script is assigned
- Look for Python errors in console

**Poor performance:**
- Reduce obstacle count in `arena_generator.py`
- Simplify collision shapes
- Reduce AI vehicle count

**Collisions don't work:**
- Verify all entities have PhysX Collider components
- Check collision layers in PhysX Configuration
- Ensure shapes match mesh sizes

## Support Resources

- O3DE Documentation: https://o3de.org/docs/
- O3DE Discord: https://discord.gg/o3de
- Forums: https://github.com/o3de/o3de/discussions

---

**This MVP gives you:**
✅ Randomized arena generation
✅ Drivable player vehicle
✅ AI opponent vehicles
✅ Floating power-ups
✅ Physics collisions
✅ Solid foundation for expansion

Good luck with your project! You've got a great starting point to build your Twisted Metal-style game. 🎮