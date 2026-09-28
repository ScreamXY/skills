# Editing and export

## Sources and chronology

Prefer embedded capture metadata: photo EXIF dates and offsets, QuickTime creation dates, and camera metadata. Convert them to one project time zone before sorting. A download or export date is not a capture date. Check camera clocks when dates disagree with the scene. Keep uncertainty visible in the inventory.

Treat a split screen as one time interval containing its sources. Check both sources' days. Do not infer chronology from the left-to-right placement of simultaneous images. Identify paired stills and Live Photo clips so they are not counted as unrelated moments.

Keep a machine-readable plan. Record each shot's source identity, original capture time, source in/out times, output start and frame count, speed, layout, transition length, public source, and audio cue. Also record the project time zone, frame rate, dimensions, and expected runtime. Use stable shot IDs for audio cues and caches; list positions change when a film is reordered.

## Framing and motion

Choose one delivery canvas. Use a crop only if it preserves the important people and action. For mixed portrait and landscape sources, consider a clean inset over a dark blurred background or a deliberate split screen. Apply public masks before making any background copy.

Use small, smooth photo moves with a clear subject. Avoid enlarging a still beyond useful detail. Prepare its orientation before choosing the pan. Prefer a moving Live Photo excerpt when the motion helps the story. Check loops and holds for visible jumps.

For action, vary pacing through selected moments, slow motion, and sound. Do not stretch low-frame-rate footage into jerky slow motion. Retiming a clip also retimes its mask and audio. Place the ending on a final-day moment; a deliberate held frame can support the closing title.

## Real transitions and exact timing

A punch zoom, flash, or color effect inside one shot is not a transition between two shots. Build transitions from the outgoing and incoming images. Use longer dissolves for scenery and shorter moves for action. Do not put an effect at every cut simply because it is available.

Count frames at the chosen output frame rate. Reserve source handles around boundaries so transitions do not silently shorten the film or shift the music. If using the separate-body-and-bridge method from the holiday edit:

- Give a shot `N` timeline frames, with half-handles `hin` and `hout` for its incoming and outgoing transitions. Use even transition lengths for this method.
- Render `N + hin + hout` source frames. Retiming must include these handles.
- Its body starts at rendered frame `2 * hin` and ends before frame `frames - 2 * hout`. Its length is `N - hin - hout` and must be positive.
- Build each bridge from the previous shot's final transition-length frames and the next shot's first transition-length frames. Count each bridge once.
- Assert that all bodies and bridges add up to the planned film length. Compare bridge endpoints with their source frames.

This is one tested approach, not a requirement to use FFmpeg. A video editor can manage the overlap directly. In either approach, verify the resulting frame count and sync.

When using FFmpeg, normalize timestamps, time bases, dimensions, frame rates, sample aspect ratio, pixel format, and color before combining inputs. For a bridge of `T` frames, the previous workflow used an `xfade` duration of `(T - 1) / fps`, followed by an exact `T`-frame trim. Verify endpoints with the installed version. A bounded zoom on each input plus a dissolve can be more predictable than an unchecked zoom transition.

Use explicit per-part durations when concatenating separately encoded pieces. Metadata rounding can otherwise accumulate into audio drift. Do not add a seek option to a still-image input; seeking even to zero produced empty output in the previous workflow. Reject empty or truncated renders before assembly.

Invalidate cached renders when sources, frame counts, timing handles, crop, mask data, title artwork, GPS overlays, or other effects change. A file existing at an old shot number does not make it reusable. Include referenced asset contents in the cache decision, not just their filenames.

## Color and sound

Check phone HDR and camera footage before combining them. Choose an intentional delivery color space. For an SDR export, tone-map HDR where needed; changing color tags alone does not convert HDR. Check brightness and skin tones in the rendered samples. In the previous 1080p workflow, every final part needed consistent limited-range BT.709 tags; some image/zoom filters dropped tags and required correction before joining.

Choose music that fits the energy and is licensed for the intended use, including the public edition. Save the source, license evidence, required credit, and the edited excerpt information. A reference video's soundtrack is not automatically available for reuse. Do not hard-code the previous film's track into future projects.

Cut important beats and action together without forcing every shot to the same duration. Preserve useful natural sound. Lower the music around voices and featured action, fade clip audio across transitions, and keep transition sounds subtle. Rebuild audio timing from shot IDs after reordering. An approximate target of -16 LUFS with true-peak headroom around -1.5 dBTP is a starting point, not a substitute for listening. Recheck the encoded export for clipping and sync.

## GPS, when useful

Check whether the camera recorded GPS before promising an overlay. Inspect fix quality, gaps, accuracy indicators, timestamps, and the selected excerpt. Align the data with the source clip and its speed changes. Skip unusable data and report why.

Label camera speed as camera speed: a following camera's speed is not automatically the child's speed. Show original measured speed on slow-motion replay and label the replay speed. Do not infer values that the recording cannot support. For public exports, prefer a simple relative route without coordinates or location labels, and strip embedded GPS metadata.

## Final checks

Decode the complete exports. Check video and audio durations, expected frames, aspect ratio, color metadata, and output streams. Inspect every transition for bad endpoints, flashes, black frames, or broken scale. Sample source sound alignment around slowed clips and scene changes. Review the finished opening and ending after all changes.

Keep a short verification record distinguishing automated checks, visual inspection, and listening. Report unperformed checks honestly. Leave previous exports intact so the user can compare revisions.
