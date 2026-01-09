# O3DE Vehicle Combat Camera System - Implementation Guide

## Overview
This guide walks you through implementing the vehicle combat camera system and settings menu in O3DE step-by-step.

---

## Part 1: Project Setup

### 1.1 Create the Component Files

Create these files in your O3DE project:

```
YourProject/
├── Gem/
│   └── Code/
│       └── Source/
│           └── Components/
│               ├── VehicleCombatCameraComponent.h
│               ├── VehicleCombatCameraComponent.cpp
│               ├── CameraSettingsMenuComponent.h
│               └── CameraSettingsMenuComponent.cpp
```

### 1.2 Add to CMakeLists.txt

In your gem's `CMakeLists.txt`, add:

```cmake
ly_add_target(
    NAME YourProject.Static STATIC
    # ... existing code ...
    FILES_CMAKE
        yourproject_files.cmake
    INCLUDE_DIRECTORIES
        PUBLIC
            Include
        PRIVATE
            Source
    BUILD_DEPENDENCIES
        PUBLIC
            AZ::AzCore
            AZ::AzFramework
            Legacy::CryCommon
            Gem::LyShine
            Gem::AtomLyIntegration_CommonFeatures.Public
)
```

### 1.3 Register Components

In your gem's module file (e.g., `YourProjectModule.cpp`):

```cpp
#include <AzCore/Memory/SystemAllocator.h>
#include <AzCore/Module/Module.h>
#include <Components/VehicleCombatCameraComponent.h>
#include <Components/CameraSettingsMenuComponent.h>

class YourProjectModule
    : public AZ::Module
{
public:
    AZ_RTTI(YourProjectModule, "{YOUR-GUID-HERE}", AZ::Module);
    AZ_CLASS_ALLOCATOR(YourProjectModule, AZ::SystemAllocator, 0);

    YourProjectModule()
    {
        m_descriptors.insert(m_descriptors.end(), {
            VehicleCombat::VehicleCombatCameraComponent::CreateDescriptor(),
            VehicleCombat::CameraSettingsMenuComponent::CreateDescriptor(),
        });
    }
};

AZ_DECLARE_MODULE_CLASS(Gem_YourProject, YourProjectModule)
```

---

## Part 2: Implement the Camera Component

### 2.1 Complete the Header File

Copy the camera component header from the artifact into `VehicleCombatCameraComponent.h`.

### 2.2 Implement the CPP File

Create `VehicleCombatCameraComponent.cpp`:

```cpp
#include "VehicleCombatCameraComponent.h"
#include <AzCore/Serialization/SerializeContext.h>
#include <AzCore/Serialization/EditContext.h>
#include <AzCore/Component/TransformBus.h>
#include <AzFramework/Physics/PhysicsScene.h>
#include <AzFramework/Physics/Common/PhysicsSceneQueries.h>

namespace VehicleCombat
{
    void VehicleCombatCameraComponent::GetProvidedServices(
        AZ::ComponentDescriptor::DependencyArrayType& provided)
    {
        provided.push_back(AZ_CRC_CE("VehicleCombatCameraService"));
    }

    void VehicleCombatCameraComponent::GetRequiredServices(
        AZ::ComponentDescriptor::DependencyArrayType& required)
    {
        required.push_back(AZ_CRC_CE("TransformService"));
    }

    // Copy the implementation methods from the artifact
    // Add the missing method implementations:

    void VehicleCombatCameraComponent::UpdateFirstPersonCamera(float deltaTime)
    {
        // Attach camera to vehicle cockpit position
        AZ::Vector3 vehiclePos;
        AZ::Quaternion vehicleRot;
        
        AZ::TransformBus::EventResult(vehiclePos, m_vehicleEntity,
            &AZ::TransformBus::Events::GetWorldTranslation);
        AZ::TransformBus::EventResult(vehicleRot, m_vehicleEntity,
            &AZ::TransformBus::Events::GetWorldRotationQuaternion);
        
        // Cockpit offset (adjust based on your vehicle model)
        AZ::Vector3 cockpitOffset(1.5f, 0.0f, 1.2f);
        AZ::Vector3 worldOffset = vehicleRot.TransformVector(cockpitOffset);
        
        m_currentPosition = vehiclePos + worldOffset;
        m_currentRotation = vehicleRot;
        
        // Apply to camera
        AZ::TransformBus::Event(m_cameraEntity,
            &AZ::TransformBus::Events::SetWorldTranslation, m_currentPosition);
        AZ::TransformBus::Event(m_cameraEntity,
            &AZ::TransformBus::Events::SetWorldRotationQuaternion, m_currentRotation);
    }

    void VehicleCombatCameraComponent::UpdateTopDownCamera(float deltaTime)
    {
        // Position camera directly above vehicle
        AZ::Vector3 vehiclePos;
        AZ::TransformBus::EventResult(vehiclePos, m_vehicleEntity,
            &AZ::TransformBus::Events::GetWorldTranslation);
        
        float topDownHeight = 30.0f;
        m_currentPosition = vehiclePos + AZ::Vector3(0.0f, 0.0f, topDownHeight);
        
        // Look straight down
        m_currentRotation = AZ::Quaternion::CreateRotationZ(0.0f) * 
                           AZ::Quaternion::CreateRotationX(-AZ::Constants::HalfPi);
        
        // Apply to camera
        AZ::TransformBus::Event(m_cameraEntity,
            &AZ::TransformBus::Events::SetWorldTranslation, m_currentPosition);
        AZ::TransformBus::Event(m_cameraEntity,
            &AZ::TransformBus::Events::SetWorldRotationQuaternion, m_currentRotation);
    }

    void VehicleCombatCameraComponent::UpdatePhotoModeCamera(float deltaTime)
    {
        // Free-flying camera controlled by input
        // Movement is handled in input events
        
        AZ::TransformBus::Event(m_cameraEntity,
            &AZ::TransformBus::Events::SetWorldTranslation, m_photoModePosition);
        AZ::TransformBus::Event(m_cameraEntity,
            &AZ::TransformBus::Events::SetWorldRotationQuaternion, m_photoModeRotation);
    }

    void VehicleCombatCameraComponent::SetDrawDistance(float distance)
    {
        // Update rendering draw distance
        // This is engine-specific - you'll need to hook into O3DE's streaming system
        
        // Example pseudo-code:
        // RenderBus::Broadcast(&RenderBus::Events::SetDrawDistance, distance);
    }

    void VehicleCombatCameraComponent::UpdateStreamingPriority()
    {
        // Tell the engine to prioritize loading assets in the camera's view direction
        
        AZ::Vector3 forward = m_currentRotation.TransformVector(AZ::Vector3(1.0f, 0.0f, 0.0f));
        AZ::Vector3 priorityPosition = m_currentPosition + (forward * m_streamingRadius);
        
        // Hook into O3DE's streaming system
        // StreamingBus::Broadcast(&StreamingBus::Events::SetPriorityPosition, priorityPosition);
    }

    void VehicleCombatCameraComponent::SetCombatState(CombatState state)
    {
        m_combatState = state;
    }

    void VehicleCombatCameraComponent::SetTargetEntity(AZ::EntityId targetId)
    {
        m_targetEntity = targetId;
    }

} // namespace VehicleCombat
```

### 2.3 Add Physics Collision Detection

For proper camera collision avoidance, add this method:

```cpp
void VehicleCombatCameraComponent::HandleCollisionAvoidance(AZ::Vector3& position)
{
    AZ::Vector3 vehiclePos;
    AZ::TransformBus::EventResult(vehiclePos, m_vehicleEntity,
        &AZ::TransformBus::Events::GetWorldTranslation);
    
    // Raycast from vehicle to desired camera position
    AzPhysics::RayCastRequest request;
    request.m_start = vehiclePos;
    request.m_direction = (position - vehiclePos).GetNormalized();
    request.m_distance = (position - vehiclePos).GetLength();
    
    AzPhysics::SceneQueryHits result;
    if (auto* sceneInterface = AZ::Interface<AzPhysics::SceneInterface>::Get())
    {
        if (AzPhysics::SceneHandle sceneHandle = sceneInterface->GetSceneHandle(
            AzPhysics::DefaultPhysicsSceneName))
        {
            result = sceneInterface->QueryScene(sceneHandle, &request);
        }
    }
    
    // If we hit something, move camera closer
    if (result.m_hits.size() > 0)
    {
        float hitDistance = result.m_hits[0].m_distance;
        AZ::Vector3 safePosition = vehiclePos + request.m_direction * (hitDistance - 0.3f);
        position = safePosition;
    }
}
```

---

## Part 3: Set Up in the Editor

### 3.1 Create Camera Entity

1. Open O3DE Editor
2. Create a new entity: `Right-click in Entity Outliner → Create Entity`
3. Name it "VehicleCamera"
4. Add the **Camera** component to it
5. Configure camera settings:
   - Near Clip: 0.1
   - Far Clip: 1000.0
   - FOV: 90

### 3.2 Create Vehicle Entity

1. Create your vehicle entity (or use existing)
2. Ensure it has:
   - **Transform** component
   - **Physics** component (RigidBody)
   - **Mesh** component for the vehicle model

### 3.3 Add Camera Component

1. Select your vehicle entity
2. Click **Add Component**
3. Find **Vehicle Combat Camera Component**
4. In the component properties:
   - Set **Vehicle Entity** to your vehicle entity
   - Set **Camera Entity** to the VehicleCamera entity you created

### 3.4 Link to Main Camera

Set the VehicleCamera as the active game camera:

```cpp
// In your game's initialization code
AZ::EntityId cameraEntityId = /* your camera entity ID */;
Camera::CameraRequestBus::Event(cameraEntityId,
    &Camera::CameraRequestBus::Events::MakeActiveView);
```

---

## Part 4: Input Binding

### 4.1 Create Input Bindings

Create or edit `your_project.inputbindings`:

```json
{
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
        }
    ]
}
```

### 4.2 Handle Input in Component

The input handling is already in the component via `OnInputChannelEventFiltered`. Make sure it's properly filtering events:

```cpp
bool VehicleCombatCameraComponent::OnInputChannelEventFiltered(
    const AzFramework::InputChannel& inputChannel)
{
    const AzFramework::InputChannelId& channelId = inputChannel.GetInputChannelId();
    
    // Camera mode cycling
    if (channelId == AzFramework::InputDeviceKeyboard::Key::AlphanumericC)
    {
        if (inputChannel.IsStateBegan())
        {
            CycleCameraMode();
            return true;
        }
    }
    
    // Photo mode toggle
    if (channelId == AzFramework::InputDeviceKeyboard::Key::F6)
    {
        if (inputChannel.IsStateBegan())
        {
            if (m_currentMode == CameraMode::PhotoMode)
            {
                SetCameraMode(m_previousMode);
            }
            else
            {
                SetCameraMode(CameraMode::PhotoMode);
            }
            return true;
        }
    }
    
    return false;
}
```

---

## Part 5: Implement the Settings Menu

### 5.1 Create UI Canvas

1. In O3DE Editor: `Tools → UI Editor`
2. Create new canvas: `File → New Canvas`
3. Save as: `UI/Canvases/CameraSettingsMenu.uicanvas`

OR use the programmatic creation in the menu component (it will auto-generate).

### 5.2 Add Menu Component to Game Entity

1. Create a "GameManager" entity
2. Add **Camera Settings Menu Component**
3. Link the **Vehicle Camera Component** field to your camera component entity

### 5.3 Connect to UI System

In your game initialization code:

```cpp
// Enable UI canvas
AZ::EntityId canvasId;
UiCanvasManagerBus::BroadcastResult(canvasId,
    &UiCanvasManagerBus::Events::LoadCanvas,
    "UI/Canvases/CameraSettingsMenu.uicanvas");

if (canvasId.IsValid())
{
    UiCanvasBus::Event(canvasId,
        &UiCanvasBus::Events::SetEnabled, false); // Hidden by default
}
```

---

## Part 6: Testing & Debugging

### 6.1 Test Camera Modes

In play mode, press:
- **C** - Cycle through camera modes
- **F1** - Open settings menu
- **F6** - Toggle photo mode

### 6.2 Debug Camera Position

Add debug drawing to visualize camera:

```cpp
#include <AzFramework/Entity/GameEntityContextBus.h>

void VehicleCombatCameraComponent::OnTick(float deltaTime, AZ::ScriptTimePoint time)
{
    // ... existing code ...
    
    #ifdef AZ_DEBUG_BUILD
    // Draw debug line from vehicle to camera
    AzFramework::DebugDisplayRequestBus::Broadcast(
        &AzFramework::DebugDisplayRequests::DrawLine,
        vehiclePos, m_currentPosition, AZ::Colors::Green, 0.0f);
    #endif
}
```

### 6.3 Common Issues

**Camera not following vehicle:**
- Verify Vehicle Entity field is set correctly
- Check that vehicle has Transform component
- Ensure TickBus is connected in Activate()

**Input not working:**
- Verify InputChannelEventListener is connected
- Check input bindings file is loaded
- Ensure priority is high enough to receive events

**Menu not showing:**
- Check UI canvas loads successfully
- Verify LyShine gem is enabled
- Check console for UI-related errors

---

## Part 7: Performance Optimization

### 7.1 Reduce Update Frequency

For distant cameras, reduce update rate:

```cpp
void VehicleCombatCameraComponent::OnTick(float deltaTime, AZ::ScriptTimePoint time)
{
    // Update counter
    static int frameCounter = 0;
    frameCounter++;
    
    // Update camera every frame when close, every 2-3 frames when far
    if (m_vehicleSpeed < 10.0f && frameCounter % 2 != 0)
    {
        return; // Skip this frame
    }
    
    // ... rest of update code ...
}
```

### 7.2 Cache Component Queries

```cpp
void VehicleCombatCameraComponent::Activate()
{
    // Cache frequently accessed components
    AZ::TransformBus::EventResult(m_cachedVehicleTransform, m_vehicleEntity,
        &AZ::TransformBus::Events::GetTransform);
}
```

### 7.3 LOD for Camera Effects

Disable expensive effects when not visible:

```cpp
void VehicleCombatCameraComponent::ApplyCameraEffects(float deltaTime)
{
    // Only apply if we're the active camera
    AZ::EntityId activeCamera;
    Camera::CameraSystemRequestBus::BroadcastResult(activeCamera,
        &Camera::CameraSystemRequestBus::Events::GetActiveCamera);
    
    if (activeCamera != m_cameraEntity)
        return;
    
    // ... apply effects ...
}
```

---

## Part 8: Advanced Features

### 8.1 Add Replay System

Create a simple replay recorder:

```cpp
struct CameraKeyframe
{
    float timestamp;
    AZ::Vector3 position;
    AZ::Quaternion rotation;
    float fov;
};

class ReplayRecorder
{
    AZStd::vector<CameraKeyframe> m_keyframes;
    bool m_recording = false;
    
    void RecordFrame(float time, const AZ::Vector3& pos, 
                     const AZ::Quaternion& rot, float fov)
    {
        if (!m_recording) return;
        m_keyframes.push_back({time, pos, rot, fov});
    }
    
    void PlaybackFrame(float time, AZ::Vector3& outPos, 
                       AZ::Quaternion& outRot, float& outFov)
    {
        // Interpolate between keyframes
        // ... implementation ...
    }
};
```

### 8.2 Add Cinematic Camera Paths

Use splines for cinematic shots:

```cpp
void VehicleCombatCameraComponent::FollowSplinePath(
    AZ::EntityId splineEntity, float normalizedTime)
{
    // Query spline position
    AZ::Vector3 splinePos;
    LmbrCentral::SplineComponentRequestBus::EventResult(splinePos,
        splineEntity,
        &LmbrCentral::SplineComponentRequestBus::Events::GetPosition,
        normalizedTime);
    
    m_currentPosition = splinePos;
    
    // Look at vehicle
    AZ::Vector3 vehiclePos;
    AZ::TransformBus::EventResult(vehiclePos, m_vehicleEntity,
        &AZ::TransformBus::Events::GetWorldTranslation);
    
    AZ::Vector3 lookDir = (vehiclePos - splinePos).GetNormalized();
    m_currentRotation = AZ::Quaternion::CreateShortestArc(
        AZ::Vector3(1, 0, 0), lookDir);
}
```

---

## Part 9: Integration with Game Systems

### 9.1 Connect to Combat System

```cpp
// In your combat/damage system
void OnVehicleTakeDamage(AZ::EntityId vehicleId, float damage, 
                         const AZ::Vector3& hitDirection)
{
    // Find camera component
    VehicleCombatCameraComponent* camera = nullptr;
    AZ::ComponentApplicationBus::BroadcastResult(camera,
        &AZ::ComponentApplicationBus::Events::FindComponent,
        vehicleId);
    
    if (camera)
    {
        camera->ApplyImpactShake(hitDirection, damage * 0.1f);
        
        if (damage > 50.0f)
        {
            camera->SetCombatState(CombatState::Damaged);
        }
    }
}
```

### 9.2 Connect to Targeting System

```cpp
void OnTargetAcquired(AZ::EntityId targetVehicleId)
{
    // Tell camera to track this target
    VehicleCombatCameraComponent* camera = GetPlayerCamera();
    if (camera)
    {
        camera->SetTargetEntity(targetVehicleId);
        camera->SetCombatState(CombatState::Aiming);
    }
}
```

---

## Part 10: Troubleshooting Checklist

- [ ] All header files included correctly
- [ ] Components registered in module class
- [ ] CMakeLists.txt updated with new files
- [ ] Gem rebuilt after adding components
- [ ] Camera entity created in scene
- [ ] Vehicle entity linked in component
- [ ] Input bindings configured
- [ ] UI canvas created (if using menu)
- [ ] LyShine gem enabled
- [ ] Physics components on vehicle for collision detection
- [ ] Camera component activated in editor

---

## Resources

- **O3DE Documentation**: https://www.o3de.org/docs/
- **Component Development**: https://www.o3de.org/docs/user-guide/components/
- **Input System**: https://www.o3de.org/docs/user-guide/interactivity/input/
- **UI System (LyShine)**: https://www.o3de.org/docs/user-guide/interactivity/user-interface/

---

**Next Steps:**
1. Implement the basic camera component first
2. Test in editor with a simple vehicle
3. Add menu system once camera works
4. Fine-tune settings for your specific game feel