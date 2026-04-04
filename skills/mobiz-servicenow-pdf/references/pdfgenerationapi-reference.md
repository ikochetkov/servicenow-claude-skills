# PDFGenerationAPI Reference

## Plugin Details

- **Plugin ID:** `com.snc.apppdfgenerator`
- **Namespace:** `sn_pdfgeneratorutils`
- **Available since:** Paris
- **Engine:** iText7 (upgraded from iText5)
- **Activated by default:** Yes

## Method Signatures

### convertToPDF

```javascript
/**
 * @param {String} html - Complete HTML document string
 * @param {String} targetTable - Table to attach the PDF to
 * @param {String} targetSysId - sys_id of the record to attach to
 * @param {String} pdfName - Filename for the PDF (API auto-appends .pdf)
 * @param {String} [fontSysId] - sys_id from sys_pdf_generation_font_family (optional)
 * @returns {Object} { status: 'success'|'failure', attachment_id: String, message: String, request_id: String }
 */
new sn_pdfgeneratorutils.PDFGenerationAPI().convertToPDF(html, targetTable, targetSysId, pdfName, fontSysId);
```

### convertToPDFWithHeaderFooter

```javascript
/**
 * @param {String} html - Complete HTML document string
 * @param {String} targetTable - Table to attach the PDF to
 * @param {String} targetSysId - sys_id of the record
 * @param {String} pdfName - Filename for the PDF
 * @param {Object} pageProperties - Page layout configuration
 * @param {String} [fontSysId] - sys_id from sys_pdf_generation_font_family
 * @returns {Object} { status: 'success'|'failure', attachment_id: String, message: String, request_id: String }
 */
new sn_pdfgeneratorutils.PDFGenerationAPI().convertToPDFWithHeaderFooter(html, targetTable, targetSysId, pdfName, pageProperties, fontSysId);
```

## pageProperties Object

| Property | Type | Values | Description |
|----------|------|--------|-------------|
| `HeaderImageAttachmentId` | String | sys_id | Attachment sys_id of header image |
| `HeaderImageAlignment` | String | `'LEFT'`, `'CENTER'`, `'RIGHT'` | Header image alignment |
| `PageSize` | String | `'A4'`, `'LETTER'`, `'LEGAL'` | Page size |
| `PageOrientation` | String | `'landscape'`, `'portrait'` | Page orientation |
| `GeneratePageNumber` | String | `'true'`, `'false'` | Auto page numbering |
| `TopOrBottomMargin` | String | numeric (points) | Top/bottom margin (72 = 1 inch) |
| `LeftOrRightMargin` | String | numeric (points) | Left/right margin (36 = 0.5 inch) |
| `FooterText` | String | text | Footer text content |
| `FooterTextAlignment` | String | `'LEFT'`, `'CENTER'`, `'RIGHT'` | Footer text alignment |

## CSS3 Paged Media Support

### @page Rule

```css
@page {
    size: A4 portrait;           /* or: A4 landscape, LETTER, LEGAL */
    margin-left: 1cm;
    margin-top: 15mm;
    margin-right: 1cm;
    margin-bottom: 15mm;
}
```

### Page Numbers via CSS

```css
@page {
    @bottom-right {
        font-family: sans-serif;
        font-weight: bold;
        font-size: 10px;
        content: counter(page);
    }
}
/* Or with total: */
@page {
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
    }
}
```

### Running Headers/Footers via CSS

```css
@page {
    @top-center {
        content: element(runningHeader);
    }
}

#pageHeader {
    position: running(runningHeader);
}
```

```html
<div id="pageHeader">
    Report Title - Page <span id="pageNum"></span>
</div>
```

```css
#pageNum:before {
    content: counter(page);
}
```

## Custom Fonts

1. Navigate to **sys_pdf_generation_font_family**
2. Create new record (e.g., name: "CustomFont")
3. Attach `.ttf` font files to the record
4. Note the record's sys_id
5. Reference in CSS:
```css
body { font-family: CustomFont, sans-serif; }
```
6. Pass sys_id as `fontSysId` parameter to `convertToPDF`

## SVG Support

Inline SVG is fully supported. Always include the `xmlns` attribute:

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 200" width="400" height="200">
    <rect x="10" y="10" width="100" height="80" fill="#4CAF50" />
    <circle cx="200" cy="100" r="50" fill="#D8242A" />
    <text x="200" y="105" text-anchor="middle" font-size="16" fill="white">75%</text>
    <path d="M 10 180 L 390 180" stroke="#333" stroke-width="1" />
</svg>
```

Supported SVG elements: `<rect>`, `<circle>`, `<ellipse>`, `<line>`, `<path>`, `<text>`, `<g>`, `<polygon>`, `<polyline>`

## Image Support

### Base64 inline (recommended)

```html
<img src="data:image/png;base64,iVBORw0KGgo..." width="200" />
<img src="data:image/svg+xml;base64,PHN2Zy..." width="150" />
```

### External URL (must be publicly accessible)

```html
<img src="https://public-url.com/image.png" width="200" />
```

**Note:** ServiceNow-internal URLs (attachments, etc.) are NOT accessible to the PDF renderer.

## Known Issues by Version

| Version | Issue | Status |
|---------|-------|--------|
| San Diego | `@page` CSS rules ignored | Fixed in Tokyo |
| San Diego | Running headers not rendered | Fixed in Tokyo |
| All | `position: absolute` not supported | Use alternative layout |
| All | `display: flex` partially supported | Basic flex works; `margin-top: auto` does not |
| All | External image URLs may fail | Use base64 data URIs |

## Community Resources

- [Generating Custom PDFs - PDFGenerationAPI](https://www.servicenow.com/community/developer-articles/generating-custom-pdfs-using-the-new-pdfgenerationapi/ta-p/2318979)
- [ServiceNow PDF Generation API Magic](https://www.servicenow.com/community/developer-blog/servicenow-pdf-generation-api-magic-learn-the-power-of/ba-p/2333214)
- [Building a PDF Report using PDFGenerationAPI](https://www.servicenow.com/community/brazil-snug/building-a-pdf-report-using-pdfgenerationapi/ta-p/2436540)
- [PDF Generator Plugin FAQ](https://www.servicenow.com/community/hrsd-articles/pdf-generator-plugin-faq/ta-p/2310037)
