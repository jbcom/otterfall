# Otter Pipeline Proof-of-Concept

## Authorization
**Date**: November 18, 2025  
**Approved By**: User  
**Scope**: Generate ONE otter model through complete Meshy pipeline as validation test

## Authorized Asset

**Species**: River Otter (player character)

**Pipeline Stages**:
1. Text-to-3D: Sculpture style base model in A-pose
2. Auto-rigging: Add skeleton for animations  
3. Animation: Apply creature animations from Meshy catalog
4. Retexture: Realistic fur texture

**Expected Outputs**:
- `client/public/models/otter/otter_text3d.glb` - Base sculpted model
- `client/public/models/otter/otter_rigged.glb` - Rigged model with skeleton
- `client/public/models/otter/otter_animated.glb` - Model with animations
- `client/public/models/otter/otter_final.glb` - Fully textured final asset

## Prompt Specification

From `client/src/ecs/data/predatorSpecies.ts`:

```typescript
meshyPrompt: 'sculpture style river otter standing upright on hind legs in A-pose, sleek furry mammal with long tail and webbed paws, clean geometry, no water'
meshyArtStyle: 'sculpture'
```

## Pipeline Execution Workflow

### Prerequisites
1. Meshy API key set in environment (`MESHY_API_KEY`)
2. Webhook receiver running (see below)
3. ngrok tunnel exposing webhook endpoint

### Step 1: Start Webhook Receiver

```bash
# Terminal 1: Start FastAPI webhook server
cd python
uv run python scripts/run_webhook_server.py

# Terminal 2: Expose with ngrok
ngrok http 8000
# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
```

### Step 2: Run Otter Pipeline

```bash
# Terminal 3: Execute pipeline with webhook URL
cd python
uv run python scripts/run_otter_pipeline.py \
  --callback-base-url https://abc123.ngrok.io
```

The script will:
1. Submit text-to-3D task with callback URL
2. Wait for webhook notification
3. Download GLB artifact
4. Submit rigging task
5. Wait for webhook
6. Submit animation task  
7. Wait for webhook
8. Submit retexture task
9. Wait for webhook
10. Download final GLB

### Step 3: Validate in glTF Viewer

```bash
# Open in Three.js editor or glTF viewer
open https://gltf-viewer.donmccurdy.com/
# Drag and drop: client/public/models/otter/otter_final.glb
```

## Validation Checklist

### Text-to-3D Model
- [ ] Otter is in A-pose (arms/legs extended)
- [ ] Standing upright on hind legs
- [ ] Visible features: tail, webbed paws, sleek body
- [ ] Clean geometry (no artifacts, holes)
- [ ] No water or environment elements

### Rigged Model
- [ ] Skeleton visible in viewer
- [ ] Joints positioned correctly (shoulders, hips, spine)
- [ ] Mesh deforms with bone rotations
- [ ] No mesh tearing or weight paint issues

### Animated Model
- [ ] Animations embedded in GLB
- [ ] At least one animation plays correctly
- [ ] Smooth transitions, no popping
- [ ] Character stays upright during animations

### Final Textured Model
- [ ] Realistic fur texture applied
- [ ] Proper UV mapping (no stretching)
- [ ] PBR materials (base color, roughness, normal map)
- [ ] Color matches species spec (brownish with white chest/throat)

## Quality Acceptance Criteria

**Geometry**:
- Polygon count: 5k-15k triangles (mobile-friendly)
- No degenerate faces or non-manifold edges
- Proper normals (no inverted faces)

**Rigging**:
- Minimum 15 bones (spine, limbs, tail)
- Weight painting allows full range of motion
- Root bone at ground level

**Textures**:
- Resolution: 1024x1024 or 2048x2048
- Format: PNG or JPEG for diffuse, PNG for normal/roughness
- PBR workflow (metallic-roughness)

**File Size**:
- Final GLB < 10MB (ideally < 5MB for web)

## Pipeline Execution Log

### Run Date: _____________

**Text-to-3D**:
- Task ID: ________________
- Status: ⬜ PENDING ⬜ SUCCEEDED ⬜ FAILED
- Duration: _____ minutes
- GLB URL: ________________
- Notes: ____________________________________

**Rigging**:
- Task ID: ________________
- Status: ⬜ PENDING ⬜ SUCCEEDED ⬜ FAILED  
- Duration: _____ minutes
- GLB URL: ________________
- Notes: ____________________________________

**Animation**:
- Task ID: ________________
- Status: ⬜ PENDING ⬜ SUCCEEDED ⬜ FAILED
- Duration: _____ minutes
- Selected Animations: ____________________________________
- GLB URL: ________________
- Notes: ____________________________________

**Retexture**:
- Task ID: ________________
- Status: ⬜ PENDING ⬜ SUCCEEDED ⬜ FAILED
- Duration: _____ minutes
- Texture Prompt: "realistic river otter fur, brown with white chest"
- GLB URL: ________________
- Notes: ____________________________________

## glTF Validation Results

**Viewer**: ⬜ Three.js Editor ⬜ glTF Viewer ⬜ Blender ⬜ Other: __________

**Visual Quality**: ⬜ Excellent ⬜ Good ⬜ Acceptable ⬜ Needs Revision

**Issues Found**:
- ____________________________________
- ____________________________________
- ____________________________________

**Prompt Engineering Feedback**:
- ____________________________________
- ____________________________________
- ____________________________________

## Next Steps After Validation

If PoC succeeds:
- [ ] Document successful prompts and settings
- [ ] Create batch generation script for remaining species
- [ ] Define quality standards for full catalog

If PoC fails:
- [ ] Identify failure point (text3d, rigging, animation, retexture)
- [ ] Iterate on prompts/parameters
- [ ] Re-run failed stage only

## Archived Artifacts

- Webhook logs: `python/tests/integration/cassettes/webhooks/otter_poc/`
- Downloaded GLBs: `client/public/models/otter/`
- Manifest: `python/.mesh_toolkit_data/otter/manifest.json`
