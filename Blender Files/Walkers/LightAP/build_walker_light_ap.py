"""Build the test light anti-personnel walker for Black Curtain.

A BT-5-inspired two-legged walker: a low riveted hull with a pointed nose and a
driver's hatch on the glacis, a cylindrical observation turret with a rear
bustle, twin headlights, and a shielded water-cooled machine gun in a sponson
on each side. Reverse-knee legs, rigid mechanical skinning (every part follows
exactly one bone) and a looping in-place walk cycle.

Conventions: meters, +X forward, +Y left, +Z up, origin on the ground between
the feet. Unreal gets +X forward after FBX export.

Usage (headless):
  blender --background --factory-startup --python build_walker_light_ap.py -- \
      --out <dir> [--stills <dir>] [--strip <dir>] [--export] [--blend]
"""
import argparse
import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

# --- Dimensions -------------------------------------------------------------
HIP_Z = 2.45      # hip axle height
HULL_Z = 2.30     # hull bottom
HULL_H = 0.90
LEG_Y = 1.12      # leg plane offset from the center line
THIGH = 1.35
SHIN = 1.35
ANKLE_Z = 0.24    # ankle height when the foot is on the ground

# --- Walk cycle -------------------------------------------------------------
FPS = 30
CYCLE = 36        # frames per full cycle (1.2 s)
DUTY = 0.55       # share of the cycle each foot is on the ground
STRIDE = 1.8      # foot travel during stance, meters
LIFT = 0.38       # swing height, meters
BOB = 0.04        # body bob, meters
ROLL = 1.5        # body roll, degrees
# Ground speed that keeps the feet from sliding, for the Unreal movement setup.
WALK_SPEED = STRIDE / (DUTY * CYCLE / FPS)

PALETTE = {
    "Hull": ("#4B5A32", 0.80, 0.0),
    "DarkMetal": ("#2B2B29", 0.60, 0.3),
    "Steel": ("#74746C", 0.45, 0.6),
    "Rust": ("#6B3A22", 0.90, 0.0),
    "Ammo": ("#4A4A2A", 0.85, 0.0),
    "Stripe": ("#E6E2D6", 0.80, 0.0),
    "Glass": ("#F4E7A8", 0.20, 0.0),
    "Ground": ("#8A8A84", 0.95, 0.0),
    "Figure": ("#B8B8B0", 0.90, 0.0),
}

MATS = {}
PARTS = []


def srgb_to_linear(hex_color):
    h = hex_color.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return out


def make_materials():
    for name, (hex_color, rough, metal) in PALETTE.items():
        m = bpy.data.materials.new("M_Walker_" + name)
        if m.node_tree is None:
            m.use_nodes = True
        rgb = srgb_to_linear(hex_color)
        m.diffuse_color = (*rgb, 1.0)
        bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Roughness"].default_value = rough
        bsdf.inputs["Metallic"].default_value = metal
        if name == "Glass":
            bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 2.0
        MATS[name] = m


# --- bmesh primitives ---------------------------------------------------------
AXIS_ROT = {
    "X": Matrix.Rotation(math.radians(90), 4, "Y"),
    "Y": Matrix.Rotation(math.radians(-90), 4, "X"),
    "Z": Matrix.Identity(4),
}


def bm_box(center, size, yaw=0.0, pitch=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size), verts=bm.verts)
    rot = Matrix.Rotation(math.radians(yaw), 4, "Z") @ Matrix.Rotation(math.radians(pitch), 4, "Y")
    bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector(center)) @ rot, verts=bm.verts)
    return bm


def bm_cyl(center, radius, depth, axis="Z", seg=12, radius2=None):
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=seg,
        radius1=radius, radius2=radius if radius2 is None else radius2, depth=depth,
        matrix=Matrix.Translation(Vector(center)) @ AXIS_ROT[axis])
    return bm


def bm_rod(a, b, radius, seg=8):
    a, b = Vector(a), Vector(b)
    d = b - a
    rot = d.normalized().to_track_quat("Z", "Y").to_matrix().to_4x4()
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=seg, radius1=radius, radius2=radius,
        depth=d.length, matrix=Matrix.Translation((a + b) / 2) @ rot)
    return bm


def bm_hull(points, bevel=0.0):
    bm = bmesh.new()
    for p in points:
        bm.verts.new(Vector(p))
    res = bmesh.ops.convex_hull(bm, input=bm.verts[:])
    bmesh.ops.delete(bm, geom=res["geom_interior"], context="VERTS")
    bmesh.ops.delete(bm, geom=[v for v in res["geom_unused"] if isinstance(v, bmesh.types.BMVert)], context="VERTS")
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(1.0), verts=bm.verts[:], edges=bm.edges[:])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    if bevel > 0:
        bmesh.ops.bevel(bm, geom=bm.edges[:], offset=bevel, segments=1, profile=0.5,
                        affect="EDGES", clamp_overlap=True)
    return bm


def bm_beam(a, b, w0, t0, w1=None, t1=None, bevel=0.015):
    """A tapered rectangular beam from a to b in the XZ plane; w is half-width in Y, t half-thickness."""
    a, b = Vector(a), Vector(b)
    d = (b - a).normalized()
    lat = Vector((0.0, 1.0, 0.0))
    n = lat.cross(d).normalized()
    w1 = w0 if w1 is None else w1
    t1 = t0 if t1 is None else t1
    pts = []
    for p, w, t in ((a, w0, t0), (b, w1, t1)):
        for sy in (-1, 1):
            for sn in (-1, 1):
                pts.append(p + lat * w * sy + n * t * sn)
    return bm_hull(pts, bevel)


def add_part(bm, bone, mat, name="part"):
    me = bpy.data.meshes.new(name)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(MATS[mat])
    vg = ob.vertex_groups.new(name=bone)
    vg.add(list(range(len(me.vertices))), 1.0, "REPLACE")
    PARTS.append(ob)
    return ob


# --- Leg geometry -------------------------------------------------------------
def solve_knee(hip, ankle):
    """Two-bone IK in the leg's XZ plane; the knee bends backward (reverse joint)."""
    dx, dz = ankle.x - hip.x, ankle.z - hip.z
    d = min(math.hypot(dx, dz), THIGH + SHIN - 1e-4)
    a1 = math.atan2(dz, dx)
    cos_a = (THIGH ** 2 + d ** 2 - SHIN ** 2) / (2 * THIGH * d)
    ang = a1 - math.acos(max(-1.0, min(1.0, cos_a)))
    return Vector((hip.x + THIGH * math.cos(ang), hip.y, hip.z + THIGH * math.sin(ang)))


def leg_points(side):
    hip = Vector((0.0, LEG_Y * side, HIP_Z))
    ankle = Vector((0.0, LEG_Y * side, ANKLE_Z))
    knee = solve_knee(hip, ankle)
    ankle = knee + (ankle - knee).normalized() * SHIN
    return hip, knee, ankle


def mg_pivot(side):
    return Vector((0.78, 0.98 * side, HULL_Z + 0.62))


# --- Model ---------------------------------------------------------------------
def build_body():
    z0 = HULL_Z
    top = z0 + HULL_H

    # Hull: long, low, riveted, with the BT's pointed nose.
    pts = []
    for s in (-1, 1):
        w = 0.85 * s
        pts += [(-1.35, w, z0 + 0.10), (-1.35, w, z0 + 0.80), (-1.22, w, z0), (-1.24, w, top),
                (0.55, w, z0), (0.55, w, top),
                (1.45, 0.38 * s, z0 + 0.22), (1.45, 0.38 * s, z0 + 0.45), (1.25, 0.38 * s, z0 + 0.04)]
    add_part(bm_hull(pts, bevel=0.03), "body", "Hull", "hull")

    # Driver's hatch on the glacis, with a vision slit.
    slope = math.degrees(math.atan2(0.45, 0.90))
    add_part(bm_box((0.80, 0.0, z0 + 0.80), (0.36, 0.46, 0.06), pitch=slope), "body", "Hull", "driver_hatch")
    add_part(bm_box((0.86, 0.0, z0 + 0.80), (0.05, 0.26, 0.03), pitch=slope), "body", "DarkMetal", "driver_slit")

    # Turret: BT-5-style cylinder with a rear bustle; observation only, no main gun.
    tz, th, tx = top, 0.42, -0.15
    pts = []
    for i in range(12):
        a = 2 * math.pi * i / 12
        pts.append((tx + 0.62 * math.cos(a), 0.62 * math.sin(a), tz))
        pts.append((tx + 0.56 * math.cos(a), 0.56 * math.sin(a), tz + th))
    pts += [(-1.0, s * 0.36, tz + 0.06) for s in (-1, 1)] + [(-1.0, s * 0.33, tz + 0.36) for s in (-1, 1)]
    add_part(bm_hull(pts, bevel=0.025), "body", "Hull", "turret")
    add_part(bm_cyl((tx, 0, tz + 0.025), 0.68, 0.05, seg=16), "body", "DarkMetal", "turret_ring")
    r_lo, r_hi = 0.62 - 0.06 * (0.17 / th), 0.62 - 0.06 * (0.23 / th)
    add_part(bm_cyl((tx, 0, tz + 0.20), r_lo + 0.008, 0.06, seg=12, radius2=r_hi + 0.008), "body", "Stripe", "turret_stripe")
    add_part(bm_cyl((tx + 0.08, 0.12, tz + th + 0.025), 0.24, 0.05, seg=12), "body", "Hull", "hatch")
    add_part(bm_box((tx - 0.15, 0.12, tz + th + 0.07), (0.05, 0.05, 0.05)), "body", "DarkMetal", "hatch_handle")
    add_part(bm_box((tx + 0.40, -0.22, tz + th + 0.06), (0.10, 0.12, 0.12)), "body", "DarkMetal", "periscope")
    for a in (-40, 0, 40):
        r = 0.62 - 0.06 * (0.25 / th)
        c = (tx + r * math.cos(math.radians(a)), r * math.sin(math.radians(a)), tz + 0.25)
        add_part(bm_box(c, (0.04, 0.16, 0.035), yaw=a), "body", "DarkMetal", "vision_slit")

    # Searchlight on the turret roof: this walker hunts infantry, day and night.
    add_part(bm_box((tx + 0.25, -0.30, tz + th + 0.06), (0.08, 0.08, 0.10)), "body", "DarkMetal", "searchlight_post")
    add_part(bm_cyl((tx + 0.28, -0.30, tz + th + 0.20), 0.10, 0.20, axis="X"), "body", "Hull", "searchlight")
    add_part(bm_cyl((tx + 0.385, -0.30, tz + th + 0.20), 0.085, 0.02, axis="X"), "body", "Glass", "searchlight_lens")

    # Twin headlights on brackets above the glacis.
    for s in (-1, 1):
        add_part(bm_box((1.08, 0.47 * s, z0 + 0.62), (0.06, 0.06, 0.14)), "body", "DarkMetal", "headlight_bracket")
        add_part(bm_cyl((1.12, 0.47 * s, z0 + 0.74), 0.11, 0.16, axis="X"), "body", "Hull", "headlight")
        add_part(bm_cyl((1.205, 0.47 * s, z0 + 0.74), 0.09, 0.02, axis="X"), "body", "Glass", "headlight_lens")

    # Machine-gun sponsons and ammo boxes.
    za, zb = z0 + 0.42, z0 + 0.82
    for s in (-1, 1):
        pts = []
        for z in (za, zb):
            pts += [(0.0, 0.84 * s, z), (0.0, 1.12 * s, z), (0.5, 1.12 * s, z), (0.72, 1.0 * s, z), (0.72, 0.84 * s, z)]
        add_part(bm_hull(pts, bevel=0.02), "body", "Hull", "sponson")
        p = mg_pivot(s)
        add_part(bm_cyl((p.x - 0.03, p.y, p.z), 0.14, 0.1, axis="X"), "body", "DarkMetal", "ball_mount")
        add_part(bm_box((0.25, 1.16 * s, p.z - 0.02), (0.30, 0.08, 0.18)), "body", "Ammo", "ammo_box")
        add_part(bm_box((0.25, 1.205 * s, p.z + 0.03), (0.12, 0.012, 0.03)), "body", "DarkMetal", "ammo_latch")

    # Engine deck: exhaust stacks, muffler and grille.
    add_part(bm_cyl((-1.41, 0, z0 + 0.48), 0.085, 0.95, axis="Y", seg=10), "body", "Rust", "muffler")
    for s in (-1, 1):
        add_part(bm_box((-1.39, 0.40 * s, z0 + 0.48), (0.10, 0.06, 0.20)), "body", "DarkMetal", "muffler_strap")
        add_part(bm_cyl((-1.25, 0.55 * s, top + 0.2), 0.075, 0.55, seg=10), "body", "Rust", "exhaust")
        add_part(bm_cyl((-1.25, 0.55 * s, top + 0.49), 0.10, 0.06, seg=10, radius2=0.085), "body", "DarkMetal", "exhaust_cap")
    for i in range(5):
        add_part(bm_box((-1.18 + 0.08 * i, 0, top + 0.015), (0.045, 0.9, 0.03)), "body", "DarkMetal", "grille")

    # Hip axle and housings.
    add_part(bm_cyl((0, 0, HIP_Z), 0.17, 2.0, axis="Y", seg=12), "body", "DarkMetal", "hip_axle")
    for s in (-1, 1):
        add_part(bm_cyl((0, 0.92 * s, HIP_Z), 0.27, 0.14, axis="Y", seg=14), "body", "Hull", "hip_housing")

    # Rivets along the hull sides and around the turret base.
    for s in (-1, 1):
        for zr in (z0 + 0.10, z0 + 0.80):
            for i in range(11):
                x = -1.25 + 0.175 * i
                add_part(bm_cyl((x, (0.85 + 0.01) * s, zr), 0.022, 0.03, axis="Y", seg=6), "body", "Hull", "rivet")
    for i in range(16):
        a = 2 * math.pi * i / 16
        if math.cos(a) < -0.8:
            continue  # hidden under the bustle
        c = (tx + 0.615 * math.cos(a), 0.615 * math.sin(a), tz + 0.07)
        bm = bm_cyl((0, 0, 0), 0.02, 0.03, axis="X", seg=6)
        bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector(c)) @ Matrix.Rotation(a, 4, "Z"), verts=bm.verts)
        add_part(bm, "body", "Hull", "rivet")


def build_mgs():
    for s, side in ((1, "l"), (-1, "r")):
        p = mg_pivot(s)
        bone = "mg_" + side
        add_part(bm_box((p.x + 0.08, p.y, p.z + 0.02), (0.04, 0.30, 0.26)), bone, "Hull", "mg_shield")
        add_part(bm_cyl((p.x + 0.36, p.y, p.z), 0.065, 0.55, axis="X", seg=10), bone, "DarkMetal", "mg_jacket")
        for dx in (0.14, 0.60):
            add_part(bm_cyl((p.x + dx, p.y, p.z), 0.076, 0.03, axis="X", seg=10), bone, "Steel", "mg_band")
        add_part(bm_cyl((p.x + 0.70, p.y, p.z), 0.03, 0.16, axis="X", seg=8), bone, "Steel", "mg_barrel")
        add_part(bm_cyl((p.x + 0.79, p.y, p.z), 0.045, 0.06, axis="X", seg=8, radius2=0.03), bone, "DarkMetal", "mg_muzzle")
        add_part(bm_box((p.x + 0.56, p.y, p.z + 0.09), (0.02, 0.012, 0.06)), bone, "DarkMetal", "mg_sight")
        add_part(bm_box((p.x - 0.10, p.y, p.z), (0.30, 0.12, 0.14)), bone, "DarkMetal", "mg_receiver")


def build_leg(side_sign, side):
    hip, knee, ankle = leg_points(side_sign)
    th, sh, ft = "thigh_" + side, "shin_" + side, "foot_" + side
    y = hip.y

    lat = Vector((0, 1, 0))
    add_part(bm_cyl(hip, 0.24, 0.34, axis="Y", seg=12), th, "DarkMetal", "hip_hub")
    add_part(bm_beam(hip, knee, 0.15, 0.21, 0.12, 0.15, bevel=0.025), th, "Hull", "thigh")
    d = (knee - hip).normalized()
    n = lat.cross(d).normalized()
    add_part(bm_rod(hip + d * 0.30 + n * 0.25, hip + d * 1.05 + n * 0.20, 0.055), th, "Steel", "thigh_ram")
    add_part(bm_beam(hip + d * 0.26 + n * 0.12, hip + d * 0.30 + n * 0.29, 0.05, 0.035), th, "DarkMetal", "ram_clamp")
    add_part(bm_beam(hip + d * 1.01 + n * 0.10, hip + d * 1.05 + n * 0.24, 0.05, 0.035), th, "DarkMetal", "ram_clamp")
    for t in (0.2, 0.45, 0.7):  # rivets down the outer face of the thigh
        c = hip + d * (THIGH * t) + lat * (0.155 if y > 0 else -0.155)
        add_part(bm_cyl(c, 0.022, 0.03, axis="Y", seg=6), th, "Hull", "rivet")

    add_part(bm_cyl(knee, 0.20, 0.36, axis="Y", seg=12), sh, "DarkMetal", "knee_hub")
    # Armored knee cap on the joint's rear point.
    u1, u2 = (hip - knee).normalized(), (ankle - knee).normalized()
    out = -(u1 + u2).normalized()
    tang = lat.cross(out).normalized()
    cap = knee + out * 0.16
    pts = [cap + out * so * 0.06 + tang * st * 0.22 + lat * sl * 0.19
           for so in (-1, 1) for st in (-1, 1) for sl in (-1, 1)]
    pts += [cap + out * 0.09 + lat * sl * 0.15 for sl in (-1, 1)]
    add_part(bm_hull(pts, bevel=0.02), sh, "Hull", "knee_cap")
    add_part(bm_beam(knee, ankle, 0.13, 0.17, 0.10, 0.12, bevel=0.025), sh, "Hull", "shin")
    d = (ankle - knee).normalized()
    n = lat.cross(d).normalized()
    add_part(bm_rod(knee + d * 0.32 - n * 0.21, knee + d * 1.10 - n * 0.17, 0.05), sh, "Steel", "shin_ram")
    add_part(bm_beam(knee + d * 0.30 - n * 0.10, knee + d * 0.34 - n * 0.25, 0.045, 0.035), sh, "DarkMetal", "ram_clamp")

    add_part(bm_cyl(ankle, 0.15, 0.30, axis="Y", seg=10), ft, "DarkMetal", "ankle_hub")
    ax = ankle.x
    pts = []
    for sy in (-1, 1):
        pts += [(ax - 0.48, y + 0.27 * sy, 0.0), (ax + 0.62, y + 0.27 * sy, 0.0),
                (ax - 0.48, y + 0.27 * sy, 0.07), (ax + 0.62, y + 0.27 * sy, 0.06),
                (ax - 0.36, y + 0.22 * sy, 0.16), (ax + 0.44, y + 0.22 * sy, 0.16)]
    add_part(bm_hull(pts, bevel=0.025), ft, "DarkMetal", "foot")
    for ty in (-0.14, 0.14):
        pts = []
        for sy in (-1, 1):
            pts += [(ax + 0.44, y + ty + 0.08 * sy, 0.0), (ax + 0.44, y + ty + 0.08 * sy, 0.11),
                    (ax + 0.80, y + ty + 0.05 * sy, 0.0), (ax + 0.80, y + ty + 0.05 * sy, 0.035)]
        add_part(bm_hull(pts, bevel=0.01), ft, "DarkMetal", "toe")
    for sy in (-1, 1):
        add_part(bm_box((ax, y + 0.17 * sy, 0.22), (0.28, 0.05, 0.20)), ft, "Hull", "ankle_bracket")


def join_parts():
    bpy.ops.object.select_all(action="DESELECT")
    for ob in PARTS:
        ob.select_set(True)
    bpy.context.view_layer.objects.active = PARTS[0]
    bpy.ops.object.join()
    mesh = bpy.context.view_layer.objects.active
    mesh.name = "SK_WalkerLightAP"
    mesh.data.name = "SK_WalkerLightAP"
    mesh.data.uv_layers.new(name="UVMap")
    # Every vertex must follow exactly one bone at full weight.
    names = {g.index: g.name for g in mesh.vertex_groups}
    for v in mesh.data.vertices:
        gs = [g for g in v.groups if g.weight > 0]
        assert len(gs) == 1 and abs(gs[0].weight - 1.0) < 1e-6, f"vertex {v.index} has groups {[names[g.group] for g in gs]}"
    return mesh


# --- Rig -----------------------------------------------------------------------
def build_armature():
    data = bpy.data.armatures.new("Armature")
    arm = bpy.data.objects.new("Armature", data)
    bpy.context.scene.collection.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    eb = data.edit_bones

    def bone(name, head, tail, parent=None, connect=False):
        b = eb.new(name)
        b.head, b.tail, b.roll = Vector(head), Vector(tail), 0.0
        if parent:
            b.parent = eb[parent]
            b.use_connect = connect

    bone("root", (0, 0, 0), (0, 0, 0.4))
    bone("body", (0, 0, HIP_Z), (0, 0, HIP_Z + 0.6), "root")
    for s, side in ((1, "l"), (-1, "r")):
        hip, knee, ankle = leg_points(s)
        bone("thigh_" + side, hip, knee, "body")
        bone("shin_" + side, knee, ankle, "thigh_" + side, connect=True)
        bone("foot_" + side, ankle, ankle + Vector((0.4, 0, 0)), "shin_" + side, connect=True)
        p = mg_pivot(s)
        bone("mg_" + side, p, p + Vector((0.35, 0, 0)), "body")
    bpy.ops.object.mode_set(mode="OBJECT")
    return arm


def skin(mesh, arm):
    mesh.parent = arm
    mod = mesh.modifiers.new("Armature", "ARMATURE")
    mod.object = arm


def foot_target(phase):
    """Ankle offset (x, z) from the hip line for a phase in [0, 1)."""
    if phase < DUTY:
        s = phase / DUTY
        return STRIDE / 2 - STRIDE * s, ANKLE_Z
    s = (phase - DUTY) / (1 - DUTY)
    smooth = s * s * (3 - 2 * s)
    return -STRIDE / 2 + STRIDE * smooth, ANKLE_Z + LIFT * math.sin(math.pi * s)


def animate(arm):
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 0, CYCLE
    pose = arm.pose
    for pb in pose.bones:
        pb.rotation_mode = "QUATERNION"
    rest = {b.name: b.matrix_local.copy() for b in arm.data.bones}
    prev = {}

    def set_matrix(name, m, frame):
        pb = pose.bones[name]
        pb.matrix = m
        bpy.context.view_layer.update()
        q = pb.rotation_quaternion.copy()
        if name in prev and prev[name].dot(q) < 0:
            pb.rotation_quaternion = -q
        prev[name] = pb.rotation_quaternion.copy()
        pb.keyframe_insert("rotation_quaternion", frame=frame)
        pb.keyframe_insert("location", frame=frame)

    def aim(name, head, tip, frame):
        r = rest[name]
        q = r.col[1].xyz.normalized().rotation_difference((tip - head).normalized())
        set_matrix(name, Matrix.Translation(head) @ (q.to_matrix() @ r.to_3x3()).to_4x4(), frame)

    for f in range(CYCLE + 1):
        p = (f % CYCLE) / CYCLE
        # Body: highest at each mid-stance, rolling slightly toward the planted leg.
        bob = BOB * math.cos(2 * math.pi * 2 * (p - DUTY / 2))
        roll = math.radians(ROLL) * math.cos(2 * math.pi * (p - DUTY / 2))
        head = rest["body"].translation
        m = (Matrix.Translation((0, 0, bob)) @ Matrix.Translation(head) @ Matrix.Rotation(roll, 4, "X")
             @ Matrix.Translation(-head) @ rest["body"])
        set_matrix("body", m, f)
        delta = pose.bones["body"].matrix @ rest["body"].inverted()
        for s, side, offset in ((1, "l", 0.0), (-1, "r", 0.5)):
            hip = delta @ rest["thigh_" + side].translation
            fx, fz = foot_target((p + offset) % 1.0)
            ankle = Vector((rest["thigh_" + side].translation.x + fx, LEG_Y * s, fz))
            knee = solve_knee(hip, ankle)
            aim("thigh_" + side, hip, knee, f)
            ankle_reached = knee + (ankle - knee).normalized() * SHIN
            aim("shin_" + side, knee, ankle_reached, f)
            set_matrix("foot_" + side, Matrix.Translation(ankle_reached) @ rest["foot_" + side].to_3x3().to_4x4(), f)
        for side in ("l", "r"):
            # Guns ride on the body: rest pose relative to the body, not to the rig.
            set_matrix("mg_" + side, delta @ rest["mg_" + side], f)
    arm.animation_data.action.name = "Walk"

    # Check: each gun keeps a fixed offset from the body on every frame.
    worst = 0.0
    base = None
    for f in range(CYCLE + 1):
        scene.frame_set(f)
        rel = pose.bones["body"].matrix.inverted() @ pose.bones["mg_l"].matrix
        if base is None:
            base = rel.copy()
        worst = max(worst, (rel.translation - base.translation).length)
    scene.frame_set(0)
    print(f"MGCHECK max gun drift relative to body = {worst * 1000:.2f} mm")
    assert worst < 1e-3, "guns drift relative to the body"


# --- Staging and rendering ------------------------------------------------------
def build_stage():
    scene = bpy.context.scene
    bm = bm_box((0, 0, -0.05), (80, 80, 0.1))
    me = bpy.data.meshes.new("ground")
    bm.to_mesh(me)
    bm.free()
    ground = bpy.data.objects.new("Ground", me)
    ground.data.materials.append(MATS["Ground"])
    scene.collection.objects.link(ground)

    # A 1.8 m person for scale.
    figure = []
    for bm, nm in ((bm_cyl((2.3, 1.9, 0.78), 0.22, 1.56, seg=12), "fig_body"),
                   (bm_cyl((2.3, 1.9, 1.68), 0.12, 0.24, seg=10), "fig_head")):
        me = bpy.data.meshes.new(nm)
        bm.to_mesh(me)
        bm.free()
        ob = bpy.data.objects.new(nm, me)
        ob.data.materials.append(MATS["Figure"])
        scene.collection.objects.link(ob)
        figure.append(ob)

    world = bpy.data.worlds.new("World")
    scene.world = world
    if world.node_tree is None:
        world.use_nodes = True
    bg = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
    bg.inputs["Color"].default_value = (*srgb_to_linear("#A9B4BE"), 1.0)
    bg.inputs["Strength"].default_value = 0.7

    for name, energy, rot, shadow in (("Sun", 3.2, (50, 0, 35), True), ("Fill", 0.6, (60, 0, 215), False)):
        ld = bpy.data.lights.new(name, "SUN")
        ld.energy = energy
        ld.angle = math.radians(2.0)
        ld.use_shadow = shadow
        lo = bpy.data.objects.new(name, ld)
        lo.rotation_euler = tuple(math.radians(a) for a in rot)
        scene.collection.objects.link(lo)
    return figure


def setup_render(res, samples=48):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    for dev_type in ("OPTIX", "CUDA"):
        try:
            prefs.compute_device_type = dev_type
            prefs.get_devices()
            if any(d.type == dev_type for d in prefs.devices):
                for d in prefs.devices:
                    d.use = d.type == dev_type
                scene.cycles.device = "GPU"
                break
        except Exception:
            continue
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"


def camera(loc, target, lens=45.0, ortho=None):
    cd = bpy.data.cameras.new("cam")
    if ortho:
        cd.type = "ORTHO"
        cd.ortho_scale = ortho
    else:
        cd.lens = lens
    co = bpy.data.objects.new("cam", cd)
    bpy.context.scene.collection.objects.link(co)
    co.location = loc
    co.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = co
    return co


def render(path):
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("RENDERED", path)


def render_stills(outdir, arm):
    os.makedirs(outdir, exist_ok=True)
    arm.data.pose_position = "REST"
    setup_render((1280, 720))
    shots = {
        "walker_front34": ((8.6, 6.4, 4.0), (0.3, 0.2, 2.0), 42),
        "walker_side": ((0.2, 13.0, 2.4), (0.2, 0.0, 2.0), 42),
        "walker_rear34": ((-8.2, -6.6, 4.6), (-0.2, 0.0, 2.2), 42),
        "walker_mg_closeup": ((3.4, 3.4, 3.5), (0.85, 1.0, 2.9), 50),
    }
    for name, (loc, target, lens) in shots.items():
        camera(loc, target, lens)
        render(os.path.join(outdir, name + ".png"))
    arm.data.pose_position = "POSE"


def render_strip(outdir, arm, figure):
    import numpy as np
    os.makedirs(outdir, exist_ok=True)
    for ob in figure:
        ob.hide_render = True
    arm.data.pose_position = "POSE"
    setup_render((640, 640), samples=32)
    camera((0.0, 14.0, 2.0), (0.0, 0.0, 2.0), ortho=5.6)
    frames = [0, CYCLE // 4, CYCLE // 2, 3 * CYCLE // 4]
    paths = []
    for f in frames:
        bpy.context.scene.frame_set(f)
        path = os.path.join(outdir, f"walk_f{f:02d}.png")
        render(path)
        paths.append(path)
    imgs = [bpy.data.images.load(p) for p in paths]
    w, h = imgs[0].size
    arrays = [np.array(im.pixels[:], dtype=np.float32).reshape(h, w, 4) for im in imgs]
    strip = np.concatenate(arrays, axis=1)
    out = bpy.data.images.new("strip", width=w * len(arrays), height=h, alpha=True)
    out.pixels.foreach_set(strip.ravel())
    out.filepath_raw = os.path.join(outdir, "walker_walk_strip.png")
    out.file_format = "PNG"
    out.save()
    print("RENDERED", out.filepath_raw)
    for ob in figure:
        ob.hide_render = False


def action_fcurves(action):
    try:
        return list(action.fcurves)  # legacy actions
    except AttributeError:
        out = []
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    out.extend(bag.fcurves)
        return out


def to_centimeters(arm, mesh):
    """Unreal reads raw FBX values as centimeters and ignores the unit tag, so bake x100 into the data.

    Scales the rig and mesh by 100 and applies it, then scales the location keys to match
    (rotations are unaffected by a uniform scale). Run after saving the .blend.
    """
    bpy.ops.object.select_all(action="DESELECT")
    arm.scale = (100.0, 100.0, 100.0)
    arm.select_set(True)
    mesh.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for fc in action_fcurves(arm.animation_data.action):
        if fc.data_path.endswith(".location"):
            for kp in fc.keyframe_points:
                kp.co.y *= 100.0
                kp.handle_left.y *= 100.0
                kp.handle_right.y *= 100.0
            fc.update()
    bpy.context.scene.unit_settings.scale_length = 0.01
    bpy.context.view_layer.update()
    height = max((mesh.matrix_world @ v.co).z for v in mesh.data.vertices)
    print(f"CM height={height:.1f}")


def export_fbx(path, arm, mesh):
    to_centimeters(arm, mesh)
    bpy.ops.object.select_all(action="DESELECT")
    arm.select_set(True)
    mesh.select_set(True)
    bpy.context.view_layer.objects.active = arm
    arm.data.pose_position = "POSE"
    bpy.ops.export_scene.fbx(
        filepath=path, use_selection=True, object_types={"ARMATURE", "MESH"},
        apply_scale_options="FBX_SCALE_ALL", global_scale=1.0, axis_forward="-Z", axis_up="Y",
        mesh_smooth_type="FACE", use_tspace=False,
        add_leaf_bones=False, armature_nodetype="NULL", use_armature_deform_only=False,
        bake_anim=True, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=False,
        bake_anim_use_all_actions=False, bake_anim_force_startend_keying=True,
        bake_anim_step=1.0, bake_anim_simplify_factor=0.0)
    print("EXPORTED", path)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--stills")
    ap.add_argument("--strip")
    ap.add_argument("--export", action="store_true")
    ap.add_argument("--blend", action="store_true")
    args = ap.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)

    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob)
    make_materials()
    build_body()
    build_mgs()
    build_leg(1, "l")
    build_leg(-1, "r")
    mesh = join_parts()
    arm = build_armature()
    skin(mesh, arm)
    animate(arm)
    figure = build_stage()

    tris = sum(len(p.vertices) - 2 for p in mesh.data.polygons)
    print(f"STATS tris={tris} verts={len(mesh.data.vertices)} materials={len(mesh.data.materials)} "
          f"bones={len(arm.data.bones)} walk_speed={WALK_SPEED:.2f} m/s")

    if args.stills:
        render_stills(args.stills, arm)
    if args.strip:
        render_strip(args.strip, arm, figure)
    if args.blend:  # saved in meters, before export converts the scene to centimeters
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(args.out, "WalkerLightAP.blend"))
        print("SAVED blend")
    if args.export:
        export_fbx(os.path.join(args.out, "SK_WalkerLightAP.fbx"), arm, mesh)


if __name__ == "__main__":
    main()
