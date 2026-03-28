# Demo: "5 Python tricks that changed how I code"

**Command:**
```bash
faceless-video-gen "5 Python tricks that changed how I code" \
  --voice en-US-AriaNeural --duration 60
```

**Generated script excerpt:**
> Did you know that most Python developers are still writing 10 extra lines of code every day — for no reason?
> Here are five tricks that will make your code cleaner, faster, and easier to read.
> First: use walrus operators to assign and check in one shot. Instead of fetching a value and checking it in two lines, write `if data := fetch():` and you're done.
> Second: f-string debugging. Add an equals sign — `f"{my_var=}"` — and Python prints the variable name and value together. No more `print("my_var:", my_var)`.
> ...

**Output:** `output.mp4` — 62 seconds, 1280×720, ~18 MB

**Pipeline timing (gpt-4o-mini + picsum fallback):**
| Step | Time |
|---|---|
| Script generation | ~3s |
| edge-tts voiceover | ~5s |
| Image fetch (10 × picsum) | ~8s |
| MoviePy assembly | ~15s |
| **Total** | **~31s** |
