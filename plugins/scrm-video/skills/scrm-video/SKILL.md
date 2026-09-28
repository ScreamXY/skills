---
name: scrm-video
description: Use when the user says "make a holiday video", "edit these photos and videos", "combine these films", "add transitions", or "make a public version with comic face masks". Build or revise a personal travel, family, or action film from existing media, with music, photo motion, and a checked timeline.
disable-model-invocation: true
---

# Video

## Language

English is the user's second language. Use short sentences and common words. Avoid idioms and slang. Technical terms are fine.

## Editing preferences

Treat these as the user's defaults. A new request can override them.

- Show good times, family moments, and action. Give quiet scenes room to breathe.
- Keep days in capture order. Put hiking, cycling, and climbing in their real sequence. Do not move an earlier day's scenery to the ending or preview later days at the start unless requested.
- Use more of the useful b-roll: paths, scenery, details, travel, and small moments. A longer film is welcome when the added footage adds something.
- Use real transitions between shots, timed to the action and music. Mix dissolves with restrained slides, wipes, zooms, or whip transitions. Keep direct cuts where they suit the scene.
- Give still photos gentle pans or zooms. Use Live Photo motion when it adds life.
- Choose the format that suits the footage and destination. Keep people well framed. Do not force every source into the same crop.
- Choose matching music. Preserve selected voices, laughter, movement, and outdoor sounds. Use a different track when asked for a fresh musical direction.
- For family holiday films, default to matching private and public exports. Keep normal faces in the private film. Cover the designated children's faces with fitted, animated comic masks in the public film.
- Use reference edits for pacing, transitions, and mood. Do not silently reuse their footage or music.
- Add GPS graphics only when the source data supports them. Treat them as an optional detail, not the main story.

## Start and resume

Inspect the existing edit folder before starting again. Reuse media, plans, mask assets, licenses, and verified work. Keep originals and earlier exports. Write each revision to a new folder or versioned files.

Use the tools already available. Ask before installing software, packages, plugins, or downloaded models. Do not install this skill or publish a film as part of editing unless asked.

Use available file access, shell commands, media tools, or app controls in either Codex or Claude Code. Do not depend on a specific tool name. If cloud access, image generation, or tracking is unavailable, explain the missing capability and request only what is needed. Continue independent work on local media.

Resolve relative dates such as "last two days" into explicit dates in the user's time zone. State the range. Check the selected media against it. Carry forward the format and face-mask choices already given. Ask only for missing choices that affect the result, such as which children to mask or which download folder to use. Child ages and appearance change; keep their current descriptions in the project, not in this reusable skill.

If downloads or Photos exports stall, compare expected and available items. Continue with complete files and keep a missing-items list. Do not silently treat a partial export as complete. If the user requests it, use an available keep-awake method during export. A locked session needs the user to unlock it.

## Build the film

1. Inventory the sources. Read capture timestamps, time zones, orientation, duration, frame rate, dimensions, audio, color space, and available GPS. Pair Live Photo stills and clips. Do not use file modification times as capture dates without marking that fallback.
2. Make contact sheets and sample video clips. Select both action and b-roll. Check the whole collection, not just the first exported items.
3. Save a timeline with source paths, capture dates, selected source ranges, crops, speed changes, output frames, transitions, music cues, and mask requirements. Check day order before rendering. Mark uncertain dates; do not invent them. Choose an ending from the final day. Recheck this after adding footage or reordering shots.
4. For rendering, transitions, music, or GPS, read [Editing and export](references/editing-and-export.md). Use one timeline for both editions so their timing and soundtrack match.
5. Before making a public edition, read [Comic masks](references/comic-masks.md). Mask the source frames before crops, backgrounds, split screens, slow motion, and transitions.
6. Render short samples of new layouts, effects, or mask behavior before the full export. Revise samples that fail. Then finish both films and their checks.

## Check and deliver

Check capture dates against the final timeline. Review the opening, day boundaries, and ending. Earlier-day shots must not appear after later-day activities under the chronological default.

Review all selected scenes and every transition. Inspect the public film at full size, including face turns, small background appearances, transition frames, and held frames. Contact sheets help navigation; they do not prove that every exposed face is covered. Fix gaps or use the fallback in the mask reference before calling a public version ready.

Check the finished files, not only intermediate clips: full decode, expected frame count and duration, dimensions, frame rate, color, audio sync, clipping, and unintended black or frozen frames. Listen to the final mix when playback is available. State any check that could not be completed.

Deliver links to clearly named `PRIVATE` and `PUBLIC` files, the runtime, and a short account of the changes and checks. Keep music credits beside the exports. Preserve the timeline, source inventory, mask data, render instructions, and review notes so a later session can revise the film. Do not place private media or face assets in the skill repository.
