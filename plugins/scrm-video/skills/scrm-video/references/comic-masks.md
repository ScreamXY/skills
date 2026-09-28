# Comic masks for a public film

## Identify the subjects

Reuse the user's current descriptions and choices. If the targets are unclear, ask which children or people to cover. Do not assume every child is theirs. Confirm against current reference frames when needed; a past age, hairstyle, or helmet is not a permanent identifier.

Keep the originals and an unmasked private edition. Use the same timeline and sound for the public edition. Keep face references, generated assets, tracking data, and review frames in the media project, outside this plugin repository.

## Create a small set of usable masks

Use available image-generation or illustration tools for the requested comic style. Make consistent, opaque face assets for each target, with transparent space around the mask. Keep enough coverage around the real face to allow small tracking errors. Prepare front, three-quarter, and profile variants if the footage needs them.

Use the image tool's own instructions. This skill requires no particular image service or installed model. If new tools or models are needed, ask before installing them. If the comic assets cannot be made with available tools, explain that limit and agree on a fallback while continuing the private edit.

A comic face inspired by a child is a visual replacement, not a guarantee of anonymity. Do not claim that the child cannot be recognized from the replacement, voice, clothing, companions, or setting. If the user wants stronger anonymity, use generic figures and address those other cues too.

## Fit and animate

Track each target separately through position, scale, rotation, and head pose. Use landmarks or careful manual keyframes to fit perspective. A flat sticker following only the face center is not the requested fitted mask.

Use stable smoothing without visible lag. Match turns with the correct variant or perspective warp. Keep the real face fully covered, including at the edges. Preserve helmet, hand, or foreground occlusion only when it does not expose the face. Avoid sudden size changes, sliding masks, or a front-facing face pasted on a profile view.

Add restrained blinking or expression changes when useful. Anchor animation to the tracked head; do not let a blink, mouth movement, or transparent region reveal real eyes or facial features. Test representative turns, fast motion, close-ups, and small faces before processing all clips.

## Protect every output path

Render masks into source frames before cropping, scaling, blur-background duplication, split screens, speed changes, transitions, and closing holds. Both sides of a transition must come from the correct public source. A cached private background or a single unmasked bridge frame can expose a face.

Maintain a source audit: which selected clips show each target, where a mask is needed, and which masked file supplies each public timeline entry. Include briefly visible faces, distant appearances, reflections when identifiable, and both people when they share a frame. Do not skip a target just because they are in the background.

Review coverage through each interval where a target's face is visible, not only at detector keyframes. Face detectors can miss profiles, motion blur, partial faces, and small background faces. Inspect turns and tracking failures frame by frame. Check the final public export as well as the mask intermediates.

If tracking is uncertain, widen the cover, correct the keyframes, or use an opaque cover or strong blur for that interval. Another option is to omit the shot. Make a visible fallback clear to the user. Do not silently keep an exposed frame. If coverage cannot be checked, label the public export as a draft and identify the remaining review instead of calling it ready to share.
