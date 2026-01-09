"""
O3DE Vehicle Combat Camera System - Automated Setup Script
Run this from the O3DE Editor Python console or as an editor script

This script will:
1. Create all necessary entities
2. Add required components
3. Set up the camera system
4. Configure basic vehicle setup
5. Create input bindings
"""

import azlmbr.bus as bus
import azlmbr.editor as editor
import azlmbr.entity as entity
import azlmbr.math as math
import azlmbr.components as components
import azlmbr.legacy.general as general
import os
import json

class O3DECameraSetup:
    def __init__(self):
        self.created_entities = {}
        self.project_path = os.path.dirname(os.path.dirname(editor.EditorToolsApplicationRequestBus(bus.Broadcast, 'GetGameFolder')))
        print(f"Project path: {self.project_path}")
        
    def create_entity(self, name, parent_id=None):
        """Create a new entity with a given name"""
        entity_id = editor.ToolsApplicationRequestBus(bus.Broadcast, 'CreateNewEntity', parent_id)
        editor.EditorEntityAPIBus(bus.Event, 'SetName', entity_id, name)
        print(f"✓ Created entity: {name}")
        return entity_id
    
    def add_component(self, entity_id, component_type_name):
        """Add a component to an entity by type name"""
        component_type = editor.EditorComponentAPIBus(bus.Broadcast, 'FindComponentTypeIdsByEntityType', [component_type_name], 0)
        
        if component_type:
            component = editor.EditorComponentAPIBus(bus.Broadcast, 'AddComponentsOfType', entity_id, component_type)
            print(f"  ✓ Added component: {component_type_name}")
            return component[0] if component else None
        else:
            print(f"  ✗ Could not find component: {component_type_name}")
            return None
    
    def set_component_property(self, entity_id, component_id, property_path, value):
        """Set a property on a component"""
        outcome = editor.EditorComponentAPIBus(bus.Broadcast, 'SetComponentProperty', component_id, property_path, value)
        if outcome.IsSuccess():
            print(f"    ✓ Set property: {property_path}")
        else:
            print(f"    ✗ Failed to set property: {property_path}")
        return outcome.IsSuccess()
    
    def setup_camera_entity(self):
        """Create and configure the camera entity"""
        print("\n=== Setting up Camera Entity ===")
        
        camera_id = self.create_entity("VehicleCamera")
        self.created_entities['camera'] = camera_id
        
        # Add Camera component
        camera_component = self.add_component(camera_id, "Camera")
        if camera_component:
            self.set_component_property(camera_id, camera_component, "Field of View", 90.0)
            self.set_component_property(camera_id, camera_component, "Near Clip Distance", 0.1)
            self.set_component_property(camera_id, camera_component, "Far Clip Distance", 1000.0)
        
        # Set initial position (behind and above origin)
        transform = math.Transform_CreateTranslation(math.Vector3(0.0, -10.0, 5.0))
        editor.EditorTransformComponentRequestBus(bus.Event, 'SetWorldTM', camera_id, transform)
        
        return camera_id
    
    def setup_vehicle_entity(self):
        """Create and configure a basic vehicle entity"""
        print("\n=== Setting up Vehicle Entity ===")
        
        vehicle_id = self.create_entity("PlayerVehicle")
        self.created_entities['vehicle'] = vehicle_id
        
        # Add mesh component (you'll need to set the mesh asset later)
        mesh_component = self.add_component(vehicle_id, "Mesh")
        
        # Add physics - Rigid Body
        rigid_body = self.add_component(vehicle_id, "PhysX Rigid Body")
        if rigid_body:
            self.set_component_property(vehicle_id, rigid_body, "Initial linear velocity", math.Vector3(0, 0, 0))
            self.set_component_property(vehicle_id, rigid_body, "Mass", 1500.0)  # Car mass in kg
        
        # Add collider
        collider = self.add_component(vehicle_id, "PhysX Collider")
        
        # Set vehicle at origin
        transform = math.Transform_CreateTranslation(math.Vector3(0.0, 0.0, 1.0))
        editor.EditorTransformComponentRequestBus(bus.Event, 'SetWorldTM', vehicle_id, transform)
        
        return vehicle_id
    
    def setup_game_manager(self):
        """Create game manager entity for camera and menu systems"""
        print("\n=== Setting up Game Manager ===")
        
        manager_id = self.create_entity("GameManager")
        self.created_entities['manager'] = manager_id
        
        # Add Script Canvas or Lua Script component for game logic
        script_component = self.add_component(manager_id, "Script Canvas")
        
        return manager_id
    
    def setup_ground_plane(self):
        """Create a simple ground plane to drive on"""
        print("\n=== Setting up Ground Plane ===")
        
        ground_id = self.create_entity("GroundPlane")
        self.created_entities['ground'] = ground_id
        
        # Add mesh component
        mesh_component = self.add_component(ground_id, "Mesh")
        
        # Add physics collider
        collider = self.add_component(ground_id, "PhysX Static Rigid Body")
        box_collider = self.add_component(ground_id, "PhysX Collider")
        
        # Scale it up to make a large ground
        transform = math.Transform_CreateScale(math.Vector3(100.0, 100.0, 1.0))
        editor.EditorTransformComponentRequestBus(bus.Event, 'SetLocalTM', ground_id, transform)
        
        return ground_id
    
    def setup_lighting(self):
        """Set up basic lighting for the scene"""
        print("\n=== Setting up Lighting ===")
        
        # Directional light (sun)
        light_id = self.create_entity("DirectionalLight")
        self.created_entities['light'] = light_id
        
        light_component = self.add_component(light_id, "Directional Light")
        
        # Rotate to angle downward
        rotation = math.Quaternion_CreateFromEulerAngles(math.Vector3(-45.0, 0.0, 0.0))
        transform = math.Transform_CreateRotation(rotation)
        editor.EditorTransformComponentRequestBus(bus.Event, 'SetLocalTM', light_id, transform)
        
        return light_id
    
    def create_input_bindings(self):
        """Create input bindings file"""
        print("\n=== Creating Input Bindings ===")
        
        bindings = {
            "version": 1,
            "bindings": [
                {
                    "name": "camera_cycle",
                    "event_generator": "keyboard_key_c",
                    "event_name": "camera_cycle"
                },
                {
                    "name": "camera_look_back",
                    "event_generator": "gamepad_button_r1",
                    "event_name": "camera_look_back"
                },
                {
                    "name": "camera_menu",
                    "event_generator": "keyboard_key_f1",
                    "event_name": "camera_menu"
                },
                {
                    "name": "photo_mode",
                    "event_generator": "keyboard_key_f6",
                    "event_name": "photo_mode"
                },
                {
                    "name": "vehicle_forward",
                    "event_generator": "keyboard_key_w",
                    "event_name": "vehicle_forward"
                },
                {
                    "name": "vehicle_backward",
                    "event_generator": "keyboard_key_s",
                    "event_name": "vehicle_backward"
                },
                {
                    "name": "vehicle_left",
                    "event_generator": "keyboard_key_a",
                    "event_name": "vehicle_left"
                },
                {
                    "name": "vehicle_right",
                    "event_generator": "keyboard_key_d",
                    "event_name": "vehicle_right"
                }
            ]
        }
        
        # Save to project input folder
        input_folder = os.path.join(self.project_path, "Config", "Input")
        os.makedirs(input_folder, exist_ok=True)
        
        input_file = os.path.join(input_folder, "vehicle_camera.inputbindings")
        
        try:
            with open(input_file, 'w') as f:
                json.dump(bindings, f, indent=4)
            print(f"✓ Created input bindings: {input_file}")
            return True
        except Exception as e:
            print(f"✗ Failed to create input bindings: {e}")
            return False
    
    def create_component_source_files(self):
        """Create the C++ source files for the camera component"""
        print("\n=== Creating Component Source Files ===")
        
        # This creates template files - you'll need to fill in the actual implementation
        gem_code_path = os.path.join(self.project_path, "Gem", "Code", "Source", "Components")
        os.makedirs(gem_code_path, exist_ok=True)
        
        # Header file template
        header_content = '''#pragma once

#include <AzCore/Component/Component.h>
#include <AzCore/Component/TransformBus.h>
#include <AzCore/Component/TickBus.h>

namespace VehicleCombat
{
    class VehicleCombatCameraComponent
        : public AZ::Component
        , public AZ::TickBus::Handler
    {
    public:
        AZ_COMPONENT(VehicleCombatCameraComponent, "{12345678-1234-1234-1234-123456789012}");

        static void Reflect(AZ::ReflectContext* context);
        
        void Activate() override;
        void Deactivate() override;
        void OnTick(float deltaTime, AZ::ScriptTimePoint time) override;

    private:
        AZ::EntityId m_vehicleEntity;
        AZ::EntityId m_cameraEntity;
        AZ::Vector3 m_currentPosition;
    };
}
'''
        
        # CPP file template
        cpp_content = '''#include "VehicleCombatCameraComponent.h"
#include <AzCore/Serialization/SerializeContext.h>

namespace VehicleCombat
{
    void VehicleCombatCameraComponent::Reflect(AZ::ReflectContext* context)
    {
        if (auto serializeContext = azrtti_cast<AZ::SerializeContext*>(context))
        {
            serializeContext->Class<VehicleCombatCameraComponent, AZ::Component>()
                ->Version(1)
                ->Field("VehicleEntity", &VehicleCombatCameraComponent::m_vehicleEntity)
                ->Field("CameraEntity", &VehicleCombatCameraComponent::m_cameraEntity);
        }
    }

    void VehicleCombatCameraComponent::Activate()
    {
        AZ::TickBus::Handler::BusConnect();
    }

    void VehicleCombatCameraComponent::Deactivate()
    {
        AZ::TickBus::Handler::BusDisconnect();
    }

    void VehicleCombatCameraComponent::OnTick(float deltaTime, AZ::ScriptTimePoint time)
    {
        // Basic camera follow logic here
        AZ::Vector3 vehiclePos;
        AZ::TransformBus::EventResult(vehiclePos, m_vehicleEntity,
            &AZ::TransformBus::Events::GetWorldTranslation);
        
        // Position camera behind vehicle
        m_currentPosition = vehiclePos + AZ::Vector3(0.0f, -10.0f, 5.0f);
        
        AZ::TransformBus::Event(m_cameraEntity,
            &AZ::TransformBus::Events::SetWorldTranslation, m_currentPosition);
    }
}
'''
        
        try:
            header_file = os.path.join(gem_code_path, "VehicleCombatCameraComponent.h")
            cpp_file = os.path.join(gem_code_path, "VehicleCombatCameraComponent.cpp")
            
            with open(header_file, 'w') as f:
                f.write(header_content)
            print(f"✓ Created: {header_file}")
            
            with open(cpp_file, 'w') as f:
                f.write(cpp_content)
            print(f"✓ Created: {cpp_file}")
            
            return True
        except Exception as e:
            print(f"✗ Failed to create source files: {e}")
            return False
    
    def create_readme(self):
        """Create a README with next steps"""
        print("\n=== Creating README ===")
        
        readme_content = '''# Vehicle Combat Camera System - Setup Complete!

## What Was Created

### Entities:
- **VehicleCamera**: The camera that will follow your vehicle
- **PlayerVehicle**: Your vehicle entity (needs mesh and physics setup)
- **GameManager**: Manages game systems
- **GroundPlane**: A surface to drive on
- **DirectionalLight**: Basic lighting

### Files:
- Input bindings: Config/Input/vehicle_camera.inputbindings
- Component templates: Gem/Code/Source/Components/

## Next Steps

### 1. Add a Vehicle Mesh
1. Select the "PlayerVehicle" entity in the Entity Outliner
2. Find the "Mesh" component in the Entity Inspector
3. Click the folder icon next to "Model Asset"
4. Choose a vehicle mesh from your assets
   (You may need to import one first: Assets → Import)

### 2. Set Up the Camera Link
Since we can't create custom components from Python, we have two options:

**Option A: Use Script Canvas (Easier)**
1. Select "GameManager" entity
2. Add "Script Canvas" component
3. Create a new Script Canvas graph
4. Add logic to:
   - Get PlayerVehicle position every frame
   - Set VehicleCamera position behind vehicle
   - Add offset: (0, -10, 5) relative to vehicle

**Option B: Write C++ Component (More powerful)**
1. The template files are in Gem/Code/Source/Components/
2. Fill in the full implementation from the artifacts
3. Rebuild your project
4. Add "Vehicle Combat Camera Component" to PlayerVehicle

### 3. Test Basic Camera
1. Press Ctrl+G to enter Play Mode
2. The camera should be positioned behind your vehicle
3. If using physics, the vehicle should respond to gravity

### 4. Add Vehicle Controls
Create a Script Canvas graph with:
- Input events (W/A/S/D)
- Apply forces to the vehicle's Rigid Body
- Simple arcade-style driving physics

### 5. Enhance the Camera (Optional)
- Add smooth follow using lerp
- Add look-ahead prediction
- Add camera shake on collisions
- Implement the full combat camera system

## Controls (Once Set Up)

- **W/A/S/D**: Drive vehicle (needs scripting)
- **C**: Cycle camera modes (needs component)
- **F1**: Open camera menu (needs component)
- **F6**: Photo mode (needs component)

## Troubleshooting

**Camera not following vehicle?**
- Make sure the Script Canvas or component is active
- Check that entity IDs are correctly linked
- Verify the vehicle entity is actually moving

**Vehicle falls through ground?**
- Make sure GroundPlane has PhysX Static Rigid Body
- Check that vehicle has PhysX Rigid Body
- Verify collision layers are set correctly

**Nothing visible in viewport?**
- Check that camera is the active camera
- Make sure lighting is set up
- Verify entities are not disabled

## Resources

- O3DE Documentation: https://www.o3de.org/docs/
- Script Canvas Guide: https://www.o3de.org/docs/user-guide/scripting/script-canvas/
- Vehicle Physics Tutorial: Check O3DE YouTube channel

## Need Help?

1. Check the O3DE Discord: https://discord.gg/o3de
2. Forum: https://github.com/o3de/o3de/discussions
3. Documentation: https://www.o3de.org/docs/

Good luck with your Twisted Metal-style game!
'''
        
        try:
            readme_file = os.path.join(self.project_path, "CAMERA_SETUP_README.md")
            with open(readme_file, 'w') as f:
                f.write(readme_content)
            print(f"✓ Created: {readme_file}")
            return True
        except Exception as e:
            print(f"✗ Failed to create README: {e}")
            return False
    
    def run_full_setup(self):
        """Run the complete setup process"""
        print("="*60)
        print("O3DE Vehicle Combat Camera System - Automated Setup")
        print("="*60)
        
        try:
            # Create entities
            self.setup_camera_entity()
            self.setup_vehicle_entity()
            self.setup_game_manager()
            self.setup_ground_plane()
            self.setup_lighting()
            
            # Create files
            self.create_input_bindings()
            self.create_component_source_files()
            self.create_readme()
            
            print("\n" + "="*60)
            print("✓ SETUP COMPLETE!")
            print("="*60)
            print("\nWhat was created:")
            for name, entity_id in self.created_entities.items():
                print(f"  • {name}: Entity ID {entity_id}")
            
            print("\nNext Steps:")
            print("  1. Check the Entity Outliner (right side) - you'll see all entities")
            print("  2. Read CAMERA_SETUP_README.md in your project folder")
            print("  3. Add a mesh to the PlayerVehicle entity")
            print("  4. Set up basic vehicle movement with Script Canvas")
            print("  5. Make VehicleCamera the active camera")
            
            print("\nFiles created:")
            print(f"  • {os.path.join(self.project_path, 'CAMERA_SETUP_README.md')}")
            print(f"  • Config/Input/vehicle_camera.inputbindings")
            print(f"  • Gem/Code/Source/Components/VehicleCombatCameraComponent.*")
            
            return True
            
        except Exception as e:
            print(f"\n✗ Setup failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False

# Main execution
def main():
    """Main entry point for the script"""
    print("\n" + "="*60)
    print("Starting O3DE Camera System Setup...")
    print("="*60 + "\n")
    
    setup = O3DECameraSetup()
    success = setup.run_full_setup()
    
    if success:
        print("\n🎉 All done! Check the Entity Outliner to see your new entities.")
        print("📖 Read CAMERA_SETUP_README.md for next steps.\n")
    else:
        print("\n❌ Setup encountered errors. Check the output above.")
    
    return success

# Run the setup
if __name__ == "__main__":
    main()
