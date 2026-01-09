# O3DE Camera Setup - Step-by-Step for Complete Beginners

Let's build your vehicle combat camera system from scratch, one simple step at a time.

---

## Part 1: Understanding What You See (5 minutes)

You're looking at the **O3DE Editor**. Here's what you see:

```
┌─────────────────────────────────────────────────────────┐
│  File  Edit  Tools  View                    [Menus]     │
├─────────────────────────────────────────────────────────┤
│ 📁 Entity Outliner  │                    │ 🔧 Inspector  │
│ (List of things     │   [3D Viewport]    │ (Properties)  │
│  in your scene)     │   (Your game view) │               │
│                     │                    │               │
│                     │                    │               │
│                     │                    │               │
└─────────────────────────────────────────────────────────┘
```

- **Left Panel (Entity Outliner)**: List of all objects in your game world
- **Center (Viewport)**: Where you see and interact with your 3D world
- **Right Panel (Inspector)**: Shows properties of selected objects

That "grey thing floating" is probably the default entity. Let's start fresh!

---

## Part 2: Create Your First Entity - The Camera (10 minutes)

### Step 1: Create a Camera Entity

1. **Right-click** in the **Entity Outliner** (left panel)
2. Click **"Create entity"**
3. You'll see a new item appear called "Entity1" or similar
4. **Right-click on it** → **Rename** → Type `VehicleCamera` → Press Enter

### Step 2: Add Camera Component

1. Make sure `VehicleCamera` is **selected** (click on it)
2. Look at the **Inspector panel** (right side)
3. At the bottom of the Inspector, click **"Add Component"** button
4. In the search box, type `camera`
5. Click **"Camera"** from the list
6. You should now see "Camera" appear in the Inspector!

### Step 3: Position the Camera

Still in the Inspector with VehicleCamera selected:

1. Find the **Transform** component (it's always there)
2. Look for **Translate** (this is the position)
3. Change the values to:
   - X: `0`
   - Y: `-10` (negative 10)
   - Z: `5`

This puts the camera 10 meters back and 5 meters up from the center.

### Step 4: Make This the Active Camera

1. With VehicleCamera still selected
2. In the Camera component, find the checkbox **"Be this active camera on activate"**
3. **Check that box** ✓

🎉 You now have a camera!

---

## Part 3: Create Something to See (10 minutes)

### Step 1: Create a Ground

1. **Right-click** in Entity Outliner
2. **Create entity**
3. Rename it to `Ground`
4. With Ground selected, click **Add Component**
5. Search for and add **"Mesh"**
6. In the Mesh component, next to **"Model Asset"**, click the **📁 folder icon**
7. Navigate to: `Engine` → `Primitives` → Double-click **`plane.fbx`**

Now you have a ground plane!

### Step 2: Make the Ground Solid (Add Physics)

Still with Ground selected:

1. **Add Component** → Search for **"PhysX Static Rigid Body"** → Add it
2. **Add Component** → Search for **"PhysX Collider"** → Add it

### Step 3: Make the Ground Bigger

In the Transform component:

1. Find **Scale**
2. Change all three values to:
   - X: `50`
   - Y: `50`
   - Z: `1`

Now you have a big ground plane!

---

## Part 4: Create Your Vehicle (15 minutes)

### Step 1: Create Vehicle Entity

1. **Right-click** in Entity Outliner
2. **Create entity**
3. Rename it to `PlayerVehicle`
4. In Transform, set **Translate Z** to `2` (so it's above the ground)

### Step 2: Add a Mesh (Visual)

1. With PlayerVehicle selected, **Add Component** → **Mesh**
2. Click the folder icon next to Model Asset
3. For now, let's use a simple cube: Navigate to `Engine` → `Primitives` → `cube.fbx`
   - (Later you can replace this with an actual car model)

### Step 3: Add Physics (So It Can Move)

1. **Add Component** → Search for **"PhysX Rigid Body"**
2. In PhysX Rigid Body component:
   - Find **Mass** → Set it to `1500` (weight of a car in kg)
3. **Add Component** → Search for **"PhysX Collider"**

### Step 4: Scale the Vehicle

In Transform → Scale:
- X: `2`
- Y: `4` (longer, like a car)
- Z: `1.5`

---

## Part 5: Add Lighting (5 minutes)

You need light to see anything!

### Step 1: Create a Light

1. **Right-click** in Entity Outliner
2. **Create entity**
3. Rename to `Sun`
4. **Add Component** → Search for **"Directional Light"**

### Step 2: Angle the Light

In Transform → Rotate:
- X: `-45` (negative 45 degrees)
- Y: `0`
- Z: `0`

Now your scene is lit!

---

## Part 6: Test Your Scene (2 minutes)

### Press Ctrl+G to Play!

1. Press **Ctrl + G** (or click the ▶️ Play button)
2. You should see:
   - Your vehicle (cube) from the camera's perspective
   - The vehicle should fall onto the ground due to gravity
   - Everything should be lit

### Exit Play Mode

Press **Ctrl + G** again (or press Escape)

---

## Part 7: Make Camera Follow Vehicle - Simple Version (20 minutes)

Now let's make the camera follow your vehicle using **Script Canvas** (visual scripting - no code needed!)

### Step 1: Create a Script Entity

1. **Right-click** in Entity Outliner → **Create entity**
2. Rename to `CameraController`
3. **Add Component** → Search for **"Script Canvas"**

### Step 2: Create a New Script

1. In the Script Canvas component, click **"📄 New script"**
2. Save it as: `camera_follow.scriptcanvas` in your project folder
3. The Script Canvas editor window will open

### Step 3: Build the Camera Logic

You'll see a graph editor. We need to:
- Every frame, get the vehicle's position
- Set the camera behind the vehicle

Here's what to do in Script Canvas:

**Add Nodes:**

1. **On Entity Activated** (this is already there - the starting point)

2. **On Tick** node:
   - Right-click in graph → Search "On Tick"
   - This runs every frame

3. **Get Entity by Name** node (to find PlayerVehicle):
   - Right-click → Search "Get Entity by Name"
   - In the node, type `PlayerVehicle` in the Name field

4. **Transform Get World Translation** (get vehicle position):
   - Right-click → Search "Get World Translation"
   - Connect the Entity output from previous node to Transform input

5. **Vector3 Add** node:
   - Right-click → Search "Vector3 Add"
   - This will offset the camera behind the vehicle
   - Set the second input to: `(0, -10, 5)`

6. **Get Entity by Name** again (to find VehicleCamera):
   - Type `VehicleCamera` in Name field

7. **Transform Set World Translation**:
   - Right-click → Search "Set World Translation"
   - Connect camera entity and the result from Vector3 Add

**Connect Everything:**

```
On Tick → Get PlayerVehicle Entity
  ↓
Get PlayerVehicle Position
  ↓
Add Offset (0, -10, 5)
  ↓
Get VehicleCamera Entity
  ↓
Set Camera Position
```

This is visual - drag lines between the output pins and input pins.

### Step 4: Save and Close

- Press **Ctrl + S** to save
- Close the Script Canvas window

---

## Part 8: Test the Follow Camera (2 minutes)

1. Press **Ctrl + G** to play
2. The camera should now be positioned behind your vehicle
3. If the vehicle falls due to gravity, the camera follows it!

---

## Part 9: Add Vehicle Movement (Optional, 15 minutes)

Want to actually drive? Add this to a new script:

### Create Vehicle Controller Script

1. Select PlayerVehicle
2. **Add Component** → **Script Canvas**
3. Create new script: `vehicle_controls.scriptcanvas`

### Add These Nodes:

1. **On Tick**
2. **Input - Is Key Down** (check for W key)
   - If pressed, apply forward force
3. **PhysX Apply Force**
   - Force: `(1000, 0, 0)` when W is pressed
   - Connect to PlayerVehicle's Rigid Body

Repeat for:
- **S key**: Apply force `(-1000, 0, 0)` (backward)
- **A key**: Apply torque for left turn
- **D key**: Apply torque for right turn

---

## Troubleshooting

### "I don't see anything when I press Ctrl+G!"
- Make sure VehicleCamera has "Be this active camera on activate" checked
- Check that your camera is not inside the ground (Z should be positive)

### "My vehicle disappears!"
- It probably fell through the ground
- Make sure Ground has both PhysX Static Rigid Body AND PhysX Collider
- Check that Ground's Z position is 0 or below your vehicle

### "Script Canvas is confusing!"
- That's okay! You can skip the camera following for now
- Just position the camera manually and see your scene first
- Come back to scripting later

### "Where's the Python console?"
- Don't use it! It's unstable. Stick to the Editor UI and Script Canvas.

---

## What's Next?

Once you have this basic setup working:

1. **Import a car model** (replace the cube)
2. **Add better vehicle physics** (wheel colliders, suspension)
3. **Implement the full camera system** (banking, shake, combat awareness)
4. **Add arena boundaries and obstacles**
5. **Create weapon systems**

---

## Quick Reference

**Essential Keyboard Shortcuts:**
- `Ctrl + G` - Play/Stop game
- `W/A/S/D` - Move camera in editor
- `Right Mouse + Drag` - Rotate camera view
- `Middle Mouse + Drag` - Pan camera
- `Mouse Wheel` - Zoom in/out
- `Ctrl + Z` - Undo
- `Ctrl + S` - Save

**Essential Components:**
- **Transform** - Position, rotation, scale (every entity has this)
- **Mesh** - Visual appearance
- **Camera** - What the player sees
- **PhysX Rigid Body** - Dynamic physics (moves, falls)
- **PhysX Static Rigid Body** - Static physics (doesn't move)
- **PhysX Collider** - Defines collision shape
- **Script Canvas** - Visual scripting logic

---

## Need Help?

If you get stuck:
1. Check the Entity Outliner - is everything there?
2. Check the Inspector - do entities have the right components?
3. Check Transform values - are things positioned sensibly?
4. Try deleting everything and starting over (it's okay!)

You can do this! Start with Part 1 and work through step by step. Don't rush!