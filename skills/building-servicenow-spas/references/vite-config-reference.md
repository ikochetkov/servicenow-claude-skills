# Vite Configuration & Deployment Reference

## Contents
- vite.config.ts template
- package.json (web directory)
- Root package.json scripts
- index.html template
- tsconfig.json
- Deploy script (scripts/deploy-to-sn.js)
- .env file template
- Build output verification

## vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react'; // or vue(), svelte(), etc.
import { viteSingleFile } from 'vite-plugin-singlefile';

export default defineConfig({
  plugins: [react(), viteSingleFile()],
  build: {
    // Inline all assets up to ~10MB to ensure everything goes into one file
    assetsInlineLimit: 10000000,
  },
  server: {
    port: 3000,
    proxy: {
      // Proxy API calls to Express backend during local development
      '/api': 'http://localhost:3001',
    },
  },
});
```

**Key points:**
- `viteSingleFile()` inlines all JS, CSS, and small assets into a single HTML file
- `assetsInlineLimit: 10000000` ensures images and fonts are base64-encoded inline
- The proxy forwards `/api/*` requests to the Express backend for local development

## package.json (web/ directory)

```json
{
  "name": "my-sn-app",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^7.0.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.0",
    "typescript": "^5.7.0",
    "vite": "^6.0.0",
    "vite-plugin-singlefile": "^2.0.0"
  },
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  }
}
```

## Root package.json scripts

```json
{
  "scripts": {
    "dev": "concurrently \"tsx watch src/server/index.ts\" \"cd web && npm run dev\"",
    "build": "cd web && npm run build",
    "build:sn": "cd web && npm run build",
    "deploy:sn": "npm run build:sn && node scripts/deploy-to-sn.js",
    "server": "tsx src/server/index.ts"
  }
}
```

## index.html (project root, not in public/)

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>My ServiceNow App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**Important:** Vite expects `index.html` at the project root (not in `public/`). The `src` attribute in the script tag must point to your entry file.

## tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src"]
}
```

**Key:** `"moduleResolution": "bundler"` is required for Vite.

## Deploy Script: scripts/deploy-to-sn.js

```javascript
#!/usr/bin/env node

/**
 * Deploy SPA to ServiceNow.
 *
 * Reads the built single-file HTML from web/dist/index.html and PATCHes it
 * into a ServiceNow system property.
 *
 * Usage:
 *   node scripts/deploy-to-sn.js
 *
 * Requires .env with:
 *   SERVICENOW_INSTANCE_URL, SERVICENOW_USER, SERVICENOW_PASSWORD
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

// Load .env
const envPath = path.join(ROOT, '.env');
if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf-8');
  for (const line of envContent.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eqIdx = trimmed.indexOf('=');
    if (eqIdx === -1) continue;
    const key = trimmed.slice(0, eqIdx).trim();
    const val = trimmed.slice(eqIdx + 1).trim();
    process.env[key] = val;
  }
}

const INSTANCE_URL = process.env.SERVICENOW_INSTANCE_URL;
const USER = process.env.SERVICENOW_USER;
const PASSWORD = process.env.SERVICENOW_PASSWORD;

// IMPORTANT: Replace this with the actual sys_id of your system property
const PROPERTY_SYS_ID = 'YOUR_PROPERTY_SYS_ID_HERE';
const PROPERTY_NAME = 'your_namespace.spa_html';

if (!INSTANCE_URL || !USER || !PASSWORD) {
  console.error('Missing required env vars: SERVICENOW_INSTANCE_URL, SERVICENOW_USER, SERVICENOW_PASSWORD');
  process.exit(1);
}

const htmlPath = path.join(ROOT, 'web', 'dist', 'index.html');
if (!fs.existsSync(htmlPath)) {
  console.error(`Build output not found: ${htmlPath}`);
  console.error('Run "npm run build:sn" first.');
  process.exit(1);
}

const html = fs.readFileSync(htmlPath, 'utf-8');
const sizeKB = (Buffer.byteLength(html, 'utf-8') / 1024).toFixed(1);
console.log(`Deploying SPA to ServiceNow (${sizeKB} KB)...`);

// Use the standard Table API to PATCH the system property value
const tableApiUrl = `${INSTANCE_URL}/api/now/table/sys_properties/${PROPERTY_SYS_ID}`;
const auth = Buffer.from(`${USER}:${PASSWORD}`).toString('base64');

try {
  const response = await fetch(tableApiUrl, {
    method: 'PATCH',
    headers: {
      'Authorization': `Basic ${auth}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: JSON.stringify({ value: html }),
  });

  if (!response.ok) {
    const text = await response.text();
    console.error(`Deploy failed: HTTP ${response.status}`);
    console.error(text.slice(0, 500));
    process.exit(1);
  }

  const result = await response.json();
  const updatedName = result?.result?.name;
  console.log('Deploy successful!');
  console.log(`  Property: ${updatedName || PROPERTY_NAME}`);
  console.log(`  Size: ${sizeKB} KB`);
  console.log(`  SPA URL: ${INSTANCE_URL}/api/<namespace>/<api_id>/app`);
} catch (err) {
  console.error('Deploy failed:', err.message);
  process.exit(1);
}
```

## .env file template

```bash
# ServiceNow instance credentials (never commit this file)
SERVICENOW_INSTANCE_URL=https://your-instance.service-now.com
SERVICENOW_USER=admin
SERVICENOW_PASSWORD=your_password

# Optional: Override API base URL for frontend
# VITE_API_BASE_URL=http://localhost:3001
```

Add `.env` to `.gitignore`:
```
.env
```

## Build Output Verification

After running `npm run build`, verify:

```bash
# Should produce a single file
ls -la web/dist/index.html

# Check file size (should be < 4MB for system property storage)
wc -c web/dist/index.html

# Open in browser — UI should render (API calls will fail but layout loads)
open web/dist/index.html
```
