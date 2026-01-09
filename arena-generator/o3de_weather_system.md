# O3DE Weather System for Twisted Metal Arena

## Overview
This integrates dynamic weather into your arena, adapting weather systems for O3DE. Weather affects visibility, handling, and atmosphere.

## File Structure

```
TwistedMetalArena/
├── Scripts/
│   ├── weather_manager.py
│   ├── weather_effects.py
│   └── weather_transitions.py
├── Config/
│   └── weather_config.json
└── Assets/
    ├── Particles/
    │   ├── rain_system.particle
    │   ├── snow_system.particle
    │   └── fog_system.particle
    └── Materials/
        └── weather_materials/
```

## Weather Configuration File

### weather_config.json
Place in: `TwistedMetalArena/Config/weather_config.json`

This is your adapted weather database:

```json
{
  "version": "1.0",
  "weather_types": {
    "EXTRASUNNY": {
      "sun_intensity": 1.0,
      "cloud_coverage": 0.0,
      "wind_min": 0.1,
      "wind_max": 0.3,
      "rain_intensity": 0.0,
      "wetness": 0.0,
      "snow_intensity": 0.0,
      "fog_density": 0.0,
      "visibility_range": 1000.0,
      "vehicle_grip_multiplier": 1.0,
      "sky_color": [0.4, 0.6, 0.9],
      "ambient_light": [0.8, 0.8, 0.9],
      "particle_system": null
    },
    "CLEAR": {
      "sun_intensity": 0.9,
      "cloud_coverage": 0.1,
      "wind_min": 0.1,
      "wind_max": 0.4,
      "rain_intensity": 0.0,
      "wetness": 0.0,
      "snow_intensity": 0.0,
      "fog_density": 0.0,
      "visibility_range": 900.0,
      "vehicle_grip_multiplier": 1.0,
      "sky_color": [0.45, 0.65, 0.85],
      "ambient_light": [0.75, 0.75, 0.85],
      "particle_system": null
    },
    "CLOUDS": {
      "sun_intensity": 0.6,
      "cloud_coverage": 0.4,
      "wind_min": 0.2,
      "wind_max": 0.5,
      "rain_intensity": 0.0,
      "wetness": 0.0,
      "snow_intensity": 0.0,
      "fog_density": 0.0,
      "visibility_range": 700.0,
      "vehicle_grip_multiplier": 1.0,
      "sky_color": [0.5, 0.55, 0.65],
      "ambient_light": [0.6, 0.6, 0.7],
      "particle_system": null
    },
    "FOGGY": {
      "sun_intensity": 0.0,
      "cloud_coverage": 1.0,
      "wind_min": 0.0,
      "wind_max": 0.1,
      "rain_intensity": 0.0,
      "wetness": 0.0,
      "snow_intensity": 0.0,
      "fog_density": 1.0,
      "visibility_range": 150.0,
      "vehicle_grip_multiplier": 0.95,
      "sky_color": [0.6, 0.6, 0.6],
      "ambient_light": [0.4, 0.4, 0.5],
      "particle_system": "fog"
    },
    "OVERCAST": {
      "sun_intensity": 0.0,
      "cloud_coverage": 1.0,
      "wind_min": 0.2,
      "wind_max": 0.6,
      "rain_intensity": 0.0,
      "wetness": 0.0,
      "snow_intensity": 0.0,
      "fog_density": 0.0,
      "visibility_range": 600.0,
      "vehicle_grip_multiplier": 1.0,
      "sky_color": [0.4, 0.4, 0.5],
      "ambient_light": [0.5, 0.5, 0.6],
      "particle_system": null
    },
    "RAIN": {
      "sun_intensity": 0.0,
      "cloud_coverage": 1.0,
      "wind_min": 0.6,
      "wind_max": 1.1,
      "rain_intensity": 0.8,
      "wetness": 0.8,
      "snow_intensity": 0.0,
      "fog_density": 0.2,
      "visibility_range": 300.0,
      "vehicle_grip_multiplier": 0.7,
      "sky_color": [0.3, 0.3, 0.4],
      "ambient_light": [0.4, 0.4, 0.5],
      "particle_system": "rain"
    },
    "THUNDER": {
      "sun_intensity": 0.0,
      "cloud_coverage": 1.0,
      "wind_min": 1.0,
      "wind_max": 1.5,
      "rain_intensity": 1.0,
      "wetness": 1.0,
      "snow_intensity": 0.0,
      "fog_density": 0.7,
      "visibility_range": 200.0,
      "vehicle_grip_multiplier": 0.6,
      "sky_color": [0.2, 0.2, 0.3],
      "ambient_light": [0.3, 0.3, 0.4],
      "particle_system": "rain_heavy",
      "has_lightning": true,
      "lightning_interval_min": 3.0,
      "lightning_interval_max": 8.0
    },
    "SNOW": {
      "sun_intensity": 0.0,
      "cloud_coverage": 1.0,
      "wind_min": 0.1,
      "wind_max": 0.2,
      "rain_intensity": 0.0,
      "wetness": 0.0,
      "snow_intensity": 0.5,
      "fog_density": 0.5,
      "visibility_range": 250.0,
      "vehicle_grip_multiplier": 0.5,
      "sky_color": [0.7, 0.7, 0.75],
      "ambient_light": [0.8, 0.8, 0.9],
      "particle_system": "snow"
    },
    "BLIZZARD": {
      "sun_intensity": 0.0,
      "cloud_coverage": 1.0,
      "wind_min": 1.0,
      "wind_max": 1.4,
      "rain_intensity": 0.0,
      "wetness": 0.1,
      "snow_intensity": 1.0,
      "fog_density": 1.0,
      "visibility_range": 100.0,
      "vehicle_grip_multiplier": 0.4,
      "sky_color": [0.8, 0.8, 0.85],
      "ambient_light": [0.6, 0.6, 0.7],
      "particle_system": "snow_heavy"
    },
    "SMOG": {
      "sun_intensity": 0.9,
      "cloud_coverage": 0.1,
      "wind_min": 0.0,
      "wind_max": 0.2,
      "rain_intensity": 0.0,
      "wetness": 0.0,
      "snow_intensity": 0.0,
      "fog_density": 0.8,
      "visibility_range": 200.0,
      "vehicle_grip_multiplier": 0.95,
      "sky_color": [0.6, 0.5, 0.4],
      "ambient_light": [0.7, 0.6, 0.5],
      "particle_system": "fog"
    }
  },
  "weather_cycle": [
    {"weather": "EXTRASUNNY", "duration": 120},
    {"weather": "CLEAR", "duration": 120},
    {"weather": "CLOUDS", "duration": 100},
    {"weather": "OVERCAST", "duration": 60},
    {"weather": "RAIN", "duration": 300},
    {"weather": "CLEARING", "duration": 60},
    {"weather": "CLEAR", "duration": 180},
    {"weather": "FOGGY", "duration": 60},
    {"weather": "CLEAR", "duration": 240},
    {"weather": "OVERCAST", "duration": 60},
    {"weather": "THUNDER", "duration": 120},
    {"weather": "CLEARING", "duration": 60}
  ],
  "transition_duration": 5.0
}
```

## Python Scripts

### weather_manager.py
Place in: `TwistedMetalArena/Scripts/weather_manager.py`

```python
import azlmbr.bus as bus
import azlmbr.entity as entity
import azlmbr.math as math
import azlmbr.render as render
import json
import random

class WeatherManager:
    def __init__(self):
        self.entity_id = None
        self.current_weather = "CLEAR"
        self.target_weather = "CLEAR"
        self.weather_config = {}
        self.transition_progress = 1.0
        self.transition_duration = 5.0
        self.cycle_timer = 0.0
        self.current_cycle_index = 0
        self.auto_cycle = True
        
        # Weather state
        self.current_sun_intensity = 1.0
        self.current_fog_density = 0.0
        self.current_wind = 0.1
        self.current_visibility = 1000.0
        
        # Particle systems
        self.active_particles = []
        
        # Lightning
        self.lightning_timer = 0.0
        self.lightning_next = 0.0
        
        self.load_config()
        
    def load_config(self):
        """Load weather configuration from JSON"""
        try:
            with open('Config/weather_config.json', 'r') as f:
                config = json.load(f)
                self.weather_config = config['weather_types']
                self.weather_cycle = config['weather_cycle']
                self.transition_duration = config['transition_duration']
                print(f"Loaded {len(self.weather_config)} weather types")
        except Exception as e:
            print(f"Error loading weather config: {e}")
            self.create_default_config()
            
    def create_default_config(self):
        """Create minimal default config if file not found"""
        self.weather_config = {
            "CLEAR": {
                "sun_intensity": 1.0,
                "fog_density": 0.0,
                "wind_min": 0.1,
                "wind_max": 0.3,
                "visibility_range": 1000.0,
                "vehicle_grip_multiplier": 1.0,
                "particle_system": None
            }
        }
        self.weather_cycle = [{"weather": "CLEAR", "duration": 300}]
        
    def OnActivate(self, entity_id):
        """Called when entity activates"""
        self.entity_id = entity_id
        
        # Tick handler
        self.tick_handler = bus.NotificationHandler('TickBus')
        self.tick_handler.connect()
        self.tick_handler.add_callback('OnTick', self.on_tick)
        
        # Set initial weather
        self.set_weather("CLEAR")
        
    def OnDeactivate(self):
        """Cleanup"""
        if self.tick_handler:
            self.tick_handler.disconnect()
        self.cleanup_particles()
        
    def on_tick(self, delta_time, time_point):
        """Update every frame"""
        if not self.entity_id or not self.entity_id.IsValid():
            return
            
        # Handle weather transitions
        if self.transition_progress < 1.0:
            self.transition_progress += delta_time / self.transition_duration
            self.transition_progress = min(1.0, self.transition_progress)
            self.update_transition()
            
        # Handle weather cycling
        if self.auto_cycle:
            self.cycle_timer += delta_time
            current_cycle = self.weather_cycle[self.current_cycle_index]
            
            if self.cycle_timer >= current_cycle['duration']:
                self.advance_weather_cycle()
                
        # Handle lightning
        if self.has_lightning():
            self.update_lightning(delta_time)
            
    def set_weather(self, weather_name, instant=False):
        """Change to a specific weather type"""
        if weather_name not in self.weather_config:
            print(f"Weather type {weather_name} not found")
            return
            
        self.target_weather = weather_name
        
        if instant:
            self.current_weather = weather_name
            self.transition_progress = 1.0
            self.apply_weather_immediate()
        else:
            self.transition_progress = 0.0
            
        print(f"Weather changing to: {weather_name}")
        
    def update_transition(self):
        """Smoothly transition between weather states"""
        if self.transition_progress >= 1.0:
            self.current_weather = self.target_weather
            self.apply_weather_immediate()
            return
            
        # Get current and target weather data
        current_data = self.weather_config.get(self.current_weather, {})
        target_data = self.weather_config.get(self.target_weather, {})
        
        # Interpolate values
        t = self.transition_progress
        
        # Sun intensity
        current_sun = current_data.get('sun_intensity', 1.0)
        target_sun = target_data.get('sun_intensity', 1.0)
        self.current_sun_intensity = self.lerp(current_sun, target_sun, t)
        
        # Fog density
        current_fog = current_data.get('fog_density', 0.0)
        target_fog = target_data.get('fog_density', 0.0)
        self.current_fog_density = self.lerp(current_fog, target_fog, t)
        
        # Apply to render settings
        self.apply_render_settings()
        
    def apply_weather_immediate(self):
        """Apply weather settings immediately"""
        weather_data = self.weather_config[self.current_weather]
        
        self.current_sun_intensity = weather_data.get('sun_intensity', 1.0)
        self.current_fog_density = weather_data.get('fog_density', 0.0)
        self.current_visibility = weather_data.get('visibility_range', 1000.0)
        self.current_wind = (weather_data.get('wind_min', 0.1) + 
                            weather_data.get('wind_max', 0.3)) / 2.0
        
        self.apply_render_settings()
        self.update_particle_systems(weather_data)
        
        # Notify vehicles of grip change
        grip = weather_data.get('vehicle_grip_multiplier', 1.0)
        self.broadcast_grip_change(grip)
        
    def apply_render_settings(self):
        """Apply lighting and fog to O3DE renderer"""
        # Get the global light entity (usually the sun)
        # You'll need to find your directional light entity
        
        # Set sun intensity
        # render.LightComponentRequestBus(bus.Event, 'SetIntensity', 
        #                                 sun_entity, self.current_sun_intensity)
        
        # Set fog density (using O3DE's fog system)
        # This is a simplified example - actual implementation depends on your setup
        pass
        
    def update_particle_systems(self, weather_data):
        """Create/destroy particle systems based on weather"""
        # Clean up existing particles
        self.cleanup_particles()
        
        # Spawn new particles if needed
        particle_type = weather_data.get('particle_system')
        if particle_type:
            self.spawn_particle_system(particle_type)
            
    def spawn_particle_system(self, particle_type):
        """Create particle system for weather effect"""
        # This creates a particle emitter entity
        # You'll need to have particle assets set up
        
        particle_entity = bus.EditorToolsApplicationRequestBus(
            bus.Broadcast, 'CreateNewEntity', entity.EntityId()
        )
        
        # Position above player area
        transform = math.Transform_CreateTranslation(math.Vector3(0, 0, 50))
        bus.TransformBus(bus.Event, 'SetWorldTM', particle_entity, transform)
        
        # Add particle component
        # particle_component = bus.EditorComponentAPIBus(
        #     bus.Broadcast, 'AddComponentsOfType',
        #     particle_entity, ['Particle']
        # )
        
        self.active_particles.append(particle_entity)
        
    def cleanup_particles(self):
        """Remove all active weather particle systems"""
        for particle_entity in self.active_particles:
            if particle_entity.IsValid():
                bus.EditorToolsApplicationRequestBus(
                    bus.Broadcast, 'DestroyEntity', particle_entity
                )
        self.active_particles.clear()
        
    def has_lightning(self):
        """Check if current weather has lightning"""
        weather_data = self.weather_config.get(self.current_weather, {})
        return weather_data.get('has_lightning', False)
        
    def update_lightning(self, delta_time):
        """Handle lightning strikes"""
        self.lightning_timer += delta_time
        
        if self.lightning_timer >= self.lightning_next:
            self.trigger_lightning()
            weather_data = self.weather_config[self.current_weather]
            min_interval = weather_data.get('lightning_interval_min', 3.0)
            max_interval = weather_data.get('lightning_interval_max', 8.0)
            self.lightning_next = random.uniform(min_interval, max_interval)
            self.lightning_timer = 0.0
            
    def trigger_lightning(self):
        """Create a lightning flash"""
        print("⚡ Lightning strike!")
        
        # Flash the ambient light briefly
        # This would temporarily boost the sun intensity
        # Then fade back over 0.2 seconds
        
    def advance_weather_cycle(self):
        """Move to next weather in cycle"""
        self.current_cycle_index = (self.current_cycle_index + 1) % len(self.weather_cycle)
        next_weather = self.weather_cycle[self.current_cycle_index]['weather']
        self.set_weather(next_weather)
        self.cycle_timer = 0.0
        
    def broadcast_grip_change(self, grip_multiplier):
        """Notify all vehicles of grip change"""
        # Use EBus to notify vehicle controllers
        # They can adjust their handling based on this
        pass
        
    def lerp(self, a, b, t):
        """Linear interpolation"""
        return a + (b - a) * t
        
    def set_random_weather(self):
        """Set a random weather type"""
        weather_list = list(self.weather_config.keys())
        random_weather = random.choice(weather_list)
        self.set_weather(random_weather)
        
    def skip_to_weather(self, weather_name):
        """Jump directly to a weather type (for testing)"""
        self.set_weather(weather_name, instant=True)
        self.auto_cycle = False  # Stop auto cycling
```

### weather_effects.py
Place in: `TwistedMetalArena/Scripts/weather_effects.py`

```python
import azlmbr.bus as bus
import azlmbr.math as math

class WeatherEffects:
    """Handles visual effects for different weather conditions"""
    
    def __init__(self):
        self.entity_id = None
        self.screen_effects = []
        
    def OnActivate(self, entity_id):
        self.entity_id = entity_id
        
    def apply_rain_drops_to_camera(self, intensity):
        """Add rain drops to camera view"""
        # This would use a post-process effect or UI overlay
        # with animated rain drops on the "windshield"
        pass
        
    def apply_snow_accumulation(self, intensity):
        """Add snow to edges of camera view"""
        # Frost effect on camera edges
        pass
        
    def apply_fog_blur(self, density):
        """Add distance blur for fog"""
        # Depth-based blur effect
        pass
        
    def create_puddles(self, wetness):
        """Create reflective puddles on arena floor"""
        # Modify floor material to add reflection
        pass
        
    def add_wind_sway(self, wind_strength):
        """Make debris/obstacles sway in wind"""
        # Apply slight rotation animation to objects
        pass
```

## Integration Steps

### Step 1: Add Weather Manager to Scene

1. Create empty entity: "Weather_Manager"
2. Add Script Component
3. Attach `weather_manager.py`
4. Place the `weather_config.json` in your Config folder

### Step 2: Update Vehicle Controller

Modify `vehicle_controller.py` to respond to weather:

```python
class VehicleController:
    def __init__(self):
        # ... existing code ...
        self.grip_multiplier = 1.0
        
        # Listen for weather changes
        self.weather_handler = bus.NotificationHandler('WeatherChangeNotificationBus')
        self.weather_handler.connect()
        self.weather_handler.add_callback('OnGripChange', self.on_grip_change)
        
    def on_grip_change(self, new_grip):
        """Adjust handling based on weather"""
        self.grip_multiplier = new_grip
        print(f"Vehicle grip now: {new_grip}")
        
    def on_tick(self, delta_time, time_point):
        # ... existing movement code ...
        
        # Apply grip to turning
        effective_turn_speed = self.turn_speed * self.grip_multiplier
        
        # If very slippery (snow/ice), add drift
        if self.grip_multiplier < 0.6:
            # Reduce control
            turn *= 0.7
```

### Step 3: Console Commands for Testing

Add these to test weather in-game:

```python
# In weather_manager.py, add console command handlers
def register_console_commands(self):
    """Register debug commands"""
    # weather.set RAIN
    # weather.random
    # weather.cycle true/false
    pass
```

### Step 4: Create Simple Particle Effects

For MVP, create basic particles:

**Rain Particle:**
- Small white stretched sprites
- Falling downward with gravity
- Spawn continuously above player

**Snow Particle:**
- Larger white sprites
- Gentle falling with slight wind sway
- Lower spawn rate than rain

**Fog Particle:**
- Large soft sprites
- Very slow movement
- Low opacity, high density

## Combat Arena Integration Ideas

Make weather affect gameplay:

1. **Rain**: Slippery handling, reduced visibility (harder to aim)
2. **Thunder**: Lightning strikes create hazards in arena
3. **Fog**: Hide from enemies, ambush opportunities
4. **Snow**: Slow movement, leave vehicle tracks
5. **Clear**: Standard combat, no modifiers

## Usage Examples

```python
# Set specific weather
weather_manager.set_weather("THUNDER")

# Random weather
weather_manager.set_random_weather()

# Enable auto cycling
weather_manager.auto_cycle = True

# Quick test (instant change)
weather_manager.skip_to_weather("BLIZZARD")
```

## Performance Tips

1. **Limit particle count** - Max 2000-3000 particles
2. **Use fog sparingly** - Heavy fog kills FPS
3. **Cache weather states** - Don't recalculate every frame
4. **LOD for particles** - Reduce particle count at distance

## Future Enhancements

- **Regional weather**: Different weather in arena zones
- **Weather power-ups**: Control weather as a weapon
- **Time of day**: Sync with lighting system
- **Weather damage**: Rain/snow damages vehicles over time
- **Puddle physics**: Vehicles splash through water

---

This gives you a full weather system that makes your arena feel alive and adds strategic depth to combat! 🌦️⚡❄️