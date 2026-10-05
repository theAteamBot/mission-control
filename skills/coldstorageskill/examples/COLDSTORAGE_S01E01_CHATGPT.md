# COLD STORAGE S01E01 "IPO Night": ChatGPT file

Upload this one file to ChatGPT (ideally a ChatGPT Project named COLD STORAGE). It has three parts, run in order:

1. **Part 1: Standing rules.** Follow them for everything in this file. Paste them into the Project instructions so later episodes inherit them.
2. **Part 2: Cast kit.** 33 cast photos. Skip any file that already exists in the Project.
3. **Part 3: Episode 1 images.** Keyframes, storyboard sheets, new looks, cover, text cards.

Deliver two zips: `COLDSTORAGE_CAST_KIT.zip` and `COLDSTORAGE_S01E01_IMAGES.zip`. **v3 rules (2026-10-03):** no readable text inside any image (signs, screens, documents blank, blurred, from the back or out of frame), phones from the back only, and every talking START frame is an emotion-matched 9:16 medium close up (face 16 to 18% of the height) with a soft closed mouth. **v4 (2026-10-05):** every image is native 9:16, cast photos included, and never too tight. These images get animated in ComfyUI (a second ChatGPT chat directs that with COLDSTORAGE_S01E01_COMFYUI.md), so realism and identity here decide the whole episode: if a face looks even slightly plastic or off model, regenerate it.

---

# PART 1: STANDING RULES

You are the image department for **COLD STORAGE**, an ultra-realistic 9:16 vertical betrayal, romance, revenge drama set in Manhattan, Queens and the Hamptons. Claude writes the story and gives you image packs (`COLDSTORAGE_S01_..._CHATGPT_PACK.md`). Your only job: make exactly the images a pack lists, to its standards. Never change the story, dialogue, characters or shot plan.

## When I upload a pack

1. Read the whole pack first.
2. **Never regenerate a file that already exists in this Project** (same filename). Reuse it as the face and costume reference. Only make what's missing. If unsure, list what exists and ask me once.
3. Tell me your plan in 3 to 5 lines, then run everything in **one continuous pass**. Never stop to ask "shall I continue?"
4. Deliver every file with its exact filename, zipped in the pack's folder layout, plus `00_QA_REPORT.md`.

## The cast (faces never change)

| Name | Saved character | Fixed look |
|---|---|---|
| Cole Harlan | Cole | American man, 29 then 32, 6'2", athletic, chiseled jaw, warm hazel eyes, dark brown hair. Four looks: FOUNDER (tousled hair, white open collar shirt, navy blazer), ROCK BOTTOM (grown out hair, soaked gray hoodie), VALET (cropped hair, red valet vest, black bow tie), VAULT (slicked back hair, black three piece suit, black leather gloves) |
| Sienna Hollis | Sienna | American woman, 29, long dark brown waves, green eyes, olive skin, black blazer, white tee |
| Vivian Draycourt | Vivian | American woman, 28, platinum blonde Hollywood waves, icy blue eyes, red lip, silver sequined gown, diamonds |
| Grant Kessler | Grant | American man, 30, golden blond, blue eyes, white smile, navy suit, no tie |
| Richard Draycourt | Richard | American man, 58, silver swept back hair, steel gray eyes, charcoal suit, gold cufflinks |
| Tyler Draycourt | Tyler | American man, 31, dark hair, smirk, open black silk shirt, gold chain |
| Nico Vargas | Nico | Latino American man, 29, curly hair, backwards cap, gray hoodie, headphones |
| Mr. Hale | Hale | American man, 55, gray buzz cut, black suit, earpiece |
| Ruth Bell | Ruth | Black American woman, 64, silver curls, reading glasses on a chain, navy staff cardigan |
| Grace Harlan | Grace | American woman, 58, silver-streaked hair, hazel eyes (Cole's eyes), cream cardigan |

**CHARACTER LOCK:** every person looks exactly like their cast photo and the pack's IDENTITY LOCK line: same face, hair, skin tone, age, build, eye colour. Nobody goes bald. No hairstyle changes. Cole wears exactly the look named on the WHO line. If a photo and the IDENTITY LOCK line disagree, the line wins.

## Look: real life, beautiful people

- **Realism:** every image must look like a still from a real live action drama, never AI. Real skin with pores, fine lines and tiny imperfections, real hair with flyaways, real fabric with creases, practical light, shallow depth of field, natural color, subtle film grain.
- **Beauty:** everyone is movie-star attractive the way real actors look on an unfiltered set photo. Beauty from bone structure, light and confidence, never from retouching. Always tasteful and fully clothed.
- **Never:** airbrushed or waxy skin, beauty filters, perfect symmetry, glossy CGI look, HDR, oversaturation, illustration.
- **Cinematic:** shot like a Hollywood feature on ARRI Alexa 35 with Cooke primes. Every SHOT line starts with the lens and angle; use exactly what it says.

## Framing: native 9:16, not too close (David, 2026-10-05)

- **Every image is composed for a tall 9:16 frame** (1080 x 1920 minimum), never a 4:5 or square crop. If your tool can't output 9:16, generate the tallest ratio it offers with extra room above and below, then crop to 9:16 with Python. Never stretch.
- **Default is the 9:16 medium close up:** head to mid torso, air on both sides of the shoulders, top of the head about 300 px from the top, eyes on the upper third line (about 640 px), **face 16 to 18% of the frame height**. Hands and body language read.
- **Close up (face 22 to 25%) only when the SHOT line says close up.** Extreme close up only when it says so. **When in doubt, go one size wider.** Too tight is the most common mistake.
- **Medium (waist up, face 10 to 12%)** for arrivals and two people stacked in depth. **Full or wide (head to toe)** only when the SHOT line asks.
- **Depth, not width:** never two faces side by side. Two people = one soft in the foreground low in frame, one sharp behind.
- **Safe zones (1080 x 1920):** no faces or key action in the top 13% (250 px), the bottom 22% (420 px) or the right 8% (90 px). Faces live in the center.

## No text, no phone screens (David, 2026-10-03)

- **No readable text inside any picture.** AI garbles text. Signs, screens, monitors, documents, letters, labels, name tags, menus and headlines are blank, blurred, seen from the back or out of frame.
- **Phones are seen from the back only,** never a lit screen.
- Every word the story needs (captions, "three years earlier", a text message, a headline, Vault cards) is made with **Python as a clean overlay**, never generated inside an image.

## Talking keyframes (START frames for lines)

- One speaker, a 9:16 medium close up (head to mid torso, face 16 to 18% of frame height) unless the SHOT line says close up, three-quarter to camera, eyes on the listener just off camera.
- **The face already shows the line's opening emotion** (brows, eye tension, lip press or jaw set), identity exactly as the cast photo, **mouth soft and closed**. Never open-mouth, mid-word, outstretched arms or a blank neutral face.

## Order of work

1. **Part A cast photos** (only missing ones): **native 9:16, 1080 x 1920 minimum**, plain warm gray studio backdrop. Full body photos are head to toe filling the tall frame with a little air above the head and below the feet. The `-03` face reference is a **9:16 medium close up** (head to mid torso, face 16 to 18% of the height, three-quarter), never a tight headshot. **Clean files, no label strip** (ComfyUI uses them as references). Labels go on a separate Python index sheet `00_INDEX/CAST_INDEX.png`: thumbnails with `NAME | saved character "Name" | look` under each.
2. **Part B storyboard sheets** in STORYBOARD INDEX order: one generation per sheet, a 3 x 2 grid of six vertical 9:16 panels, thin white gutters, an empty black strip under each panel. Add the labels in the black strips with Python (line 1: ID · role · caption, line 2: WHO: ...). Never draw text inside a panel. Never generate a single frame on its own.
3. **Part C covers:** 9:16, one huge emotional face, the villain small behind, overlay text added with Python exactly as written, EP number bottom left.
4. **Part D VAULT CARDS:** Python only, never image generation. Black glass background, thin gold rule, white serif headline, small gray caps, 1080 x 1920 top band layout. Types: ACQUIRED, DEAL KILLED, LOAN CALLED, EVICTED, BALANCE, STOCK, EXPOSED, BANKRUPT.

## QA every image, zoomed in

Identity match, correct look for the scene, two arms, five fingers per hand, no cut-off heads, no readable text inside pictures (signs, screens, documents blank or blurred), phones from the back only, talking frames emotion-matched with a closed mouth, no guns, no gore, faces in the centre band, real skin. Fix or regenerate anything that fails. Log it in `00_QA_REPORT.md`. No em dashes or en dashes in any label.

---

# PART 2: CAST KIT

## 0. INSTRUCTIONS

You are the image department for COLD STORAGE, an ultra-realistic 9:16 vertical betrayal, romance, revenge drama set in Manhattan, Queens and the Hamptons. Make exactly the images below, nothing else.

1. Read this whole pack first. Tell me your plan in 3 to 5 lines, then run everything in **one continuous pass**. Never stop to ask "shall I continue?"
2. **One generation per photo.** Native 9:16, 1080 x 1920 minimum (2160 x 3840 if you can), photoreal.
3. **Faces lock after the first photo of each character.** Every later photo of that character (back view, close up, other looks) is made from their `-01` photo as the face reference. Same face, bone structure, eye colour, skin tone, hair. Nobody goes bald. No hairstyle changes unless the look says so.
4. **No text inside any photo, and no label strip.** The files stay clean because ComfyUI uses them as references. Build `00_INDEX/CAST_INDEX.png` with Python: thumbnails with `NAME | saved character "Name" | look` under each.
5. **QA every image zoomed in:** identity match, correct outfit for the look, two arms, five fingers per hand, no cut-off heads, no extra people, no text in the picture, real skin (pores, not plastic). Fix or regenerate anything that fails.
6. Deliver one zip, `COLDSTORAGE_CAST_KIT.zip`, in the manifest layout, plus `00_QA_REPORT.md` listing every file and its pass/fail.

## 1. MANIFEST

```
COLDSTORAGE_CAST_KIT/
  00_INDEX/00_QA_REPORT.md
  01_CAST/COLE/     CAST-COLE-01.png ... CAST-COLE-06.png
  01_CAST/SIENNA/   CAST-SIENNA-01.png ... -03
  01_CAST/VIVIAN/   CAST-VIVIAN-01.png ... -03
  01_CAST/GRANT/    CAST-GRANT-01.png ... -03
  01_CAST/RICHARD/  CAST-RICHARD-01.png ... -03
  01_CAST/TYLER/    CAST-TYLER-01.png ... -03
  01_CAST/NICO/     CAST-NICO-01.png ... -03
  01_CAST/HALE/     CAST-HALE-01.png ... -03
  01_CAST/RUTH/     CAST-RUTH-01.png ... -03
  01_CAST/GRACE/    CAST-GRACE-01.png ... -03
```
Total: 33 photos.

## 2. GLOBAL LOOK (append to every prompt below)

**BEAUTY:** `genuinely very attractive the way a real movie star looks on an unfiltered set photo: great bone structure, striking eyes, healthy skin, natural expression. Beautiful because of the face, the light and the confidence, never because of retouching. Tasteful and fully clothed.`

**REALISM:** `a real photograph of a real person, not AI, not a render. Shot on ARRI Alexa 35, 50mm Cooke prime, soft natural key light with a gentle rim. True-to-life skin: visible pores, fine lines, faint under-eye texture, a few tiny moles or freckles, natural oil sheen, peach fuzz catching the light. Real hair with flyaways. Real fabric with creases. Slight natural facial asymmetry. Accurate hands, five fingers. Natural muted color, true skin tones, subtle film grain. NEVER: airbrushed skin, beauty filter, plastic or waxy skin, perfect symmetry, glossy CGI look, oversaturated color, HDR, illustration, text, watermark.`

**CAST PHOTO RULES:** full body photos are head to toe on a plain warm gray studio backdrop with soft even light, so the reference is clean. The `-03` face reference is a 9:16 medium close up: head to mid torso, face 16 to 18% of the frame height, air on both sides of the shoulders, three-quarter, same backdrop. Never a tight headshot.

## 3. CAST AND LOOK LEDGER

| Character | Saved character | Age | Looks in this kit | Photos |
|---|---|---|---|---|
| Cole Harlan | "Cole" | 29 then 32 | FOUNDER, ROCK BOTTOM, VALET, VAULT | 01 to 06 |
| Sienna Hollis | "Sienna" | 29 | BLAZER | 01 to 03 |
| Vivian Draycourt | "Vivian" | 28 | GALA GOWN | 01 to 03 |
| Grant Kessler | "Grant" | 30 | NAVY SUIT | 01 to 03 |
| Richard Draycourt | "Richard" | 58 | CHARCOAL SUIT | 01 to 03 |
| Tyler Draycourt | "Tyler" | 31 | SILK SHIRT | 01 to 03 |
| Nico Vargas | "Nico" | 29 | HOODIE | 01 to 03 |
| Mr. Hale | "Hale" | 55 | BLACK SUIT | 01 to 03 |
| Ruth Bell | "Ruth" | 64 | STAFF CARDIGAN | 01 to 03 |
| Grace Harlan | "Grace" | 58 | CARDIGAN | 01 to 03 |

## 4. PART A: CAST PHOTOS

### 🎨 CAST-COLE-01: Full body front, FOUNDER look · 9:16 · **Save as `CAST-COLE-01.png`**
A breathtakingly handsome 29 year old American man, 6'2", lean athletic build, strong jawline and cheekbones, warm hazel eyes, thick dark brown tousled hair, a few days of natural stubble, an easy knowing smile, crisp white open collar shirt, tailored navy blazer, dark trousers, brown leather shoes. Standing relaxed, one hand in pocket, head to toe, facing camera.

### 🎨 CAST-COLE-02: Full body back, FOUNDER look · 9:16 · **Save as `CAST-COLE-02.png`**
Same man, same outfit and hair, from behind, head to toe, head turned slightly so the jaw profile shows. Face reference: CAST-COLE-01.

### 🎨 CAST-COLE-03: Face reference, 9:16 medium close up, three-quarter · 9:16 · **Save as `CAST-COLE-03.png`**
Same man, 9:16 medium close up from head to mid torso, face about 17% of the frame height, three-quarter angle, warm half smile, eyes to lens, white shirt and navy blazer. Face reference: CAST-COLE-01.

### 🎨 CAST-COLE-04: Full body front, ROCK BOTTOM look · 9:16 · **Save as `CAST-COLE-04.png`**
The same man at 32, thinner, dark hair grown out and uncut, heavier stubble, tired hazel eyes, still handsome under the exhaustion. A worn gray hoodie darkened by rain, faded black jeans, scuffed sneakers, holding one cardboard box. Head to toe. Face reference: CAST-COLE-01.

### 🎨 CAST-COLE-05: Full body front, VALET look · 9:16 · **Save as `CAST-COLE-05.png`**
The same man at 32, dark brown hair cropped short, sculpted jaw under stubble, warm but guarded hazel eyes, fitted red valet vest over a white shirt, black bow tie, black trousers, black shoes, a valet key ring in one hand. Head to toe. Face reference: CAST-COLE-01.

### 🎨 CAST-COLE-06: Full body front, VAULT look · 9:16 · **Save as `CAST-COLE-06.png`**
The same man at 32 at his most devastating, dark brown hair slicked back, clean shaven, calm piercing hazel eyes, a sharply tailored black three piece suit, black shirt, no tie, black leather gloves, one old steel watch. Head to toe. Face reference: CAST-COLE-01.

### 🎨 CAST-SIENNA-01: Full body front · 9:16 · **Save as `CAST-SIENNA-01.png`**
A stunningly beautiful 29 year old American woman, long glossy dark brown waves, striking green eyes, olive skin with a natural glow, high cheekbones, full lips, natural makeup, fitted black blazer over a white tee, tailored black trousers, black ankle boots, a slim watch. Confident and warm. Head to toe.
**CAST-SIENNA-02:** same, full body back, head turned slightly. **CAST-SIENNA-03:** same, 9:16 medium close up, head to mid torso, three-quarter, a skeptical half smile.

### 🎨 CAST-VIVIAN-01: Full body front · 9:16 · **Save as `CAST-VIVIAN-01.png`**
A dazzlingly glamorous 28 year old American woman, platinum blonde hair in soft Hollywood waves, icy blue eyes, sculpted cheekbones, a classic red lip, a silver sequined couture gown, diamond necklace, silver heels. Poised, a faint superior smile. Head to toe.
**-02:** full body back. **-03:** 9:16 medium close up, head to mid torso, three-quarter, cool amused stare.

### 🎨 CAST-GRANT-01: Full body front · 9:16 · **Save as `CAST-GRANT-01.png`**
A strikingly handsome 30 year old American man, golden blond swept hair, bright blue eyes, a bright white smile, sun kissed skin, chiseled jaw, fitted navy designer suit, white shirt, no tie, loafers. Easy golden boy charm. Head to toe.
**-02:** full body back. **-03:** 9:16 medium close up, head to mid torso, three-quarter, charming smile that doesn't reach his eyes.

### 🎨 CAST-RICHARD-01: Full body front · 9:16 · **Save as `CAST-RICHARD-01.png`**
A devastatingly handsome 58 year old American silver fox, thick silver swept back hair, chiseled features, steel gray eyes, trim and powerful, bespoke charcoal three piece suit, white shirt, dark tie, gold cufflinks. Perfectly still. Head to toe.
**-02:** full body back. **-03:** 9:16 medium close up, head to mid torso, three-quarter, unreadable calm.

### 🎨 CAST-TYLER-01: Full body front · 9:16 · **Save as `CAST-TYLER-01.png`**
A dangerously attractive 31 year old American man, thick dark hair, dark eyes, sharp jaw, a lazy cruel smirk, open black silk shirt, thin gold chain, cream trousers, suede loafers, designer sunglasses in hand. Head to toe.
**-02:** full body back. **-03:** 9:16 medium close up, head to mid torso, three-quarter, smirking.

### 🎨 CAST-NICO-01: Full body front · 9:16 · **Save as `CAST-NICO-01.png`**
A very good looking 29 year old Latino American man, curly dark hair under a backwards black cap, warm brown eyes, dimpled grin, fit build, gray hoodie, black joggers, clean white sneakers, headphones around his neck. Head to toe.
**-02:** full body back. **-03:** 9:16 medium close up, head to mid torso, three-quarter, mid laugh.

### 🎨 CAST-HALE-01: Full body front · 9:16 · **Save as `CAST-HALE-01.png`**
A distinguished, handsome 55 year old American man, gray buzz cut, strong jaw, calm gray eyes, broad shouldered, immaculate black suit, white shirt, black tie, clear coil earpiece, hands folded in front. Head to toe.
**-02:** full body back. **-03:** 9:16 medium close up, head to mid torso, three-quarter, perfectly neutral.

### 🎨 CAST-RUTH-01: Full body front · 9:16 · **Save as `CAST-RUTH-01.png`**
A lovely 64 year old Black American woman, silver natural curls, warm brown eyes, laugh lines, reading glasses on a beaded chain, navy hotel staff cardigan over a white blouse, black slacks, comfortable shoes, holding a thermos. Warm, sharp, knowing. Head to toe.
**-02:** full body back. **-03:** 9:16 medium close up, head to mid torso, three-quarter, teasing smile over her glasses.

### 🎨 CAST-GRACE-01: Full body front · 9:16 · **Save as `CAST-GRACE-01.png`**
A beautiful, elegant 58 year old American woman, soft silver-streaked brown hair, kind hazel eyes (the same eyes as Cole), warm smile, cream knit cardigan over a pale blue blouse, soft gray trousers, flats. Head to toe.
**-02:** full body back. **-03:** 9:16 medium close up, head to mid torso, three-quarter, proud gentle smile.

## 5. FINAL CHECK

Before zipping: Cole's four looks are clearly the same man. Grace and Cole share the same hazel eyes. Every photo has its black strip. No text inside any photo. 33 files.

---

# PART 3: EPISODE 1 IMAGES

## 0. INSTRUCTIONS

Follow Part 1. This pack feeds a **local ComfyUI pipeline (LTX-2.5 and LTX-2.3)**, so it's different from a normal storyboard pack in one way:

- **Every keyframe is its own full resolution image** (9:16, 1080 x 1920 minimum, 2160 x 3840 if you can). ComfyUI animates each one directly, so it must be clean: **no label strip, no text, no border** on keyframes.
- After all keyframes are done, **also build the storyboard sheets** from them with Python (6 per sheet, labels in black strips below), as the overview.

Rules:
1. Read the whole pack. Plan in 3 to 5 lines. Run everything in one continuous pass.
2. Reuse existing cast photos as face references (CAST-COLE-01, -05, CAST-VIVIAN-01, CAST-GRANT-01). Never regenerate an existing file.
3. **Cole must be the same man in every frame.** VALET look in K01 only, FOUNDER look everywhere else.
4. If your image tool can't output 9:16 directly, generate at the tallest ratio it offers with extra headroom and crop to 9:16 with Python. Never stretch.
5. Composition: native 9:16, faces in the center, eyes on the upper third line, nothing important in the top 13%, bottom 22% or right 8% (platform UI and captions go there).
6. QA every keyframe zoomed: identity, look, hands, no readable text anywhere (signs, screens, documents, labels blank or blurred), phones from the back only, real skin. Talking START frames (K02, K05, K06, K08, K10, K14, K21): one speaker, a 9:16 medium close up (head to mid torso, face 16 to 18% of the height) except K02 and K05, which keep their approved close ups, three-quarter, the line's opening emotion on the face, mouth soft and closed. Fix or regenerate.
7. Deliver `COLDSTORAGE_S01E01_IMAGES.zip` in the manifest layout plus `00_QA_REPORT.md`.

## 1. MANIFEST

```
COLDSTORAGE_S01E01_IMAGES/
  00_INDEX/00_QA_REPORT.md
  01_CAST/           CAST-VIVIAN-04.png, CAST-GRANT-04.png, CAST-CONCIERGE-01.png
  02_KEYFRAMES/      E01-K01.png ... E01-K21.png   (clean, 9:16, no text)
  03_STORYBOARD/     E01-SHEET-1.png ... E01-SHEET-4.png   (Python, labeled)
  04_COVER/          COVER-E01.jpg
  05_CARDS/          CARD-E01-HOOK.png, CARD-E01-3YEARS.png, CARD-E01-SCREEN.png, CARD-ENDCARD.png
```

## 2. GLOBAL LOOK (append to every keyframe prompt)

`A real film still from a live action prestige drama, not AI, not a render. Vertical 9:16. Shot on ARRI Alexa 35 with Cooke anamorphic lenses, shallow depth of field, practical motivated light, light atmospheric haze. True-to-life skin: pores, fine lines, faint under-eye texture, tiny imperfections, natural sheen. Real hair with flyaways. Real fabric with creases. Natural muted color, true skin tones, subtle 35mm grain. Everyone is movie-star attractive the way real actors look on an unfiltered set photo. Tasteful. NEVER: airbrushed or waxy skin, beauty filter, perfect symmetry, CGI gloss, HDR, oversaturation, illustration, text, watermark, extra fingers.`

**Color script for this episode:** K01 to K03 gala: warm chandelier gold with cool bounce from the room (phones only from the back, no screen glow). K04 to K12 IPO party and hotel: warm amber and gold. K13 to K19 the betrayal: warm turning cold, blue city light through the suite window. K20 tag: black marble, one warm lamp.

## 3. CAST, LOOKS, LOCATIONS

| Who | Look this episode | Reference |
|---|---|---|
| COLE | VALET (K01 only), FOUNDER (all else) | CAST-COLE-05, CAST-COLE-01 |
| VIVIAN | GALA GOWN (K01 to K03), SILK ROBE (K16 to K18) | CAST-VIVIAN-01, new CAST-VIVIAN-04 |
| GRANT | NAVY SUIT (K05, K06), DRESS SHIRT OPEN AT COLLAR (K16 to K17) | CAST-GRANT-01, new CAST-GRANT-04 |
| CONCIERGE | Hotel uniform | new CAST-CONCIERGE-01 |

**IDENTITY LOCK (paste the matching lines into every keyframe with that person):**
- COLE FOUNDER: `29 year old American man, 6'2", athletic, chiseled jaw, warm hazel eyes, dark brown tousled hair, light natural stubble, white open collar shirt, tailored navy blazer`
- COLE VALET: `same man at 32, dark brown hair cropped short, heavier stubble, guarded hazel eyes, red valet vest over white shirt, black bow tie`
- VIVIAN: `28 year old American woman, platinum blonde soft Hollywood waves, icy blue eyes, sculpted cheekbones, classic red lip`
- GRANT: `30 year old American man, golden blond swept hair, bright blue eyes, perfect white smile, tan, chiseled jaw`

**Locations:** THE DRAYCOURT GRAND BALLROOM (crystal chandeliers, black tie crowd, marble). PAXWELL LOBBY (glass skyscraper lobby at night, giant blank LED wall, champagne tower, confetti). HOTEL CONCIERGE DESK (dark wood, brass, warm lamps). PENTHOUSE CORRIDOR (dim, warm sconces, long carpet runner). PENTHOUSE SUITE (floor to ceiling windows, Manhattan night skyline, warm lamps, white bedding). VAULT OFFICE (black marble desk, one brass lamp).

**Props:** a chilled champagne bottle with a blank plain gold foil neck (no label, no text) and two empty flutes. A thick legal deed with a fountain pen (its text always blurred and unreadable). Champagne flutes.

## 4. PART A: NEW LOOK PHOTOS

### 🎨 CAST-VIVIAN-04: Full body front, SILK ROBE look · 9:16 · Save as `CAST-VIVIAN-04.png`
Same woman as CAST-VIVIAN-01, platinum hair slightly tousled, a champagne silk robe tied at the waist, fully covered, barefoot, a thin diamond bracelet. Plain warm gray studio backdrop, head to toe.

### 🎨 CAST-GRANT-04: Full body front, OPEN SHIRT look · 9:16 · Save as `CAST-GRANT-04.png`
Same man as CAST-GRANT-01, white dress shirt with the top three buttons undone, sleeves loose, navy suit trousers, barefoot, hair slightly messed. Studio backdrop, head to toe.

### 🎨 CAST-CONCIERGE-01: Full body front · 9:16 · Save as `CAST-CONCIERGE-01.png`
A pretty 30 year old American woman hotel concierge, dark hair in a neat low bun, warm brown eyes, charcoal hotel uniform blazer with a small brass name bar (blank, no text), pearl studs. Studio backdrop, head to toe.

## 5. PART B: KEYFRAMES (clean, 9:16, one image each)

Each keyframe is the FIRST frame of a ComfyUI clip (END frames are marked). Same clip IDs as the ComfyUI file.

### E01-K01 · START · C01 · Save as `E01-K01.png`
WHO: VIVIAN (gala gown, left edge, only her hand and glass fully in frame, face partly visible) · COLE (VALET, centre)
SHOT: 50mm, eye level, tight medium close up on Cole, stacked 9:16 framing.
ACTION: A champagne flute tilted above Cole's head, the first stream of champagne just leaving the rim. Cole stands perfectly still, eyes calm, looking straight ahead, not at her.
SETTING: Draycourt Grand ballroom, chandeliers blurred into gold bokeh above him.
LIGHT: warm chandelier top light, a rim from the chandeliers on his hair, cool room bounce on the edges of frame. Guests behind him hold phones seen only from the back.

### E01-K02 · START · C02 · Save as `E01-K02.png`
WHO: VIVIAN (gala gown, centre)
SHOT: 85mm, slightly low angle, close up, three-quarter.
ACTION: Vivian holds the empty flute, chin lifted, eyes dropped to him, a small cruel amused closed-lip smile already on her face (the opening emotion of her line), mouth soft and closed. Face about 25% of frame height.
SETTING: ballroom, chandeliers as soft gold bokeh behind her head.
LIGHT: warm key from camera left, diamonds catching light.

### E01-K03 · START · C03 · Save as `E01-K03.png`
WHO: GUESTS (black tie, three in foreground, crowd behind)
SHOT: 35mm, eye level, stacked depth: three phones held up in the foreground low in frame, seen only from the back (plain dark phone backs, no screens visible), laughing faces in the middle, chandeliers above.
ACTION: Guests filming and laughing. No phone screen is visible anywhere. (v3: this frame is now a reference for the background of C01; it is not its own shot.)
LIGHT: warm gold chandeliers above, soft cool room bounce on faces (no screen glow).

### E01-K04 · START · C04 · Save as `E01-K04.png`
WHO: none (crowd far below)
SHOT: 24mm, high overhead looking down from a mezzanine, vertical: a champagne tower in the lower third, the party crowd around it, confetti hanging in the air.
SETTING: Paxwell lobby, glass skyscraper at night, a giant blank glowing LED wall on the right (no text, it gets filled in the edit).
LIGHT: warm amber practicals, cool city light through the glass.

### E01-K05 · START · C05 · Save as `E01-K05.png`
WHO: GRANT (navy suit, centre, three-quarter to camera)
SHOT: 85mm, eye level, close up, head and chest, face about 25% of frame height, Cole off camera right.
ACTION: Grant holding a champagne flute, eyes glistening with proud disbelief, brows slightly raised, the beginning of a disbelieving smile, lips closed, looking at Cole just off camera. Gold confetti drifting.
SETTING: Paxwell lobby party, confetti falling, bokeh behind.
LIGHT: warm amber key, confetti catching light.

### E01-K06 · START · C06 · Save as `E01-K06.png`
WHO: COLE (FOUNDER, centre)
SHOT: 65mm, eye level, 9:16 medium close up, head to mid torso, face about 17% of frame height, three-quarter, eyes on the upper third line.
ACTION: Cole with a secret grin pulling at one corner of his mouth, boyish and nervous, lips closed, looking at Grant just off camera, his eyes about to search the crowd for Vivian.
LIGHT: warm key, oval bokeh of party lights behind.

### E01-K07 · START · C07 · Save as `E01-K07.png`
WHO: COLE (FOUNDER, hand only)
SHOT: 100mm macro insert.
ACTION: Cole's hand lifting a chilled champagne bottle with a blank plain gold foil neck off a silver tray, two empty flutes between his fingers. (Not its own shot; the bottle grab plays in the C06X continuation. Make it only as a reference.)
LIGHT: warm, shallow focus, confetti out of focus.

### E01-K08 · START · C08 · Save as `E01-K08.png`
WHO: CONCIERGE (behind the desk, centre, three-quarter to camera)
SHOT: 65mm, eye level, 9:16 medium close up, head to mid torso, face about 17% of frame height, Cole off camera.
ACTION: The concierge with a soft courteous smile and a hint of knowing curiosity, lips closed, looking at Cole just off camera. Her brass name bar is blank, no text.
SETTING: hotel concierge desk, dark wood, brass lamps.
LIGHT: warm lamp light, soft.

### E01-K09 · START · C09 · Save as `E01-K09.png`
WHO: COLE (FOUNDER, centre, inside elevator)
SHOT: 35mm, eye level, symmetrical, through elevator doors half closed.
ACTION: Cole inside a brass elevator holding the champagne bottle and two flutes, smiling to himself, the doors closing from both sides.
LIGHT: warm brass interior light, darker lobby in front.

### E01-K10 · START · C10 · Save as `E01-K10.png`
WHO: COLE (FOUNDER, centre, three-quarter to camera)
SHOT: 65mm, eye level, 9:16 medium close up, head to mid torso with the bottle and flutes in frame, face about 17% of frame height, the dim corridor and warm sconces soft behind him.
ACTION: Cole holding the champagne bottle and two empty flutes at his chest, leaning toward a door just off camera, a playful hopeful almost-smile, mouth soft and closed, brows lifted.
LIGHT: warm sconces in a rhythm down the walls, a door at the far end.

### E01-K11 · START · C11 · Save as `E01-K11.png`
WHO: COLE (FOUNDER, hand and face)
SHOT: 50mm, close up, stacked: his hand on a brass door handle low in frame, his face above, listening.
ACTION: Cole stops with his hand on the handle, smile fading, head tilted: he's heard something through the door. (v3: reference only; this beat now opens C12.)
LIGHT: warm sconce side light, darker door.

### E01-K12 · START · C12 · Save as `E01-K12.png`
WHO: COLE (FOUNDER, centre)
SHOT: 40mm, eye level, medium close up, framed in a doorway, the room's cold light spilling on his face.
ACTION: Cole just after pushing the door open, frozen, eyes widening.
LIGHT: warm corridor behind him, cold blue suite light on his face.

### E01-K13 · END · C12 · Save as `E01-K13.png`
Same camera position and framing as K12, but tighter (as if the lens zoomed in while the camera pulled back): Cole's face larger in frame, the corridor behind him stretched and distant. Make it by editing K12.

### E01-K14 · START · C13 · Save as `E01-K14.png`
WHO: VIVIAN (SILK ROBE, centre, three-quarter to camera) · GRANT (OPEN SHIRT, soft and out of focus beside her)
SHOT: 65mm, eye level, 9:16 medium close up on Vivian, head to mid torso, face about 17% of frame height, the Manhattan skyline in the tall window behind.
ACTION: Vivian on the edge of the bed, fully covered in the robe, chin lifted, caught but not sorry, a flicker of contempt at one corner of her mouth, lips closed, eyes locked on the doorway just off camera.
LIGHT: cold blue city light through the windows, one warm bedside lamp.
TASTEFUL: fully covered, no nudity, nothing suggestive beyond the embrace.

### E01-K15 · START · C14 · Save as `E01-K15.png`
WHO: COLE (FOUNDER, hand only)
SHOT: low angle close to the carpet, 50mm.
ACTION: The chilled champagne bottle mid-fall, just leaving Cole's open fingers, the blank gold foil neck catching the light.
LIGHT: warm lamp glint on the wet glass, cold room light.

### E01-K16 · END · C14 · Save as `E01-K16.png`
Same camera: the bottle on its side on the carpet, champagne foaming out into a dark wet patch spreading toward Cole's shoes, out of focus behind it.

### E01-K17 · START · C15 · Save as `E01-K17.png`
WHO: COLE (FOUNDER, centre)
SHOT: 85mm anamorphic, extreme close up, eyes in the upper third.
ACTION: Cole's face breaking: jaw tight, eyes glassing over, one tear held on the lower lid, not falling.
LIGHT: cold blue window light, a thin warm edge from the corridor behind.

### E01-K18 · START · C16 · Save as `E01-K18.png`
WHO: none (a black gloved hand)
SHOT: 100mm, top down insert, vertical.
ACTION: A black leather gloved hand holding a fountain pen above the signature line of a thick legal deed on black marble. The deed's text is blurred and unreadable.
LIGHT: one warm brass desk lamp, deep shadow.

### E01-K19 · END · C16 · Save as `E01-K19.png`
Same camera: the signature finished, the pen lifted. Edit K18.

### E01-K21 · START · C08B · Save as `E01-K21.png`
WHO: COLE (FOUNDER, centre, leaning on the concierge desk)
SHOT: 65mm, eye level, 9:16 medium close up, head to mid torso, face about 17% of frame height, three-quarter, the concierge's shoulder soft in the foreground low in frame.
ACTION: Cole leaning in with a nervous excited half smile, eyes lit up, lips closed, looking at the concierge just off camera (the wink and finger to the lips come after the line, in the render).
SETTING: concierge desk, brass lamps as warm bokeh.
LIGHT: warm lamp key, soft rim.

### E01-K20 · START · C03B (hook close up) · Save as `E01-K20.png`
WHO: COLE (VALET, centre)
SHOT: 85mm, extreme close up.
ACTION: Champagne running down Cole's face and collar, eyes open and completely calm, looking straight into the lens.
LIGHT: gold chandelier rim, wet highlights on his skin.

## 6. PART B2: STORYBOARD SHEETS (Python only, after the keyframes)

Lay the keyframes out in order, 6 per sheet (3 x 2), thin white gutters, black strip under each with two lines: `E01-K01 · START · C01 · Champagne pour` and `WHO: VIVIAN (gown) · COLE (VALET)`. Four sheets: K01 to K06, K07 to K12, K13 to K18, K19 to K21.

**Resolution note for ComfyUI:** LTX renders at 736 x 1280 and the episode is cut at 720 x 1280; SeedVR2 takes the finished masters to 1080 x 1920 only after every episode is done. Deliver keyframes at 1080 x 1920 or larger; ComfyUI resizes them. Keep the subject's face large and sharp: LTX locks identity from the first frame. Realism lives or dies here: if a keyframe looks even slightly plastic, regenerate it, because the video model copies the skin it's given.

## 7. PART C: COVER

### 🎨 COVER-E01 · 9:16 · Save as `COVER-E01.jpg`
Extreme close up of Cole (VALET) with champagne running down his face, eyes calm and dangerous, filling the upper two thirds. Vivian small and out of focus behind his shoulder, holding the empty flute, laughing. Gold chandelier bokeh.
**Text overlay (Python):** `SHE DOESN'T KNOW` on two lines, bold white condensed sans, lower middle. `EP 1` small, bottom left.

## 8. PART D: TEXT CARDS (Python only, transparent PNG, 1080 x 1920)

| File | Text | Style |
|---|---|---|
| CARD-E01-HOOK.png | SHE DOESN'T KNOW I'M WORTH $5 BILLION | Bold white condensed sans, black stroke, 2 to 4 words per line, lower middle safe area |
| CARD-E01-3YEARS.png | 3 YEARS EARLIER | Small white serif caps, centred |
| CARD-E01-SCREEN.png | PAXWELL · IPO TOMORROW | Clean white sans on transparent, overlaid on the blank lobby LED wall in the edit (the keyframe wall stays blank) |
| CARD-ENDCARD.png | COLD STORAGE | Full black 1080 x 1920 background, white serif wordmark centred, thin gold rule under it |
