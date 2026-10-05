#!/usr/bin/env python3
"""COLD STORAGE director: drives a local ComfyUI to render a microdrama episode.

Standard library only. Run it with ComfyUI's own venv python:
    C:\\AI\\ComfyUI\\venv\\Scripts\\python.exe cs_director.py <command> ...

Commands
    lint     <episode.json>                    Hook gate, 90 s runtime, shot length, dialogue timing, no-text and
                                               transition rules. Run first; it must PASS.
    inspect  <workflow_api.json>               List nodes and suggest a slot map for config.json.
    prompts  <episode.json>                    Print the final injected prompt for every shot.
    run      <episode.json> [--only C01,C02] [--takes 3] [--take-start 1] [--dry-run]
                                               Queue every shot, in dependency order, grouped by model.
    qa       <episode.json>                    Contact sheets (cast photo | first | middle | last frame) for every take
                                               plus a QA report to fill in. Nothing ships without it.
    sfxbed   <episode.json>                    Place every sound effect cue on one timeline WAV (sfx_bed).
    musicbed <episode.json>                    Place every music cue at its shot, trimmed with a short fade (music_bed).
    assemble <episode.json> [--takes-pick picks.json]
                                               Normalize clips, seamless continuation joins, 0.5 s dissolve into the
                                               end card, mix dialogue + SFX + music, -14 LUFS. 720 x 1280 master.

Standing rules (v3): every episode is about 90 s total including the end card (12 to 15 shots of 6 to 8 s,
never under 5 s). Dialogue voices are generated inside the LTX-2.3 render (W4 / C02 idlora_23 method), never
from TTS line WAVs. No audio or video speed changes. No generated on-screen text. Phones show backs only.
Upscale to 1080 x 1920 with SeedVR2 only after every episode is finished.
Camera (v4): every shot names a lens and an angle on the 9:16 rules (SKILL.md 5D); lint checks them.

Everything an episode needs (images, voices, music) lives under the project root
named in config.json ("project_root"), with episode paths relative to it.
"""
import argparse
import copy
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOOK_TYPES = {"status_violation", "identity_reveal", "time_pressure", "unanswered_question"}

# v3 timing rules (David, 2026-10-03 20:29 CT)
RUNTIME_TARGET_S = 90.0      # whole episode, end card included
RUNTIME_WARN_S = 2.0         # lint warns outside 88 to 92 s
RUNTIME_FAIL_S = 6.0         # lint fails outside 84 to 96 s (trims in the cut take a little off the plan)
SHOT_MIN_S = 5.0             # every edited shot (a clip plus its continuations) is at least 5 s
SHOT_TYPICAL_S = (6.0, 8.0)  # typical shot length
SHOTS_PER_EP = (12, 15)      # about 90 s / 6 to 8 s
WPS_RANGE = (2.5, 3.5)       # natural speech pace, words per second
LEAD_IN_MAX_S = 0.5          # silence before the first word
TAIL_MIN_S = 0.3             # after the last word, before any cut (hard floor)
REACTION_S = (1.0, 2.0)      # held reaction after the last word (target)

# 9:16 camera rules (v4, SKILL.md 5D). The keyframe bakes in lens and angle; the video model inherits them.
LENS_RANGE_MM = (24, 135)    # under 24 mm warps faces and lines in a tall frame; AI video turns it to chaos
TALK_LENS_MM = (50, 100)     # talking: 50 to 65 medium close up default, 85 close up for the line that lands
ANGLES = ("eye level", "chest height", "shoulder height", "low", "high", "overhead", "top down", "ground level",
          "over the shoulder", "pov", "dutch")
LATERAL_MOVES = ("pan left", "pan right", "pans left", "pans right", "truck left", "truck right", "tracks left",
                 "tracks right", "lateral tracking", "crab ")
BANNED_EDIT = ["speed ramp", "ramp to", "retime", "slow down", "speed up", "freeze the", "freeze frame",
               "freeze on", "to black", "cut on the black", "smash", "flash", "slate", "snap zoom", "whip"]
TEXT_WORDS = ["sign", "screen", "monitor", "document", "deed", "letter", "label", "name tag", "nametag",
              "caption", "headline", "newspaper", "led wall", "billboard", "menu", "text", "words", "writing"]
TEXT_SAFE = ["blurred", "unreadable", "out of focus", "out of frame", "back of", "backs", "blank", "no text",
             "no readable", "face down", "turned away"]
SLOT_NAMES = ["positive", "negative", "start_image", "end_image", "face_ref", "voice_ref",
              "seed", "frames", "width", "height", "fps", "filename_prefix", "img_strength", "img_compression"]

# ---------------------------------------------------------------- realism template

REALISM_PREFIX = (
    "Photorealistic live action vertical drama, indistinguishable from real footage of real people, "
    "shot on ARRI Alexa 35 with Cooke anamorphic lenses, 24fps film motion blur, shallow depth of field, "
    "practical motivated light, subtle handheld drift."
)
NO_TEXT = (
    "No readable text anywhere in frame: any sign, screen, document or label is blank, blurred or out of frame. "
    "Phones are seen only from the back."
)
CONTINUOUS = (
    "One continuous real-time shot at natural speed, continuous natural motion from the first frame to the last, "
    "never pauses, stalls or freezes, no slow motion."
)
REALISM_SKIN = (
    "True-to-life skin with visible pores, fine lines, subtle freckles and tiny imperfections, "
    "natural skin texture with real subsurface scattering, subtle facial asymmetry, flyaway hairs, "
    "real fabric creases. Natural blinking, breathing and micro-expressions. Natural muted color, true skin tones."
)
NEGATIVE = (
    "plastic skin, waxy skin, airbrushed, smooth skin, beauty filter, porcelain skin, doll face, CGI, 3D render, "
    "video game, cartoon, anime, illustration, oversaturated, HDR, glossy, morphing face, changing face, identity drift, "
    "wide open mouth, exaggerated expression, distorted teeth, extra fingers, extra limbs, distorted hands, "
    "frozen background people, flicker, warping, jitter, text, readable text, letters, signage, subtitles, captions, "
    "watermark, logo, phone screen, lit phone screen, cut, jump cut, flash, fade to black, slow motion, frozen face, "
    "static face, blank stare, mouthing silently"
)


def camera_text(ep, shot):
    """Lens and angle words for the prompt. Off by default: the keyframe already carries lens and angle, and the
    approved W4 / C02 prompt shape only changes after David's side-by-side (SKILL.md section 0). Turn it on with
    "camera_in_prompt": true at the top of the episode JSON (silent 2.5 shots only, never dialogue)."""
    if not ep.get("camera_in_prompt") or shot.get("line") or not (shot.get("lens") or shot.get("angle")):
        return ""
    bits = [f"{str(shot['lens']).rstrip('m')}mm lens" if shot.get("lens") else "", shot.get("angle", "")]
    return "Camera: " + ", ".join(b for b in bits if b) + ", the framing of the first frame holds."


def build_prompt(ep, shot):
    """Movie Builder style [VISUAL] [SPEECH] [SOUNDS] prompt with the realism template injected."""
    chars = ep["characters"]
    who = []
    # With a face reference (ID-LoRA) the reference carries identity, so keep text vague (Movie Builder rule).
    use_identity = not (shot["pipeline"].startswith("idlora") or shot["pipeline"] == "ia2v_23")
    for c in shot.get("cast", []) if use_identity else []:
        if c in chars:
            who.append(f"{c.split('_')[0].title()} is {chars[c]['identity']}.")
    line = shot.get("line")
    acting, delivery = shot.get("acting", ""), ""
    if "Delivery:" in acting:
        acting, delivery = (x.strip() for x in acting.split("Delivery:", 1))
    talk = ""
    if line:
        # W4 / C02 dialogue wording; the acting beats replace the single emotion adjective.
        talk = " ".join(x for x in [
            "The speaker starts talking within half a second, saying the line clearly at a natural conversational pace:",
            "lips and jaw move with every word, natural talking head movement, subtle head nods, eyebrow raises on key "
            "words, natural blinks between phrases.",
            acting,
            "Locked off camera, no zoom, framing stays exactly as in the first frame, one continuous shot.",
        ] if x)
    visual = " ".join(x for x in [
        REALISM_PREFIX,
        f"Shot: {shot.get('shot', '')}." if shot.get("shot") else "",
        camera_text(ep, shot),
        " ".join(who),
        shot["visual"],
        talk,
        f"Lighting: {shot['light']}." if shot.get("light") else "",
        CONTINUOUS if not shot.get("line") else "",
        NO_TEXT,
        REALISM_SKIN,
    ] if x)
    speech = f'"{line}"' if line else "none"
    sounds = shot.get("sounds", "natural room tone")
    if delivery:
        sounds = f"{delivery.rstrip('.')}, {sounds}"
    if line and shot.get("speaker"):
        sounds = f"{shot['speaker'].split('_')[0].title()} speaks: {sounds}"
    return f"[VISUAL] {visual}\n[SPEECH] {speech}\n[SOUNDS] {sounds}"


# ---------------------------------------------------------------- lint / hook gate

def chain_src(s):
    """'chain:C05' or 'chain:C05@89' -> ('C05', 89 or None)."""
    si = s.get("start_image", "")
    if not si.startswith("chain:"):
        return None, None
    ref = si.split(":", 1)[1]
    if "@" in ref:
        sid, fr = ref.split("@", 1)
        return sid, int(fr)
    return ref, None


def edit_shots(ep):
    """Group each clip with the continuation clips that follow it: one group = one edited shot on screen."""
    groups = []
    for s in ep["shots"]:
        src, _ = chain_src(s)
        if groups and s.get("continuation") and (src is None or src == groups[-1][-1]["id"]):
            groups[-1].append(s)
        else:
            groups.append([s])
    return groups


def line_frames(words, fps=24):
    """Suggested 8n+1 frame count for a talking clip, sized from the natural line plus handles (W4 table:
    up to 6 words 97 f, 7 to 10 words 105 f, 11 to 14 words 121 f). The held reaction can continue in a
    chained continuation clip; never squeeze a line into fewer frames."""
    f = 97 if words <= 6 else 105 if words <= 10 else 121
    need = LEAD_IN_MAX_S + words / 3.0 + TAIL_MIN_S
    while f / fps < need:
        f += 8
    return f


def lint(ep):
    errs, warns = [], []
    fps = ep.get("fps", 24)
    hook = ep.get("hook", {})
    if hook.get("type") not in HOOK_TYPES:
        errs.append(f"HOOK GATE: hook.type must be one of {sorted(HOOK_TYPES)}, got {hook.get('type')!r}")
    if float(hook.get("first_beat_s", 99)) > 1.0:
        errs.append("HOOK GATE: first beat must land by 1.0 s")
    if not hook.get("caption"):
        warns.append("HOOK GATE: no hook caption for seconds 1 to 3")
    ids = [s["id"] for s in ep["shots"]]
    if len(ids) != len(set(ids)):
        errs.append("duplicate shot ids")
    total = 0.0
    for i, s in enumerate(ep["shots"]):
        f = int(s["frames"])
        total += f / fps
        if (f - 1) % 8:
            errs.append(f"{s['id']}: frames {f} is not 8n+1 (try {((f - 1) // 8) * 8 + 1})")
        if f / fps > 8.05:
            warns.append(f"{s['id']}: {f / fps:.1f} s is over 8 s, faces drift on long clips; continue it in a chained clip")
        if s["pipeline"] not in ("i2v_25", "flf_25", "idlora_23", "ia2v_23", "lipsync_25") and not s["pipeline"].startswith("idlora"):
            errs.append(f"{s['id']}: unknown pipeline {s['pipeline']}")
        if s["pipeline"] == "flf_25" and not s.get("end_image"):
            errs.append(f"{s['id']}: flf_25 needs end_image")
        src, _ = chain_src(s)
        if src and src not in ids[:i]:
            errs.append(f"{s['id']}: chains from {src}, which isn't an earlier shot")
        if s.get("line_audio"):
            errs.append(f"{s['id']}: line_audio is not allowed. Voices are generated inside the LTX-2.3 render "
                        "(W4 / C02 method); no TTS line WAVs or lock takes as driving audio")
        if s.get("line"):
            words = len(re.findall(r"[\w']+", s["line"]))
            secs = f / fps
            if words > 12:
                errs.append(f"{s['id']}: line is {words} words, lip sync max is 12")
            hard = LEAD_IN_MAX_S + words / 3.0 + TAIL_MIN_S
            soft = LEAD_IN_MAX_S + words / WPS_RANGE[0] + REACTION_S[0]
            nxt = ep["shots"][i + 1] if i + 1 < len(ep["shots"]) else None
            continued = bool(nxt and nxt.get("continuation") and chain_src(nxt)[0] in (s["id"], None))
            if secs < hard:
                errs.append(f"{s['id']}: {words} words can't play in full in {secs:.1f} s at a natural pace "
                            f"(needs {hard:.1f} s: lead-in, speech at 3 w/s, 0.3 s tail). Use {line_frames(words, fps)} f. "
                            "Never force a line into fewer frames or speed it up")
            elif secs < soft and not continued:
                warns.append(f"{s['id']}: {secs:.1f} s leaves no room for the held 1 to 2 s reaction after the last word; "
                             f"use {line_frames(words, fps)} f plus a chained continuation clip")
            if not s.get("acting"):
                warns.append(f"{s['id']}: no 'acting' direction (2 to 3 physical beats tied to words plus delivery)")
            if not s.get("speaker"):
                errs.append(f"{s['id']}: has a line but no speaker")
            elif s["speaker"] not in ep["characters"]:
                errs.append(f"{s['id']}: speaker {s['speaker']} isn't in characters")
            if s["pipeline"] in ("i2v_25", "flf_25"):
                errs.append(f"{s['id']}: dialogue on a 2.5 pipeline. Lines render on idlora_23 (W4 / C02 method)")
            if s["pipeline"] == "lipsync_25":
                errs.append(f"{s['id']}: lipsync_25 needs pre-rendered audio; not allowed for dialogue (W4 rule)")
        lens = s.get("lens")
        if lens is None and not s.get("continuation"):
            warns.append(f"{s['id']}: no 'lens' (mm). Pick it from the 9:16 lens ladder (50 to 65 talking medium close up, "
                         "85 close up for the line that lands, 50 medium or stacked two shot, 35 walk and talk, 24 to 28 overhead or vertical architecture)")
        elif lens is not None:
            mm = int(re.sub(r"\D", "", str(lens)) or 0)
            if not LENS_RANGE_MM[0] <= mm <= LENS_RANGE_MM[1]:
                warns.append(f"{s['id']}: {mm} mm is outside {LENS_RANGE_MM[0]} to {LENS_RANGE_MM[1]} mm for 9:16")
            if s.get("line") and not TALK_LENS_MM[0] <= mm <= TALK_LENS_MM[1]:
                warns.append(f"{s['id']}: talking shot on {mm} mm; lines play on {TALK_LENS_MM[0]} to "
                             f"{TALK_LENS_MM[1]} mm (50 to 65 medium close up default, 85 for the line that lands)")
        angle = str(s.get("angle", "")).lower()
        if angle and not any(a in angle for a in ANGLES):
            warns.append(f"{s['id']}: angle {angle!r} isn't on the angle list {ANGLES}")
        if s.get("line") and any(a in angle for a in ("overhead", "top down", "ground level")):
            warns.append(f"{s['id']}: a line from {angle}; talking shots sit at eye or chest height (low or high a few degrees)")
        mv = (s.get("visual", "") + " " + s.get("shot", "")).lower()
        if any(m in mv for m in LATERAL_MOVES):
            warns.append(f"{s['id']}: lateral move in a 9:16 frame; move on the depth axis (push in, pull back) "
                         "or tilt instead, and keep one move per shot")
        for c in s.get("cast", []):
            if c not in ep["characters"]:
                errs.append(f"{s['id']}: cast member {c} isn't in characters")
        text = json.dumps(s, ensure_ascii=False)
        if "\u2014" in text or "\u2013" in text:
            errs.append(f"{s['id']}: contains an em or en dash")
        edit = " ".join(str(s.get(k, "")) for k in ("out", "edit", "transition")).lower()
        for b in BANNED_EDIT:
            if b in edit:
                errs.append(f"{s['id']}: '{b}' in out/edit. No speed changes, freezes, flash cuts, cuts to black, "
                            "slates or snap zooms; use a clean cut on motion or sound, or a dissolve")
                break
        vis = (s.get("visual", "") + " " + s.get("light", "")).lower()
        if "snap zoom" in vis or "flash" in vis or "slow motion" in vis.replace("no slow motion", ""):
            errs.append(f"{s['id']}: snap zoom, flash or slow motion in the visual; render at natural speed")
        if "phone" in vis and not any(w in vis for w in ("back of", "backs", "from the back", "phone back", "face down")):
            warns.append(f"{s['id']}: mentions a phone; phones show their backs only, never a screen")
        hits = [w for w in TEXT_WORDS if re.search(rf"\b{re.escape(w)}", vis)]
        if hits and not any(w in vis for w in TEXT_SAFE):
            warns.append(f"{s['id']}: mentions {', '.join(hits)}; no readable text in any rendered shot. Stage it blank, "
                         "blurred, from the back or out of frame; add real text in the edit as an overlay")
    groups = edit_shots(ep)
    for g in groups:
        secs = sum(int(x["frames"]) for x in g) / fps
        name = "+".join(x["id"] for x in g)
        if secs < SHOT_MIN_S - 0.05:
            errs.append(f"{name}: edited shot is {secs:.1f} s; every shot is at least {SHOT_MIN_S:.0f} s "
                        "(typically 6 to 8). Extend with a chained continuation or merge it, never by holding frames")
    n = len(groups)
    if not SHOTS_PER_EP[0] <= n <= SHOTS_PER_EP[1]:
        warns.append(f"{n} edited shots; a 90 s episode is usually {SHOTS_PER_EP[0]} to {SHOTS_PER_EP[1]} shots of 6 to 8 s")
    target = float(ep.get("runtime_target_s", RUNTIME_TARGET_S))
    runtime = total + float(ep.get("end_card_s", 0))
    if abs(runtime - target) > RUNTIME_FAIL_S:
        errs.append(f"RUNTIME: {runtime:.1f} s planned (shots {total:.1f} s + end card); every episode is about {target:.0f} s total")
    elif abs(runtime - target) > RUNTIME_WARN_S:
        warns.append(f"RUNTIME: {runtime:.1f} s planned; aim for {target:.0f} s total including the end card")
    for m in ep.get("music_cues", []):
        if m.get("from_shot") not in ids:
            errs.append(f"music cue {m.get('id')}: unknown shot {m.get('from_shot')}")
    for c in ep.get("sfx_cues", []):
        if c.get("shot") not in ids:
            errs.append(f"sfx cue {c.get('file')}: unknown shot {c.get('shot')}")
    if ep["shots"] and ep["shots"][0].get("line") is None and not ep["shots"][0].get("visual"):
        errs.append("HOOK GATE: first shot has no visual")
    return errs, warns, total


# ---------------------------------------------------------------- ComfyUI client

class Comfy:
    def __init__(self, url):
        self.url = url.rstrip("/")
        self.client_id = str(uuid.uuid4())

    def _req(self, path, data=None, headers=None, timeout=60, retries=6):
        """One persistent keep-alive connection (no new socket per poll), retry with backoff."""
        import http.client
        u = urllib.parse.urlparse(self.url)
        delay = 2
        for attempt in range(retries):
            try:
                if getattr(self, "_conn", None) is None:
                    self._conn = http.client.HTTPConnection(u.hostname, u.port or 80, timeout=timeout)
                self._conn.timeout = timeout
                if self._conn.sock is not None:
                    self._conn.sock.settimeout(timeout)
                self._conn.request("POST" if data is not None else "GET", path, body=data,
                                   headers=dict(headers or {}, Connection="keep-alive"))
                r = self._conn.getresponse()
                body = r.read()
                if r.getheader("Connection", "").lower() == "close":
                    self._close()
                if r.status >= 400:
                    raise urllib.error.HTTPError(self.url + path, r.status, body[:300].decode("utf-8", "replace"), r.headers, None)
                return body
            except urllib.error.HTTPError:
                raise
            except (OSError, http.client.HTTPException) as e:
                self._close()
                if attempt == retries - 1:
                    raise
                print(f"  (connection problem: {e}; retrying in {delay}s)", flush=True)
                time.sleep(delay)
                delay = min(delay * 2, 30)

    def _close(self):
        try:
            if getattr(self, "_conn", None) is not None:
                self._conn.close()
        finally:
            self._conn = None

    def ping(self):
        return json.loads(self._req("/system_stats"))

    def upload(self, path, subfolder="cold_storage"):
        """Upload an image or audio file into ComfyUI's input folder. Returns the name LoadImage/LoadAudio expect."""
        path = Path(path)
        boundary = uuid.uuid4().hex
        parts = []
        for name, value in (("subfolder", subfolder), ("type", "input"), ("overwrite", "true")):
            parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
        parts.append((f'--{boundary}\r\nContent-Disposition: form-data; name="image"; filename="{path.name}"\r\n'
                      f"Content-Type: application/octet-stream\r\n\r\n").encode() + path.read_bytes() + b"\r\n")
        parts.append(f"--{boundary}--\r\n".encode())
        res = json.loads(self._req("/upload/image", b"".join(parts),
                                   {"Content-Type": f"multipart/form-data; boundary={boundary}"}, timeout=300))
        return f"{res['subfolder']}/{res['name']}" if res.get("subfolder") else res["name"]

    def queue(self, workflow):
        body = json.dumps({"prompt": workflow, "client_id": self.client_id, "front": bool(os.environ.get("CS_FRONT"))}).encode()
        res = json.loads(self._req("/prompt", body, {"Content-Type": "application/json"}))
        if res.get("node_errors"):
            raise RuntimeError(f"ComfyUI rejected the workflow: {json.dumps(res['node_errors'])[:800]}")
        return res["prompt_id"]

    def wait(self, prompt_id, poll=5, timeout=3 * 3600):
        start = time.time()
        while time.time() - start < timeout:
            hist = json.loads(self._req(f"/history/{prompt_id}"))
            if prompt_id in hist:
                item = hist[prompt_id]
                status = item.get("status", {})
                if status.get("status_str") == "error":
                    msgs = [m for m in status.get("messages", []) if m[0] == "execution_error"]
                    raise RuntimeError(f"render failed: {json.dumps(msgs)[:800]}")
                if status.get("completed", True):
                    return item.get("outputs", {})
            time.sleep(poll)
            poll = min(poll * 1.5, 15)  # back off while a long render runs
        raise TimeoutError(prompt_id)

    def download_outputs(self, outputs, dest_dir, stem):
        """Save every file a finished prompt produced. Returns saved paths, videos first."""
        dest_dir.mkdir(parents=True, exist_ok=True)
        saved = []
        for node_out in outputs.values():
            for key, items in node_out.items():
                if not isinstance(items, list):
                    continue
                for it in items:
                    if not isinstance(it, dict) or "filename" not in it:
                        continue
                    q = urllib.parse.urlencode({"filename": it["filename"], "subfolder": it.get("subfolder", ""),
                                                "type": it.get("type", "output")})
                    data = self._req(f"/view?{q}", timeout=600)
                    ext = Path(it["filename"]).suffix
                    out = dest_dir / f"{stem}{'' if not saved else '_' + str(len(saved))}{ext}"
                    out.write_bytes(data)
                    saved.append(out)
        saved.sort(key=lambda p: p.suffix.lower() not in (".mp4", ".webm", ".mov", ".mkv"))
        return saved


# ---------------------------------------------------------------- workflow templates

def load_config():
    cfg_path = HERE / "config.json"
    if not cfg_path.exists():
        sys.exit("config.json not found next to cs_director.py. Copy config.example.json to config.json and fill it in.")
    return json.loads(cfg_path.read_text(encoding="utf-8"))


def patch(workflow, slot_map, slot, value):
    """Write value into every [node_id, input_name] mapped to slot. Missing slots are skipped."""
    targets = slot_map.get(slot) or []
    if targets and isinstance(targets[0], str):
        targets = [targets]
    for node_id, inp in targets:
        node = workflow.get(str(node_id))
        if node is None:
            raise KeyError(f"slot {slot}: node {node_id} isn't in the workflow (re-run inspect)")
        node["inputs"][inp] = value
    return bool(targets)


SLOT_HINTS = [
    ("seed", lambda ct, k: k in ("seed", "noise_seed")),
    ("frames", lambda ct, k: k in ("length", "num_frames", "frames", "frame_count")),
    ("width", lambda ct, k: k == "width"),
    ("height", lambda ct, k: k == "height"),
    ("fps", lambda ct, k: k in ("frame_rate", "fps")),
    ("filename_prefix", lambda ct, k: k == "filename_prefix"),
    ("img_strength", lambda ct, k: "ImgToVideo" in ct and k == "strength"),
    ("img_compression", lambda ct, k: "Preprocess" in ct and k == "img_compression"),
]


def inspect(path):
    wf = json.loads(Path(path).read_text(encoding="utf-8"))
    if "nodes" in wf and "links" in wf:
        sys.exit("That's a UI-format workflow. In ComfyUI: Workflow > Export (API), then inspect that file.")
    suggest = {s: [] for s in SLOT_NAMES}
    print(f"\n{path}: {len(wf)} nodes\n")
    for nid, node in sorted(wf.items(), key=lambda kv: int(kv[0]) if kv[0].isdigit() else 0):
        ct = node.get("class_type", "?")
        title = node.get("_meta", {}).get("title", "")
        scalar = {k: v for k, v in node.get("inputs", {}).items() if not isinstance(v, list)}
        print(f"  [{nid}] {ct}  {('(' + title + ')') if title else ''}")
        for k, v in scalar.items():
            sv = str(v)
            print(f"        {k} = {sv[:70] + '...' if len(sv) > 70 else sv}")
        tl = title.lower()
        for k in scalar:
            if ct.startswith("LoadImage") and k == "image":
                slot = ("end_image" if any(w in tl for w in ("end", "last")) else
                        "face_ref" if any(w in tl for w in ("face", "ref", "protagonist", "identity")) else "start_image")
                suggest[slot].append([nid, k])
            elif "LoadAudio" in ct and k in ("audio", "audio_file", "file"):
                suggest["voice_ref"].append([nid, k])
            elif k in ("text", "prompt") and isinstance(scalar[k], str):
                slot = "negative" if any(w in tl for w in ("neg",)) or "worst" in scalar[k].lower() or "blurry" in scalar[k].lower() else "positive"
                suggest[slot].append([nid, k])
            else:
                for slot, test in SLOT_HINTS:
                    if test(ct, k):
                        suggest[slot].append([nid, k])
    print("\nSuggested slot map (check it, then paste into config.json under this pipeline's \"slots\"):\n")
    found = {k: v for k, v in suggest.items() if v}
    print("{\n" + ",\n".join(f'  "{k}": {json.dumps(v)}' for k, v in found.items()) + "\n}")
    multi = [k for k, v in suggest.items() if len(v) > 1 and k not in ("seed",)]
    if multi:
        print(f"\nCheck these by hand, more than one node matched: {', '.join(multi)}")
        print("Two seeds is normal for two-stage LTX workflows. Keep both; the director offsets stage 2.")


# ---------------------------------------------------------------- run

def resolve(root, rel):
    p = Path(rel)
    return p if p.is_absolute() else root / p


def last_frame(video, out_png):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.5", "-i", str(video),
                    "-update", "1", "-q:v", "1", str(out_png)], check=True)
    return out_png


def chain_seed_index(video, explicit, tail_trim):
    """Frame a continuation starts from: the explicit @frame, else the near-rest frame tail_trim frames before
    the end (LTX decelerates in the last frames). assemble joins at this same frame."""
    if explicit is not None:
        return explicit
    return max(frame_count(video) - 1 - tail_trim, 0)


def frame_png(video, idx, out_png):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-vf", f"select=eq(n\\,{idx})",
                    "-vsync", "0", "-frames:v", "1", "-q:v", "1", str(out_png)], check=True)
    return out_png


def seed_for(ep, shot, take):
    """Same seed for every shot in a seed group (consistent look), shifted per take."""
    rnd = random.Random(f"{ep['episode']}:{shot.get('seed_group', shot['id'])}")
    return (rnd.randrange(1, 2 ** 31) + (take - 1) * 7919) % (2 ** 31)


def run(ep_path, only=None, takes=None, dry=False, take_start=1):
    cfg = load_config()
    ep = json.loads(Path(ep_path).read_text(encoding="utf-8"))
    errs, warns, total = lint(ep)
    for w in warns:
        print("WARN ", w)
    if errs:
        for e in errs:
            print("ERROR", e)
        sys.exit("Fix lint errors first.")
    root = Path(cfg["project_root"])
    renders = root / "renders" / ep["episode"]
    takes = takes or cfg.get("takes", 3)
    comfy = None if dry else Comfy(cfg.get("comfy_url", "http://127.0.0.1:8188"))
    if comfy:
        stats = comfy.ping()
        dev = stats.get("devices", [{}])[0]
        print(f"ComfyUI up: {dev.get('name', '?')}, {dev.get('vram_total', 0) // 2 ** 20} MB VRAM")

    shots = [s for s in ep["shots"] if not only or s["id"] in only]
    by_id = {s["id"]: s for s in ep["shots"]}
    # Dependency order, then group by pipeline so each model loads once per batch.
    order = []
    def visit(s):
        si = s.get("start_image", "")
        if si.startswith("chain:"):
            dep = by_id[si.split(":", 1)[1]]
            if dep in shots and dep not in order:
                visit(dep)
        if s not in order:
            order.append(s)
    pipe_rank = {p: i for i, p in enumerate(cfg.get("pipeline_order", ["i2v_25", "flf_25", "lipsync_25", "idlora_23", "ia2v_23"]))}
    for s in sorted(shots, key=lambda s: (pipe_rank.get(s["pipeline"], 99), ep["shots"].index(s))):
        visit(s)

    uploaded = {}
    def up(rel):
        p = resolve(root, rel)
        if not p.exists():
            raise FileNotFoundError(f"missing asset: {p}")
        if dry:
            return f"cold_storage/{p.name}"
        if str(p) not in uploaded:
            uploaded[str(p)] = comfy.upload(p)
        return uploaded[str(p)]

    picks_path = renders / "picks.json"
    picks = json.loads(picks_path.read_text()) if picks_path.exists() else {}
    w, h = cfg.get("width", 736), cfg.get("height", 1280)
    for s in order:
        pc = cfg["pipelines"].get(s["pipeline"])
        if not pc:
            sys.exit(f"config.json has no pipeline {s['pipeline']}")
        template = json.loads(resolve(HERE, pc["template"]).read_text(encoding="utf-8"))
        slots = pc["slots"]
        prompt = build_prompt(ep, s)
        si = s.get("start_image", "")
        if si.startswith("chain:"):
            src, at = chain_src(s)
            pick = picks.get(src, 1)
            src_vid = renders / src / f"{src}_take{pick}.mp4"
            if dry:
                start_name = f"cold_storage/{src}_seed.png"
            else:
                if not src_vid.exists():
                    sys.exit(f"{s['id']} chains from {src_vid}, which doesn't exist yet")
                idx = chain_seed_index(src_vid, at, int(cfg.get("chain_tail_trim", 6)))
                start_name = comfy.upload(frame_png(src_vid, idx, renders / src / f"{src}_F{idx}.png"))
        else:
            start_name = up(si)
        for t in range(take_start, take_start + takes):
            wf = copy.deepcopy(template)
            patch(wf, slots, "positive", prompt)
            patch(wf, slots, "negative", NEGATIVE + (", " + s["negative"] if s.get("negative") else ""))
            patch(wf, slots, "start_image", start_name)
            if s.get("continuation"):
                # Continuations hold the seed frame exactly (W4: strength 1.0, img_compression 0).
                for slot, val in cfg.get("continuation_overrides", {"img_strength": 1.0, "img_compression": 0}).items():
                    patch(wf, slots, slot, val)
            if s.get("end_image"):
                patch(wf, slots, "end_image", up(s["end_image"]))
            spk = s.get("speaker") or (s.get("cast") or [None])[0]
            if spk and (s["pipeline"].startswith("idlora") or s["pipeline"] in ("ia2v_23", "lipsync_25")):
                ch = ep["characters"][spk]
                patch(wf, slots, "face_ref", up(ch["face_ref"]))
                patch(wf, slots, "voice_ref", up(ch["voice_ref"]))
            seed = seed_for(ep, s, t)
            seed_targets = slots.get("seed") or []
            if seed_targets and isinstance(seed_targets[0], str):
                seed_targets = [seed_targets]
            for i, (nid, inp) in enumerate(seed_targets):
                wf[str(nid)]["inputs"][inp] = seed + i * 1000003  # stage 2 seed offset
            patch(wf, slots, "frames", int(s["frames"]))
            patch(wf, slots, "width", w)
            patch(wf, slots, "height", h)
            patch(wf, slots, "fps", ep.get("fps", 24))
            patch(wf, slots, "filename_prefix", f"cold_storage/{ep['episode']}/{s['id']}_take{t}")
            tag = f"{s['id']} take {t}/{takes} [{s['pipeline']}] {int(s['frames'])}f seed {seed}"
            if dry:
                out = renders / s["id"]
                out.mkdir(parents=True, exist_ok=True)
                (out / f"{s['id']}_take{t}.workflow.json").write_text(json.dumps(wf, indent=1), encoding="utf-8")
                print("DRY  ", tag)
                continue
            print("QUEUE", tag, flush=True)
            pid = comfy.queue(wf)
            outputs = comfy.wait(pid)
            files = comfy.download_outputs(outputs, renders / s["id"], f"{s['id']}_take{t}")
            print("DONE ", tag, "->", files[0].name if files else "no files")
    print(f"\nFinished. Review takes in {renders}, then write picks.json like {{\"C01\": 2, \"C02\": 1}}.")
    print("Shots that chain from another shot use the picked take, so pick those first and re-run the chained shots.")


# ---------------------------------------------------------------- assemble

def ffprobe_has_audio(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return bool(r.stdout.strip())


def frame_count(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                        "stream=nb_read_frames", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return int(r.stdout.strip().split(",")[0])
    except ValueError:
        return 0


def qa(ep_path):
    """Contact sheet per take: the speaker's or lead's cast photo, then first, middle and last frame, same height."""
    cfg = load_config()
    ep = json.loads(Path(ep_path).read_text(encoding="utf-8"))
    root = Path(cfg["project_root"])
    renders = root / "renders" / ep["episode"]
    out_dir = renders / "_qa"
    out_dir.mkdir(parents=True, exist_ok=True)
    report = [f"# QA report {ep['episode']}", "",
              "Pass a take only if ALL boxes are true. Watch at 1x with sound, then 0.5x, then frame by frame at the cut points.",
              "Dialogue: Whisper transcript equals the script word for word, 2.5 to 3.5 words/s, first word within 0.5 s,",
              "1 to 2 s held reaction after the last word (0.3 s minimum before any cut), lips close on b, m, p, voice in character",
              "and carrying the emotion. Identity: same face, eyes, hair, age as the cast photo in all three frames.",
              "Pick nothing that is blank, frozen (over 0.5 s unmotivated), overacted or uncanny. Any doubt is a fail.", ""]
    for s in ep["shots"]:
        who = s.get("speaker") or next((c for c in s.get("cast", [])), None)
        ref = resolve(root, ep["characters"][who]["face_ref"]) if who else None
        takes = sorted((renders / s["id"]).glob(f"{s['id']}_take*.mp4"))
        takes = [p for p in takes if re.fullmatch(rf"{re.escape(s['id'])}_take\d+\.mp4", p.name)]
        report.append(f"## {s['id']} [{s['pipeline']}]" + (f" line: \"{s['line']}\" ({s['speaker']})" if s.get("line") else ""))
        for v in takes:
            n = frame_count(v)
            if n < 3:
                report.append(f"- [ ] {v.name}: unreadable video, FAIL")
                continue
            sheet = out_dir / f"{v.stem}_sheet.png"
            idx = [0, n // 2, n - 1]
            sel = "+".join(f"eq(n\\,{i})" for i in idx)
            inputs = ["-i", str(v)]
            graph = f"[0:v]select='{sel}',scale=-2:640,tile=3x1[f]"
            if ref and ref.exists():
                inputs += ["-i", str(ref)]
                graph += ";[1:v]scale=-2:640[r];[r][f]hstack=inputs=2[o]"
                outl = "[o]"
            else:
                outl = "[f]"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", graph, "-map", outl,
                            "-frames:v", "1", "-vsync", "0", str(sheet)], check=True)
            checks = ["identity matches cast photo in all 3 frames", "right look and wardrobe",
                      "photoreal live action, no AI tells, real skin, not plastic", "hands and fingers correct",
                      "no readable text, logos or watermarks anywhere; phones show backs only",
                      "camera move and action as written, natural speed, no unmotivated freeze over 0.5 s",
                      "continues cleanly from the previous shot's seed frame (continuations)"]
            if s.get("line"):
                checks += ["Whisper transcript equals the script word for word, nothing clipped",
                           "2.5 to 3.5 words/s, first word within 0.5 s", "held 1 to 2 s reaction after the last word",
                           "acting beats land on their words; face and voice carry the emotion, not blank or overacted",
                           "voice generated in the render, matches the character's reference"]
                if s.get("lipsync", True):
                    checks += ["lips close on b/m/p, mouth still when silent, no drift"]
            report.append(f"- {v.name} · sheet `_qa/{sheet.name}`")
            report += [f"  - [ ] {c}" for c in checks]
        report.append(f"- PICK: take __  (if no take passes: more takes with new seeds, then a better emotion-matched start keyframe; never a substitute method)")
        report.append("")
    (out_dir / "QA_REPORT.md").write_text("\n".join(report), encoding="utf-8")
    print(f"QA sheets and report: {out_dir}")


def shot_starts(ep):
    fps, t, out = ep.get("fps", 24), 0.0, {}
    for s in ep["shots"]:
        out[s["id"]] = t
        t += int(s["frames"]) / fps
    return out, t


def sfxbed(ep_path):
    """Lay every sfx cue at its shot start + offset into one stereo 48 kHz WAV the length of the episode."""
    cfg = load_config()
    ep = json.loads(Path(ep_path).read_text(encoding="utf-8"))
    root = Path(cfg["project_root"])
    starts, total = shot_starts(ep)
    total += float(ep.get("end_card_s", 0))
    cues = ep.get("sfx_cues", [])
    if not cues:
        sys.exit("no sfx_cues in the episode")
    missing = [c["file"] for c in cues if not resolve(root, c["file"]).exists()]
    if missing:
        sys.exit("missing sfx files: " + ", ".join(sorted(set(missing))))
    out = resolve(root, ep.get("sfx_bed", f"sfx/{ep['episode']}_sfx.wav"))
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
    chains, labels = [], ["[0:a]"]
    for i, c in enumerate(cues, start=1):
        cmd += ["-i", str(resolve(root, c["file"]))]
        at = starts[c["shot"]] + float(c.get("at", 0))
        ms = int(round(at * 1000))
        chains.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={c.get('db', 0)}dB,adelay={ms}|{ms}[c{i}]")
        labels.append(f"[c{i}]")
    graph = ";".join(chains) + ";" + "".join(labels) + f"amix=inputs={len(labels)}:duration=first:normalize=0[a]"
    subprocess.run(cmd + ["-filter_complex", graph, "-map", "[a]", "-ar", "48000", str(out)], check=True)
    print(f"SFX bed: {out} ({len(cues)} cues, {total:.1f} s)")


def musicbed(ep_path):
    """Lay music cues at their start shots, each trimmed to its length with a 0.5 s fade out. SILENCE cues are skipped."""
    cfg = load_config()
    ep = json.loads(Path(ep_path).read_text(encoding="utf-8"))
    root = Path(cfg["project_root"])
    starts, total = shot_starts(ep)
    total += float(ep.get("end_card_s", 0))
    cues = [m for m in ep.get("music_cues", []) if not m["prompt"].startswith("SILENCE")]
    missing = [m["file"] for m in cues if not resolve(root, m["file"]).exists()]
    if missing:
        sys.exit("missing music files: " + ", ".join(missing))
    out = resolve(root, ep.get("music_bed", f"music/{ep['episode']}_score.wav"))
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
    chains, labels = [], ["[0:a]"]
    for i, m in enumerate(cues, start=1):
        cmd += ["-i", str(resolve(root, m["file"]))]
        ms = int(round(starts[m["from_shot"]] * 1000))
        d = float(m["seconds"])
        chains.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{d},"
                      f"afade=t=out:st={max(d - 0.5, 0)}:d=0.5,adelay={ms}|{ms}[m{i}]")
        labels.append(f"[m{i}]")
    graph = ";".join(chains) + ";" + "".join(labels) + f"amix=inputs={len(labels)}:duration=first:normalize=0[a]"
    subprocess.run(cmd + ["-filter_complex", graph, "-map", "[a]", "-ar", "48000", str(out)], check=True)
    print(f"Music bed: {out} ({len(cues)} cues, {total:.1f} s)")


def media_seconds(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def assemble(ep_path, picks_file=None):
    """Rough cut at the 720 x 1280 render master. Continuations join seamlessly at their seed frame (A up to and
    including the seed frame, then B from its frame 1). Other joins are clean cuts; real scene or time changes
    get their dissolves in the finish. A 0.5 s dissolve leads into the end card. No speed changes anywhere.
    SeedVR2 upscaling to 1080 x 1920 happens only after every episode is done."""
    cfg = load_config()
    ep = json.loads(Path(ep_path).read_text(encoding="utf-8"))
    root = Path(cfg["project_root"])
    renders = root / "renders" / ep["episode"]
    picks = json.loads(Path(picks_file or renders / "picks.json").read_text()) if (picks_file or (renders / "picks.json").exists()) else {}
    W, H = cfg.get("final_width", 720), cfg.get("final_height", 1280)
    fps = ep.get("fps", 24)
    tail_trim = int(cfg.get("chain_tail_trim", 6))
    work = renders / "_assembly"
    work.mkdir(parents=True, exist_ok=True)
    shots = ep["shots"]
    srcs = {}
    for s in shots:
        srcs[s["id"]] = renders / s["id"] / f"{s['id']}_take{picks.get(s['id'], 1)}.mp4"
        if not srcs[s["id"]].exists():
            sys.exit(f"missing {srcs[s['id']]}")
    norm = []
    base_vf = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},fps={fps},format=yuv420p"
    for i, s in enumerate(shots):
        src = srcs[s["id"]]
        first = 1 if (s.get("continuation") and chain_src(s)[0]) else 0
        last = None
        nxt = shots[i + 1] if i + 1 < len(shots) else None
        if nxt and nxt.get("continuation") and chain_src(nxt)[0] == s["id"]:
            last = chain_seed_index(src, chain_src(nxt)[1], tail_trim)
        trim = f"trim=start_frame={first}" + (f":end_frame={last + 1}" if last is not None else "") + ",setpts=PTS-STARTPTS,"
        a0, a1 = first / fps, (last + 1) / fps if last is not None else None
        atrim = f"atrim=start={a0:.4f}" + (f":end={a1:.4f}" if a1 else "") + ",asetpts=PTS-STARTPTS,afade=t=in:d=0.015,"
        dst = work / f"{len(norm):02d}_{s['id']}.mp4"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src)]
        if ffprobe_has_audio(src):
            af = ["-af", atrim + "aresample=48000"]
        else:
            cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest"]
            af = []
        cmd += ["-vf", trim + base_vf, *af, "-c:v", "libx264", "-crf", "12", "-preset", "slow",
                "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", str(dst)]
        subprocess.run(cmd, check=True)
        norm.append(dst)
    lst = work / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in norm), encoding="utf-8")
    cut = work / "cut.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-c:a", "aac", "-b:a", "256k", str(cut)], check=True)
    card = ep.get("end_card")
    if card and resolve(root, card).exists():
        xd = 0.5
        cs = float(ep.get("end_card_s", 2.0))
        cardclip = work / "ENDCARD.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-t", f"{cs + xd:.3f}",
                        "-i", str(resolve(root, card)), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                        "-shortest", "-vf", base_vf, "-c:v", "libx264", "-crf", "12", "-c:a", "aac", "-ar", "48000",
                        "-ac", "2", str(cardclip)], check=True)
        off = media_seconds(cut) - xd
        withcard = work / "cut_card.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(cut), "-i", str(cardclip), "-filter_complex",
                        f"[0:v][1:v]xfade=transition=fade:duration={xd}:offset={off:.3f}[v];"
                        f"[0:a][1:a]acrossfade=d={xd}[a]", "-map", "[v]", "-map", "[a]",
                        "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-c:a", "aac", "-b:a", "256k", str(withcard)],
                       check=True)
        cut = withcard
    final = renders / f"COLDSTORAGE_{ep['episode']}.mp4"
    beds = []
    sfx = ep.get("sfx_bed")
    if sfx and resolve(root, sfx).exists():
        beds.append((resolve(root, sfx), cfg.get("sfx_db", -3)))
    music = ep.get("music_bed")
    if music and resolve(root, music).exists():
        beds.append((resolve(root, music), cfg.get("music_db", -16)))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(cut)]
    for path, _ in beds:
        cmd += ["-i", str(path)]
    parts = [f"[{i}:a]volume={db}dB[b{i}]" for i, (_, db) in enumerate(beds, start=1)]
    mix_in = "[0:a]" + "".join(f"[b{i}]" for i in range(1, len(beds) + 1))
    graph = ";".join(parts + [f"{mix_in}amix=inputs={len(beds) + 1}:duration=first:dropout_transition=0:normalize=0,"
                                f"loudnorm=I=-14:TP=-1.0:LRA=11[a]"])
    subprocess.run(cmd + ["-filter_complex", graph, "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                          "-c:a", "aac", "-b:a", "320k", str(final)], check=True)
    secs = media_seconds(final)
    print(f"Rough cut: {final} ({secs:.1f} s, {W} x {H})")
    if abs(secs - float(ep.get("runtime_target_s", RUNTIME_TARGET_S))) > RUNTIME_WARN_S:
        print(f"WARN runtime {secs:.1f} s; every episode is about {ep.get('runtime_target_s', RUNTIME_TARGET_S):.0f} s total")
    print("Finish in Resolve: dissolves on real scene or time changes, captions and cards as clean overlays, grade, grain.")
    print("Then run the line gate (Whisper vs script, 0.3 s after every last word). No speed changes, no freezes.")


# ---------------------------------------------------------------- cli

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("lint"); a.add_argument("episode")
    a = sub.add_parser("inspect"); a.add_argument("workflow")
    a = sub.add_parser("prompts"); a.add_argument("episode")
    a = sub.add_parser("run"); a.add_argument("episode"); a.add_argument("--only")
    a.add_argument("--takes", type=int); a.add_argument("--dry-run", action="store_true"); a.add_argument("--take-start", type=int, default=1)
    a = sub.add_parser("qa"); a.add_argument("episode")
    a = sub.add_parser("sfxbed"); a.add_argument("episode")
    a = sub.add_parser("musicbed"); a.add_argument("episode")
    a = sub.add_parser("assemble"); a.add_argument("episode"); a.add_argument("--takes-pick")
    args = ap.parse_args()
    if args.cmd == "lint":
        ep = json.loads(Path(args.episode).read_text(encoding="utf-8"))
        errs, warns, total = lint(ep)
        for w in warns:
            print("WARN ", w)
        for e in errs:
            print("ERROR", e)
        print(f"\n{len(ep['shots'])} clips in {len(edit_shots(ep))} edited shots, {total:.1f} s plus "
              f"{ep.get('end_card_s', 0)} s end card = {total + float(ep.get('end_card_s', 0)):.1f} s "
              f"(target {float(ep.get('runtime_target_s', RUNTIME_TARGET_S)):.0f} s). "
              f"Hook: {ep.get('hook', {}).get('type')}. {'PASS' if not errs else 'FAIL'}")
        sys.exit(1 if errs else 0)
    if args.cmd == "inspect":
        inspect(args.workflow)
    elif args.cmd == "prompts":
        ep = json.loads(Path(args.episode).read_text(encoding="utf-8"))
        for s in ep["shots"]:
            print(f"\n===== {s['id']} [{s['pipeline']}] =====\n{build_prompt(ep, s)}")
        print(f"\n===== NEGATIVE (every shot) =====\n{NEGATIVE}")
    elif args.cmd == "run":
        run(args.episode, set(args.only.split(",")) if args.only else None, args.takes, args.dry_run, args.take_start)
    elif args.cmd == "qa":
        qa(args.episode)
    elif args.cmd == "sfxbed":
        sfxbed(args.episode)
    elif args.cmd == "musicbed":
        musicbed(args.episode)
    elif args.cmd == "assemble":
        assemble(args.episode, args.takes_pick)


if __name__ == "__main__":
    main()
