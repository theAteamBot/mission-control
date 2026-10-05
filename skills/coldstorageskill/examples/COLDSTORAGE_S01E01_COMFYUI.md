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
  images\     every PNG and JPG from COLDSTORAGE_CAST_KIT.zip and COLDSTORAGE_S01E01_IMAGES.zip, flattened into this one folder
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
| VIVIAN | American female, late 20s, bright upper-class Manhattan accent, sweet on top, cruel underneath | "Did you really think I'd stay with a nobody? Look at you. You park cars." |
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

**Runtime: 87.9 s of picture + 2 s end card = 89.9 s (target 90 s).** 21 clips in 14 edited shots, every edited shot at least 5 s. Each line is one W4 dialogue clip sized to the line plus a chained silent continuation (`X`) that carries the held reaction.

## Transitions (the signature of the show)

Every cut in this episode is designed. Same-scene shots continue from the previous shot's frame; scene and time changes are clean cuts on motion or sound, or 12 f dissolves. No flash cuts, cuts to black, slates, snap zooms, speed ramps or freeze frames.

| # | Between | Transition | How |
|---|---|---|---|
| T1 | C03B → T1 | **Match transform: champagne becomes confetti** | FLF2V clip: start = last kept frame of C03B, end = K04. The droplets drift up and turn to gold confetti as the camera lifts into the lobby. The time jump is carried by the move and the 3 YEARS EARLIER overlay |
| T2 | C08BX → C09 | **Cut on his turn, sound leads** | J-cut: the elevator ding plays 0.5 s before we cut |
| T3 | C09 → C10 | **Dissolve on the closing doors** | 12 f dissolve as the doors meet, into the corridor close-up. Never to black |
| T4 | C12 | **Dolly zoom reveal** | FLF2V clip K12 → K13: his hand on the handle, the door opens, the corridor stretches as his face grows. Room tone drops to silence |
| T5 | C14 → C15 | **Cut on the last glug** | The champagne bottle falls at natural speed, rolls and spills; cut on the last glug into his face. The champagne he brought up to celebrate is the champagne she pours on him three years later |
| T6 | C15 → C16 | **Silence, one hit, dissolve** | C15 holds on his living face (breathing, never a freeze), one low hit, 0.5 s dissolve to the tag |
| T7 | C01 → C02 | **Reaction cut on the splash** | Cut on the splash sound, match it across the cut |
| T8 | C05 → C05X, C06 → C06X, C08A → C08AX, C08B → C08BX, C13 → C13X | **Continuity chains** | Each continuation starts from the line clip's near-rest frame; `assemble` joins at that exact frame |
| T9 | C06X → C08A | **Dissolve to the hotel** | 12 f dissolve, the lobby room tone leads |

## Shot list

The director builds each final prompt from the JSON with the realism, continuity and no-text templates and each line's acting beats (`python cs_director.py prompts episodes\S01E01.json` to read them all).

| Shot | Starts (plan) | Frames | Model | Keyframes | Seed | Line |
|---|---|---|---|---|---|---|
| C01 | 0:00.0 | 145 (6.0 s) | LTX-2.5 I2V | E01-K01 | S1 |  |
| C02 | 0:06.0 | 97 (4.0 s) | LTX-2.3 ID-LoRA (W4) | E01-K02 | S1 | Vivian: "Oops. Tip's included." |
| C02X | 0:10.1 | 49 (2.0 s) | LTX-2.5 I2V continuation | chain:C02 | S1 |  |
| C03B | 0:12.1 | 145 (6.0 s) | LTX-2.5 I2V | E01-K20 | S1 |  |
| T1 | 0:18.2 | 145 (6.0 s) | LTX-2.5 FLF continuation | chain:C03B to E01-K04 | S2 |  |
| C05 | 0:24.2 | 97 (4.0 s) | LTX-2.3 ID-LoRA (W4) | E01-K05 | S2 | Grant: "Brother. We did it." |
| C05X | 0:28.3 | 49 (2.0 s) | LTX-2.5 I2V continuation | chain:C05 | S2 |  |
| C06 | 0:30.3 | 105 (4.4 s) | LTX-2.3 ID-LoRA (W4) | E01-K06 | S2 | Cole: "We did. Where's Viv? She has to see this." |
| C06X | 0:34.7 | 41 (1.7 s) | LTX-2.5 I2V continuation | chain:C06 | S2 |  |
| C08A | 0:36.4 | 105 (4.4 s) | LTX-2.3 ID-LoRA (W4) | E01-K08 | S3 | Concierge: "Miss Draycourt went up to the penthouse suite." |
| C08AX | 0:40.8 | 41 (1.7 s) | LTX-2.5 I2V continuation | chain:C08A | S3 |  |
| C08B | 0:42.5 | 97 (4.0 s) | LTX-2.3 ID-LoRA (W4) | E01-K21 | S3 | Cole: "Perfect. Don't tell her I'm coming." |
| C08BX | 0:46.5 | 49 (2.0 s) | LTX-2.5 I2V continuation | chain:C08B | S3 |  |
| C09 | 0:48.5 | 121 (5.0 s) | LTX-2.5 I2V | E01-K09 | S3 |  |
| C10 | 0:53.6 | 121 (5.0 s) | LTX-2.3 ID-LoRA (W4) | E01-K10 | S3 | Cole: "Viv? We're public. Come celebrate." |
| C12 | 0:58.6 | 145 (6.0 s) | LTX-2.5 FLF | E01-K12 to E01-K13 | S4 |  |
| C13 | 1:04.7 | 97 (4.0 s) | LTX-2.3 ID-LoRA (W4) | E01-K14 | S4 | Vivian: "Cole." |
| C13X | 1:08.7 | 49 (2.0 s) | LTX-2.5 I2V continuation | chain:C13 | S4 |  |
| C14 | 1:10.8 | 121 (5.0 s) | LTX-2.5 FLF | E01-K15 to E01-K16 | S4 |  |
| C15 | 1:15.8 | 169 (7.0 s) | LTX-2.5 I2V | E01-K17 | S4 |  |
| C16 | 1:22.8 | 121 (5.0 s) | LTX-2.5 FLF | E01-K18 to E01-K19 | S5 |  |

Starts are plan times before trims; the join frames and the end card dissolve take a few frames off. Check the real runtime that `assemble` prints.

## Acting (every line, written into the JSON `acting` field)

| Line | Start keyframe shows | Beats on words | After the last word | Delivery |
|---|---|---|---|---|
| C02 Vivian "Oops. Tip's included." | chin up, cruel closed-lip smile | lip curls on "Oops", tilts the flute on "Tip's included" | holds the smile, lowers the glass (C02X) | light, sweet, cold drop on "included" |
| C05 Grant "Brother. We did it." | glistening eyes, brows up | leans in on "Brother", breathy half laugh on "We did it" | proud grin, nod, raises his glass (C05X) | warm, low, close, catch of breath |
| C06 Cole "We did. Where's Viv? She has to see this." | boyish grin at one corner | nod on "We did", eyes search the crowd on "Where's Viv", grin breaks on "see this" | grabs a champagne bottle and two flutes off a tray (C06X) | smooth, happy, rising on "see this" |
| C08A Concierge "Miss Draycourt went up to the penthouse suite." | courteous smile, knowing | head tilt on "Miss Draycourt", eyes up on "penthouse suite" | polite nod, glance to the elevators (C08AX) | warm, professional, quiet |
| C08B Cole "Perfect. Don't tell her I'm coming." | leaning in, excited half smile | eyes light on "Perfect", voice drops on "Don't tell her" | wink, finger to lips, taps the desk (C08B, C08BX) | conspiratorial, low |
| C10 Cole (half whisper) "Viv? We're public. Come celebrate." | bottle and flutes at his chest, leaning to the door | brows lift on "Viv", proud almost-smile on "We're public", lifts the bottle on "Come celebrate" | waits, listening, smile holding | soft playful half whisper |
| C13 Vivian "Cole." | chin up, caught, not sorry | contempt at one mouth corner on "Cole" | holds his gaze, jaw sets, looks away (C13X) | cool, flat, quiet |

## Finish (after `cs_director.py assemble`)

1. **Transitions:** the T3, T6 and T9 dissolves (12 f; T6 0.5 s). J-cuts at T2 and T9 (sound 0.5 s early). No speed changes, no freezes.
2. **Overlays (the only text in the episode):** `CARD-E01-HOOK.png` over C03B from 0.5 s, `CARD-E01-3YEARS.png` fading in 1 s into T1, `CARD-E01-SCREEN.png` laid onto the blank LED wall in T1. The end card is added by the director with a 0.5 s dissolve.
3. **Captions:** burned in as clean overlays, bold white, black stroke, 2 to 4 words at a time, lower middle safe area. Every spoken line, timed to the render's own audio.
4. **Grade:** gala and party warm gold, suite cold teal. Match skin tones shot to shot. Don't smooth skin.
5. **Texture:** light 35 mm grain and gentle halation over the whole episode.
6. **Music (Stable Audio 3, exact durations from `music_cues`):**

| Cue | From | Seconds | Prompt |
|---|---|---|---|
| M1 | C01 | 18.2 | tense cinematic film score, solo cello drone, low strings, sparse and dark, 70 bpm, no drums, no vocals |
| M2 | T1 | 30.4 | warm cinematic uplift, piano and strings, hopeful and romantic, 96 bpm, light pulse, no vocals |
| M3 | C09 | 10.1 | quiet intimate romantic piano, nervous, slowly thinning to nothing, no vocals |
| M4 | C12 | 24.2 | SILENCE: generate nothing, pad with digital silence |
| M5 | C16 | 7.0 | one low piano note into a cold dark 4 note motif, cinematic, ends clean |

The director builds these with `musicbed` (Step 7). Fine-tune ducking in the finish.
7. **Export master:** 720 x 1280, 24 fps, H.264 high bitrate, clean mastered audio at -14 LUFS, no watermark, `COLDSTORAGE_S01E01.mp4`. SeedVR2 to 1080 x 1920 only after the last episode.

## Final QA before you publish

- [ ] Runtime about 90 s including the end card, 14 edited shots, none under 5 s
- [ ] Cole's face is the same man in every clip
- [ ] Every line voiced in the render, Whisper word for word, 2.5 to 3.5 w/s, first word within 0.5 s, held reaction after the last word, nothing clipped
- [ ] The acting beats land; no blank, frozen, overacted or uncanny faces, no flat voices
- [ ] No readable text generated inside any clip; phones from the back only; the deed blurred
- [ ] Hands correct in C06X, C08BX, C12, C14, C16
- [ ] Hook lands in the first second, caption by second 3
- [ ] Every transition lands on motion or sound; no flash cuts, cuts to black, slates, snap zooms, speed changes or freeze frames
- [ ] Last 3 seconds: silence, a living held face, one hit, 0.5 s dissolve to the end card

## Release pack

- **Title:** `She Poured Champagne On The Valet. He's Worth $5 Billion | COLD STORAGE Ep 1`
- **Caption:** "The night my company went public, my best friend took my girl. Then he took my company."
- **Hashtags:** #shortdrama #secretbillionaire #revengedrama #betrayal #minidrama
- **Pinned comment:** "Would you have walked in, or walked away?"
- **✂️ Clip for Shorts:** 0:00 to 0:12, the pour and "Oops. Tip's included."

---

## Appendix A: `director\cs_director.py` (ChatGPT: create this file byte for byte)

```python
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
```

## Appendix B: `director\config.example.json` (ChatGPT: fill every NODE_ID from the `inspect` output, save as config.json)

```json
{
  "comfy_url": "http://127.0.0.1:8188",
  "project_root": "C:/AI/ColdStorage",
  "takes": 4,
  "_render_note": "Render 736 x 1280 (LTX needs multiples of 32), 24 fps, single stage. assemble center-crops to the 720 x 1280 master. SeedVR2 upscale to 1080 x 1920 runs only after every episode is finished (upscale_width/height).",
  "width": 736,
  "height": 1280,
  "final_width": 720,
  "final_height": 1280,
  "upscale_width": 1080,
  "upscale_height": 1920,
  "chain_tail_trim": 6,
  "continuation_overrides": {
    "img_strength": 1.0,
    "img_compression": 0
  },
  "music_db": -16,
  "sfx_db": -3,
  "pipeline_order": [
    "i2v_25",
    "flf_25",
    "idlora_23"
  ],
  "pipelines": {
    "i2v_25": {
      "about": "LTX-2.5 image to video. ComfyUI template: LTX-2.5 Image to Video. Export (API) and save here.",
      "template": "workflows/ltx25_i2v_api.json",
      "slots": {
        "positive": [
          "NODE_ID",
          "text"
        ],
        "negative": [
          "NODE_ID",
          "text"
        ],
        "start_image": [
          "NODE_ID",
          "image"
        ],
        "seed": [
          [
            "NODE_ID",
            "noise_seed"
          ]
        ],
        "frames": [
          "NODE_ID",
          "length"
        ],
        "width": [
          "NODE_ID",
          "width"
        ],
        "height": [
          "NODE_ID",
          "height"
        ],
        "fps": [
          "NODE_ID",
          "frame_rate"
        ],
        "filename_prefix": [
          "NODE_ID",
          "filename_prefix"
        ],
        "img_strength": [
          "NODE_ID",
          "strength"
        ],
        "img_compression": [
          "NODE_ID",
          "img_compression"
        ]
      }
    },
    "flf_25": {
      "about": "LTX-2.5 first last frame. ComfyUI template: LTX-2.5 First-Last-Frame.",
      "template": "workflows/ltx25_flf_api.json",
      "slots": {
        "positive": [
          "NODE_ID",
          "text"
        ],
        "negative": [
          "NODE_ID",
          "text"
        ],
        "start_image": [
          "NODE_ID",
          "image"
        ],
        "end_image": [
          "NODE_ID",
          "image"
        ],
        "seed": [
          [
            "NODE_ID",
            "noise_seed"
          ]
        ],
        "frames": [
          "NODE_ID",
          "length"
        ],
        "width": [
          "NODE_ID",
          "width"
        ],
        "height": [
          "NODE_ID",
          "height"
        ],
        "fps": [
          "NODE_ID",
          "frame_rate"
        ],
        "filename_prefix": [
          "NODE_ID",
          "filename_prefix"
        ],
        "img_strength": [
          "NODE_ID",
          "strength"
        ],
        "img_compression": [
          "NODE_ID",
          "img_compression"
        ]
      }
    },
    "idlora_23": {
      "about": "LTX-2.3 ID-LoRA dialogue, the W4 / C02 method (DIALOGUE_RECIPE_W4.md): the graph embedded in the approved C02_take3.mp4. ltx-2.3-22b-distilled-1.1 Q6_K GGUF, id-lora-talkvid-3k at 1.0, LTXVReferenceAudio identity 3.0, ImgToVideoInplace 0.7, img_compression 18, CFGGuider cfg 1.0, euler, 8 manual sigmas, trim_to_audio False. The voice is generated inside the render from the character's reference WAV. Never feed a line WAV.",
      "template": "workflows/ltx23_idlora_api.json",
      "slots": {
        "positive": [
          "NODE_ID",
          "text"
        ],
        "negative": [
          "NODE_ID",
          "text"
        ],
        "start_image": [
          "NODE_ID",
          "image"
        ],
        "face_ref": [
          "NODE_ID",
          "image"
        ],
        "voice_ref": [
          "NODE_ID",
          "audio"
        ],
        "seed": [
          [
            "NODE_ID",
            "noise_seed"
          ],
          [
            "NODE_ID",
            "noise_seed"
          ]
        ],
        "frames": [
          "NODE_ID",
          "length"
        ],
        "width": [
          "NODE_ID",
          "width"
        ],
        "height": [
          "NODE_ID",
          "height"
        ],
        "fps": [
          "NODE_ID",
          "frame_rate"
        ],
        "filename_prefix": [
          "NODE_ID",
          "filename_prefix"
        ],
        "img_strength": [
          "NODE_ID",
          "strength"
        ],
        "img_compression": [
          "NODE_ID",
          "img_compression"
        ]
      }
    }
  }
}
```

## Appendix C: `director\episodes\S01E01.json` (ChatGPT: create this file byte for byte)

```json
{
  "series": "COLD STORAGE",
  "episode": "S01E01",
  "title": "IPO Night",
  "fps": 24,
  "runtime_target_s": 90,
  "hook": {
    "type": "status_violation",
    "first_beat_s": 0.4,
    "caption": "SHE DOESN'T KNOW I'M WORTH $5 BILLION",
    "why": "A billionaire is humiliated by a woman who thinks he's a valet. Status violation plus a secret identity in the first frame."
  },
  "music_bed": "music/S01E01_score.wav",
  "music_cues": [
    {
      "id": "M1",
      "from_shot": "C01",
      "seconds": 18.2,
      "prompt": "tense cinematic film score, solo cello drone, low strings, sparse and dark, 70 bpm, no drums, no vocals",
      "file": "music/S01E01_M1.wav"
    },
    {
      "id": "M2",
      "from_shot": "T1",
      "seconds": 30.4,
      "prompt": "warm cinematic uplift, piano and strings, hopeful and romantic, 96 bpm, light pulse, no vocals",
      "file": "music/S01E01_M2.wav"
    },
    {
      "id": "M3",
      "from_shot": "C09",
      "seconds": 10.1,
      "prompt": "quiet intimate romantic piano, nervous, slowly thinning to nothing, no vocals",
      "file": "music/S01E01_M3.wav"
    },
    {
      "id": "M4",
      "from_shot": "C12",
      "seconds": 24.2,
      "prompt": "SILENCE: generate nothing, pad with digital silence",
      "file": "music/S01E01_M4.wav"
    },
    {
      "id": "M5",
      "from_shot": "C16",
      "seconds": 7.0,
      "prompt": "one low piano note into a cold dark 4 note motif, cinematic, ends clean",
      "file": "music/S01E01_M5.wav"
    }
  ],
  "sfx_bed": "sfx/S01E01_sfx.wav",
  "sfx_library": {
    "sfx/champagne_pour.wav": {
      "seconds": 3,
      "prompt": "champagne pouring and splashing onto a man's hair and suit collar, close microphone, real liquid, crisp fizz, no music"
    },
    "sfx/crowd_gasp_laugh.wav": {
      "seconds": 5,
      "prompt": "upscale gala crowd gasps then breaks into cruel laughter, black tie ballroom, large room ambience, no music"
    },
    "sfx/phone_shutters.wav": {
      "seconds": 3,
      "prompt": "several smartphone camera shutter clicks, crowd murmur underneath, no music"
    },
    "sfx/single_drip.wav": {
      "seconds": 1,
      "prompt": "a single drop of liquid hitting a marble floor, close, quiet room"
    },
    "sfx/whoosh_rise.wav": {
      "seconds": 2,
      "prompt": "cinematic rising whoosh with a shimmering sparkle tail, airy, trailer quality"
    },
    "sfx/confetti_cannon.wav": {
      "seconds": 2,
      "prompt": "confetti cannon pop with paper confetti fluttering down, big party"
    },
    "sfx/party_crowd.wav": {
      "seconds": 8,
      "prompt": "glamorous skyscraper party crowd cheering and clinking champagne glasses, muffled dance beat in the distance"
    },
    "sfx/bottle_lift.wav": {
      "seconds": 2,
      "prompt": "a chilled champagne bottle lifted off a silver tray, two glass flutes clinking, close, party murmur behind"
    },
    "sfx/hotel_lobby.wav": {
      "seconds": 8,
      "prompt": "quiet luxury hotel lobby room tone, distant grand piano, soft footsteps on marble"
    },
    "sfx/elevator_ding.wav": {
      "seconds": 2,
      "prompt": "classic brass hotel elevator arrival ding"
    },
    "sfx/elevator_doors.wav": {
      "seconds": 3,
      "prompt": "heavy elevator doors sliding closed with a soft thud"
    },
    "sfx/carpet_steps.wav": {
      "seconds": 7,
      "prompt": "slow footsteps on thick hotel corridor carpet, low building hum"
    },
    "sfx/muffled_laughter.wav": {
      "seconds": 4,
      "prompt": "a man and a woman laughing intimately behind a closed hotel door, muffled"
    },
    "sfx/door_open.wav": {
      "seconds": 2,
      "prompt": "heavy hotel suite door handle turning and the door swinging open"
    },
    "sfx/heartbeat_low.wav": {
      "seconds": 4,
      "prompt": "a single slow deep heartbeat, cinematic sub bass"
    },
    "sfx/city_far.wav": {
      "seconds": 8,
      "prompt": "Manhattan at night heard from a high floor through glass, distant traffic, a faint siren"
    },
    "sfx/silk_rustle.wav": {
      "seconds": 2,
      "prompt": "a silk robe rustling as someone sits up on a bed"
    },
    "sfx/sub_hit.wav": {
      "seconds": 2,
      "prompt": "cinematic sub bass impact hit with a short dark tail, trailer style"
    },
    "sfx/pen_scratch.wav": {
      "seconds": 3,
      "prompt": "a fountain pen signing heavy paper, close microphone, scratch of the nib"
    },
    "sfx/clock_tick.wav": {
      "seconds": 3,
      "prompt": "an antique clock ticking in a quiet office"
    },
    "sfx/bottle_drop.wav": {
      "seconds": 2,
      "prompt": "a heavy champagne bottle dropping onto thick hotel carpet, a dull thud, then fizzing and glugging as it rolls and spills, close microphone, no music"
    }
  },
  "sfx_cues": [
    {
      "shot": "C01",
      "at": 0.3,
      "file": "sfx/champagne_pour.wav",
      "db": -4
    },
    {
      "shot": "C01",
      "at": 1.2,
      "file": "sfx/crowd_gasp_laugh.wav",
      "db": -8
    },
    {
      "shot": "C01",
      "at": 1.5,
      "file": "sfx/phone_shutters.wav",
      "db": -10
    },
    {
      "shot": "C03B",
      "at": 1.0,
      "file": "sfx/single_drip.wav",
      "db": -6
    },
    {
      "shot": "T1",
      "at": 0.0,
      "file": "sfx/whoosh_rise.wav",
      "db": -4
    },
    {
      "shot": "T1",
      "at": 3.0,
      "file": "sfx/party_crowd.wav",
      "db": -14
    },
    {
      "shot": "T1",
      "at": 3.4,
      "file": "sfx/confetti_cannon.wav",
      "db": -8
    },
    {
      "shot": "C06X",
      "at": 0.2,
      "file": "sfx/bottle_lift.wav",
      "db": -8
    },
    {
      "shot": "C08A",
      "at": 0.0,
      "file": "sfx/hotel_lobby.wav",
      "db": -16
    },
    {
      "shot": "C08BX",
      "at": 1.2,
      "file": "sfx/elevator_ding.wav",
      "db": -6
    },
    {
      "shot": "C09",
      "at": 1.5,
      "file": "sfx/elevator_doors.wav",
      "db": -6
    },
    {
      "shot": "C10",
      "at": 0.0,
      "file": "sfx/carpet_steps.wav",
      "db": -10
    },
    {
      "shot": "C12",
      "at": 0.0,
      "file": "sfx/muffled_laughter.wav",
      "db": -10
    },
    {
      "shot": "C12",
      "at": 2.2,
      "file": "sfx/door_open.wav",
      "db": -6
    },
    {
      "shot": "C12",
      "at": 3.6,
      "file": "sfx/heartbeat_low.wav",
      "db": -4
    },
    {
      "shot": "C13",
      "at": 0.0,
      "file": "sfx/city_far.wav",
      "db": -16
    },
    {
      "shot": "C13",
      "at": 0.5,
      "file": "sfx/silk_rustle.wav",
      "db": -12
    },
    {
      "shot": "C14",
      "at": 1.4,
      "file": "sfx/bottle_drop.wav",
      "db": -4
    },
    {
      "shot": "C15",
      "at": 5.0,
      "file": "sfx/city_far.wav",
      "db": -18
    },
    {
      "shot": "C15",
      "at": 6.6,
      "file": "sfx/sub_hit.wav",
      "db": -2
    },
    {
      "shot": "C16",
      "at": 0.0,
      "file": "sfx/pen_scratch.wav",
      "db": -6
    },
    {
      "shot": "C16",
      "at": 0.0,
      "file": "sfx/clock_tick.wav",
      "db": -14
    }
  ],
  "end_card": "images/CARD-ENDCARD.png",
  "end_card_s": 2.0,
  "characters": {
    "COLE_FOUNDER": {
      "face_ref": "images/CAST-COLE-03.png",
      "voice_ref": "voices/COLE.wav",
      "identity": "a 29 year old American man, 6'2\", athletic, chiseled jaw, warm hazel eyes, dark brown tousled hair, light natural stubble, white open collar shirt, tailored navy blazer"
    },
    "COLE_VALET": {
      "face_ref": "images/CAST-COLE-05.png",
      "voice_ref": "voices/COLE.wav",
      "identity": "the same man at 32, dark brown hair cropped short, heavier stubble, guarded hazel eyes, red valet vest over a white shirt, black bow tie"
    },
    "VIVIAN": {
      "face_ref": "images/CAST-VIVIAN-03.png",
      "voice_ref": "voices/VIVIAN.wav",
      "identity": "a 28 year old American woman, platinum blonde soft Hollywood waves, icy blue eyes, sculpted cheekbones, classic red lip"
    },
    "GRANT": {
      "face_ref": "images/CAST-GRANT-03.png",
      "voice_ref": "voices/GRANT.wav",
      "identity": "a 30 year old American man, golden blond swept hair, bright blue eyes, white smile, tan, chiseled jaw"
    },
    "CONCIERGE": {
      "face_ref": "images/CAST-CONCIERGE-01.png",
      "voice_ref": "voices/CONCIERGE.wav",
      "identity": "a pretty 30 year old American woman, dark hair in a neat low bun, warm brown eyes, charcoal hotel uniform blazer, pearl studs"
    }
  },
  "shots": [
    {
      "id": "C01",
      "pipeline": "i2v_25",
      "seed_group": "S1",
      "frames": 145,
      "start_image": "images/E01-K01.png",
      "cast": [
        "VIVIAN",
        "COLE_VALET"
      ],
      "shot": "medium close up",
      "visual": "A black tie gala ballroom under crystal chandeliers. A woman's hand in a silver sequined sleeve tilts a champagne flute over the head of a handsome valet in a red vest. Champagne pours over his hair and runs down his face and collar. He does not move or look away. His eyes stay calm, looking straight ahead. Behind him, soft and out of focus, guests laugh and hold up phones seen only from the back. Slow push in toward his face.",
      "light": "warm chandelier top light, gold rim on his wet hair, cool bounce from the room at the frame edges",
      "sounds": "champagne splashing on hair, a sharp gasp from the crowd, laughter building, phone camera shutter clicks, gala murmur, a string quartet stopping mid note",
      "out": "cut on the splash sound into C02",
      "lens": 50,
      "angle": "eye level"
    },
    {
      "id": "C02",
      "pipeline": "idlora_23",
      "seed_group": "S1",
      "frames": 97,
      "start_image": "images/E01-K02.png",
      "cast": [
        "VIVIAN"
      ],
      "speaker": "VIVIAN",
      "shot": "close up, three-quarter",
      "line": "Oops. Tip's included.",
      "visual": "Close up of a glamorous platinum blonde woman in a silver sequined gown holding an empty champagne flute at a black tie gala, three-quarter toward camera, looking down at someone just off camera.",
      "light": "warm key from camera left, diamonds catching light, chandelier bokeh behind",
      "sounds": "bright, sweet, mocking upper-class voice, close and clear, crowd laughter behind, gala room tone",
      "acting": "Before the first word her chin lifts and her eyes drop to him. On 'Oops' one corner of her red lip curls and her brows rise in fake innocence. On 'Tip's included' she tilts the empty flute toward him. After the last word she holds the small cruel closed-lip smile for a beat and lowers the glass. Delivery: light, sweet and sing-song on top, a cold flat drop on 'included', unhurried.",
      "lens": 85,
      "angle": "low"
    },
    {
      "id": "C02X",
      "pipeline": "i2v_25",
      "seed_group": "S1",
      "frames": 49,
      "start_image": "chain:C02",
      "continuation": true,
      "cast": [
        "VIVIAN"
      ],
      "shot": "close up, three-quarter",
      "visual": "Continuation of the same shot: the platinum blonde woman in a silver sequined gown is silent, mouth closed, she holds her small cruel smile, lowers the empty flute and turns her head slightly toward the laughing guests. Locked off camera, framing stays exactly as in the first frame, no cut, no zoom, nobody else enters the frame.",
      "light": "warm key from camera left, diamonds catching light, chandelier bokeh behind",
      "sounds": "crowd laughter, gala room tone",
      "out": "cut on her head turn into C03B"
    },
    {
      "id": "C03B",
      "pipeline": "i2v_25",
      "seed_group": "S1",
      "frames": 145,
      "start_image": "images/E01-K20.png",
      "cast": [
        "COLE_VALET"
      ],
      "shot": "extreme close up",
      "visual": "Extreme close up of the valet, champagne dripping from his hair down his face. He slowly lifts his eyes straight into the lens, completely calm. A single drop falls from his jaw. He breathes once, steady. Locked off camera.",
      "light": "gold chandelier rim, wet highlights on real skin with visible pores",
      "sounds": "the crowd fades to a muffled hum, a single drip, a low cello note begins",
      "edit": "CARD-E01-HOOK.png overlay from 0.5 s",
      "lens": 85,
      "angle": "eye level"
    },
    {
      "id": "T1",
      "pipeline": "flf_25",
      "seed_group": "S2",
      "frames": 145,
      "start_image": "chain:C03B",
      "end_image": "images/E01-K04.png",
      "continuation": true,
      "cast": [],
      "shot": "transition",
      "visual": "Champagne droplets drift and rise across the frame, catching gold light, turning into falling gold confetti as the camera lifts up and away in one continuous move, revealing a glass skyscraper lobby party far below: a champagne tower, gold confetti, a giant glowing blank LED wall with no text.",
      "light": "gold light catching every droplet, then warm amber party light",
      "sounds": "a soft rising whoosh, the cello note swells, the roar of a party fades in, a confetti cannon pop, glasses clinking",
      "out": "match transform, the time jump is carried by the move and the card",
      "edit": "CARD-E01-3YEARS.png fades in at 1 s, CARD-E01-SCREEN.png overlaid on the blank LED wall in the edit"
    },
    {
      "id": "C05",
      "pipeline": "idlora_23",
      "seed_group": "S2",
      "frames": 97,
      "start_image": "images/E01-K05.png",
      "cast": [
        "GRANT"
      ],
      "speaker": "GRANT",
      "shot": "close up, three-quarter",
      "line": "Brother. We did it.",
      "visual": "Close up of a handsome golden blond man in a navy suit and open white shirt holding a champagne flute at a glamorous launch party in a glass lobby, three-quarter toward camera, gold confetti drifting, looking at his best friend just off camera.",
      "light": "warm amber key, confetti catching light",
      "sounds": "warm, charming, excited male voice, close to the mic, party cheering behind",
      "acting": "Before the first word his eyes glisten and a disbelieving laugh catches in his chest. On 'Brother' his brows lift and he leans in. On 'We did it' his voice breaks into a breathy half laugh and he shakes his head slowly. After the last word he holds a proud grin and nods. Delivery: warm, low and close, thick with emotion, a catch of breath before 'did it'.",
      "lens": 85,
      "angle": "eye level"
    },
    {
      "id": "C05X",
      "pipeline": "i2v_25",
      "seed_group": "S2",
      "frames": 49,
      "start_image": "chain:C05",
      "continuation": true,
      "cast": [
        "GRANT"
      ],
      "shot": "close up, three-quarter",
      "visual": "Continuation of the same shot: the golden blond man is silent, mouth closed, beaming with proud disbelief, he laughs softly and lifts his champagne flute toward his friend just off camera. Locked off camera, framing stays exactly as in the first frame, no cut, no zoom, nobody else enters the frame.",
      "light": "warm amber key, confetti catching light",
      "sounds": "party cheering, glasses clinking"
    },
    {
      "id": "C06",
      "pipeline": "idlora_23",
      "seed_group": "S2",
      "frames": 105,
      "start_image": "images/E01-K06.png",
      "cast": [
        "COLE_FOUNDER"
      ],
      "speaker": "COLE_FOUNDER",
      "shot": "9:16 medium close up, three-quarter",
      "line": "We did. Where's Viv? She has to see this.",
      "visual": "Medium close up, head to mid torso, of a handsome dark haired man in a navy blazer and open white shirt at a launch party, three-quarter toward camera, oval anamorphic bokeh of party lights, looking at his friend just off camera.",
      "light": "warm key, oval anamorphic bokeh of party lights",
      "sounds": "warm, smooth, playful baritone, party behind him",
      "acting": "Before the first word a boyish grin pulls at one corner of his mouth. On 'We did' he nods once, warm. On 'Where's Viv' his eyes leave his friend and search the crowd over his shoulder. On 'She has to see this' the grin breaks wide but closed-lipped. After the last word he looks back at his friend, eyes bright. Delivery: smooth, happy, a little breathless, rising with excitement on 'see this'.",
      "lens": 65,
      "angle": "eye level"
    },
    {
      "id": "C06X",
      "pipeline": "i2v_25",
      "seed_group": "S2",
      "frames": 41,
      "start_image": "chain:C06",
      "continuation": true,
      "cast": [
        "COLE_FOUNDER"
      ],
      "shot": "close up, three-quarter",
      "visual": "Continuation of the same shot: the dark haired man is silent, mouth closed, grinning to himself, he lifts a chilled champagne bottle with a blank plain gold foil neck from a passing silver tray, tucks two empty flutes between his fingers, then glances toward the elevators. Locked off camera, framing stays exactly as in the first frame, no cut, no zoom, nobody else enters the frame.",
      "light": "warm key, oval anamorphic bokeh of party lights",
      "sounds": "glass clink, bottle lifted off a tray, party behind him",
      "out": "dissolve 12 f to the hotel lobby, the concierge room tone leads"
    },
    {
      "id": "C08A",
      "pipeline": "idlora_23",
      "seed_group": "S3",
      "frames": 105,
      "start_image": "images/E01-K08.png",
      "cast": [
        "CONCIERGE",
        "COLE_FOUNDER"
      ],
      "speaker": "CONCIERGE",
      "shot": "9:16 medium close up, three-quarter",
      "line": "Miss Draycourt went up to the penthouse suite.",
      "visual": "Medium close up, head to mid torso, of a pretty concierge in a charcoal uniform behind a dark wood and brass desk in a quiet luxury hotel lobby, three-quarter toward camera, looking at a guest just off camera.",
      "light": "warm brass lamp light, soft",
      "sounds": "polite warm female voice, quiet luxury hotel lobby, a piano far away",
      "acting": "Before the first word she gives a soft courteous smile. On 'Miss Draycourt' her head tilts slightly with a hint of knowing curiosity. On 'penthouse suite' her eyes glance upward toward the elevators. After the last word she holds the polite smile and gives a small nod. Delivery: warm, polite, professional, unhurried, quiet hotel volume.",
      "lens": 65,
      "angle": "eye level"
    },
    {
      "id": "C08AX",
      "pipeline": "i2v_25",
      "seed_group": "S3",
      "frames": 41,
      "start_image": "chain:C08A",
      "continuation": true,
      "cast": [
        "CONCIERGE"
      ],
      "shot": "close up, three-quarter",
      "visual": "Continuation of the same shot: the concierge is silent, mouth closed, she keeps her polite knowing smile and glances once more toward the elevators, then back to the guest. Locked off camera, framing stays exactly as in the first frame, no cut, no zoom, nobody else enters the frame.",
      "light": "warm brass lamp light, soft",
      "sounds": "quiet luxury hotel lobby, a piano far away"
    },
    {
      "id": "C08B",
      "pipeline": "idlora_23",
      "seed_group": "S3",
      "frames": 97,
      "start_image": "images/E01-K21.png",
      "cast": [
        "COLE_FOUNDER"
      ],
      "speaker": "COLE_FOUNDER",
      "shot": "9:16 medium close up, three-quarter",
      "line": "Perfect. Don't tell her I'm coming.",
      "visual": "Medium close up, head to mid torso, of the handsome dark haired man in a navy blazer leaning on a brass and dark wood concierge desk, three-quarter toward camera, brass lamps as bokeh, looking at the concierge just off camera.",
      "light": "warm lamp key, soft rim, brass lamps as bokeh",
      "sounds": "smooth, playful, low baritone, the concierge laughs softly",
      "acting": "Before the first word he leans in with a nervous excited half smile. On 'Perfect' his eyes light up. On 'Don't tell her' his voice drops and he glances around like a conspirator. After the last word he winks and raises one finger to his lips. Delivery: playful conspiratorial charm, low, lowered further on 'I'm coming'.",
      "lens": 65,
      "angle": "eye level"
    },
    {
      "id": "C08BX",
      "pipeline": "i2v_25",
      "seed_group": "S3",
      "frames": 49,
      "start_image": "chain:C08B",
      "continuation": true,
      "cast": [
        "COLE_FOUNDER"
      ],
      "shot": "close up, three-quarter",
      "visual": "Continuation of the same shot: the dark haired man is silent, he lowers his finger from his lips with a playful grin, taps the counter twice and pushes off the desk toward the elevators off camera right. Locked off camera, framing stays exactly as in the first frame, no cut, no zoom, nobody else enters the frame.",
      "light": "warm lamp key, soft rim, brass lamps as bokeh",
      "sounds": "a knuckle tap on wood, an elevator ding",
      "out": "cut on his turn, the elevator ding leads into C09"
    },
    {
      "id": "C09",
      "pipeline": "i2v_25",
      "seed_group": "S3",
      "frames": 121,
      "start_image": "images/E01-K09.png",
      "cast": [
        "COLE_FOUNDER"
      ],
      "shot": "medium, symmetrical",
      "visual": "The man stands inside a brass elevator holding a chilled champagne bottle and two empty flutes, smiling to himself, rocking gently on his heels, glancing down at the bottle, breathing out, eyes bright and excited. Near the end the two brass doors slide in and meet in the center.",
      "light": "warm brass interior light, darker lobby in front",
      "sounds": "elevator ding, doors sliding, soft hum",
      "out": "dissolve 12 f on the closing doors to the corridor",
      "lens": 35,
      "angle": "eye level"
    },
    {
      "id": "C10",
      "pipeline": "idlora_23",
      "seed_group": "S3",
      "frames": 121,
      "start_image": "images/E01-K10.png",
      "cast": [
        "COLE_FOUNDER"
      ],
      "speaker": "COLE_FOUNDER",
      "shot": "9:16 medium close up, three-quarter",
      "line": "Viv? We're public. Come celebrate.",
      "visual": "Medium close up, head to mid torso, of the dark haired man in a navy blazer in a dim luxury hotel corridor with warm sconces, three-quarter toward camera, a chilled champagne bottle and two empty flutes held at his chest, looking toward a door just off camera.",
      "light": "warm sconces in a rhythm down the walls",
      "sounds": "a soft playful half whisper, the muffled hum of the building, soft carpet footsteps far off",
      "acting": "Before the first word he takes a happy breath and leans toward the door. On 'Viv' his brows lift, playful. On 'We're public' a proud almost-smile flickers. On 'Come celebrate' he lifts the bottle a little. After the last word he waits, listening, the smile holding. Delivery: a soft playful half whisper, close to the mic, a surprise in his voice.",
      "lens": 65,
      "angle": "eye level"
    },
    {
      "id": "C12",
      "pipeline": "flf_25",
      "seed_group": "S4",
      "frames": 145,
      "start_image": "images/E01-K12.png",
      "end_image": "images/E01-K13.png",
      "cast": [
        "COLE_FOUNDER"
      ],
      "shot": "dolly zoom",
      "visual": "Close on the man's hand on a brass door handle, his face above it, the champagne bottle tucked under his other arm, his smile fading as he listens. He pushes the door open and stops in the doorway. Dolly zoom: his face grows larger in frame while the corridor behind him stretches away.",
      "light": "cold blue light from the room across his face, warm corridor behind",
      "sounds": "muffled laughter through the door, a woman's laugh, the door opening, then the room tone drains to near silence, one low heartbeat",
      "out": "cut on the heartbeat into C13",
      "lens": 40,
      "angle": "eye level"
    },
    {
      "id": "C13",
      "pipeline": "idlora_23",
      "seed_group": "S4",
      "frames": 97,
      "start_image": "images/E01-K14.png",
      "cast": [
        "VIVIAN"
      ],
      "speaker": "VIVIAN",
      "shot": "9:16 medium close up, three-quarter",
      "line": "Cole.",
      "visual": "Medium close up, head to mid torso, of a platinum blonde woman in a champagne silk robe sitting on the edge of a bed in a penthouse suite, a blond man in an open dress shirt soft and out of focus beside her, the Manhattan skyline in the windows, three-quarter toward camera, looking at the doorway just off camera.",
      "light": "cold city light through the windows, one warm bedside lamp",
      "sounds": "city far below, silk rustling, her voice cool and flat",
      "acting": "Before the first word her chin lifts and she holds his gaze, caught but not sorry. On 'Cole' a flicker of contempt pulls one corner of her mouth. After the word she stays still, eyes locked on him, and pulls the robe closer. Delivery: cool, flat, quiet, no apology.",
      "lens": 65,
      "angle": "eye level"
    },
    {
      "id": "C13X",
      "pipeline": "i2v_25",
      "seed_group": "S4",
      "frames": 49,
      "start_image": "chain:C13",
      "continuation": true,
      "cast": [
        "VIVIAN"
      ],
      "shot": "close up, three-quarter",
      "visual": "Continuation of the same shot: the platinum blonde woman is silent, mouth closed, she holds his gaze without blinking, her jaw sets, then she looks away toward the window. Locked off camera, framing stays exactly as in the first frame, no cut, no zoom, nobody else enters the frame.",
      "light": "cold city light through the windows, one warm bedside lamp",
      "sounds": "city far below, a slow breath"
    },
    {
      "id": "C14",
      "pipeline": "flf_25",
      "seed_group": "S4",
      "frames": 121,
      "start_image": "images/E01-K15.png",
      "end_image": "images/E01-K16.png",
      "cast": [],
      "shot": "low insert",
      "visual": "Low angle near the carpet: a chilled champagne bottle with a plain gold foil neck slips from a man's fingers, thuds onto thick carpet and rolls on its side, champagne foaming and glugging out into the carpet toward his shoes. Natural speed.",
      "light": "warm lamp glint on the wet glass, cold room light",
      "sounds": "a dull thud on carpet, then fizzing and glugging as the bottle rolls",
      "out": "cut on the last glug into C15",
      "lens": 50,
      "angle": "ground level"
    },
    {
      "id": "C15",
      "pipeline": "i2v_25",
      "seed_group": "S4",
      "frames": 169,
      "start_image": "images/E01-K17.png",
      "cast": [
        "COLE_FOUNDER"
      ],
      "shot": "extreme close up",
      "visual": "Extreme close up of the dark haired man's face. His jaw tightens. His eyes glass over. A tear gathers on his lower lid and he refuses to let it fall. He swallows. He does not look away. Locked off, then the faintest push in.",
      "light": "cold blue window light, a thin warm edge from the corridor behind",
      "sounds": "total silence except his breath, then a distant city siren and one low hit at the very end",
      "out": "0.5 s dissolve to the tag on the low hit",
      "lens": 85,
      "angle": "eye level"
    },
    {
      "id": "C16",
      "pipeline": "flf_25",
      "seed_group": "S5",
      "frames": 121,
      "start_image": "images/E01-K18.png",
      "end_image": "images/E01-K19.png",
      "cast": [],
      "shot": "top down insert",
      "visual": "Top down insert on a black marble desk: a black leather gloved hand signs a thick legal deed with a fountain pen, finishes the signature and lifts the pen. The deed's text is blurred and unreadable, no readable text anywhere.",
      "light": "one warm brass desk lamp, deep shadow",
      "sounds": "the scratch of a fountain pen, a clock ticking, one low piano note",
      "out": "0.5 s dissolve to the end card (the director does it)",
      "lens": 100,
      "angle": "top down"
    }
  ]
}
```
