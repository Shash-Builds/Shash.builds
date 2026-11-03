# Paste-in prompts

Each shash.builds tool also works as a plain prompt in any Claude chat. Open
the prompt, copy all of it, and paste it as your first message, or into a
Claude Project's instructions.

| Tool | Prompt | Fill in first |
|---|---|---|
| Audio Review | [initiation_prompt.md](audio-review/skills/audio-review/initiation_prompt.md) | Nothing. Upload your audio after Claude replies |
| Motion Design Taste | [motion-design-taste.md](motion-design-taste/skills/motion-design-taste/motion-design-taste.md) | Nothing. Claude asks for the video and references |
| Harsh Buyer Review | [harsh-buyer-reviewer.md](harsh-buyer-review/skills/harsh-buyer-review/harsh-buyer-reviewer.md) | Sections 1 to 3: your product, price, market and buyer |
| Social Media | [social-media.md](social-media/skills/social-media/social-media.md) | Nothing. Claude asks about your brand, audience and goal the first time |
| Transcriber | [transcriber.md](transcriber/skills/transcriber/transcriber.md) (needs a Claude that can run code; otherwise it explains the phone options) | Nothing. Upload the recording |
| Humanizer | [humanizer.md](humanizer/skills/humanizer/humanizer.md) (sections 3 to 5 work by eye; the checker needs a Claude that can run code) | Your draft, the channel it's for, and a few things you've written yourself |
| Clipper | [clipper.md](clipper/skills/clipper/clipper.md) (needs code execution and ffmpeg for the cutting) | The campaign brief and the long video |
| LinkedIn | [linkedin.md](linkedin/skills/linkedin/linkedin.md), with [humanizer.md](humanizer/skills/humanizer/humanizer.md) for the final edit | Three things you've written yourself, who you want to reach, and what you want from LinkedIn |
| AI Visuals | [ai-visuals.md](ai-visuals/skills/ai-visuals/ai-visuals.md), plus the placement's section of [purposes.md](ai-visuals/skills/ai-visuals/purposes.md) and the tool's section of [generators.md](ai-visuals/skills/ai-visuals/generators.md) | Nothing. Share the image or video, the prompt you used and where it will go |
| Ecom | [ecom.md](ecom/skills/ecom/ecom.md), plus the module you need from [modules/](ecom/skills/ecom/modules/) and the marketplace's section of [marketplaces.md](ecom/skills/ecom/marketplaces.md) | Nothing. Claude asks for your products, costs and channels the first time |
| Competitor Research | [competitor-research.md](competitor-research/skills/competitor-research/competitor-research.md) | Nothing. Claude asks for your product and the question. Pick Haiku as the model to save credits |
| Niche Research | [niche-research.md](niche-research/skills/niche-research/niche-research.md) | Your niche, audiences, platforms and goal. Pick Haiku as the model to save credits |
| Careful Mode | [careful-mode.md](careful-mode/skills/careful-mode/careful-mode.md) | Nothing |
| Master Skill | [master-full.md](../dist/master-full.md) (the Master Skill with every tool and the video workflow, in one file) | Nothing. Claude picks the tools each task needs |

Economy Mode has no paste-in version, because it needs Claude Code's
subagents.

**Shortcut for a Claude that can browse the web:** instead of pasting, send it
the prompt's raw link and ask it to follow it. For example:

> Read https://raw.githubusercontent.com/Shash-Builds/shash.builds/HEAD/skills/harsh-buyer-review/skills/harsh-buyer-review/harsh-buyer-reviewer.md and follow it for this conversation.
