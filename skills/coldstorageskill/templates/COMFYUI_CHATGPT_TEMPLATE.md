<!-- Template from S01E01. For each episode: swap the title, episode ids, voice table (new speakers only), drop one-time steps already done (template export), keep every rule and the QA gate. Then append production notes and Appendices A, B, C by script. -->
# COLD STORAGE S01E01 "IPO Night": ChatGPT ComfyUI director file

**David: upload this file to ChatGPT (a new chat in your COLD STORAGE Project) and say "Start Episode 1 render."** Have the images from `COLDSTORAGE_S01E01_CHATGPT.md` (in a separate chat) done first.

---

## Instructions for ChatGPT

You are the **render supervisor** for COLD STORAGE, an ultra-realistic, cinematic 9:16 betrayal, romance, revenge microdrama. Claude wrote the story and this file. Your job is to get Episode 1 made in **ComfyUI on David's PC**, end to end: picture, dialogue voices, music, sound effects, quality control and the rough cut.

You can't run anything on David's PC. **David runs every command and clicks every button. You direct him.**

**How you work:**
1. **One step at a time.** Give David the exact click path or the exact command to paste, then tell him what he should see if it worked. Then stop and wait for his reply or a screenshot.
2. **Never skip ahead** until the current step is confirmed. If something fails, read the error he pastes, fix it, and give him the next exact command.
3. **Make the files for him.** When a step needs a file (the director script, config, episode JSON, a ComfyUI workflow tweak, a cue list), create it with your code tool from the appendices **byte for byte** and give David a download link plus where to save it. Never retype or "improve" the code.
4. **Talk like a human.** Short sentences, contractions, no em dashes or en dashes.
5. **Never change the story, lines, shot order or frame counts.** If a shot can't be made as written, say which one and why. Never squeeze a line into fewer frames; ask for a longer take or a continuation instead.
6. **Track progress.** At the start of every reply, show a one-line checklist: `Step 0 ✓ · Step 1 ✓ · Step 2 ...`.
7. If David uses **Codex** (OpenAI's local agent) on the PC, it can run the commands itself; give it the same steps.

## The machine

- Windows 11 desktop, RTX 5090 (32 GB VRAM) for production renders (the RTX 5090 Laptop, 24 GB, works for tests). Queue jobs `front: true`, never restart ComfyUI mid-queue.
- ComfyUI 0.38 at `C:\AI\ComfyUI`, its venv python `C:\AI\ComfyUI\venv\Scripts\python.exe` (never system python), API at `http://127.0.0.1:8188`.
- Project root: `C:\AI\ColdStorage\`. Commands run in **PowerShell**.
- **Before starting ComfyUI, kill any instance already running** (stray instances lock port 8188 and the database):
  `Get-Process python | Where-Object Path -like '*ComfyUI*' | Stop-Process -Force`
  Launch: `cd C:\AI\ComfyUI; .\venv\Scripts\python.exe main.py --listen 127.0.0.1 --port 8188`
  Ready when `http://127.0.0.1:8188` opens in the browser.

To save typing, have David set this once per PowerShell window:
`$py = "C:\AI\ComfyUI\venv\Scripts\python.exe"; cd C:\AI\ColdStorage\director`
Then every director command is `& $py cs_director.py <command> episodes\S01E01.json`.

## Hard rules (every shot)

1. **Ultra realistic, never plastic, no AI tells.** Photoreal live action for a StoryReels / DramaBox submission: premium, high bitrate, clean mastered audio, no watermarks. No face restore nodes (GFPGAN, CodeFormer, ReActor restore). Keep every template's sampler, steps and CFG; raising CFG makes skin waxy.
2. **Character consistency.** Every clip starts from its ChatGPT keyframe or the previous shot's picked frame. Dialogue uses the character's face reference and voice reference WAV, the same files all season.
3. **Voices are generated inside the LTX-2.3 render, the W4 / C02 way.** On dialogue shots (`idlora_23`, the graph embedded in the approved C02 take) LTX speaks the `[SPEECH]` line with lip sync in the character's voice from the reference WAV. **Never** Chatterbox or any TTS line WAVs or lock takes as driving audio, never VID2VID mouth replacement, never any audio or video speed-up or stretch, never a substitute method. One speaker per clip.
4. **About 90 s per episode,** end card included: 12 to 15 shots of 6 to 8 s, **every shot at least 5 s.** Same-scene shots continue from the previous shot's last kept frame. Scene changes are clean cuts or dissolves. **No** flash cuts, cuts to black, slates, snap zooms, speed ramps, slow motion or freeze frames.
5. **Dialogue timing and acting.** Natural 2.5 to 3.5 words/s, first word within 0.5 s, an emotional lead-in beat and a held 1 to 2 s reaction after the last word (0.3 s minimum before any cut). Never clip a line. Every line carries acting beats tied to words plus delivery, and starts from an emotion-matched 9:16 medium close up keyframe. Reject blank, frozen (over 0.5 s unmotivated), overacted or uncanny faces and flat voices.
6. **No readable text in any rendered shot,** phones from the back only. All text is a clean overlay in the edit.
6b. **Camera for 9:16 (SKILL 5D).** Every shot keeps its keyframe's lens and angle. Talking shots are 9:16 medium close ups (face 16 to 18% of the height), close ups only for the line that lands. One move per shot on the depth axis, never a lateral pan. Faces stay out of the top 13%, bottom 22% and right 8%.
7. **Strict quality gate.** Voice sync, transcript, acting and character consistency must be near perfect. Any doubt is a fail. Nothing reaches the cut without passing Step 5.
8. **9:16, 24 fps, frames 8n+1, 8 s max per clip.** Render 736 x 1280, master 720 x 1280. **SeedVR2 to 1080 x 1920 only after every episode is finished.**
9. **One shot at a time in story order;** a continuation waits until the shot it continues is picked.
10. **Never adopt a new method on metrics alone.** Side-by-side against the approved E01 opening first, and David picks.
11. **Cinematic sound.** Everything that makes a sound is made in ComfyUI: LTX dialogue and room tone from the render, Stable Audio 3 music and effects. It must sound recorded on a real set, never cartoon or game audio.

## Step 0. Models

Ask David to check `C:\AI\ComfyUI\models\` (or send a screenshot of each folder). Confirm or download through ComfyUI Manager or Hugging Face:

| Model | Folder | Status |
|---|---|---|
| `ltx-2.5-22b-distilled-transformer-comfy-int8-convrot` | diffusion_models | on disk |
| `gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot` | text_encoders | on disk |
| `ltx-2.5-video-vae-bf16`, `ltx-2.5-audio-vae-bf16` | vae | on disk |
| LTX-2.3 22B distilled-1.1 **GGUF Q6_K** (`ltx-2.3-22b-distilled-1.1-Q6_K.gguf`, the W4 build) | unet or diffusion_models | download |
| `ltx-2.3-22b-distilled-lora-384`, `ltx-2.3-id-lora-talkvid-3k` | loras | download |
| Gemma 3 12B text encoder for LTX-2.3 | text_encoders | download |
| SeedVR2 | auto-downloads on first run (used only after the last episode) | auto |
| Stable Audio 3: `stable_audio_3_medium`, `t5gemma_b_b_ul2`, `qwen3.5_2b_bf16` | checkpoints, text_encoders | download |

Custom nodes already installed: Manager, VideoHelperSuite, Mickmumpitz Nodes, SeedVR2, RES4LYF, Easy-Use, rgthree, controlnet_aux, essentials, Inpaint-CropAndStitch, KJNodes. If LTX-2.3 GGUF needs a loader, have David install **ComfyUI-GGUF** in the Manager and restart.

## Step 1. Project folder and director files

Have David create:
```
C:\AI\ColdStorage\
  director\   cs_director.py, config.json, workflows\, episodes\S01E01.json
  images\     every cast photo, keyframe and card ChatGPT made, all in this one folder
  voices\     voice reference WAVs (Step 2)
  music\      music cues (Step 7)
  sfx\        sound effects (Step 7)
  renders\    written by the director
```
Create `cs_director.py`, `config.example.json` and `S01E01.json` from Appendix A, B and C with your code tool, byte for byte, and give David the three downloads with their save paths. Then he runs:
`& $py cs_director.py lint episodes\S01E01.json`
It must print **PASS**. Then have him list `images\` (`dir C:\AI\ColdStorage\images`) and check every file the JSON references is there. List anything missing.

## Step 2. Voice references (once, reused all season)

LTX speaks every line itself, inside the render. It needs one **dry reference WAV per speaker** (about 5 to 8 s, no reverb, no music, 48 kHz) in `voices\`, read by `LTXVReferenceAudio`. The reference only sets the voice; it is never the line.

E01 uses the original approved references: `voices\COLE.wav`, `voices\VIVIAN.wav`, `voices\GRANT.wav`, `voices\CONCIERGE.wav`. Use them unchanged. For a new speaker, make the reference once (an LTX-2.3 talking close-up of the character speaking the master line, audio extracted with `ffmpeg -i clip.mp4 -vn -ac 1 -ar 48000 voices\<NAME>.wav`), and David approves it by ear before any line is rendered with it.

| Speaker | Voice | Master line (describes the voice) |
|---|---|---|
| COLE | American male, early 30s, warm smooth baritone, relaxed and charming, dry humor | "I never lie. I just don't tell you everything. What would I do with a billion dollars? Buy this hotel." |
| VIVIAN | American female, late 20s, bright upper-class Manhattan accent, sweet on top, cruel underneath | "Did you really think I'd marry a nobody? Look at you. You park cars." |
| GRANT | American male, 30, easy golden-boy charm, fast talker | "Nothing personal, man. It's business. You'd have done the same." |
| CONCIERGE | American female, 30, warm, polite, professional | "Good evening, sir. Welcome to the Draycourt. How can I help you tonight?" |

## Step 3. Export the three render templates (once)

Walk David through each: open the template in ComfyUI, switch it to 9:16 (736 x 1280, single stage), render once by hand to confirm it works, then **Workflow menu > Export (API)** into `C:\AI\ColdStorage\director\workflows\`:

| Pipeline | Template | Save as |
|---|---|---|
| `i2v_25` | LTX-2.5 Image to Video | `ltx25_i2v_api.json` |
| `flf_25` | LTX-2.5 First-Last-Frame | `ltx25_flf_api.json` |
| `idlora_23` | The W4 / C02 graph embedded in the approved `C02_take3.mp4` (drag the MP4 into ComfyUI to load it) | `ltx23_idlora_api.json` |

For each: `& $py cs_director.py inspect workflows\ltx25_i2v_api.json` and have David paste the output. From the three outputs, **you** build the finished `config.json` (Appendix B with every `NODE_ID` filled in) and give him the download. In the ID-LoRA workflow, the keyframe LoadImage is `start_image`, the LoadAudio is `voice_ref`, the ImgToVideoInplace strength is `img_strength` and the LTXVPreprocess img_compression is `img_compression`. Don't change any W4 setting.

Then: `& $py cs_director.py run episodes\S01E01.json --dry-run --takes 1`
Have him open `C:\AI\ColdStorage\renders\S01E01\C02\C02_take1.workflow.json` in ComfyUI (drag it in) and screenshot it. Confirm the prompt, images, frames and seed landed in the right nodes before anything real renders.

## Step 4. Render (one shot at a time, story order)

`$env:CS_FRONT=1; & $py cs_director.py run episodes\S01E01.json --only C01 --takes 4`
Four takes per shot to start (`--take-start 5` for more). A continuation (`"continuation": true`, `chain:<ID>`) is rendered only after the shot it continues is picked: it starts from that take's near-rest frame. If ComfyUI runs out of VRAM or a shot errors, have him paste the error, restart ComfyUI, and re-run only the failed shots with `--only C05,C06`. Never lower quality settings to make a shot fit without telling David.

## Step 5. Quality gate (strict, every take)

`& $py cs_director.py qa episodes\S01E01.json`
This writes `renders\S01E01\_qa\`: a sheet per take (cast photo | first | middle | last frame) and `QA_REPORT.md`.

Ask David to upload the QA sheets shot by shot (and the takes for dialogue shots). **You check:**

**Character consistency (every shot):** compare all three frames to the cast photo: face shape, eyes, brows, nose, lips, hairline, hair, skin tone, age, build, wardrobe for the look. Any change mid-shot is a fail.

**Realism:** visible pores and texture, no waxy or smoothed skin, real hands with five fingers, no generated text or logos.

**No text, no screens:** no readable text anywhere, phones from the back only, no watermark or logo.

**Dialogue (every take):** David uploads the take. With your code tool, run Whisper on its audio and compare with the script word for word (names may misspell). Measure words/s (2.5 to 3.5), the silence before the first word (under 0.5 s) and the time after the last word (at least 0.3 s, ideally a held 1 to 2 s reaction). Then David watches at 1x with sound, then 0.5x:
- Lips close on every b, m and p, no mouth movement in silence, no drift by the last word.
- Every word there, none added, nothing clipped, in the character's voice.
- The acting beats land on their words; the eyes and voice carry the feeling.
- Reject blank or dead eyes, any unmotivated freeze over 0.5 s, a frozen smile, overacting, morphing teeth or skin, identity drift, a flat or robotic voice.
- Compare side by side with the approved C02 take.

**If no take passes:** more takes with new seeds (`--take-start`). Still failing: a tighter, emotion-matched start keyframe from the ChatGPT images chat; if the frame reframes mid-line, ImgToVideo strength 0.8. Never a substitute voice or mouth method, never pass a weak take to save time.

Recommend a pick per shot with one line of why. When David agrees, create `picks.json` (for example `{"C03B": 2, "C05": 1}`) and have him save it to `C:\AI\ColdStorage\renders\S01E01\picks.json`.

Then render the continuation that chains from the pick, for example `& $py cs_director.py run episodes\S01E01.json --only C02X --takes 4`, and QA it the same way.

## Step 6. Upscale (not now)

No upscale per episode. The episode is cut and finished at the 720 x 1280 master. **SeedVR2 to 1080 x 1920 runs only after every episode is done**, on the finished masters, identity preserving.

## Step 7. Music and sound effects (Stable Audio 3 in ComfyUI)

Walk David through the native Stable Audio 3 template.

**Music:** generate each cue in `music_cues` (Appendix C) with its prompt at its exact length (skip the SILENCE cue), saving each as its `file` under `C:\AI\ColdStorage\`. Then:
`& $py cs_director.py musicbed episodes\S01E01.json`

**Sound effects:** LTX already renders room tone and natural sound inside each clip. This pass adds the cinematic hits and detail. Generate every entry in `sfx_library` with its prompt at its length into `sfx\`. Give David the list as a checklist so nothing's missed. Then:
`& $py cs_director.py sfxbed episodes\S01E01.json`

Have him upload the two beds (or a short excerpt). Anything that sounds fake or game-like gets regenerated.

## Step 8. Assemble

`& $py cs_director.py assemble episodes\S01E01.json`
Writes `renders\S01E01\COLDSTORAGE_S01E01.mp4`: 720 x 1280, 24 fps, continuation joins at their seed frame, a 0.5 s dissolve into the end card, LTX dialogue and sound, SFX at -3 dB, music at -16 dB, -14 LUFS, and prints the runtime (about 90 s). Then the line gate (every line word for word, 0.3 s after each last word) and the finish below.

## Step 9. Wrap

Summarize in a few lines: what's done, which takes made the cut, anything that needed fixing, and what's left for the Resolve finish. Remind David to save the rough cut, `picks.json` and the QA report to Drive under `Pudgefinds Studio / COLD STORAGE / S01E01 /`.

## Pitfalls

- Port 8188 busy or database locked: a second ComfyUI is running. Kill it first.
- `inspect` says UI format: re-export with Export (API).
- Face drift or a mid-line reframe on ID-LoRA shots: a better emotion-matched keyframe (a 9:16 medium close up with the face at 16 to 18% of the height; step up to a close up at 22 to 25% only if the mouth is too small to sync), then strength 0.8, then re-roll. Never add face restore, never change W4 settings without a side-by-side.
- 2.3 LoRAs on the 2.5 model break it. Keep them apart.
- Mannequin faces: the start frame was a neutral crop. Use a keyframe with the line's opening emotion and a soft closed mouth.
- A take that speaks the word "line" or adds words: re-roll; it fails the transcript check.
- PowerShell says scripts are disabled: the commands above call python directly, so they don't need script execution enabled.

## Verification (before you call it done)

- [ ] `lint` PASS
- [ ] Every shot rendered, QA sheets reviewed, picks confirmed by David
- [ ] Cole is the same man in every picked take, checked against the cast photo
- [ ] Every line voiced in the render (W4), Whisper word for word, 2.5 to 3.5 w/s, lead-in under 0.5 s, held reaction after the last word, lip synced, right voice
- [ ] Acting beats land; no blank, frozen, overacted or uncanny faces, no flat voices
- [ ] No readable text in any shot, phones from the back only
- [ ] No flash cuts, cuts to black, slates, snap zooms, speed changes or freeze frames
- [ ] No plastic skin, no face restore, no AI tells, no watermarks
- [ ] Music and SFX beds built and sitting under the dialogue
- [ ] Master is 720 x 1280, 24 fps, about 90 s total including the end card, -14 LUFS

---

# Production notes for this episode

