# Posting Flow Diagrams to Slack

## Overview

Slack doesn't render Mermaid natively, so diagrams must be converted to images first. The recommended approach uses **mermaid.ink** — a free hosted API that renders Mermaid code to PNG/SVG via URL, requiring zero server-side infrastructure.

## Approach 1: mermaid.ink URL (Recommended)

### How It Works

1. Generate Mermaid code (this skill already produces Mermaid flowcharts)
2. Pako-compress + base64url encode the diagram text
3. Construct an image URL: `https://mermaid.ink/img/pako:{encoded}`
4. Post the URL in a Slack Block Kit `image` block

Slack fetches and renders the image inline — no file upload needed.

### JavaScript/Node.js Encoding

```js
import pako from 'pako';

function mermaidToImageUrl(mermaidCode, options = {}) {
  const { type = 'png', bgColor = '!white', theme = 'default' } = options;

  // Pako compress + base64url encode
  const compressed = pako.deflate(new TextEncoder().encode(mermaidCode));
  const encoded = Buffer.from(compressed)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');

  return `https://mermaid.ink/img/pako:${encoded}?type=${type}&bgColor=${bgColor}&theme=${theme}`;
}
```

### Posting to Slack

```js
// Using Slack Web API (Node.js)
await client.chat.postMessage({
  channel: channelId,
  blocks: [
    {
      type: "section",
      text: {
        type: "mrkdwn",
        text: "*Flow Diagram: MHS - Employee Registration*"
      }
    },
    {
      type: "image",
      image_url: mermaidToImageUrl(mermaidCode),
      alt_text: "MHS Employee Registration flow diagram"
    }
  ],
  text: "Flow diagram for MHS - Employee Registration" // Fallback
});
```

### URL Parameters

| Parameter | Values | Default |
|-----------|--------|---------|
| `type` | `png`, `webp`, `jpeg` | `jpeg` |
| `bgColor` | `!white`, `!transparent`, hex `FF0000` | transparent |
| `theme` | `default`, `dark`, `neutral`, `forest` | `default` |
| `width` | pixels | auto |
| `height` | pixels | auto |
| `scale` | multiplier (e.g., `2` for retina) | `1` |

### Recommended Settings for Slack

```
?type=png&bgColor=!white&theme=default&scale=2
```

- `png` for sharp text rendering
- `!white` background (transparent looks bad on dark Slack themes)
- `scale=2` for retina displays

## Approach 2: Slack File Upload (Higher Quality)

For larger/complex diagrams where URL length might be an issue, or when you need guaranteed rendering quality:

### Render Locally with Mermaid CLI

```bash
npm install -g @mermaid-js/mermaid-cli
echo "$MERMAID_CODE" | mmdc -i - -o diagram.png -b white -s 2
```

### Upload to Slack (v2 API)

The old `files.upload` was deprecated March 2025. Use the new v2 flow:

```js
// Step 1: Get upload URL
const urlResponse = await client.files.getUploadURLExternal({
  filename: 'flow-diagram.png',
  length: fileBuffer.length
});

// Step 2: Upload file to the URL
await fetch(urlResponse.upload_url, {
  method: 'POST',
  body: fileBuffer,
  headers: { 'Content-Type': 'image/png' }
});

// Step 3: Complete upload and share to channel
await client.files.completeUploadExternal({
  files: [{ id: urlResponse.file_id, title: 'Flow Diagram' }],
  channel_id: channelId,
  initial_comment: '*Flow Diagram: MHS - Employee Registration*'
});
```

### When to Use File Upload vs URL

| Factor | mermaid.ink URL | File Upload |
|--------|----------------|-------------|
| Setup | Zero — just construct URL | Requires `mmdc` + Puppeteer |
| Speed | Instant (URL construction) | Slower (render + upload) |
| Reliability | Depends on mermaid.ink uptime | Self-contained |
| Diagram size | URL length limits (~8KB encoded) | No limit |
| Quality | Good with `scale=2` | Best (local rendering) |
| Offline | No | Yes (if self-hosted) |

## Approach 3: Kroki.io (Alternative)

[Kroki.io](https://kroki.io/) is similar to mermaid.ink but supports 25+ diagram formats. Can be self-hosted for reliability.

```
https://kroki.io/mermaid/png/{base64_encoded_diagram}
```

Kroki uses plain base64 encoding (not pako compression), making encoding simpler but URLs longer.

## Tips for Slack Bot Integration

1. **Keep diagrams simple** — Use stage-level views for complex flows (30+ steps). Slack image blocks have limited width.
2. **Add a text summary** — Always include a `section` block above the diagram with key findings (state, errors, runtime).
3. **Offer drill-down** — Post the summary diagram, then let users ask for detailed subflow diagrams.
4. **Cache URLs** — If the same flow diagram is requested multiple times, cache the mermaid.ink URL.
5. **Fallback text** — Always set the `text` field on `chat.postMessage` for notifications and accessibility.
